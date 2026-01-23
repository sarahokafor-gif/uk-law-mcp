"""
Practice Directions Module

Connects to judiciary.uk for Practice Directions.
Practice Directions supplement the procedural rules with detailed guidance.
"""

import httpx
from typing import Optional
from urllib.parse import quote

JUDICIARY_BASE = "https://www.judiciary.uk"
JUSTICE_BASE = "https://www.justice.gov.uk"

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# Court of Protection Practice Directions (hosted on judiciary.uk and justice.gov.uk)
COP_PRACTICE_DIRECTIONS = {
    "1a": {
        "title": "Participation of P",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd01a",
        "description": "How P should participate in proceedings",
    },
    "2a": {
        "title": "Court Documents",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd02a",
        "description": "Requirements for court documents",
    },
    "2b": {
        "title": "Service of Documents",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd02b",
        "description": "How to serve documents",
    },
    "4b": {
        "title": "Statements of Truth",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd04b",
        "description": "Requirements for statements of truth",
    },
    "9e": {
        "title": "Applications Relating to Statutory Wills etc",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd09e",
        "description": "Applications for statutory wills, gifts, settlements",
    },
    "9f": {
        "title": "Applications Relating to Serious Medical Treatment",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd09f",
        "description": "Serious medical treatment applications",
    },
    "10aa": {
        "title": "Deprivation of Liberty Applications",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd10aa",
        "description": "Applications to authorise deprivation of liberty (Re X and COPDOL applications)",
    },
    "10b": {
        "title": "Urgent and Interim Applications",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd10b",
        "description": "Urgent applications, without notice applications",
    },
    "14a": {
        "title": "Written Evidence",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd14a",
        "description": "Requirements for witness statements and affidavits",
    },
    "14e": {
        "title": "Section 49 Reports",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd14e",
        "description": "Reports from the Official Solicitor, Public Guardian, etc.",
    },
    "15a": {
        "title": "Expert Evidence",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd15a",
        "description": "Use of expert evidence, duties of experts",
    },
    "17a": {
        "title": "Litigation Friends",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd17a",
        "description": "Appointment and duties of litigation friends",
    },
    "19b": {
        "title": "Fixed Costs in the COP",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd19b",
        "description": "Fixed costs regime for certain applications",
    },
    "20a": {
        "title": "Appeals",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd20a",
        "description": "Appeals from the Court of Protection",
    },
    "20b": {
        "title": "Appeals - Destination of Appeals",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions/pd20b",
        "description": "Which court hears COP appeals",
    },
}

# CPR Practice Directions (key ones)
CPR_PRACTICE_DIRECTIONS = {
    "pre-action": {
        "title": "Pre-Action Conduct and Protocols",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/civil/rules/pd_pre-action_conduct",
        "description": "Steps before issuing proceedings",
    },
    "3e": {
        "title": "Costs Management",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/civil/rules/part03/pd_part03e",
        "description": "Costs budgets in multi-track cases",
    },
    "6a": {
        "title": "Service within the UK",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/civil/rules/part06/pd_part06a",
        "description": "Methods of service within jurisdiction",
    },
    "22": {
        "title": "Statements of Truth",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/civil/rules/part22/pd_part22",
        "description": "Requirements for statements of truth",
    },
    "25a": {
        "title": "Interim Injunctions",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/civil/rules/part25/pd_part25a",
        "description": "Applications for interim injunctions",
    },
    "35": {
        "title": "Experts and Assessors",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/civil/rules/part35/pd_part35",
        "description": "Use of expert evidence",
    },
    "52a": {
        "title": "Appeals - General Provisions",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/civil/rules/part52/pd_part52a",
        "description": "How to appeal",
    },
    "52c": {
        "title": "Appeals to Court of Appeal",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/civil/rules/part52/pd_part52c",
        "description": "Court of Appeal civil procedure",
    },
    "54a": {
        "title": "Judicial Review",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/civil/rules/part54/pd_part54a",
        "description": "Judicial review procedure",
    },
}

# FPR Practice Directions (key ones)
FPR_PRACTICE_DIRECTIONS = {
    "3a": {
        "title": "Pre-Application Protocol",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/family/practice_directions/pd_part_03a",
        "description": "Steps before starting family proceedings",
    },
    "12b": {
        "title": "Child Arrangements Programme",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/family/practice_directions/pd_part_12b",
        "description": "Private law children cases",
    },
    "12j": {
        "title": "Domestic Abuse in Children Proceedings",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/family/practice_directions/pd_part_12j",
        "description": "Handling allegations of domestic abuse",
    },
    "25a": {
        "title": "Experts in Family Proceedings",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/family/practice_directions/pd_part_25a",
        "description": "Expert evidence in family cases",
    },
    "27a": {
        "title": "Court Bundles",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/family/practice_directions/pd_part_27a",
        "description": "Requirements for bundles in family proceedings",
    },
    "36a": {
        "title": "Transparency",
        "url": f"{JUSTICE_BASE}/courts/procedure-rules/family/practice_directions/pd_part_36a",
        "description": "Reporting restrictions and transparency",
    },
}


