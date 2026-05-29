#!/usr/bin/env python3
"""Generate dummy feedback JSON files for AI Feedback Process testing.
Each file targets ~1000 words across 10 Q&A pairs (~100 words per answer).
"""
import json, random, os
from pathlib import Path
from datetime import date, timedelta

random.seed(42)

BASE = Path(__file__).parent / "FEEDBACKS"

# ── Names ──────────────────────────────────────────────────────────────────
SURNAMES   = ["Nguyen","Le","Tran","Pham","Hoang","Vu","Bui","Do","Ngo","Duong",
               "Dang","Vo","Dinh","Ha","Lam","Phan","Truong","Luong","Huynh","Cao"]
MIDNAMES_M = ["Van","Duc","Minh","Quoc","Huu","Dinh","Thanh"]
MIDNAMES_F = ["Thi","Ngoc","Kim","Phuong","Thanh","Le"]
FIRSTNAMES = ["An","Binh","Cuong","Dung","Giang","Hai","Huong","Khanh","Lan","Linh",
               "Long","Minh","Nam","Nga","Phuc","Quang","Son","Thao","Thanh","Thu",
               "Tien","Tuan","Vy","Xuan","Yen","Hung","Hoa","Mai","Phuong","Bao"]
COMPANIES  = ["Tech Solutions Vietnam","FPT Software","VNG Corporation","Viettel Digital",
               "Momo Technology","VNPT Technology","Grab Vietnam","Shopee Vietnam",
               "Bosch Vietnam","Unilever Vietnam","Samsung Vietnam R&D","Lazada Vietnam",
               "Tiki Corporation","KMS Technology","NashTech Vietnam"]
COMPANY_ROLES = ["HR Manager","Technical Lead","Department Head","Senior Engineer",
                  "Internship Coordinator","Engineering Manager","CTO","Team Lead"]
INDUSTRIES = ["Software Development","Digital Marketing","Financial Technology","E-Commerce",
               "Telecommunications","Manufacturing","Consulting","Media & Advertising"]

def gen_name(gender="m"):
    s = random.choice(SURNAMES)
    m = random.choice(MIDNAMES_M if gender == "m" else MIDNAMES_F)
    f = random.choice(FIRSTNAMES)
    return f"{s} {m} {f}"

def gen_id(prefix, n):
    return f"{prefix}{n:04d}"

def rand_date(start_year=2025, ranges=((3,5),(10,12))):
    r = random.choice(ranges)
    month = random.randint(*r)
    day   = random.randint(1, 28)
    return date(start_year, month, day).isoformat()

# ── Schools & Services ──────────────────────────────────────────────────────
SCHOOLS = [
    {"id":"IT",  "name":"School of Information Technology",
     "programs":["Software Engineering","Computer Science","Data Science",
                 "Cybersecurity","Artificial Intelligence & Machine Learning"]},
    {"id":"COM", "name":"School of Communication",
     "programs":["Journalism","Public Relations","Advertising & Brand Management",
                 "Media Studies","Digital Communication"]},
    {"id":"BUS", "name":"School of Business Administration",
     "programs":["Business Administration","International Business",
                 "Finance & Accounting","Marketing","Human Resource Management"]},
    {"id":"ENG", "name":"School of Engineering",
     "programs":["Mechanical Engineering","Electrical Engineering","Civil Engineering",
                 "Chemical Engineering","Industrial Engineering"]},
]

SERVICES_ALL = ["FINANCE","ACADEMIC","IT_SUPPORT","STUDENT_AFFAIRS","LIBRARY","CAREER","FACILITIES"]

SERVICE_NAMES = {
    "FINANCE":"Finance Department","ACADEMIC":"Academic Affairs Office",
    "IT_SUPPORT":"IT Support Department","STUDENT_AFFAIRS":"Student Affairs Office",
    "LIBRARY":"Library Services","CAREER":"Career Center","FACILITIES":"Facilities Management",
}

# ── Answer templates ────────────────────────────────────────────────────────
# Each function returns ~100-word answer string.
# p=positive, n=negative, m=mixed. Variables: s=school_name, prog=program, svc=service_name

def _pick(pool): return random.choice(pool)

POS_ADJ  = ["exceptional","outstanding","impressive","commendable","excellent","remarkable","superb"]
NEG_ADJ  = ["inadequate","disappointing","inconsistent","insufficient","concerning","substandard","problematic"]
MID_ADJ  = ["adequate","acceptable","moderate","satisfactory","reasonable","fair","decent"]
POS_VERB = ["commend","appreciate","value","recognize","applaud","acknowledge","praise"]
NEG_VERB = ["urge","recommend","suggest","highlight","flag","raise concerns about","point out"]

def a_teaching(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"The teaching quality in my {prog} courses at the {s} has been {_pick(POS_ADJ)} this semester. "
                f"My lecturers consistently demonstrate deep subject matter expertise and present complex material "
                f"in a clear, well-structured, and engaging manner that truly enhances comprehension. "
                f"I particularly {_pick(POS_VERB)} the integration of real-world industry examples and hands-on "
                f"exercises into every session, which makes abstract theoretical concepts genuinely applicable. "
                f"The interactive teaching style — characterized by open discussions, collaborative problem-solving, "
                f"and prompt feedback on assignments — has significantly accelerated my academic growth. "
                f"The faculty's visible dedication and responsiveness to students makes me confident I am receiving "
                f"a high-calibre education that will serve me well in my future career.")
    if sentiment == "n":
        return (f"I have observed several {_pick(NEG_ADJ)} aspects of teaching quality in my {prog} courses "
                f"at the {s} this semester that I feel compelled to bring to attention. "
                f"Certain lectures are delivered without adequate structure, making it difficult to follow the "
                f"logical progression of content, and some lecturers rely heavily on reading directly from "
                f"slides rather than elaborating or encouraging discussion. "
                f"Assessment criteria are sometimes communicated after assignments are already underway, "
                f"which creates unnecessary confusion and unfair evaluation conditions. "
                f"I strongly {_pick(NEG_VERB)} the institution to invest in faculty development programs "
                f"focused on modern pedagogy, student engagement techniques, and constructive feedback practices "
                f"to address these shortcomings urgently.")
    return (f"Teaching quality in my {prog} program at the {s} has been {_pick(MID_ADJ)} overall, "
            f"though noticeably inconsistent across different modules this semester. "
            f"Several lecturers deliver material with clarity and genuine enthusiasm, making those sessions "
            f"highly productive and intellectually stimulating for the class. "
            f"However, a few courses suffer from disorganized delivery, limited interaction, and minimal "
            f"feedback on submitted work, which hampers the learning experience considerably. "
            f"I would {_pick(NEG_VERB)} the school to standardize teaching quality benchmarks and conduct "
            f"regular peer evaluations to ensure a more consistent and high-quality educational experience "
            f"for all students across every module and year level.")

def a_curriculum(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"The curriculum for my {prog} program at the {s} is well-designed and clearly aligned "
                f"with current industry demands and emerging professional trends in the field. "
                f"Course structures are logical, building progressively on foundational concepts before "
                f"introducing advanced topics, which gives students a solid intellectual scaffold. "
                f"The balance between theoretical foundations and practical application is {_pick(POS_ADJ)}, "
                f"with project-based assessments, case studies, and laboratory work that directly reflect "
                f"real-world professional scenarios I will encounter in my career. "
                f"I particularly value the inclusion of contemporary tools and technologies, which ensures "
                f"graduates are competitive and well-prepared for the demands of the modern job market.")
    if sentiment == "n":
        return (f"The {prog} curriculum at the {s} appears to lag behind current industry standards in "
                f"several significant areas that I believe require urgent review and revision. "
                f"Many courses continue to teach outdated tools and methodologies that are rarely used "
                f"in professional settings today, leaving students underprepared for actual workplace demands. "
                f"The curriculum also lacks sufficient elective depth and specialization pathways, "
                f"limiting students' ability to develop expertise in niche areas of growing importance. "
                f"I {_pick(NEG_VERB)} the Academic Affairs Office and school leadership to conduct "
                f"a thorough curriculum audit in close consultation with industry professionals and "
                f"alumni to ensure course content remains relevant, rigorous, and career-oriented.")
    return (f"The {prog} curriculum at the {s} covers the essential theoretical foundations competently "
            f"and provides a reasonable structure for academic progression throughout the degree. "
            f"Core modules are {_pick(MID_ADJ)} in their depth and breadth, covering key concepts "
            f"that form the basis of professional practice in this field. "
            f"However, the elective offerings could be significantly expanded to reflect emerging "
            f"trends and specialized career pathways that students are increasingly interested in. "
            f"Greater integration of industry collaboration — such as guest lectures, live projects, "
            f"and sponsored capstone work — would substantially strengthen the curriculum's practical "
            f"relevance and better prepare graduates for competitive employment.")

