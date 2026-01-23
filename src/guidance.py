"""
Guidance Module

Connects to gov.uk for statutory guidance and government publications.
"""

import httpx
from typing import Optional
from urllib.parse import quote, urlencode

GOV_UK_BASE = "https://www.gov.uk"

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# Government departments relevant to legal research
DEPARTMENTS = {
    "moj": "ministry-of-justice",
    "ministry of justice": "ministry-of-justice",
    "dhsc": "department-of-health-and-social-care",
    "health": "department-of-health-and-social-care",
    "dfe": "department-for-education",
    "education": "department-for-education",
    "ho": "home-office",
    "home office": "home-office",
    "dluhc": "department-for-levelling-up-housing-and-communities",
    "housing": "department-for-levelling-up-housing-and-communities",
    "dwp": "department-for-work-pensions",
    "work and pensions": "department-for-work-pensions",
    "hmcts": "hm-courts-and-tribunals-service",
    "courts": "hm-courts-and-tribunals-service",
    "opg": "office-of-the-public-guardian",
    "public guardian": "office-of-the-public-guardian",
    "cqc": "care-quality-commission",
    "laa": "legal-aid-agency",
    "legal aid": "legal-aid-agency",
}

# Key statutory guidance documents
STATUTORY_GUIDANCE = {
    # Mental Capacity
    "mca code": {
        "title": "Mental Capacity Act Code of Practice",
        "url": f"{GOV_UK_BASE}/government/publications/mental-capacity-act-code-of-practice",
        "department": "Ministry of Justice",
        "description": "Statutory guidance on the Mental Capacity Act 2005",
    },
    "mental capacity code": {
        "title": "Mental Capacity Act Code of Practice",
        "url": f"{GOV_UK_BASE}/government/publications/mental-capacity-act-code-of-practice",
        "department": "Ministry of Justice",
        "description": "Statutory guidance on the Mental Capacity Act 2005",
    },
    "mca": {
        "title": "Mental Capacity Act Code of Practice",
        "url": f"{GOV_UK_BASE}/government/publications/mental-capacity-act-code-of-practice",
        "department": "Ministry of Justice",
        "description": "Statutory guidance on the Mental Capacity Act 2005",
    },

    # DoLS
    "dols code": {
        "title": "Deprivation of Liberty Safeguards Code of Practice",
        "url": f"{GOV_UK_BASE}/government/publications/deprivation-of-liberty-safeguards-code-of-practice",
        "department": "Ministry of Justice",
        "description": "Guidance on Schedule A1 MCA 2005 (DoLS)",
    },
    "deprivation of liberty": {
        "title": "Deprivation of Liberty Safeguards Code of Practice",
        "url": f"{GOV_UK_BASE}/government/publications/deprivation-of-liberty-safeguards-code-of-practice",
        "department": "Ministry of Justice",
        "description": "Guidance on Schedule A1 MCA 2005 (DoLS)",
    },
    "dols": {
        "title": "Deprivation of Liberty Safeguards Code of Practice",
        "url": f"{GOV_UK_BASE}/government/publications/deprivation-of-liberty-safeguards-code-of-practice",
        "department": "Ministry of Justice",
        "description": "Guidance on Schedule A1 MCA 2005 (DoLS)",
    },

    # Care Act
    "care act guidance": {
        "title": "Care Act 2014 Statutory Guidance",
        "url": f"{GOV_UK_BASE}/government/publications/care-act-statutory-guidance",
        "department": "DHSC",
        "description": "Statutory guidance on adult social care duties",
    },
    "care act": {
        "title": "Care Act 2014 Statutory Guidance",
        "url": f"{GOV_UK_BASE}/government/publications/care-act-statutory-guidance",
        "department": "DHSC",
        "description": "Statutory guidance on adult social care duties",
    },
    "care and support": {
        "title": "Care Act 2014 Statutory Guidance",
        "url": f"{GOV_UK_BASE}/government/publications/care-act-statutory-guidance",
        "department": "DHSC",
        "description": "Statutory guidance on adult social care duties",
    },

    # Mental Health
    "mha code": {
        "title": "Mental Health Act 1983 Code of Practice",
        "url": f"{GOV_UK_BASE}/government/publications/code-of-practice-mental-health-act-1983",
        "department": "DHSC",
        "description": "Statutory guidance on the Mental Health Act",
    },
    "mental health code": {
        "title": "Mental Health Act 1983 Code of Practice",
        "url": f"{GOV_UK_BASE}/government/publications/code-of-practice-mental-health-act-1983",
        "department": "DHSC",
        "description": "Statutory guidance on the Mental Health Act",
    },

    # Children
    "working together": {
        "title": "Working Together to Safeguard Children",
        "url": f"{GOV_UK_BASE}/government/publications/working-together-to-safeguard-children--2",
        "department": "DfE",
        "description": "Statutory guidance on inter-agency working to safeguard children",
    },
    "safeguarding children": {
        "title": "Working Together to Safeguard Children",
        "url": f"{GOV_UK_BASE}/government/publications/working-together-to-safeguard-children--2",
        "department": "DfE",
        "description": "Statutory guidance on inter-agency working to safeguard children",
    },

    # SEND
    "send code": {
        "title": "SEND Code of Practice",
        "url": f"{GOV_UK_BASE}/government/publications/send-code-of-practice-0-to-25",
        "department": "DfE",
        "description": "Special educational needs and disability guidance",
    },
    "special educational needs": {
        "title": "SEND Code of Practice",
        "url": f"{GOV_UK_BASE}/government/publications/send-code-of-practice-0-to-25",
        "department": "DfE",
        "description": "Special educational needs and disability guidance",
    },

    # OPG guidance
    "opg guidance": {
        "title": "OPG Practice Guidance",
        "url": f"{GOV_UK_BASE}/government/collections/opg-practice-guidance",
        "department": "OPG",
        "description": "Practice guidance from Office of the Public Guardian",
    },
    "deputy guidance": {
        "title": "Guidance for Deputies",
        "url": f"{GOV_UK_BASE}/government/collections/deputies-guidance",
        "department": "OPG",
        "description": "Guidance for court-appointed deputies",
    },
    "lpa guidance": {
        "title": "LPA Guidance",
        "url": f"{GOV_UK_BASE}/power-of-attorney",
        "department": "OPG",
        "description": "Guidance on Lasting Powers of Attorney",
    },

    # Immigration
    "immigration rules": {
        "title": "Immigration Rules",
        "url": f"{GOV_UK_BASE}/guidance/immigration-rules",
        "department": "Home Office",
        "description": "The Immigration Rules",
    },

    # Legal Aid
    "legal aid guidance": {
        "title": "Legal Aid Guidance",
        "url": f"{GOV_UK_BASE}/government/collections/legal-aid-agency-guidance",
        "department": "LAA",
        "description": "Guidance for legal aid providers",
    },
}


