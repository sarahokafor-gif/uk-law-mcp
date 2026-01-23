"""
Codes of Practice Module

Direct links to key statutory codes of practice in UK law.
"""

import httpx
from typing import Optional
from urllib.parse import quote

GOV_UK_BASE = "https://www.gov.uk"

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# Mental Capacity Act Code of Practice
MCA_CODE = {
    "main": f"{GOV_UK_BASE}/government/publications/mental-capacity-act-code-of-practice",
    "chapters": {
        "1": "What is the Mental Capacity Act 2005?",
        "2": "What are the statutory principles and how should they be applied?",
        "3": "How should people be helped to make their own decisions?",
        "4": "How does the Act define 'lack of capacity'?",
        "5": "What does the Act mean when it talks about 'best interests'?",
        "6": "What protection does the Act offer for people providing care or treatment?",
        "7": "What does the Act say about Lasting Powers of Attorney?",
        "8": "What is the role of the Court of Protection and the court-appointed deputies?",
        "9": "What does the Act say about advance decisions to refuse treatment?",
        "10": "What is the new Independent Mental Capacity Advocate service?",
        "11": "How does the Act affect research projects involving a person who lacks capacity?",
        "12": "How does the Act apply to children and young people?",
        "13": "What is the relationship between the Mental Capacity Act and the Mental Health Act?",
        "14": "What happens if someone is abused or neglected?",
        "15": "What are the roles of various public bodies in protecting those who lack capacity?",
        "16": "What rules govern access to information about a person who lacks capacity?",
    },
}

# DoLS Code of Practice
DOLS_CODE = {
    "main": f"{GOV_UK_BASE}/government/publications/deprivation-of-liberty-safeguards-code-of-practice",
    "chapters": {
        "1": "What are the deprivation of liberty safeguards and why were they introduced?",
        "2": "What is deprivation of liberty?",
        "3": "How and when can deprivation of liberty be applied for and authorised?",
        "4": "What is the role of the relevant person's representative?",
        "5": "What should happen once authorization is given?",
        "6": "When can a person be moved to another place?",
        "7": "What is the Court of Protection's role?",
        "8": "What happens when a person becomes 18?",
        "9": "What are the responsibilities of NHS bodies?",
        "10": "What is the role of the Care Quality Commission?",
        "11": "How is the supervisory body's role carried out?",
    },
}

# Care Act Statutory Guidance
CARE_ACT_GUIDANCE = {
    "main": f"{GOV_UK_BASE}/government/publications/care-act-statutory-guidance",
    "chapters": {
        "1": "Promoting individual wellbeing",
        "2": "Preventing, reducing or delaying needs",
        "3": "Information and advice",
        "4": "Market shaping and commissioning",
        "5": "Managing provider failure and other service interruptions",
        "6": "Assessment and eligibility",
        "7": "Independent advocacy",
        "8": "Charging and financial assessment",
        "9": "Deferred payment agreements",
        "10": "Care and support planning",
        "11": "Personal budgets",
        "12": "Direct payments",
        "13": "Review of care and support plans",
        "14": "Safeguarding",
        "15": "Integration and partnership working",
        "16": "Delegation of local authority functions",
        "17": "Ordinary residence",
        "18": "Continuity of care",
        "19": "Transition to adult care and support",
        "20": "Continuity of care for people moving between areas",
        "21": "Cross-border placements",
        "22": "Prisons and approved premises",
        "23": "Annexes",
    },
}

# Mental Health Act Code of Practice
MHA_CODE = {
    "main": f"{GOV_UK_BASE}/government/publications/code-of-practice-mental-health-act-1983",
    "chapters": {
        "1": "The role of this Code and how to use it",
        "2": "The guiding principles",
        "3": "Human rights, equality and health inequalities",
        "4": "Information for patients, nearest relatives and others",
        "5": "The nearest relative",
        "6": "Mental disorder",
        "7": "Appropriate medical treatment",
        "8": "Applications for detention in hospital",
        "9": "Holding powers",
        "10": "Police powers",
        "11": "Conveyance of patients",
        "12": "Transfer of patients",
        "13": "Receipt and scrutiny of documents",
        "14": "Admission, guardianship and treatment under the Act",
        "15": "Duties of hospital managers",
        "16": "Communication, information and record keeping",
        "17": "Conflicts of interest",
        "18": "Doctors approved under section 12",
        "19": "Leave of absence",
        "20": "Absence without leave",
        "21": "Discharge",
        "22": "After-care",
        "23": "Medical treatment under the Act",
        "24": "Treatments requiring consent and a second opinion",
        "25": "Treatments requiring consent or a second opinion",
        "26": "The Mental Health Tribunal",
        "27": "CTO patients",
        "28": "Guardianship",
        "29": "Children and young people",
        "30": "The interface with other legislation",
        "31": "People with learning disabilities or autistic spectrum disorders",
        "32": "People with personality disorders",
        "33": "Patients concerned with criminal proceedings",
        "34": "Victims",
    },
}