def a_assessment(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"The assessment methods employed in my {prog} courses at the {s} are {_pick(POS_ADJ)} "
                f"and demonstrate a thoughtful approach to measuring genuine student understanding. "
                f"The balanced mix of individual assignments, group projects, presentations, and written "
                f"examinations ensures that different learning styles and competencies are recognized "
                f"and fairly evaluated throughout the semester. "
                f"Rubrics are consistently shared in advance, assessment criteria are transparent, "
                f"and feedback is provided promptly enough to inform improvement in subsequent tasks. "
                f"I particularly {_pick(POS_VERB)} the emphasis on applied problem-solving assessments "
                f"rather than rote memorization, which I believe is a much stronger indicator of "
                f"actual competency and readiness for professional practice.")
    if sentiment == "n":
        return (f"The assessment practices in several of my {prog} modules at the {s} are "
                f"{_pick(NEG_ADJ)} and require significant restructuring to be fair and effective. "
                f"Grading rubrics are frequently absent or vague, leaving students uncertain about "
                f"the criteria used to evaluate their work, which undermines the integrity of the process. "
                f"Feedback on submitted assessments is often delayed by several weeks or is limited "
                f"to a single grade without actionable commentary to guide improvement. "
                f"I strongly {_pick(NEG_VERB)} the Academic Affairs Office to establish clear university-wide "
                f"assessment standards, enforce timely feedback policies, and require all lecturers "
                f"to publish detailed marking criteria before assessments are assigned.")
    return (f"Assessment practices in my {prog} program at the {s} are generally {_pick(MID_ADJ)}, "
            f"though there is meaningful room for improvement in both consistency and transparency. "
            f"Some modules employ well-designed assessments that genuinely test comprehension and "
            f"application, while others rely too heavily on high-stakes end-of-semester examinations "
            f"that do not adequately reflect students' ongoing learning throughout the term. "
            f"Timely feedback is provided by some lecturers but is inconsistent across the department. "
            f"Standardizing minimum feedback turnaround times and encouraging a more diverse portfolio "
            f"of assessment types would significantly improve the learning experience for all students.")

def a_lecturer_availability(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"Lecturer availability and responsiveness at the {s} has been one of the strongest "
                f"aspects of my {prog} student experience this semester, and I genuinely {_pick(POS_VERB)} it. "
                f"Faculty members consistently maintain clearly communicated office hours, respond to "
                f"email inquiries within one to two business days, and frequently offer additional "
                f"consultation sessions during busy assessment periods. "
                f"The approachable attitude of lecturers creates a supportive learning environment "
                f"where students feel comfortable raising questions, discussing challenges, and seeking "
                f"guidance on both academic work and career-related concerns. "
                f"This level of accessibility significantly enhances engagement and outcomes and is "
                f"something I hope will be maintained and encouraged across all departments.")
    if sentiment == "n":
        return (f"Lecturer accessibility has been a {_pick(NEG_ADJ)} aspect of my experience in the "
                f"{prog} program at the {s} this semester, and I believe it warrants serious attention. "
                f"Office hours are infrequently held and rarely communicated through official channels, "
                f"making it difficult for students to plan consultations around their own timetables. "
                f"Email responses are often delayed by more than a week, and some lecturers appear "
                f"unresponsive to student queries outside of formal class time entirely. "
                f"This lack of availability creates unnecessary barriers to learning and discourages "
                f"students from seeking help when they need it most. "
                f"I urge the school to enforce minimum availability standards for all faculty members.")
    return (f"Lecturer availability at the {s} for my {prog} courses is {_pick(MID_ADJ)}, with "
            f"noticeable differences between individual faculty members in their accessibility and "
            f"responsiveness to student needs outside of scheduled class sessions. "
            f"A number of lecturers are readily available and proactive in offering support, "
            f"which I find invaluable during intensive assignment and examination periods. "
            f"Others, however, have limited and poorly communicated office hours, "
            f"making it challenging to get timely guidance on coursework challenges. "
            f"Establishing a standardized minimum availability requirement and publishing these "
            f"schedules on the student portal would greatly improve accessibility for all students.")

def a_learning_resources(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"The learning resources and materials provided for my {prog} courses at the {s} "
                f"are {_pick(POS_ADJ)} and represent a significant strength of the program. "
                f"Course packs are comprehensive, well-organized, and current, incorporating recent "
                f"academic publications, industry white papers, and multimedia content that enriches "
                f"the learning experience beyond traditional textbooks. "
                f"The university's digital library provides broad access to peer-reviewed journals "
                f"and e-books, and the Learning Management System is intuitive, well-maintained, "
                f"and effectively used by lecturers to share materials in a timely manner. "
                f"I also {_pick(POS_VERB)} the provision of recorded lectures, which allows students "
                f"to revisit complex material at their own pace — a genuinely valuable academic resource.")
    if sentiment == "n":
        return (f"The learning materials provided for several of my {prog} courses at the {s} are "
                f"{_pick(NEG_ADJ)} and fall short of what students need to succeed academically. "
                f"Required textbooks are outdated and frequently out of stock in both the campus "
                f"bookstore and the library, forcing students to source materials independently "
                f"at considerable expense and inconvenience. "
                f"The Learning Management System is inconsistently used by lecturers — some post "
                f"materials days after class, and some modules have no digital resources whatsoever. "
                f"I strongly {_pick(NEG_VERB)} the Library Services and IT Support Department "
                f"to collaborate on ensuring all course resources are accessible digitally, "
                f"current, and available before the semester commences.")
    return (f"Learning resources for my {prog} program at the {s} are {_pick(MID_ADJ)}, "
            f"with some courses providing excellent, well-curated materials and others offering "
            f"minimal guidance beyond the core required textbook. "
            f"The library's digital collection is reasonable in scope but has some notable gaps "
            f"in specialized resources relevant to advanced topics in our field. "
            f"The LMS functions adequately as a distribution platform, though its use varies "
            f"significantly between lecturers, creating an inconsistent experience across modules. "
            f"A more standardized approach to resource provision, with minimum content requirements "
            f"per course, would considerably improve the consistency and quality of the learning environment.")

def a_it_infrastructure(sentiment, s, svc="IT Support Department", **kw):
    if sentiment == "p":
        return (f"The IT infrastructure and digital learning environment provided by the {svc} "
                f"is {_pick(POS_ADJ)} and has greatly supported my studies at the {s} this semester. "
                f"Campus Wi-Fi coverage is consistently strong and reliable across all academic "
                f"buildings, laboratories, and study spaces, enabling seamless online collaboration "
                f"and research activities throughout the day. "
                f"Computer labs are well-equipped with up-to-date hardware and licensed software "
                f"relevant to my field, reducing the burden on students to source tools independently. "
                f"The IT helpdesk is responsive and knowledgeable, resolving technical issues promptly "
                f"and minimizing disruption to student workflows. "
                f"I {_pick(POS_VERB)} the university's ongoing investment in digital infrastructure.")
    if sentiment == "n":
        return (f"The IT infrastructure managed by the {svc} presents {_pick(NEG_ADJ)} challenges "
                f"that significantly disrupt the academic experience at the {s}. "
                f"Wi-Fi connectivity is unreliable in several key areas of the campus, including "
                f"the main library, multiple lecture halls, and postgraduate study rooms, "
                f"making online coursework and research frustrating and inefficient. "
                f"Computer labs frequently have outdated or malfunctioning equipment, and software "
                f"licensing issues occasionally prevent students from accessing tools required for coursework. "
                f"The IT helpdesk response time is {_pick(NEG_ADJ)}, often taking several days "
                f"to resolve straightforward technical issues. "
                f"Urgent investment in infrastructure upgrades and improved support staffing is needed.")
    return (f"The IT infrastructure at the {s}, maintained by the {svc}, performs at a "
            f"{_pick(MID_ADJ)} level that meets basic student needs but falls short of what "
            f"is required to fully support a modern, technology-dependent academic environment. "
            f"Wi-Fi connectivity is generally stable in primary teaching spaces but becomes "
            f"inconsistent during peak usage hours and in peripheral campus locations. "
            f"Software availability in computer labs is adequate for core coursework but limited "
            f"for students requiring specialized applications for advanced projects. "
            f"Expanding bandwidth capacity, updating hardware on a regular replacement cycle, "
            f"and improving helpdesk responsiveness would meaningfully elevate the digital "
            f"learning experience for the entire student community.")

def a_admin_processes(sentiment, s, svc="Academic Affairs Office", **kw):
    if sentiment == "p":
        return (f"The academic administrative processes managed by the {svc} at the {s} "
                f"have been {_pick(POS_ADJ)} this semester, and I {_pick(POS_VERB)} the efficiency "
                f"and transparency with which they are handled. "
                f"Course registration was smooth and intuitive via the student portal, "
                f"with clear instructions provided well in advance of enrollment deadlines. "
                f"Grade appeals and transcript requests are processed promptly and communicated "
                f"through official channels with regular status updates that reduce student anxiety. "
                f"Administrative staff are approachable, knowledgeable, and genuinely helpful "
                f"when students encounter difficulties navigating university policies or procedures. "
                f"The overall administrative experience reflects a student-centered approach that "
                f"I believe enhances the broader university experience significantly.")
    if sentiment == "n":
        return (f"The academic administrative processes at the {s}, overseen by the {svc}, "
                f"have been a source of considerable frustration for many students this semester. "
                f"Course registration was plagued by system errors and conflicting timetables "
                f"that took weeks to resolve, causing students to miss early enrollment advantages. "
                f"Grade dispute processes are opaque and slow, with students waiting over a month "
                f"without updates or acknowledgment of their submissions. "
                f"Communication from administrative offices is reactive rather than proactive, "
                f"and staff sometimes provide inconsistent information depending on who is contacted. "
                f"I {_pick(NEG_VERB)} a comprehensive review of administrative workflows, "
                f"with investment in both system improvements and staff training as a matter of urgency.")
    return (f"Academic administrative processes at the {s} are {_pick(MID_ADJ)} in their "
            f"execution, meeting basic requirements but leaving clear room for improvement "
            f"in both speed and user-friendliness. "
            f"The online student portal functions adequately for routine tasks such as "
            f"registration and fee payment, but navigating more complex requests — such "
            f"as grade appeals or course exemptions — remains unnecessarily cumbersome. "
            f"Communication timelines are inconsistent, with some requests handled promptly "
            f"and others taking weeks without updates or acknowledgment. "
            f"Streamlining administrative workflows, improving the student portal's UX, "
            f"and setting clear service-level response standards would meaningfully reduce "
            f"administrative friction for the entire student body.")