def get_practice_direction(pd_number: str, court: Optional[str] = None) -> str:
    """
    Get a specific Practice Direction.

    Args:
        pd_number: Practice Direction number (e.g., "10aa", "35", "12j")
        court: Court type ("cop", "cpr", "fpr") - optional, will auto-detect

    Returns:
        URL and details for the Practice Direction
    """
    pd_lower = pd_number.lower().strip().replace(" ", "").replace("-", "")

    # Try to auto-detect court if not specified
    if not court:
        if pd_lower in COP_PRACTICE_DIRECTIONS:
            court = "cop"
        elif pd_lower in CPR_PRACTICE_DIRECTIONS:
            court = "cpr"
        elif pd_lower in FPR_PRACTICE_DIRECTIONS:
            court = "fpr"

    court_lower = (court or "").lower().strip()

    # Court of Protection
    if court_lower in ["cop", "copr", "court of protection"]:
        if pd_lower in COP_PRACTICE_DIRECTIONS:
            pd = COP_PRACTICE_DIRECTIONS[pd_lower]
            return f"""Practice Direction {pd_number.upper()} - {pd['title']}

URL: {pd['url']}

Description: {pd['description']}

All CoP Practice Directions: {JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions"""
        else:
            return f"""Practice Direction {pd_number} not found in CoP Practice Directions.

Available CoP Practice Directions:
{_list_cop_pds()}

All CoP Practice Directions: {JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions"""

    # Civil Procedure Rules
    if court_lower in ["cpr", "civil"]:
        if pd_lower in CPR_PRACTICE_DIRECTIONS:
            pd = CPR_PRACTICE_DIRECTIONS[pd_lower]
            return f"""CPR Practice Direction {pd_number.upper()} - {pd['title']}

URL: {pd['url']}

Description: {pd['description']}

All CPR Practice Directions: {JUSTICE_BASE}/courts/procedure-rules/civil/rules"""
        else:
            return f"""Practice Direction {pd_number} not in quick lookup.

CPR Practice Directions are at: {JUSTICE_BASE}/courts/procedure-rules/civil/rules
Navigate to the relevant Part and look for the associated Practice Direction."""

    # Family Procedure Rules
    if court_lower in ["fpr", "family"]:
        if pd_lower in FPR_PRACTICE_DIRECTIONS:
            pd = FPR_PRACTICE_DIRECTIONS[pd_lower]
            return f"""FPR Practice Direction {pd_number.upper()} - {pd['title']}

URL: {pd['url']}

Description: {pd['description']}

All FPR Practice Directions: {JUSTICE_BASE}/courts/procedure-rules/family/practice_directions"""
        else:
            return f"""Practice Direction {pd_number} not in quick lookup.

FPR Practice Directions are at: {JUSTICE_BASE}/courts/procedure-rules/family/practice_directions"""

    # Unknown court or PD
    return f"""Could not locate Practice Direction {pd_number}.

Specify court type:
- get_practice_direction("{pd_number}", court="cop") for Court of Protection
- get_practice_direction("{pd_number}", court="cpr") for Civil
- get_practice_direction("{pd_number}", court="fpr") for Family

Or use search_practice_directions(query) to search."""


def _list_cop_pds() -> str:
    """Helper to list CoP PDs."""
    lines = []
    for code, pd in COP_PRACTICE_DIRECTIONS.items():
        lines.append(f"- PD {code.upper()}: {pd['title']}")
    return "\n".join(lines)


def search_practice_directions(query: str) -> str:
    """
    Search Practice Directions across all courts.

    Args:
        query: Search terms (e.g., "experts", "bundles", "service")

    Returns:
        Matching Practice Directions and search links
    """
    query_lower = query.lower()
    results = []

    # Search CoP PDs
    for code, pd in COP_PRACTICE_DIRECTIONS.items():
        if query_lower in pd['title'].lower() or query_lower in pd['description'].lower():
            results.append(f"CoP PD {code.upper()}: {pd['title']} - {pd['url']}")

    # Search CPR PDs
    for code, pd in CPR_PRACTICE_DIRECTIONS.items():
        if query_lower in pd['title'].lower() or query_lower in pd['description'].lower():
            results.append(f"CPR PD {code.upper()}: {pd['title']} - {pd['url']}")

    # Search FPR PDs
    for code, pd in FPR_PRACTICE_DIRECTIONS.items():
        if query_lower in pd['title'].lower() or query_lower in pd['description'].lower():
            results.append(f"FPR PD {code.upper()}: {pd['title']} - {pd['url']}")

    result = f"Search results for '{query}':\n\n"

    if results:
        result += "\n".join(results)
    else:
        result += "No Practice Directions found in quick lookup matching that query.\n"

    result += f"""

Full Practice Direction indexes:
- Court of Protection: {JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions
- Civil: {JUSTICE_BASE}/courts/procedure-rules/civil/rules
- Family: {JUSTICE_BASE}/courts/procedure-rules/family/practice_directions

Judiciary guidance and resources: {JUDICIARY_BASE}/guidance-and-resources/"""

    return result