# SEND Code of Practice
SEND_CODE = {
    "main": f"{GOV_UK_BASE}/government/publications/send-code-of-practice-0-to-25",
    "chapters": {
        "1": "Principles",
        "2": "Impartial information, advice and support",
        "3": "Working together across education, health and care",
        "4": "The Local Offer",
        "5": "Early years providers",
        "6": "Schools",
        "7": "Further education",
        "8": "Preparing for adulthood",
        "9": "Education, Health and Care needs assessments and plans",
        "10": "Children and young people in specific circumstances",
        "11": "Resolving disagreements",
    },
}


def get_mca_code(chapter: Optional[str] = None) -> str:
    """
    Get the Mental Capacity Act Code of Practice.

    Args:
        chapter: Optional chapter number (1-16)

    Returns:
        URL and chapter information
    """
    result = f"""Mental Capacity Act 2005 Code of Practice

Main document: {MCA_CODE['main']}

The MCA Code provides guidance on how to act in relation to people who lack
mental capacity to make decisions for themselves. Under s.42(5) MCA 2005,
certain people must have regard to the Code.

"""
    if chapter:
        ch = str(chapter).strip()
        if ch in MCA_CODE['chapters']:
            result += f"Chapter {ch}: {MCA_CODE['chapters'][ch]}\n\n"
            result += f"Access the Code and navigate to Chapter {ch}: {MCA_CODE['main']}"
        else:
            result += f"Chapter {ch} not found. Chapters run from 1 to 16.\n"
    else:
        result += "Chapters:\n"
        for ch_num, ch_title in MCA_CODE['chapters'].items():
            result += f"  {ch_num}. {ch_title}\n"

    result += """

Related legislation:
- Mental Capacity Act 2005: https://www.legislation.gov.uk/ukpga/2005/9/contents
- MCA regulations: https://www.legislation.gov.uk/uksi/2007/1899/contents"""

    return result


def get_dols_guidance() -> str:
    """
    Get Deprivation of Liberty Safeguards guidance.

    Returns:
        URLs and information about DoLS guidance
    """
    return f"""Deprivation of Liberty Safeguards (DoLS) Guidance

Code of Practice: {DOLS_CODE['main']}

The DoLS Code supplements the main MCA Code with guidance specific to
Schedule A1 MCA 2005 (Deprivation of Liberty Safeguards).

Chapters:
"""+ "\n".join([f"  {ch}. {title}" for ch, title in DOLS_CODE['chapters'].items()]) + f"""

IMPORTANT: DoLS applies to care homes and hospitals. For supported living
and domestic settings, deprivation of liberty must be authorised by the
Court of Protection (see Re X [2014] EWCOP 25).

Related resources:
- ADASS DoLS resources: https://www.adass.org.uk/dols
- DoLS forms: {GOV_UK_BASE}/government/collections/dols-forms
- MCA Code of Practice: {MCA_CODE['main']}
- Schedule A1 MCA 2005: https://www.legislation.gov.uk/ukpga/2005/9/schedule/A1

Liberty Protection Safeguards (LPS):
The Mental Capacity (Amendment) Act 2019 creates Liberty Protection Safeguards
to replace DoLS. Implementation has been delayed. Check for updates:
{GOV_UK_BASE}/government/publications/liberty-protection-safeguards-factsheets"""


def get_care_act_guidance(chapter: Optional[str] = None) -> str:
    """
    Get Care Act 2014 statutory guidance.

    Args:
        chapter: Optional chapter number (1-23)

    Returns:
        URL and chapter information
    """
    result = f"""Care Act 2014 Statutory Guidance

Main document: {CARE_ACT_GUIDANCE['main']}

Statutory guidance issued under s.78 Care Act 2014. Local authorities must
act under this guidance in exercising their social care functions.

"""
    if chapter:
        ch = str(chapter).strip()
        if ch in CARE_ACT_GUIDANCE['chapters']:
            result += f"Chapter {ch}: {CARE_ACT_GUIDANCE['chapters'][ch]}\n\n"
            result += f"Access the guidance and navigate to Chapter {ch}: {CARE_ACT_GUIDANCE['main']}"
        else:
            result += f"Chapter {ch} not found. Chapters run from 1 to 23.\n"
    else:
        result += "Chapters:\n"
        for ch_num, ch_title in list(CARE_ACT_GUIDANCE['chapters'].items())[:15]:
            result += f"  {ch_num}. {ch_title}\n"
        result += "  ...(and more)\n"

    result += f"""

Key chapters for legal work:
- Chapter 6: Assessment and eligibility
- Chapter 10: Care and support planning
- Chapter 14: Safeguarding
- Chapter 17: Ordinary residence
- Chapter 19: Transition to adult care

Legislation: https://www.legislation.gov.uk/ukpga/2014/23/contents"""

    return result