def a_support_services(sentiment, s, svc="Student Affairs Office", **kw):
    if sentiment == "p":
        return (f"The student support services offered by the {svc} at the {s} have been "
                f"{_pick(POS_ADJ)} and have made a genuine difference to my overall well-being "
                f"and university experience throughout the semester. "
                f"Counseling services are readily accessible, professionally delivered, and "
                f"clearly communicated to students through multiple channels including the "
                f"student portal, orientation sessions, and notice boards. "
                f"The range of support available — from academic counseling to mental health "
                f"resources and financial hardship assistance — reflects a comprehensive understanding "
                f"of the diverse challenges students face during their academic journey. "
                f"I also {_pick(POS_VERB)} the regular student welfare check-ins organized "
                f"by the office, which foster a sense of community and belonging on campus.")
    if sentiment == "n":
        return (f"Student support services at the {s}, managed by the {svc}, are "
                f"{_pick(NEG_ADJ)} and fall significantly short of what students need "
                f"to manage the academic, personal, and financial challenges of university life. "
                f"Mental health support in particular is severely limited — appointment wait times "
                f"can exceed three weeks, which is unacceptable for students experiencing acute stress. "
                f"Financial hardship assistance processes are slow, bureaucratic, and poorly communicated, "
                f"leaving vulnerable students without timely help during critical periods. "
                f"The university must urgently expand its counseling capacity, simplify hardship "
                f"application procedures, and raise awareness of available services through more "
                f"proactive and visible outreach to the student community.")
    return (f"Student support services at the {s} are {_pick(MID_ADJ)} in their scope "
            f"and delivery, covering the essential categories but lacking depth and proactivity "
            f"in several important areas that affect student well-being. "
            f"Counseling services exist and are functional, but appointment availability is "
            f"limited and wait times are often longer than appropriate for students in need. "
            f"Financial support processes are reasonably accessible but require significant "
            f"paperwork and involve delays that reduce their effectiveness in urgent situations. "
            f"Investing in additional counseling staff, simplifying support request processes, "
            f"and proactively promoting available services — especially during high-stress "
            f"periods like mid-terms — would markedly improve the student experience.")

def a_facilities(sentiment, s, svc="Facilities Management", **kw):
    if sentiment == "p":
        return (f"The physical campus environment and facilities managed by the {svc} "
                f"provide a {_pick(POS_ADJ)} learning atmosphere that I believe genuinely "
                f"contributes to academic productivity and student well-being at the {s}. "
                f"Lecture halls are spacious, well-ventilated, and equipped with modern audio-visual "
                f"technology that facilitates clear and engaging presentations. "
                f"Study spaces — including individual carrels, group collaboration rooms, and "
                f"outdoor relaxation areas — are thoughtfully designed and well-maintained "
                f"throughout the academic week. "
                f"Cleaning and security standards are consistently high, and campus maintenance "
                f"requests are typically resolved within a reasonable timeframe. "
                f"The overall physical environment reflects a commitment to providing students "
                f"with a safe, comfortable, and inspiring place to learn.")
    if sentiment == "n":
        return (f"The physical facilities at the {s}, under the responsibility of the {svc}, "
                f"present {_pick(NEG_ADJ)} conditions that negatively impact the daily "
                f"learning experience of students. "
                f"Several lecture halls have malfunctioning air conditioning systems that make "
                f"studying in warm months genuinely uncomfortable and distracting. "
                f"Toilet facilities in older buildings are poorly maintained and frequently "
                f"reported without timely resolution from the facilities team. "
                f"Study spaces are chronically insufficient relative to the student population, "
                f"particularly during examination periods when demand peaks significantly. "
                f"I urge the university to prioritize facilities maintenance budgets, "
                f"establish a transparent issue-reporting system, and expand study space "
                f"capacity as part of its next capital improvement plan.")
    return (f"Campus facilities at the {s}, maintained by the {svc}, are generally "
            f"{_pick(MID_ADJ)} and adequate for day-to-day academic activities, "
            f"though several areas require attention and investment to meet growing needs. "
            f"Core academic spaces — including lecture halls and laboratories — are "
            f"functional and reasonably maintained, though some equipment is beginning "
            f"to show age and inconsistency in performance. "
            f"Student study and relaxation spaces are insufficient during peak periods, "
            f"and the condition of older campus buildings varies considerably. "
            f"A systematic facilities audit followed by a prioritized improvement plan "
            f"would help address longstanding issues and ensure the campus environment "
            f"supports the academic ambitions of all students more effectively.")

def a_finance(sentiment, s, svc="Finance Department", **kw):
    if sentiment == "p":
        return (f"The financial services provided by the {svc} at the {s} have been "
                f"{_pick(POS_ADJ)} this semester, and I genuinely {_pick(POS_VERB)} "
                f"the clarity, transparency, and efficiency with which they are managed. "
                f"Fee statements are issued promptly and accurately, with clear breakdowns "
                f"of tuition, facility charges, and any applicable scholarship deductions "
                f"that make it easy to verify and plan payments. "
                f"Payment options are flexible and well-communicated, including installment "
                f"plans that meaningfully reduce financial pressure on students and families. "
                f"Scholarship disbursements are processed on time and confirmed through "
                f"official notifications, removing uncertainty around critical financial support. "
                f"The finance office staff are professional, patient, and genuinely helpful "
                f"when navigating complex financial queries.")
    if sentiment == "n":
        return (f"The financial services managed by the {svc} at the {s} have been "
                f"a source of {_pick(NEG_ADJ)} experiences for me and several of my peers "
                f"this semester, and I feel it is important to communicate these concerns formally. "
                f"Scholarship disbursements were delayed by over six weeks this semester "
                f"without advance notice or clear explanation to affected students, "
                f"creating significant financial hardship for those who rely on these payments. "
                f"Fee statements are sometimes inaccurate, requiring multiple correction requests "
                f"that take considerable time and follow-up effort to resolve. "
                f"I strongly {_pick(NEG_VERB)} the Finance Department to implement automated "
                f"disbursement tracking, improve error-checking processes, and establish "
                f"proactive communication protocols when delays are anticipated.")
    return (f"Financial services at the {s}, managed by the {svc}, operate at a "
            f"{_pick(MID_ADJ)} level that fulfills basic requirements without particular "
            f"distinction in either efficiency or student-centeredness. "
            f"Tuition fee management and billing are generally accurate, though "
            f"occasional discrepancies require follow-up that can be time-consuming. "
            f"Scholarship and financial aid communication could be significantly improved — "
            f"students often report uncertainty about disbursement timelines and eligibility "
            f"criteria that creates unnecessary anxiety during critical financial planning periods. "
            f"Greater transparency through automated notifications, a clearer scholarship portal, "
            f"and improved staff responsiveness to financial queries would substantially "
            f"raise the standard of financial services for the student community.")

def a_recommendations(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"I have very few concerns to raise about my overall experience in the {prog} "
                f"program at the {s}, and I genuinely believe this institution provides "
                f"an {_pick(POS_ADJ)} educational environment that prepares students well "
                f"for their future careers. "
                f"If I were to recommend any improvement, I would suggest further expanding "
                f"industry partnership opportunities — additional mentorship programs, "
                f"sponsored capstone projects, and guest lecture series from senior professionals "
                f"would enrich an already strong academic offering. "
                f"Increasing the frequency of student feedback collection and demonstrating "
                f"visible action on that feedback would further strengthen trust between "
                f"students and the institution. "
                f"Overall, I am proud to be a student here and would highly recommend "
                f"this university to future applicants without hesitation.")
    if sentiment == "n":
        return (f"My key recommendation for the {s} is to urgently address the {_pick(NEG_ADJ)} "
                f"systemic issues that have affected {prog} students this semester, "
                f"rather than treating them as isolated incidents. "
                f"A structured, transparent student feedback mechanism — where concerns are "
                f"acknowledged within a set timeframe and outcomes communicated back to students — "
                f"would significantly rebuild trust that has been eroded by unaddressed issues. "
                f"I also strongly {_pick(NEG_VERB)} leadership to conduct a comprehensive "
                f"curriculum and service quality review in genuine consultation with current students, "
                f"alumni, and industry partners. "
                f"Without meaningful action on the concerns raised in this feedback, "
                f"student satisfaction and the institution's competitive standing will continue "
                f"to decline in the years ahead.")
    return (f"My main recommendations for improving the {prog} student experience at the {s} "
            f"center on consistency, communication, and investment in areas that currently "
            f"deliver only {_pick(MID_ADJ)} outcomes. "
            f"First, standardizing teaching quality, assessment practices, and resource "
            f"provision across all modules would significantly reduce the frustration caused "
            f"by the wide variability students currently experience between courses. "
            f"Second, improving the speed and transparency of administrative and financial "
            f"communications would reduce unnecessary anxiety and wasted time for students. "
            f"Finally, expanding industry engagement through internship pipelines, "
            f"career workshops, and alumni networking events would better equip graduates "
            f"for the increasingly competitive job market they will enter upon graduation.")

def a_overall_year(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"Reflecting on the full academic year in the {prog} program at the {s}, "
                f"I can say with confidence that this has been an {_pick(POS_ADJ)} and "
                f"transformative educational experience that has exceeded my expectations "
                f"in most meaningful ways. "
                f"The combination of rigorous coursework, dedicated faculty, strong peer community, "
                f"and access to industry connections has equipped me with both the technical "
                f"competencies and professional mindset needed to succeed in my chosen field. "
                f"I have grown significantly as a learner and feel genuinely prepared for the "
                f"next stage of my academic or professional journey. "
                f"I {_pick(POS_VERB)} the institution for maintaining high standards "
                f"throughout and look forward to continuing my studies here with great enthusiasm.")
    if sentiment == "n":
        return (f"My overall academic year experience in the {prog} program at the {s} "
                f"has unfortunately been {_pick(NEG_ADJ)} and has fallen considerably short "
                f"of the expectations I had when I enrolled. "
                f"Persistent issues with teaching quality, administrative responsiveness, "
                f"infrastructure reliability, and student support have collectively impacted "
                f"my ability to learn and thrive in this environment. "
                f"I feel that despite making this feedback heard through multiple channels, "
                f"meaningful change has been slow and the institution's response to student "
                f"concerns has lacked urgency and accountability. "
                f"I sincerely hope the upcoming academic year brings substantive improvements "
                f"in all the areas I have identified, not only for my own benefit "
                f"but for all students who will follow in future cohorts.")
    return (f"My overall experience in the {prog} program at the {s} during this academic "
            f"year has been {_pick(MID_ADJ)}, with meaningful highs and some notable lows "
            f"that I believe the institution has both the capacity and responsibility to address. "
            f"The academic content, when delivered well, is genuinely rigorous and relevant, "
            f"and I have formed valuable relationships with peers and some excellent faculty members. "
            f"However, structural issues — inconsistent teaching quality, administrative inefficiencies, "
            f"and gaps in student support — have at times undermined what could otherwise be "
            f"an exceptional educational experience. "
            f"With targeted improvements and a genuine commitment to acting on student feedback, "
            f"this institution has the foundations to become truly outstanding.")