def search_guidance(query: str, department: Optional[str] = None) -> str:
    """
    Search gov.uk for guidance documents.

    Args:
        query: Search terms (e.g., "mental capacity", "safeguarding adults")
        department: Optional department filter (e.g., "moj", "dhsc", "dfe")

    Returns:
        Search URL and any quick matches
    """
    # Build search URL
    params = {
        "q": query,
        "filter_content_purpose_supergroup": "guidance_and_regulation",
    }

    if department:
        dept_lower = department.lower().strip()
        if dept_lower in DEPARTMENTS:
            params["filter_organisations[]"] = DEPARTMENTS[dept_lower]

    search_url = f"{GOV_UK_BASE}/search/all?{urlencode(params, doseq=True)}"

    result = f"Gov.uk Guidance Search: {search_url}\n\n"

    # Check for quick matches in known guidance
    query_lower = query.lower()
    matches = []
    for key, guidance in STATUTORY_GUIDANCE.items():
        if query_lower in key or query_lower in guidance['title'].lower():
            matches.append(f"- {guidance['title']}: {guidance['url']}")

    if matches:
        result += "Quick matches in key statutory guidance:\n"
        result += "\n".join(matches[:5])
        result += "\n\n"

    if department:
        result += f"Filtered by: {department}\n"

    result += """
Available department filters:
- moj: Ministry of Justice
- dhsc: Health and Social Care
- dfe: Education
- ho: Home Office
- dluhc: Housing and Communities
- dwp: Work and Pensions
- opg: Office of the Public Guardian
- laa: Legal Aid Agency"""

    return result