def get_mha_code(chapter: Optional[str] = None) -> str:
    """
    Get Mental Health Act 1983 Code of Practice.

    Args:
        chapter: Optional chapter number (1-34)

    Returns:
        URL and chapter information
    """
    result = f"""Mental Health Act 1983 Code of Practice

Main document: {MHA_CODE['main']}

Statutory guidance issued under s.118 MHA 1983. Practitioners must have
regard to the Code when exercising functions under the Act.

"""
    if chapter:
        ch = str(chapter).strip()
        if ch in MHA_CODE['chapters']:
            result += f"Chapter {ch}: {MHA_CODE['chapters'][ch]}\n\n"
            result += f"Access the Code and navigate to Chapter {ch}: {MHA_CODE['main']}"
        else:
            result += f"Chapter {ch} not found. Chapters run from 1 to 34.\n"
    else:
        result += "Selected chapters:\n"
        key_chapters = ["2", "6", "14", "22", "23", "28", "29", "30"]
        for ch_num in key_chapters:
            if ch_num in MHA_CODE['chapters']:
                result += f"  {ch_num}. {MHA_CODE['chapters'][ch_num]}\n"
        result += f"\n(Total 34 chapters - see full document for complete list)"

    result += f"""

Key chapters:
- Chapter 2: The guiding principles
- Chapter 14: Applications and detention
- Chapter 22: After-care (s.117)
- Chapter 23: Medical treatment
- Chapter 30: Interface with MCA and other legislation

Legislation: https://www.legislation.gov.uk/ukpga/1983/20/contents"""

    return result


def get_send_code(chapter: Optional[str] = None) -> str:
    """
    Get SEND Code of Practice.

    Args:
        chapter: Optional chapter number (1-11)

    Returns:
        URL and chapter information
    """
    result = f"""SEND Code of Practice: 0 to 25 years

Main document: {SEND_CODE['main']}

Statutory guidance for organisations which work with and support children
and young people with special educational needs or disabilities.

"""
    if chapter:
        ch = str(chapter).strip()
        if ch in SEND_CODE['chapters']:
            result += f"Chapter {ch}: {SEND_CODE['chapters'][ch]}\n\n"
            result += f"Access the Code and navigate to Chapter {ch}: {SEND_CODE['main']}"
        else:
            result += f"Chapter {ch} not found. Chapters run from 1 to 11.\n"
    else:
        result += "Chapters:\n"
        for ch_num, ch_title in SEND_CODE['chapters'].items():
            result += f"  {ch_num}. {ch_title}\n"

    result += f"""

Key chapters:
- Chapter 9: EHC needs assessments and plans
- Chapter 10: Specific circumstances (looked after children, custody, etc.)
- Chapter 11: Resolving disagreements (including Tribunal)

Legislation:
- Children and Families Act 2014: https://www.legislation.gov.uk/ukpga/2014/6/contents
- SEND Regulations 2014: https://www.legislation.gov.uk/uksi/2014/1530/contents

Tribunal:
- First-tier Tribunal (SEND): https://www.gov.uk/courts-tribunals/first-tier-tribunal-special-educational-needs-and-disability"""

    return result