def a_career_prep(sentiment, s, svc="Career Center", **kw):
    if sentiment == "p":
        return (f"The career preparation support provided by the {svc} at the {s} has been "
                f"{_pick(POS_ADJ)} and has made a tangible difference to my professional readiness "
                f"and employment prospects as I approach graduation. "
                f"Resume writing workshops, mock interviews, and industry networking events "
                f"have been well-organized, highly practical, and attended by credible "
                f"industry professionals who provided genuinely actionable feedback. "
                f"The internship matching program is effective, with clear communication "
                f"about available placements and strong follow-up support for students "
                f"during their internship periods. "
                f"I {_pick(POS_VERB)} the Career Center's proactive approach and its "
                f"strong relationships with employers, which have opened real opportunities "
                f"for students across all programs.")
    if sentiment == "n":
        return (f"Career preparation support from the {svc} at the {s} has been "
                f"{_pick(NEG_ADJ)} and has left many students — including myself — "
                f"feeling ill-equipped for the competitive graduate employment market. "
                f"Career workshops are infrequent, poorly promoted, and often scheduled "
                f"at times that conflict with lecture commitments, reducing student participation. "
                f"The internship database is outdated and contains many positions that "
                f"are no longer active, and support for students during internship placements "
                f"is minimal to nonexistent. "
                f"I {_pick(NEG_VERB)} the university to substantially reinvest in the "
                f"Career Center — expanding its employer network, modernizing its tools, "
                f"and increasing the frequency and quality of career development programming "
                f"across all academic programs and year levels.")
    return (f"Career preparation services at the {s}, offered through the {svc}, "
            f"are {_pick(MID_ADJ)} and meet some student needs while falling short in others. "
            f"Basic resume guidance and periodic career fairs provide a foundation, "
            f"but more intensive and personalized support would greatly benefit students "
            f"planning to enter a competitive and rapidly evolving job market. "
            f"The internship program has room for significant growth — expanding the employer "
            f"partner network, improving placement matching, and providing structured "
            f"mentorship during internship periods would make it substantially more valuable. "
            f"Regular industry panels and alumni engagement events would also meaningfully "
            f"bridge the gap between academic preparation and professional workplace expectations.")

def a_extracurricular(sentiment, s, svc="Student Affairs Office", **kw):
    if sentiment == "p":
        return (f"The extracurricular opportunities available at the {s}, coordinated by the "
                f"{svc}, are {_pick(POS_ADJ)} and represent a genuinely important complement "
                f"to the formal academic curriculum. "
                f"A wide and diverse range of student clubs, cultural societies, sports teams, "
                f"and volunteer programs are actively supported and well-resourced by the university, "
                f"enabling students to develop leadership skills, build social connections, "
                f"and pursue interests outside their academic programs. "
                f"Events are well-promoted, regularly scheduled, and inclusive in their design, "
                f"welcoming students from all backgrounds and programs to participate equally. "
                f"I {_pick(POS_VERB)} the institution's recognition that holistic student "
                f"development extends beyond classroom performance and into every dimension of "
                f"campus life.")
    if sentiment == "n":
        return (f"Extracurricular opportunities at the {s}, managed by the {svc}, are "
                f"{_pick(NEG_ADJ)} and poorly promoted, limiting student engagement "
                f"with the broader campus community significantly. "
                f"The range of active student clubs is narrow, with minimal support for "
                f"students wishing to establish new interest groups or activities that "
                f"reflect the diversity of the student population. "
                f"Events are inconsistently organized and inadequately funded, resulting "
                f"in low attendance and limited impact on the student community's sense "
                f"of belonging and engagement. "
                f"I strongly {_pick(NEG_VERB)} the Student Affairs Office to take a "
                f"more proactive and well-resourced approach to extracurricular programming, "
                f"recognizing its critical role in student retention and overall satisfaction.")
    return (f"Extracurricular activities at the {s} offer a {_pick(MID_ADJ)} range of "
            f"options that serve the interests of a portion of the student body but "
            f"do not yet reflect the full diversity of student interests and backgrounds. "
            f"Core clubs and major university events are reasonably well-organized and attended, "
            f"but support for emerging student initiatives is limited and the process "
            f"for establishing new clubs is unnecessarily bureaucratic. "
            f"Increasing the budget allocated to student activities, streamlining club "
            f"registration procedures, and investing in purpose-built student activity "
            f"spaces would encourage broader participation and strengthen the campus culture "
            f"for the benefit of all enrolled students.")

# ── Parent-specific answers ─────────────────────────────────────────────────

def a_parent_comm(sentiment, s, svc="Academic Affairs Office", child="my child", **kw):
    if sentiment == "p":
        return (f"As a parent, I find the {s}'s communication regarding {child}'s "
                f"academic progress to be {_pick(POS_ADJ)} and genuinely reassuring. "
                f"Semester progress reports are issued promptly through the parent portal, "
                f"and attendance alerts are sent in real time, allowing me to stay "
                f"informed and intervene early when needed. "
                f"I particularly {_pick(POS_VERB)} the parent information sessions organized "
                f"each semester, where faculty and administrators present academic expectations, "
                f"available support services, and the student performance outlook in detail. "
                f"The level of transparency and proactive communication from the {svc} "
                f"has greatly increased my confidence in the institution's commitment "
                f"to student success and parental partnership.")
    if sentiment == "n":
        return (f"I am {_pick(NEG_ADJ)}ly concerned about the lack of meaningful communication "
                f"from the {s} regarding {child}'s academic progress and overall welfare. "
                f"The parent portal is difficult to navigate, frequently displays outdated "
                f"information, and does not provide the real-time updates that are "
                f"essential for engaged parental monitoring. "
                f"I have sent multiple queries to the {svc} over the past term "
                f"and received responses that were delayed by weeks or were entirely generic. "
                f"As a parent who has invested significantly in my child's education, "
                f"I expect timely, accurate, and personalized communication that reflects "
                f"a genuine partnership between the university and the families it serves. "
                f"Urgent improvements to both the portal and communication processes are needed.")
    return (f"Communication from the {s} to parents regarding student progress is "
            f"{_pick(MID_ADJ)} and fulfills the minimum requirements, but falls short "
            f"of what a genuinely family-supportive institution should provide. "
            f"The parent portal provides access to basic grade and attendance data, "
            f"but the interface is somewhat outdated and not particularly intuitive "
            f"for parents who are not technology-confident. "
            f"Proactive outreach — for example, early alerts when a student's performance "
            f"or attendance begins to decline — is currently limited and reactive. "
            f"More frequent, personalized, and timely communication from the {svc} "
            f"would significantly strengthen the partnership between parents and the "
            f"institution in supporting student success.")

def a_parent_safety(sentiment, s, svc="Student Affairs Office", **kw):
    if sentiment == "p":
        return (f"Campus safety and student welfare at the {s} are {_pick(POS_ADJ)}, "
                f"and I feel confident that my child is studying in a secure "
                f"and well-monitored environment that prioritizes student well-being. "
                f"Security personnel are visibly present across campus during all hours, "
                f"CCTV coverage is comprehensive, and well-lit pathways ensure "
                f"safe movement even during evening hours. "
                f"The {svc} runs an impressive range of student welfare programs including "
                f"health screenings, mental health workshops, peer support networks, "
                f"and emergency assistance protocols that demonstrate a genuine institutional "
                f"commitment to holistic student care. "
                f"Knowing that these resources exist and are actively promoted gives "
                f"me great peace of mind as a parent.")
    if sentiment == "n":
        return (f"My confidence in the {s}'s ability to ensure {_pick(NEG_ADJ)} levels "
                f"of campus safety and student welfare has been significantly diminished "
                f"by several incidents and structural shortcomings reported to me by my child. "
                f"Security coverage appears insufficient in certain areas of campus, "
                f"particularly during late evening hours, and lighting in several pathways "
                f"is inadequate and has been reported without timely resolution. "
                f"Mental health support services are critically under-resourced — "
                f"my child was advised to wait over three weeks for a counseling appointment "
                f"during a period of acute personal difficulty, which is simply unacceptable. "
                f"I urge the {svc} to treat student welfare as a non-negotiable priority "
                f"and invest accordingly, without further delay.")
    return (f"Campus safety standards at the {s} are {_pick(MID_ADJ)}, providing "
            f"an adequate baseline of physical security and student welfare programming "
            f"while leaving meaningful room for improvement in several critical areas. "
            f"Core security measures — including campus access controls, security patrols, "
            f"and emergency contact systems — are functional and reasonably communicated. "
            f"However, mental health and counseling resources are stretched and insufficiently "
            f"staffed relative to the student population, creating unacceptable wait times "
            f"during periods of peak demand. "
            f"I would strongly encourage the {svc} to expand counseling capacity, "
            f"improve lighting and surveillance in underserved campus areas, and develop "
            f"a more proactive student welfare outreach program for at-risk individuals.")