def get_guidance(name: str) -> str:
    """
    Get a specific statutory guidance document.

    Args:
        name: Guidance name (e.g., "mca code", "care act guidance", "dols")

    Returns:
        URL and details for the guidance document
    """
    name_lower = name.lower().strip()

    # Check known guidance
    if name_lower in STATUTORY_GUIDANCE:
        guidance = STATUTORY_GUIDANCE[name_lower]
        return f"""{guidance['title']}

URL: {guidance['url']}

Department: {guidance['department']}
Description: {guidance['description']}

Note: This is statutory guidance that must be followed unless there
is a good reason to depart from it (s.42(5) MCA for MCA Code)."""

    # Try partial matches
    for key, guidance in STATUTORY_GUIDANCE.items():
        if name_lower in key:
            return f"""{guidance['title']}

URL: {guidance['url']}

Department: {guidance['department']}
Description: {guidance['description']}"""

    # Not found
    return f"""Guidance '{name}' not found in quick lookup.

Available guidance:
- mca code / mental capacity code: MCA Code of Practice
- dols code / deprivation of liberty: DoLS Code of Practice
- care act guidance: Care Act 2014 Statutory Guidance
- mha code / mental health code: MHA Code of Practice
- working together: Safeguarding Children Guidance
- send code: SEND Code of Practice
- opg guidance: OPG Practice Guidance
- deputy guidance: Guidance for Deputies
- lpa guidance: LPA Guidance
- immigration rules: Immigration Rules
- legal aid guidance: LAA Guidance

Or use search_guidance(query) to search gov.uk."""