def search_codes(query: str) -> str:
    """
    Search across all codes of practice.

    Args:
        query: Search terms (e.g., "best interests", "capacity assessment")

    Returns:
        Relevant code references and search suggestions
    """
    query_lower = query.lower()

    result = f"Searching codes of practice for: '{query}'\n\n"

    # Map common queries to relevant codes and chapters
    topic_mapping = {
        "capacity": [
            ("MCA Code", "Chapter 4: How does the Act define 'lack of capacity'?", MCA_CODE['main']),
            ("MCA Code", "Chapter 3: How should people be helped to make their own decisions?", MCA_CODE['main']),
        ],
        "best interests": [
            ("MCA Code", "Chapter 5: What does the Act mean when it talks about 'best interests'?", MCA_CODE['main']),
        ],
        "deprivation": [
            ("DoLS Code", "Chapter 2: What is deprivation of liberty?", DOLS_CODE['main']),
            ("DoLS Code", "Chapter 3: How and when can deprivation of liberty be authorised?", DOLS_CODE['main']),
        ],
        "safeguarding": [
            ("Care Act Guidance", "Chapter 14: Safeguarding", CARE_ACT_GUIDANCE['main']),
            ("MCA Code", "Chapter 14: What happens if someone is abused or neglected?", MCA_CODE['main']),
        ],
        "assessment": [
            ("Care Act Guidance", "Chapter 6: Assessment and eligibility", CARE_ACT_GUIDANCE['main']),
            ("MCA Code", "Chapter 4: How does the Act define 'lack of capacity'?", MCA_CODE['main']),
        ],
        "lpa": [
            ("MCA Code", "Chapter 7: What does the Act say about Lasting Powers of Attorney?", MCA_CODE['main']),
        ],
        "deputy": [
            ("MCA Code", "Chapter 8: What is the role of the Court of Protection and court-appointed deputies?", MCA_CODE['main']),
        ],
        "imca": [
            ("MCA Code", "Chapter 10: What is the new Independent Mental Capacity Advocate service?", MCA_CODE['main']),
        ],
        "detention": [
            ("MHA Code", "Chapter 14: Applications for detention in hospital", MHA_CODE['main']),
            ("DoLS Code", "Chapter 3: How and when can deprivation of liberty be authorised?", DOLS_CODE['main']),
        ],
        "s117": [
            ("MHA Code", "Chapter 22: After-care", MHA_CODE['main']),
        ],
        "after-care": [
            ("MHA Code", "Chapter 22: After-care", MHA_CODE['main']),
        ],
        "aftercare": [
            ("MHA Code", "Chapter 22: After-care", MHA_CODE['main']),
        ],
        "ehc": [
            ("SEND Code", "Chapter 9: Education, Health and Care needs assessments and plans", SEND_CODE['main']),
        ],
        "transition": [
            ("Care Act Guidance", "Chapter 19: Transition to adult care and support", CARE_ACT_GUIDANCE['main']),
            ("SEND Code", "Chapter 8: Preparing for adulthood", SEND_CODE['main']),
        ],
        "ordinary residence": [
            ("Care Act Guidance", "Chapter 17: Ordinary residence", CARE_ACT_GUIDANCE['main']),
        ],
    }

    found_topics = []
    for topic, refs in topic_mapping.items():
        if topic in query_lower:
            found_topics.extend(refs)

    if found_topics:
        result += "Relevant sections:\n\n"
        seen = set()
        for code, chapter, url in found_topics:
            key = f"{code}:{chapter}"
            if key not in seen:
                seen.add(key)
                result += f"- {code}: {chapter}\n  {url}\n\n"
    else:
        result += "No specific matches found. Try one of these topics:\n"
        result += "- capacity, best interests, safeguarding, assessment\n"
        result += "- deprivation, detention, lpa, deputy, imca\n"
        result += "- s117, after-care, ehc, transition, ordinary residence\n\n"

    result += f"""
All Codes of Practice:
- MCA Code: {MCA_CODE['main']}
- DoLS Code: {DOLS_CODE['main']}
- Care Act Guidance: {CARE_ACT_GUIDANCE['main']}
- MHA Code: {MHA_CODE['main']}
- SEND Code: {SEND_CODE['main']}"""

    return result


def list_all_codes() -> str:
    """
    List all available codes of practice.

    Returns:
        Index of all codes with links
    """
    return f"""Codes of Practice and Statutory Guidance

MENTAL CAPACITY ACT 2005
- MCA Code of Practice: {MCA_CODE['main']}
- DoLS Code of Practice: {DOLS_CODE['main']}

CARE ACT 2014
- Care Act Statutory Guidance: {CARE_ACT_GUIDANCE['main']}

MENTAL HEALTH ACT 1983
- MHA Code of Practice: {MHA_CODE['main']}

CHILDREN AND FAMILIES ACT 2014
- SEND Code of Practice: {SEND_CODE['main']}
- Working Together to Safeguard Children: {GOV_UK_BASE}/government/publications/working-together-to-safeguard-children--2

OTHER KEY GUIDANCE
- Charging for care guidance: {GOV_UK_BASE}/government/publications/charging-for-residential-accommodation-guide
- Ordinary residence disputes: {GOV_UK_BASE}/government/publications/care-act-statutory-guidance (Chapter 17)
- OPG practice guidance: {GOV_UK_BASE}/government/collections/opg-practice-guidance

Use:
- get_mca_code(chapter) for MCA Code
- get_dols_guidance() for DoLS guidance
- get_care_act_guidance(chapter) for Care Act guidance
- get_mha_code(chapter) for MHA Code
- get_send_code(chapter) for SEND Code
- search_codes(query) to search across all codes"""