def a_parent_financial(sentiment, s, svc="Finance Department", **kw):
    if sentiment == "p":
        return (f"The financial transparency and management provided by the {svc} at the {s} "
                f"has been {_pick(POS_ADJ)}, and I genuinely {_pick(POS_VERB)} the clarity "
                f"with which tuition fees, scholarship entitlements, and payment deadlines "
                f"are communicated to both students and their families. "
                f"Fee breakdowns are detailed, accurate, and issued well in advance of "
                f"payment deadlines, allowing adequate financial planning time. "
                f"The installment payment option is a genuinely thoughtful and practical "
                f"provision that reduces financial stress without compromising the "
                f"institution's financial management requirements. "
                f"Scholarship disbursements have been timely and confirmed through "
                f"official notifications, reinforcing trust in the university's "
                f"commitment to honoring its financial obligations to students and families.")
    if sentiment == "n":
        return (f"I have experienced {_pick(NEG_ADJ)} financial management from the {svc} "
                f"at the {s} that has caused considerable stress and inconvenience to "
                f"our family over the course of this academic year. "
                f"Scholarship disbursements were repeatedly delayed without advance notification, "
                f"and when I contacted the Finance Department for clarification, "
                f"responses were slow and sometimes contradictory between staff members. "
                f"Unexpected additional charges appeared on the fee statement mid-semester "
                f"without prior written notice, which I find both financially disruptive "
                f"and contrary to good institutional governance practices. "
                f"I formally request that the Finance Department implement automated disbursement "
                f"notifications, enforce accurate billing practices, and establish "
                f"a clear parent-facing communication protocol for all financial matters.")
    return (f"Financial management by the {svc} at the {s} has been {_pick(MID_ADJ)} "
            f"from my perspective as a parent, meeting the fundamental requirements "
            f"of tuition billing and payment processing without notable excellence or failure. "
            f"Fee statements are generally accurate, though occasional discrepancies "
            f"have required follow-up that is more time-consuming than it should be. "
            f"Communication about scholarship timelines could be significantly improved — "
            f"families benefit greatly from advance notice when disbursement dates shift "
            f"or eligibility criteria change, and this is currently lacking. "
            f"I would welcome a dedicated parent-facing financial FAQ and communication "
            f"channel to reduce the need for direct contact for routine financial queries.")

def a_parent_portal(sentiment, s, svc="IT Support Department", **kw):
    if sentiment == "p":
        return (f"The parent portal provided by the {s}, supported by the {svc}, "
                f"is {_pick(POS_ADJ)} in its design, functionality, and reliability, "
                f"and has become an invaluable tool for staying connected to my child's "
                f"academic journey throughout the year. "
                f"The interface is intuitive and well-organized, presenting grade information, "
                f"attendance records, fee statements, and university announcements in "
                f"a clear and accessible format that requires no technical expertise. "
                f"The system is reliably available, with minimal downtime, and "
                f"notifications are pushed promptly for important academic events "
                f"and institutional announcements. "
                f"I {_pick(POS_VERB)} the university's investment in digital parent "
                f"engagement tools, which I believe genuinely strengthen the home-university "
                f"partnership and support better student outcomes.")
    if sentiment == "n":
        return (f"The parent portal at the {s}, managed by the {svc}, is {_pick(NEG_ADJ)} "
                f"in its functionality, reliability, and user experience, and has "
                f"been more of a source of frustration than a useful communication tool. "
                f"The interface is dated and difficult to navigate, with key information "
                f"such as grade details and attendance records buried under multiple menu layers. "
                f"The system experiences frequent downtime — often during critical periods "
                f"such as grade release and enrollment — and error messages provide "
                f"no useful guidance for resolving access issues independently. "
                f"I strongly {_pick(NEG_VERB)} a complete redesign of the parent portal "
                f"with a focus on intuitive UX, mobile compatibility, and real-time "
                f"data synchronization to bring it in line with modern digital standards.")
    return (f"The parent portal at the {s} functions at a {_pick(MID_ADJ)} level "
            f"that provides access to essential information but lacks the polish "
            f"and reliability expected of a modern institutional digital platform. "
            f"Grade and attendance data are generally accessible, though refresh rates "
            f"can be slow and the interface requires familiarity before becoming navigable. "
            f"The portal is not optimized for mobile devices, which is a significant "
            f"limitation given that most parents primarily use smartphones for digital access. "
            f"Push notification functionality exists but is inconsistently triggered, "
            f"meaning important updates are sometimes missed. "
            f"A targeted UX improvement initiative — focusing on mobile responsiveness, "
            f"navigation clarity, and reliable notifications — would greatly increase "
            f"parental engagement and satisfaction with the digital experience.")

def a_parent_counseling(sentiment, s, svc="Academic Affairs Office", child="my child", **kw):
    if sentiment == "p":
        return (f"Academic counseling and advising services at the {s}, coordinated by the "
                f"{svc}, have been {_pick(POS_ADJ)} in supporting {child}'s academic "
                f"planning and decision-making throughout the year. "
                f"Assigned academic advisors are knowledgeable, approachable, and "
                f"proactively schedule meetings at key decision points in the academic calendar — "
                f"such as course selection, internship planning, and graduation preparation. "
                f"The quality and consistency of advice my child has received has "
                f"given our family confidence that their academic trajectory is being "
                f"thoughtfully guided by experienced professionals who understand both "
                f"the program requirements and the student's individual goals. "
                f"This service is clearly a strength of the institution.")
    if sentiment == "n":
        return (f"Academic counseling services at the {s} have been {_pick(NEG_ADJ)} "
                f"in their availability, quality, and proactivity from my perspective as a parent "
                f"observing {child}'s experience this academic year. "
                f"Appointments with academic advisors are difficult to secure, often requiring "
                f"weeks of waiting for a short session that does not always result in "
                f"actionable or personalized guidance. "
                f"The advice provided is sometimes generic and does not demonstrate "
                f"familiarity with the student's individual history, goals, or challenges. "
                f"I strongly {_pick(NEG_VERB)} the {svc} to increase its counseling "
                f"staff capacity, invest in advisor training, and implement proactive "
                f"outreach to students who may be struggling academically before "
                f"their situations deteriorate into formal academic difficulties.")
    return (f"Academic counseling at the {s} is {_pick(MID_ADJ)}, covering essential "
            f"advising needs without providing the depth and personalization that "
            f"would truly distinguish the service. "
            f"My child has found their assigned advisor to be approachable and knowledgeable "
            f"on the whole, though appointment availability is sometimes limited during "
            f"peak periods of the academic calendar. "
            f"The counseling provided tends to be reactive — responding to student-initiated "
            f"queries rather than proactively identifying and addressing potential challenges "
            f"before they escalate. "
            f"A more structured check-in model, combined with a larger and better-trained "
            f"advising team, would significantly improve the consistency and impact "
            f"of academic counseling across the institution.")

def a_parent_overall(sentiment, s, **kw):
    if sentiment == "p":
        return (f"As a parent who has closely observed my child's experience at the {s} "
                f"over the past year, I can say with genuine satisfaction that the institution "
                f"has provided an {_pick(POS_ADJ)} educational and personal development environment "
                f"that has exceeded our family's expectations in most meaningful respects. "
                f"The combination of academic rigor, caring faculty, comprehensive student support, "
                f"and strong career preparation has resulted in visible and meaningful growth "
                f"in my child's competence, confidence, and professional readiness. "
                f"I would enthusiastically recommend this university to other families "
                f"seeking a high-quality, student-centered tertiary education for their children, "
                f"and I look forward to continuing to partner with the institution as my child "
                f"completes the remainder of their degree.")
    if sentiment == "n":
        return (f"Reflecting on my child's full year of study at the {s}, I find myself "
                f"with {_pick(NEG_ADJ)} concerns about the institution's ability to "
                f"consistently deliver on the educational and welfare commitments it promotes "
                f"to prospective students and their families. "
                f"Persistent issues with teaching quality in certain departments, "
                f"administrative responsiveness, digital platform reliability, and "
                f"student support capacity have collectively made a difficult academic "
                f"transition more challenging than it needed to be. "
                f"I would strongly urge university leadership to prioritize meaningful "
                f"engagement with the concerns raised in parent feedback, establish "
                f"clear accountability mechanisms, and communicate specific improvement "
                f"actions transparently to the parent community in the coming semester.")
    return (f"My overall assessment of the {s} as a parent is that it offers a "
            f"{_pick(MID_ADJ)} educational experience with genuine strengths that are "
            f"unfortunately balanced by structural weaknesses that need sustained attention. "
            f"The academic programs are broadly well-designed, and there are individual "
            f"faculty members and support staff who clearly go above and beyond for students. "
            f"However, system-level inconsistencies in service quality, communication, "
            f"and resource provision create an uneven experience that depends too heavily "
            f"on which individual staff members a student encounters. "
            f"I encourage the institution to invest in building reliable systems and "
            f"consistent standards that ensure every student — regardless of program or year — "
            f"receives the same high-quality support and educational experience.")

# ── Internship (employer) answers ───────────────────────────────────────────

