"""AI extraction service: calls DeepSeek once per feedback, stores Q&A-level mentions."""
import asyncio
import json
import logging
import os
from datetime import datetime, timezone

from openai import AsyncOpenAI
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.batch import Batch, BatchStatus
from app.models.extraction import EntityType, Extraction, Sentiment
from app.models.feedback import Feedback
from app.services.entities import ALL_ENTITIES

logger = logging.getLogger(__name__)

_CONCURRENCY = 10  # max simultaneous DeepSeek calls


def _system_prompt() -> str:
    schools = "\n".join(f"  - {name} → ID: {id_}" for id_, (name, t) in ALL_ENTITIES.items() if t == "school")
    services = "\n".join(f"  - {name} → ID: {id_}" for id_, (name, t) in ALL_ENTITIES.items() if t == "service")
    return f"""You analyse university feedback to find mentions of specific schools and service departments.

Known schools:
{schools}

Known services:
{services}

For each Q&A pair that mentions a known entity, add one entry per entity mentioned.
Return ONLY a JSON object: {{"mentions": [...]}}
Empty array if nothing found.

Each mention:
  {{"qa_index": <1-based int>, "entity_id": "<exact ID above>", "entity_type": "school" or "service", "sentiment": "positive" or "negative"}}

Rules:
- Use exact IDs from the lists; never invent new IDs.
- sentiment=positive means complimentary/satisfied; sentiment=negative means critical/dissatisfied.
- One entry per entity per Q&A pair — no duplicates."""


def _user_message(body_json: list) -> str:
    parts = []
    for i, item in enumerate(body_json, 1):
        q = item.get(f"question_{i}", "")
        a = item.get(f"answer_{i}", "")
        parts.append(f"Q{i}: {q}\nA{i}: {a}")
    return "\n\n".join(parts)


async def _call_once(client: AsyncOpenAI, sem: asyncio.Semaphore, feedback: Feedback) -> list[dict]:
    system = _system_prompt()
    user = _user_message(feedback.body_json)
    async with sem:
        for attempt in range(2):
            try:
                resp = await client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                    response_format={"type": "json_object"},
                    temperature=0,
                )
                data = json.loads(resp.choices[0].message.content)
                return data.get("mentions", [])
            except (json.JSONDecodeError, KeyError, AttributeError) as e:
                if attempt == 0:
                    logger.warning("Feedback %s: parse error, retrying — %s", feedback.feedback_id, e)
                    continue
                logger.error("Feedback %s: extraction failed after retry — %s", feedback.feedback_id, e)
            except Exception as e:
                logger.error("Feedback %s: DeepSeek error — %s", feedback.feedback_id, e)
                break
    return []


def _to_extraction_rows(mentions: list[dict], feedback: Feedback, batch_id: str) -> list[Extraction]:
    rows = []
    body = feedback.body_json or []
    seen = set()  # deduplicate (qa_index, entity_id)

    for m in mentions:
        qa_idx = m.get("qa_index")
        entity_id = str(m.get("entity_id", "")).upper()
        entity_type_str = m.get("entity_type", "")
        sentiment_str = m.get("sentiment", "")

        if not qa_idx or entity_id not in ALL_ENTITIES:
            continue
        if entity_type_str not in ("school", "service"):
            continue
        if sentiment_str not in ("positive", "negative"):
            continue

        key = (qa_idx, entity_id)
        if key in seen:
            continue
        seen.add(key)

        try:
            pair = body[qa_idx - 1]
            source_q = pair.get(f"question_{qa_idx}", "")
            source_a = pair.get(f"answer_{qa_idx}", "")
        except (IndexError, AttributeError):
            continue

        rows.append(Extraction(
            feedback_id=feedback.id,
            batch_id=batch_id,
            entity_id=entity_id,
            entity_type=EntityType.SCHOOL if entity_type_str == "school" else EntityType.SERVICE,
            source_question=source_q,
            source_answer=source_a,
            sentiment=Sentiment.POSITIVE if sentiment_str == "positive" else Sentiment.NEGATIVE,
        ))
    return rows


async def _run(batch_id: str, db: Session) -> tuple[int, int]:
    client = AsyncOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY", "no-key"),
        base_url="https://api.deepseek.com",
    )
    sem = asyncio.Semaphore(_CONCURRENCY)
    feedbacks = db.query(Feedback).filter(Feedback.batch_id == batch_id).all()

    results = await asyncio.gather(
        *[_call_once(client, sem, f) for f in feedbacks],
        return_exceptions=True,
    )

    total, failed = 0, 0
    for feedback, result in zip(feedbacks, results):
        if isinstance(result, Exception):
            logger.error("Feedback %s raised: %s", feedback.feedback_id, result)
            failed += 1
            continue
        rows = _to_extraction_rows(result, feedback, batch_id)
        for row in rows:
            db.add(row)
        total += len(rows)

    db.commit()
    return total, failed


def run_extraction(batch_id: str) -> tuple[int, int]:
    """Sync entry point for BackgroundTask. Creates its own DB session."""
    db: Session = SessionLocal()
    try:
        batch = db.get(Batch, batch_id)
        if not batch:
            return 0, 0
        batch.status = BatchStatus.EXTRACTING
        db.commit()

        total, failed = asyncio.run(_run(batch_id, db))

        batch = db.get(Batch, batch_id)
        batch.status = BatchStatus.EXTRACTED
        batch.completed_at = datetime.now(timezone.utc)
        db.commit()
        logger.info("Batch %s extracted: %d mentions, %d feedbacks failed", batch_id, total, failed)
        return total, failed
    except Exception as e:
        db.rollback()
        batch = db.get(Batch, batch_id)
        if batch:
            batch.status = BatchStatus.FAILED
            db.commit()
        logger.error("Batch %s extraction error: %s", batch_id, e)
        return 0, 0
    finally:
        db.close()