def list_practice_directions(court: str) -> str:
    """
    List all Practice Directions for a court.

    Args:
        court: Court type ("cop", "cpr", "fpr", "civil", "family")

    Returns:
        List of Practice Directions with links
    """
    court_lower = court.lower().strip()

    if court_lower in ["cop", "copr", "court of protection"]:
        result = "Court of Protection Practice Directions\n\n"
        for code, pd in COP_PRACTICE_DIRECTIONS.items():
            result += f"PD {code.upper()}: {pd['title']}\n  {pd['url']}\n\n"
        result += f"\nFull index: {JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions"
        return result

    if court_lower in ["cpr", "civil"]:
        result = "Civil Procedure Rules Practice Directions (selected)\n\n"
        for code, pd in CPR_PRACTICE_DIRECTIONS.items():
            result += f"PD {code.upper()}: {pd['title']}\n  {pd['url']}\n\n"
        result += f"\nFull index: {JUSTICE_BASE}/courts/procedure-rules/civil/rules"
        return result

    if court_lower in ["fpr", "family"]:
        result = "Family Procedure Rules Practice Directions (selected)\n\n"
        for code, pd in FPR_PRACTICE_DIRECTIONS.items():
            result += f"PD {code.upper()}: {pd['title']}\n  {pd['url']}\n\n"
        result += f"\nFull index: {JUSTICE_BASE}/courts/procedure-rules/family/practice_directions"
        return result

    return f"""Court '{court}' not recognised.

Available courts:
- cop / copr / court of protection
- cpr / civil
- fpr / family

Use list_practice_directions("cop") for Court of Protection Practice Directions."""


def get_judiciary_guidance(topic: str) -> str:
    """
    Get links to judiciary.uk guidance resources.

    Args:
        topic: Topic to search for (e.g., "experts", "vulnerable witnesses", "mckenzie friend")

    Returns:
        Links to relevant guidance
    """
    topic_lower = topic.lower().strip()

    # Known guidance documents
    guidance_docs = {
        "experts": {
            "title": "Guidance for Experts",
            "url": f"{JUDICIARY_BASE}/guidance-and-resources/expert-guidance/",
        },
        "mckenzie": {
            "title": "McKenzie Friends - Practice Guidance",
            "url": f"{JUDICIARY_BASE}/guidance-and-resources/",
        },
        "vulnerable": {
            "title": "Vulnerable Witnesses and Parties",
            "url": f"{JUDICIARY_BASE}/guidance-and-resources/",
        },
        "reporting": {
            "title": "Reporting Restrictions",
            "url": f"{JUDICIARY_BASE}/guidance-and-resources/",
        },
        "remotehearings": {
            "title": "Remote Hearings",
            "url": f"{JUDICIARY_BASE}/guidance-and-resources/",
        },
        "costs": {
            "title": "Costs Guidance",
            "url": f"{JUDICIARY_BASE}/guidance-and-resources/",
        },
    }

    # Check for matches
    for key, doc in guidance_docs.items():
        if key in topic_lower or topic_lower in key:
            return f"""{doc['title']}

URL: {doc['url']}

Judiciary Guidance and Resources: {JUDICIARY_BASE}/guidance-and-resources/

Note: Judiciary.uk contains judicial guidance, speeches, and resources.
For procedural rules, use the court rules tools."""

    # General response
    return f"""Judiciary.uk Guidance Search

Search term: {topic}

Main resources page: {JUDICIARY_BASE}/guidance-and-resources/

Key guidance areas:
- Expert evidence guidance
- McKenzie Friends guidance
- Remote hearings protocol
- Reporting restrictions guidance
- Vulnerable witnesses guidance

For Practice Directions, use:
- get_practice_direction(pd_number, court)
- search_practice_directions(query)"""


def get_court_of_protection_guidance() -> str:
    """
    Get all Court of Protection guidance resources.

    Returns:
        Links to CoP guidance, rules, and practice directions
    """
    return f"""Court of Protection Guidance and Resources

RULES AND PRACTICE DIRECTIONS
- Court of Protection Rules 2017: https://www.legislation.gov.uk/uksi/2017/1035/contents
- Practice Directions Index: {JUSTICE_BASE}/courts/procedure-rules/court-of-protection/practice-directions

KEY PRACTICE DIRECTIONS
{_list_cop_pds()}

FORMS
- Court of Protection Forms: https://www.gov.uk/government/collections/court-of-protection-forms

GUIDANCE
- Judiciary CoP guidance: {JUDICIARY_BASE}/courts-and-tribunals/tribunals/court-of-protection/
- Official Solicitor: https://www.gov.uk/government/organisations/official-solicitor-and-public-trustee

MENTAL CAPACITY ACT
- MCA Code of Practice: https://www.gov.uk/government/publications/mental-capacity-act-code-of-practice
- Legislation: https://www.legislation.gov.uk/ukpga/2005/9/contents

CASE LAW
- CoP judgments: https://caselaw.nationalarchives.gov.uk/courts/ewcop"""