def a_intern_technical(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"The intern from the {s}'s {prog} program demonstrated {_pick(POS_ADJ)} "
                f"technical competency that significantly exceeded our initial expectations "
                f"for a student at this stage of their academic career. "
                f"Their foundational knowledge in core discipline areas was solid, "
                f"well-structured, and readily applicable to real workplace challenges "
                f"encountered during the internship period. "
                f"They adapted quickly to our internal tools, methodologies, and technical "
                f"standards, requiring minimal remedial instruction before becoming a "
                f"productive and largely self-directed contributor to assigned projects. "
                f"The depth of practical skills, particularly in applied problem-solving "
                f"and technical documentation, was notably strong and reflects well "
                f"on the quality of the {s}'s curriculum design and delivery.")
    if sentiment == "n":
        return (f"The intern's technical competency revealed {_pick(NEG_ADJ)} gaps "
                f"between what the {s}'s {prog} curriculum covers and the practical "
                f"skills required in a professional workplace environment. "
                f"While the intern possessed a reasonable theoretical grounding in core concepts, "
                f"they struggled to translate this knowledge into practical application "
                f"without significant guidance and hand-holding from senior team members. "
                f"Proficiency in industry-standard tools and workflows was below "
                f"the level we typically expect from graduates at a comparable stage, "
                f"and several foundational technical skills needed to be reinforced on the job. "
                f"We strongly recommend the {s} review its curriculum to better align "
                f"academic content with current industry tool and practice standards.")
    return (f"The intern from the {s}'s {prog} program showed {_pick(MID_ADJ)} technical "
            f"competency, with a solid theoretical foundation that required additional "
            f"scaffolding to translate effectively into professional practice. "
            f"Core technical knowledge in the primary discipline areas was present and "
            f"generally accurate, enabling the intern to engage meaningfully with assigned tasks "
            f"after an initial onboarding period. "
            f"However, familiarity with specific industry-standard tools and processes "
            f"was limited, requiring time investment from senior staff to bridge the gap. "
            f"Stronger emphasis on applied tool training and industry-facing projects "
            f"within the curriculum would produce more immediately effective graduates "
            f"and reduce the onboarding burden on host companies.")

def a_intern_professionalism(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"The professional attitude demonstrated by this intern from the {s}'s "
                f"{prog} program was {_pick(POS_ADJ)} and genuinely impressed our team "
                f"throughout the internship period. "
                f"Punctuality, reliability, and a consistently positive and collaborative "
                f"work ethic were evident from the very first week, requiring no correction "
                f"or management intervention to maintain. "
                f"The intern communicated proactively, raised concerns and questions through "
                f"appropriate channels, and responded to feedback constructively "
                f"and without defensiveness. "
                f"Their professional maturity — particularly in managing competing deadlines, "
                f"handling ambiguity, and engaging respectfully with colleagues at all levels "
                f"— reflects a level of preparation that speaks well of the {s}'s "
                f"commitment to producing work-ready graduates.")
    if sentiment == "n":
        return (f"The intern's professional conduct required {_pick(NEG_ADJ)} levels of "
                f"management intervention that were unexpected for a student from the {s}'s "
                f"{prog} program at this career stage. "
                f"Punctuality was inconsistent during the first half of the internship period, "
                f"and proactive communication about delays or challenges was largely absent "
                f"without repeated prompting from supervisors. "
                f"Response to constructive feedback was occasionally defensive, and the intern "
                f"demonstrated some difficulty adapting to workplace expectations around "
                f"presentation, tone, and professional documentation standards. "
                f"We recommend the {s} incorporate more structured professional readiness "
                f"training — including workplace simulation, communication skills, and "
                f"feedback-receiving practice — into its curriculum before students enter the workforce.")
    return (f"This intern's professionalism was {_pick(MID_ADJ)}, showing genuine commitment "
            f"and a positive attitude that formed a solid foundation, with some areas "
            f"requiring coaching and development during the placement period. "
            f"Reliability and punctuality were good overall, though proactive communication "
            f"about progress and obstacles was inconsistent and required encouragement from supervisors. "
            f"The intern engaged positively with team members and accepted feedback constructively "
            f"in most situations, demonstrating the willingness to learn that is essential "
            f"for professional growth. "
            f"Additional preparation in formal workplace communication — particularly "
            f"written reporting standards and stakeholder update practices — "
            f"would improve the professional impact of graduates from this program.")

def a_intern_teamwork(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"The intern integrated into our team environment {_pick(POS_ADJ)}ly "
                f"and became a valued collaborative contributor from an early stage "
                f"of the internship, consistently demonstrating the interpersonal skills "
                f"required to function effectively in a professional team setting. "
                f"They participated actively in team meetings, contributed ideas respectfully "
                f"and constructively, and took clear ownership of their assigned workstreams "
                f"without requiring constant supervision or direction from colleagues. "
                f"During group project phases, the intern's ability to coordinate tasks, "
                f"manage shared deadlines, and maintain positive relationships under pressure "
                f"was {_pick(POS_ADJ)} and significantly contributed to successful outcomes. "
                f"These teamwork capabilities reflect very well on the interpersonal "
                f"skills development embedded in the {s}'s {prog} program.")
    if sentiment == "n":
        return (f"The intern's ability to collaborate effectively within a team environment "
                f"was {_pick(NEG_ADJ)} and required more management attention than anticipated. "
                f"Contribution to group tasks was often uneven — the intern sometimes "
                f"worked in isolation rather than coordinating with colleagues, "
                f"leading to duplicated effort and avoidable misalignments in shared workstreams. "
                f"Communication within the team was reactive rather than proactive, "
                f"and the intern occasionally struggled with the shared accountability "
                f"and compromise that effective team collaboration demands. "
                f"We recommend the {s} incorporate more structured team-based project work "
                f"and collaborative simulation into the {prog} curriculum to better "
                f"prepare students for the realities of modern workplace team dynamics.")
    return (f"This intern's teamwork skills were {_pick(MID_ADJ)}, with a genuine "
            f"willingness to collaborate balanced by some developmental areas "
            f"that became apparent as project complexity increased. "
            f"The intern worked well in low-ambiguity team tasks with clear role definitions, "
            f"but required additional support when navigating more complex team dynamics "
            f"involving competing priorities, unclear ownership, or conflicting perspectives. "
            f"Communication within the team improved noticeably over the internship duration, "
            f"which is an encouraging sign of learning and adaptability. "
            f"Further emphasis on collaborative project work, cross-functional team exercises, "
            f"and conflict resolution skills in the {prog} curriculum would produce "
            f"more team-ready graduates for the professional environment.")

def a_intern_problem_solving(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"The intern's problem-solving abilities were among the most {_pick(POS_ADJ)} "
                f"attributes they brought to our organization from the {s}'s {prog} program. "
                f"When confronted with unfamiliar challenges or technical obstacles, "
                f"the intern approached them systematically — breaking problems into "
                f"manageable components, forming and testing hypotheses, and escalating "
                f"appropriately only when genuinely blocked by limitations beyond their current capability. "
                f"Their intellectual curiosity, persistence under pressure, and willingness "
                f"to explore unconventional solutions made them a genuinely valuable "
                f"problem-solver within the team. "
                f"This quality is difficult to teach in the workplace and speaks highly "
                f"of the critical thinking culture embedded in the {s}'s academic programs.")
    if sentiment == "n":
        return (f"Problem-solving was a {_pick(NEG_ADJ)} area for this intern, "
                f"representing the most significant gap between the {s}'s {prog} graduates "
                f"and our professional workforce expectations. "
                f"The intern often sought direct guidance from supervisors before "
                f"attempting independent analysis or solution development, "
                f"limiting their ability to work autonomously on complex assignments. "
                f"When initial approaches failed, pivoting strategy independently proved difficult, "
                f"and the intern sometimes became visibly discouraged rather than "
                f"treating failure as diagnostic information to inform the next attempt. "
                f"Building a stronger culture of structured problem-solving — through case studies, "
                f"debugging exercises, and open-ended challenges — in the {prog} curriculum "
                f"would produce significantly more effective graduates.")
    return (f"Problem-solving capabilities for this intern from the {s}'s {prog} program "
            f"were {_pick(MID_ADJ)}, reflecting a sound foundational analytical approach "
            f"with room for development in handling more complex, ambiguous challenges. "
            f"For well-defined problems with clear parameters, the intern performed "
            f"competently and demonstrated sound logical reasoning and structured analysis. "
            f"However, when problems were ambiguous, multi-layered, or required "
            f"creative reframing of assumptions, the intern benefited significantly "
            f"from supervisor guidance to stay productive. "
            f"Incorporating more open-ended, ill-defined problem scenarios into coursework "
            f"and assessments would better prepare graduates for the messy, "
            f"constraint-rich challenges of professional practice.")

def a_intern_adaptability(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"The intern's adaptability to our workplace culture, processes, and "
                f"evolving project requirements was {_pick(POS_ADJ)} and demonstrated "
                f"a level of professional resilience and flexibility that we consistently "
                f"value in permanent hires. "
                f"Changes to project scope, team structure, and delivery timelines were "
                f"managed with composure, and the intern made adjustments to their "
                f"work approach quickly and effectively without requiring extended "
                f"support or reassurance from management. "
                f"They were proactive in seeking to understand the context behind "
                f"changes rather than simply executing instructions, which allowed them "
                f"to contribute meaningfully even in fluid project environments. "
                f"This quality reflects a well-rounded education at the {s} that "
                f"extends beyond technical training to genuine professional agility.")
    if sentiment == "n":
        return (f"Adaptability to changing conditions and evolving requirements was "
                f"a {_pick(NEG_ADJ)} challenge for this intern from the {s}'s {prog} program, "
                f"and it became a recurring obstacle during the internship period. "
                f"When project scope or priorities shifted — as they regularly do in "
                f"a professional environment — the intern's response was often slow "
                f"and required significant reassurance and directive guidance from supervisors. "
                f"Tolerance for ambiguity and the ability to operate effectively "
                f"without complete information or a fully defined task specification "
                f"were noticeably underdeveloped relative to our expectations. "
                f"We recommend the {s} expose students to more dynamic, "
                f"ambiguity-tolerant project environments during their studies to "
                f"develop this critical professional competency before graduation.")
    return (f"This intern showed {_pick(MID_ADJ)} adaptability to our work environment, "
            f"adjusting reasonably well to most situations while requiring additional "
            f"support when changes occurred at a faster pace or scale than anticipated. "
            f"Day-to-day routine adjustments — such as modified task priorities or "
            f"new tool adoption — were handled efficiently and without notable disruption. "
            f"More significant changes, such as project pivots or team restructuring, "
            f"required more guidance to navigate smoothly and confidently. "
            f"Greater exposure to agile methodologies, sprint-based workflows, and "
            f"change management principles in the {prog} curriculum would strengthen "
            f"the adaptability of graduates entering dynamic professional environments.")