def get_forms(form_type: str) -> str:
    """
    Get links to official court forms.

    Args:
        form_type: Type of forms (e.g., "cop", "lpa", "family", "civil")

    Returns:
        Links to form collections
    """
    form_type_lower = form_type.lower().strip()

    form_collections = {
        "cop": {
            "title": "Court of Protection Forms",
            "url": f"{GOV_UK_BASE}/government/collections/court-of-protection-forms",
            "key_forms": [
                "COP1: Application form",
                "COP3: Assessment of capacity",
                "COP9: Application relating to statutory wills etc",
                "COPDOL11: Deprivation of liberty application",
                "COP24: Witness statement",
            ],
        },
        "court of protection": {
            "title": "Court of Protection Forms",
            "url": f"{GOV_UK_BASE}/government/collections/court-of-protection-forms",
            "key_forms": [
                "COP1: Application form",
                "COP3: Assessment of capacity",
                "COP9: Application relating to statutory wills etc",
                "COPDOL11: Deprivation of liberty application",
                "COP24: Witness statement",
            ],
        },
        "lpa": {
            "title": "Lasting Power of Attorney Forms",
            "url": f"{GOV_UK_BASE}/government/collections/lasting-power-of-attorney-forms",
            "key_forms": [
                "LP1F: Property and financial affairs LPA",
                "LP1H: Health and welfare LPA",
                "LP2: Continuation sheets",
                "LP3: LPA register search",
                "LPC: Certificate provider form",
            ],
        },
        "lasting power of attorney": {
            "title": "Lasting Power of Attorney Forms",
            "url": f"{GOV_UK_BASE}/government/collections/lasting-power-of-attorney-forms",
            "key_forms": [
                "LP1F: Property and financial affairs LPA",
                "LP1H: Health and welfare LPA",
                "LP2: Continuation sheets",
                "LP3: LPA register search",
            ],
        },
        "family": {
            "title": "Family Court Forms",
            "url": f"{GOV_UK_BASE}/government/collections/court-and-tribunal-forms#family-court-forms",
            "key_forms": [
                "C1: Application for a section 8 order",
                "C100: Application under Children Act 1989",
                "C2: Application in existing proceedings",
                "D8: Divorce/dissolution petition",
                "FL401: Non-molestation/occupation order",
            ],
        },
        "civil": {
            "title": "Civil Court Forms",
            "url": f"{GOV_UK_BASE}/government/collections/court-and-tribunal-forms#civil-court-forms",
            "key_forms": [
                "N1: Claim form",
                "N244: Application notice",
                "N215: Certificate of service",
                "N161: Appeal notice",
                "N251: Notice of funding",
            ],
        },
        "dols": {
            "title": "DoLS Forms",
            "url": f"{GOV_UK_BASE}/government/collections/dols-forms",
            "key_forms": [
                "Form 1: Standard authorisation request",
                "Form 3: Urgent authorisation",
                "Form 4: Standard authorisation",
                "Form 10: RPR appointment",
            ],
        },
    }

    if form_type_lower in form_collections:
        fc = form_collections[form_type_lower]
        result = f"""{fc['title']}

URL: {fc['url']}

Key forms:
"""
        for form in fc['key_forms']:
            result += f"- {form}\n"

        result += f"""
All court and tribunal forms:
{GOV_UK_BASE}/government/collections/court-and-tribunal-forms"""
        return result

    # Not found
    return f"""Form type '{form_type}' not recognised.

Available form collections:
- cop: Court of Protection forms (COP1, COP3, COP9, COPDOL11, COP24, etc.)
- lpa: Lasting Power of Attorney forms (LP1F, LP1H, etc.)
- family: Family court forms (C1, C100, D8, FL401, etc.)
- civil: Civil court forms (N1, N244, etc.)
- dols: DoLS forms (Form 1, Form 3, Form 4, etc.)

All forms: {GOV_UK_BASE}/government/collections/court-and-tribunal-forms"""


def get_department_publications(department: str) -> str:
    """
    Get link to a department's publications page.

    Args:
        department: Department code or name (e.g., "moj", "dhsc", "opg")

    Returns:
        Link to department publications
    """
    dept_lower = department.lower().strip()

    if dept_lower in DEPARTMENTS:
        dept_slug = DEPARTMENTS[dept_lower]
        return f"""Publications from {department.upper()}

Publications: {GOV_UK_BASE}/government/publications?departments[]={dept_slug}
Guidance: {GOV_UK_BASE}/government/collections?departments[]={dept_slug}
Department page: {GOV_UK_BASE}/government/organisations/{dept_slug}"""

    # Try partial match
    for key, slug in DEPARTMENTS.items():
        if dept_lower in key:
            return f"""Publications from {key.title()}

Publications: {GOV_UK_BASE}/government/publications?departments[]={slug}
Guidance: {GOV_UK_BASE}/government/collections?departments[]={slug}
Department page: {GOV_UK_BASE}/government/organisations/{slug}"""

    return f"""Department '{department}' not recognised.

Available departments:
- moj: Ministry of Justice
- dhsc: Department of Health and Social Care
- dfe: Department for Education
- ho: Home Office
- dluhc: Levelling Up, Housing and Communities
- dwp: Work and Pensions
- hmcts: HM Courts and Tribunals Service
- opg: Office of the Public Guardian
- cqc: Care Quality Commission
- laa: Legal Aid Agency"""