def a_intern_english(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"The intern's English communication proficiency — both written and spoken — "
                f"was {_pick(POS_ADJ)} and met the professional standards required "
                f"for effective participation in our bilingual team environment. "
                f"Written reports, emails, and documentation were consistently clear, "
                f"professionally structured, and free of errors that would compromise "
                f"understanding or credibility in a client-facing context. "
                f"Verbal communication in meetings and collaborative sessions was "
                f"confident and coherent, enabling full participation in discussions "
                f"with both local and international colleagues. "
                f"The intern's English proficiency reflects well on the language preparation "
                f"embedded in the {s}'s {prog} program and is a strong asset "
                f"in our increasingly international work environment.")
    if sentiment == "n":
        return (f"English communication proficiency was a {_pick(NEG_ADJ)} limitation "
                f"for this intern from the {s}'s {prog} program that impacted "
                f"their effectiveness in several key areas of their role. "
                f"Written communication — including emails and technical documentation — "
                f"frequently contained grammatical and structural errors that required "
                f"editing by supervisors before use in internal or external contexts. "
                f"Verbal participation in English-language meetings was hesitant, "
                f"limiting the intern's ability to contribute fully to discussions "
                f"or to represent the team confidently in broader organizational settings. "
                f"We strongly recommend the {s} elevate its English communication "
                f"training requirements — particularly for professional writing and "
                f"spoken business English — as a core graduation competency for all programs.")
    return (f"English communication capability for this intern was {_pick(MID_ADJ)}, "
            f"sufficient for routine internal tasks but requiring development to meet "
            f"the standards expected in professional, client-facing, or international contexts. "
            f"Reading comprehension of English-language materials was generally strong, "
            f"enabling effective research and document processing independently. "
            f"However, written composition — particularly formal reports and professional emails — "
            f"required editing support, and verbal fluency in meetings was limited, "
            f"particularly when discussions moved at pace or involved complex technical vocabulary. "
            f"Strengthening English for Professional Purposes training in the {prog} "
            f"curriculum would meaningfully enhance graduates' communication readiness "
            f"for the modern, increasingly international workplace.")

def a_intern_curriculum_feedback(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"Based on our experience with this intern from the {s}'s {prog} program, "
                f"we are {_pick(POS_ADJ)}ly impressed with the alignment between the academic "
                f"curriculum and the practical demands of our industry. "
                f"The foundational knowledge, theoretical frameworks, and applied skills "
                f"the intern brought to the role mapped closely to what we require "
                f"in graduate-level professional practitioners in this field. "
                f"In particular, the project-based and problem-solving components of "
                f"the curriculum appear to have translated well into workplace readiness. "
                f"We would encourage the {s} to continue developing its industry connections "
                f"and to involve practitioners actively in curriculum review to maintain "
                f"this strong alignment as the professional landscape continues to evolve.")
    if sentiment == "n":
        return (f"Our experience with this intern has highlighted {_pick(NEG_ADJ)} gaps "
                f"between what the {s}'s {prog} curriculum delivers and what the "
                f"professional industry actually requires from graduates in this field. "
                f"Specifically, the intern lacked working proficiency in several tools "
                f"and methodologies that are now industry standard, requiring us to "
                f"invest significant onboarding time in areas that should be covered academically. "
                f"Soft skills — particularly professional communication, project management, "
                f"and stakeholder management — also appeared underdeveloped relative "
                f"to what professional roles at this level require from day one. "
                f"We would welcome the opportunity to engage with the {s}'s curriculum "
                f"design team to provide specific, actionable recommendations for improvement.")
    return (f"Our curriculum-related feedback for the {s}'s {prog} program, "
            f"based on this internship experience, is {_pick(MID_ADJ)}: there is "
            f"a reasonable foundation but meaningful gaps that the institution could "
            f"address to significantly improve graduate readiness. "
            f"Core theoretical knowledge is adequately covered, and the intern was "
            f"able to apply foundational concepts with reasonable effectiveness. "
            f"However, gaps exist in applied tool proficiency, project management fundamentals, "
            f"and the professional communication standards expected in industry settings. "
            f"We recommend more regular and structured industry consultations to ensure "
            f"the curriculum remains current, and greater emphasis on workplace simulation "
            f"through live projects, internships, and industry-sponsored assessments.")

def a_intern_performance(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"The overall performance of this intern from the {s}'s {prog} program "
                f"has been {_pick(POS_ADJ)} and has added genuine value to our organization "
                f"during the internship period in ways we did not fully anticipate at the outset. "
                f"Key deliverables were completed on time, to the required quality standard, "
                f"and in some cases with additional initiative that exceeded the brief. "
                f"The intern's contributions to ongoing team projects have been meaningful "
                f"and will have a lasting impact beyond the duration of their placement. "
                f"We are very satisfied with the investment we made in hosting this intern "
                f"and have recommended internally that we continue and expand our partnership "
                f"with the {s}'s internship program in the coming academic year.")
    if sentiment == "n":
        return (f"Overall, the intern's performance during this placement was {_pick(NEG_ADJ)} "
                f"and fell below the standard we expected based on the {s}'s {prog} program reputation. "
                f"While the intern showed genuine enthusiasm and willingness to engage "
                f"with assigned tasks, output quality was inconsistent, deadlines were "
                f"occasionally missed without adequate advance communication, "
                f"and independent contribution to team goals was limited relative "
                f"to the support investment required from supervisors. "
                f"We encourage the {s} to strengthen the preparatory components of "
                f"its internship program — including pre-placement coaching and more "
                f"rigorous selection criteria — to better match student readiness "
                f"with the expectations of professional host organizations.")
    return (f"This intern's overall performance was {_pick(MID_ADJ)}, delivering "
            f"a useful contribution to the team while also clearly indicating areas "
            f"where additional academic preparation would improve professional readiness. "
            f"Assigned tasks were generally completed to a functional standard, "
            f"with quality improving progressively as the intern built familiarity "
            f"with our tools, processes, and expectations over the placement period. "
            f"The growth trajectory was positive and suggests genuine potential "
            f"that a stronger academic foundation would help realize more quickly. "
            f"We see this internship as a successful learning experience for the student "
            f"and encourage the {s} to continue building practical readiness "
            f"into its curriculum to produce even more effective graduates.")

def a_intern_hire_again(sentiment, s, prog, **kw):
    if sentiment == "p":
        return (f"Based on this intern's performance and the overall quality of graduates "
                f"we have observed from the {s}'s {prog} program, we would absolutely "
                f"consider hiring from this institution in the future — both for internships "
                f"and for permanent graduate positions. "
                f"The intern's technical competency, professional attitude, collaborative "
                f"skills, and growth mindset align closely with the profile we seek "
                f"when making graduate hiring decisions. "
                f"We are actively discussing a return internship offer for this individual "
                f"and have already flagged the {s} as a preferred graduate source "
                f"institution for our talent acquisition team. "
                f"We would encourage the {s} to continue deepening its industry "
                f"partnerships and look forward to an ongoing and mutually beneficial "
                f"relationship with the institution in the years ahead.")
    if sentiment == "n":
        return (f"While we respect the {s} as an institution and do not question "
                f"its academic credentials, our experience with this particular intern "
                f"from the {prog} program has given us {_pick(NEG_ADJ)} reservations "
                f"about recruiting heavily from this cohort in the near future. "
                f"The skill gaps and professional readiness challenges encountered "
                f"during this placement represent a significant onboarding investment "
                f"that strains our capacity as a host organization. "
                f"We would encourage the {s} to engage directly with industry partners "
                f"— including ourselves — to understand the specific competency gaps "
                f"and develop targeted solutions before we could confidently increase "
                f"our intake of graduates from this program. "
                f"We remain open to future engagement if meaningful curriculum improvements "
                f"are implemented and communicated to the industry community.")
    return (f"We would cautiously consider hiring from the {s}'s {prog} program again, "
            f"with the expectation that the skill and readiness gaps we observed in "
            f"this internship experience would be addressed through curriculum improvements "
            f"in the near term. "
            f"The intern's core attitude and growth potential were positive, and these "
            f"qualities form a solid basis for future professional development. "
            f"However, we would want to see stronger applied technical skills, "
            f"better English communication preparation, and more structured professional "
            f"readiness training before we significantly expand our intake from this institution. "
            f"We encourage the {s} to reach out to us directly to establish "
            f"a closer industry-academia collaboration that benefits both "
            f"future interns and our organization's talent development strategy.")

# ── Question banks ──────────────────────────────────────────────────────────

MID_TERM_Qs = [
    "How would you rate the overall quality of teaching in your courses this semester so far?",
    "How well does the course content align with current industry standards and your career aspirations?",
    "How effective are the assessment methods (assignments, quizzes, exams) in evaluating your understanding of the subject matter?",
    "How would you describe the availability and responsiveness of your lecturers outside of scheduled class time?",
    "How satisfied are you with the learning resources and materials provided for your courses this semester?",
    "How would you rate the IT infrastructure and digital learning tools provided by the university to support your studies?",
    "How efficient have you found the academic administrative processes such as registration, grade appeals, and scheduling?",
    "How would you evaluate the quality and accessibility of student support services currently available at this university?",
    "How well does the university's physical environment and facilities support your daily learning experience?",
    "What specific improvements would you most like to see implemented for the remainder of this semester?",
]

YEAR_END_Qs = [
    "Reflecting on the full academic year, how would you rate your overall educational experience at this university?",
    "How effectively do you believe this year's coursework has prepared you for your future career or further academic studies?",
    "How would you assess the progression of your academic skills and knowledge throughout this academic year?",
    "How satisfied are you with the extracurricular activities, student clubs, and personal development opportunities available?",
    "How well has the university's Career Center prepared you for internship opportunities and graduate employment?",
    "How would you rate the university's financial services, including tuition fee management and scholarship support?",
    "How would you evaluate the IT infrastructure and digital services provided by the university over the course of the year?",
    "How satisfied are you with the library resources — both physical and digital — that were available throughout the academic year?",
    "How effectively did the university communicate important information, deadlines, and updates throughout the academic year?",
    "What are your key recommendations for improving the overall student experience in the coming academic year?",
]

PARENTS_Qs = [
    "How would you rate the university's communication with parents regarding your child's academic progress and welfare?",
    "How satisfied are you with the quality of education your child is receiving at this university?",
    "How confident are you in the university's ability to prepare your child for future career opportunities?",
    "How would you assess the campus safety measures and student welfare programs in place at this institution?",
    "How transparent and straightforward have you found the university's financial policies, fee management, and scholarship communication?",
    "How effective do you find the parent portal and digital communication systems provided by the university?",
    "How satisfied are you with the academic counseling and advising support your child receives?",
    "How well does the university address students' mental health and personal well-being needs?",
    "How would you evaluate the quality and suitability of the university's physical facilities and campus environment?",
    "What improvements would you suggest to enhance the university's support for both students and their families?",
]

INTERNSHIP_Qs = [
    "How would you rate the technical competency of the student intern in their relevant field of study?",
    "How well did the intern demonstrate professional communication and interpersonal skills in the workplace?",
    "How effectively did the intern collaborate with team members and contribute to group projects?",
    "How would you assess the intern's problem-solving abilities and approach to challenging or unfamiliar tasks?",
    "How quickly and effectively did the intern adapt to your company's work culture, tools, and environment?",
    "How proficient was the intern in English communication, both written and verbal, for professional purposes?",
    "How well did the intern's academic training align with the practical demands and standards of your industry?",
    "What specific technical or soft skill areas do you believe the university curriculum should strengthen for future graduates?",
    "How would you rate the intern's overall performance and value contribution to your organization during the placement?",
    "Based on your experience with this intern, would you consider hiring from this university in the future, and why?",
]

ANSWER_FUNCS = {
    "MID_TERM":  [a_teaching, a_curriculum, a_assessment, a_lecturer_availability,
                  a_learning_resources, a_it_infrastructure, a_admin_processes,
                  a_support_services, a_facilities, a_recommendations],
    "YEAR_END":  [a_overall_year, a_career_prep, a_curriculum, a_extracurricular,
                  a_career_prep, a_finance, a_it_infrastructure, a_learning_resources,
                  a_admin_processes, a_recommendations],
    "PARENTS":   [a_parent_comm, a_teaching, a_career_prep, a_parent_safety,
                  a_parent_financial, a_parent_portal, a_parent_counseling,
                  a_support_services, a_facilities, a_parent_overall],
    "INTERNSHIP":[a_intern_technical, a_intern_professionalism, a_intern_teamwork,
                  a_intern_problem_solving, a_intern_adaptability, a_intern_english,
                  a_intern_curriculum_feedback, a_intern_curriculum_feedback,
                  a_intern_performance, a_intern_hire_again],
}

# Service routing heuristics per question index
SERVICE_HINTS = {
    "MID_TERM":  [None, "ACADEMIC", "ACADEMIC", None, "LIBRARY", "IT_SUPPORT",
                  "ACADEMIC", "STUDENT_AFFAIRS", "FACILITIES", None],
    "YEAR_END":  [None, "CAREER", "ACADEMIC", "STUDENT_AFFAIRS", "CAREER",
                  "FINANCE", "IT_SUPPORT", "LIBRARY", "ACADEMIC", None],
    "PARENTS":   ["ACADEMIC", None, "CAREER", "STUDENT_AFFAIRS", "FINANCE",
                  "IT_SUPPORT", "ACADEMIC", "STUDENT_AFFAIRS", "FACILITIES", None],
    "INTERNSHIP":[None, None, None, None, None, None, "CAREER", "ACADEMIC", None, "CAREER"],
}

SENTIMENT_WEIGHTS = {
    "p": 0.40, "n": 0.25, "m": 0.35,
}

def weighted_sentiment():
    r = random.random()
    if r < 0.40: return "p"
    if r < 0.65: return "n"
    return "m"

def overall_sentiment_label(sentiments):
    pos = sentiments.count("p")
    neg = sentiments.count("n")
    if pos >= 7:  return "positive"
    if neg >= 7:  return "negative"
    if pos > neg: return "mostly_positive"
    if neg > pos: return "mostly_negative"
    return "mixed"

def derive_services(fb_type, sentiments, school_id, q_sentiments):
    svcs = set()
    hints = SERVICE_HINTS[fb_type]
    for i, s in enumerate(q_sentiments):
        if hints[i] and s in ("n", "m"):
            svcs.add(hints[i])
        if hints[i] and s == "p":
            svcs.add(hints[i])
    if fb_type in ("MID_TERM", "YEAR_END"):
        svcs.add("ACADEMIC")
    if fb_type == "INTERNSHIP":
        svcs.add("CAREER")
    return sorted(svcs)

# ── Generators per type ──────────────────────────────────────────────────────

def gen_student_persona(idx, school):
    gender = random.choice(["m", "f"])
    name   = gen_name(gender)
    year   = random.randint(1, 4)
    prog   = random.choice(school["programs"])
    return {
        "id":      gen_id("SV2024", idx),
        "name":    name,
        "gender":  "Male" if gender == "m" else "Female",
        "role":    "student",
        "school":  school["name"],
        "school_id": school["id"],
        "year":    year,
        "program": prog,
    }, prog

def gen_parent_persona(idx, school):
    gender = random.choice(["m", "f"])
    name   = gen_name(gender)
    child_gender = random.choice(["m", "f"])
    child_name = gen_name(child_gender)
    prog = random.choice(school["programs"])
    return {
        "id":           gen_id("PAR", idx),
        "name":         name,
        "role":         "parent",
        "child_name":   child_name,
        "child_id":     gen_id("SV2023", idx),
        "child_school": school["name"],
        "child_school_id": school["id"],
        "child_year":   random.randint(1, 4),
        "child_program": prog,
    }, prog

def gen_employer_persona(idx, school):
    company    = random.choice(COMPANIES)
    ev_name    = gen_name(random.choice(["m","f"]))
    ev_role    = random.choice(COMPANY_ROLES)
    industry   = random.choice(INDUSTRIES)
    intern_gender = random.choice(["m","f"])
    intern_name   = gen_name(intern_gender)
    prog = random.choice(school["programs"])
    return {
        "id":             gen_id("EMP", idx),
        "company":        company,
        "industry":       industry,
        "evaluator_name": ev_name,
        "evaluator_role": ev_role,
        "role":           "employer",
        "intern_id":      gen_id("SV2023", idx + 1000),
        "intern_name":    intern_name,
        "intern_school":  school["name"],
        "intern_school_id": school["id"],
        "intern_program": prog,
    }, prog

def build_feedback(fb_type, idx, total=50):
    school     = random.choice(SCHOOLS)
    school_id  = school["id"]

    if fb_type == "PARENTS":
        persona, prog = gen_parent_persona(idx, school)
    elif fb_type == "INTERNSHIP":
        persona, prog = gen_employer_persona(idx, school)
    else:
        persona, prog = gen_student_persona(idx, school)

    q_sentiments = [weighted_sentiment() for _ in range(10)]
    overall = overall_sentiment_label(q_sentiments)
    related_svcs = derive_services(fb_type, overall, school_id, q_sentiments)

    Qs = {"MID_TERM": MID_TERM_Qs, "YEAR_END": YEAR_END_Qs,
          "PARENTS": PARENTS_Qs, "INTERNSHIP": INTERNSHIP_Qs}[fb_type]
    Afns = ANSWER_FUNCS[fb_type]

    body = []
    for i, (q, afn, sent) in enumerate(zip(Qs, Afns, q_sentiments)):
        svc_name = SERVICE_NAMES.get(SERVICE_HINTS[fb_type][i], "Student Support Services")
        answer = afn(sentiment=sent, s=school["name"], prog=prog, svc=svc_name)
        body.append({f"question_{i+1}": q, f"answer_{i+1}": answer})

    date_ranges = {
        "MID_TERM":   ((10, 11),),
        "YEAR_END":   ((4, 5),),
        "PARENTS":    ((11, 12),),
        "INTERNSHIP": ((3, 8),),
    }
    month_range = random.choice(date_ranges[fb_type])
    month = random.randint(*month_range)
    day   = random.randint(1, 28)
    fb_date = date(2025, month, day).isoformat()

    prefix = {"MID_TERM": "MID", "YEAR_END": "YE", "PARENTS": "PAR", "INTERNSHIP": "INT"}[fb_type]
    fb_id  = f"{prefix}-2025-{idx:03d}"

    return {
        "metadata": {
            "feedback_id": fb_id,
            "date": fb_date,
            "type": fb_type,
            "persona": persona,
            "related_schools":   [school_id],
            "related_services":  related_svcs,
            "overall_sentiment": overall,
        },
        "body": body,
    }

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    for fb_type in ["MID_TERM", "YEAR_END", "PARENTS", "INTERNSHIP"]:
        out_dir = BASE / fb_type
        out_dir.mkdir(parents=True, exist_ok=True)
        for i in range(1, 51):
            fb = build_feedback(fb_type, i)
            path = out_dir / f"{i:03d}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(fb, f, ensure_ascii=False, indent=2)
        print(f"  {fb_type}: 50 files written to {out_dir}")

if __name__ == "__main__":
    main()
