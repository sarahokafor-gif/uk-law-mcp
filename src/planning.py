"""
Planning Module

Connects to Planning Inspectorate and planning decision databases:
- Planning appeal decisions
- Called-in application decisions
- Secretary of State planning decisions
"""

import httpx
from typing import Optional
from urllib.parse import quote, urlencode

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# Base URLs
PINS_BASE = "https://www.gov.uk/government/organisations/planning-inspectorate"
APPEALS_SEARCH = "https://acp.planninginspectorate.gov.uk"
NATIONAL_INFRASTRUCTURE = "https://infrastructure.planninginspectorate.gov.uk"

# Planning appeal types
APPEAL_TYPES = {
    "householder": "Householder planning appeals (HAS procedure)",
    "full_planning": "Full planning appeals (written reps, hearing, inquiry)",
    "enforcement": "Enforcement notice appeals",
    "listed_building": "Listed building and conservation area appeals",
    "advertisement": "Advertisement consent appeals",
    "ldc": "Lawful development certificate appeals",
    "trees": "Tree preservation order appeals",
    "rights_of_way": "Public rights of way orders",
    "compulsory_purchase": "Compulsory purchase order inquiries",
}


def search_planning_appeals(
    query: str,
    location: Optional[str] = None,
    appeal_type: Optional[str] = None,
    decision: Optional[str] = None
) -> str:
    """
    Search Planning Inspectorate appeal decisions.

    Args:
        query: Search terms (e.g., "green belt", "residential", "change of use")
        location: Optional location filter (town, borough, county)
        appeal_type: Optional appeal type (householder, enforcement, etc.)
        decision: Optional outcome filter ("allowed", "dismissed", "split")

    Returns:
        Search URL and guidance
    """
    # Appeals Casework Portal
    search_url = f"{APPEALS_SEARCH}/pap/search"

    result = f"""Planning Inspectorate Appeal Decisions

Appeals Casework Portal: {search_url}

Searching for: {query}"""

    if location:
        result += f"\nLocation: {location}"
    if appeal_type:
        result += f"\nType: {appeal_type}"
    if decision:
        result += f"\nOutcome: {decision}"

    result += f"""

The Planning Inspectorate handles:
- Planning appeals (s.78 TCPA 1990)
- Enforcement appeals (s.174 TCPA 1990)
- Listed building consent appeals
- Advertisement consent appeals
- Lawful development certificate appeals
- Tree preservation order appeals

Appeal procedures:
- Written representations (most common)
- Hearing (for local/expert views)
- Inquiry (for complex/significant cases)

How to search:
1. Go to {search_url}
2. Enter search criteria (reference, location, keywords)
3. Filter by date range, appeal type, decision

Decision letters include:
- Inspector's assessment of main issues
- Application of planning policies
- Planning balance
- Formal decision

These decisions are persuasive (not binding) but demonstrate
how planning policies are applied in practice.

Appeal types:
"""
    for code, description in APPEAL_TYPES.items():
        result += f"- {code}: {description}\n"

    return result


def get_planning_decision(reference: str) -> str:
    """
    Get a specific planning appeal decision.

    Args:
        reference: Planning Inspectorate appeal reference (e.g., "APP/X1234/W/23/1234567")

    Returns:
        Link to search for the decision
    """
    # Reference format: APP/[LPA code]/[type]/[year]/[number]
    search_url = f"{APPEALS_SEARCH}/pap/search"

    return f"""Planning Appeal Decision

Reference: {reference}
Search Portal: {search_url}

Enter the appeal reference in the search box to find the decision.

Reference format explained:
- APP = Appeal
- X1234 = Local Planning Authority code
- W = Appeal type (W = s.78 planning, C = enforcement, etc.)
- 23 = Year (20XX)
- 1234567 = Case number

Decision types:
- Allowed: Appeal succeeds, permission granted
- Dismissed: Appeal fails, refusal upheld
- Part allowed/dismissed: Split decision
- Withdrawn: Appellant withdrew appeal
- Invalid: Appeal not accepted

The decision letter is the key document - it contains the
Inspector's full reasoning.

If you have a specific LPA reference rather than PINS reference,
search by the site address or LPA case number."""


def search_sos_planning_decisions(query: str) -> str:
    """
    Search Secretary of State planning decisions.

    Args:
        query: Search terms (e.g., development name, location)

    Returns:
        Search URL for SoS decisions

    Note: SoS decisions are for called-in applications and recovered appeals
    """
    search_url = f"{PINS_BASE}/collections/planning-recovered-appeals-and-called-in-planning-applications"

    result = f"""Secretary of State Planning Decisions

SoS decisions collection: {search_url}

Searching for: {query}

The Secretary of State decides:

Called-in applications (s.77 TCPA 1990):
- Applications of more than local importance
- Major controversial developments
- Those involving significant government policy issues

Recovered appeals:
- Appeals recovered from Inspectors for SoS decision
- Usually where significant policy issues arise

The process:
1. Inquiry held by Planning Inspector
2. Inspector provides report and recommendation
3. SoS makes final decision (may agree or disagree with Inspector)

SoS decision letters are published on gov.uk with:
- Inspector's report
- SoS's decision letter
- Any direction under Article 31

Recent SoS decisions:
{PINS_BASE}/collections/planning-recovered-appeals-and-called-in-planning-applications

These decisions carry significant weight as they represent
government interpretation of planning policy."""

    return result


def search_called_in_decisions(query: str) -> str:
    """
    Search called-in planning application decisions.

    Args:
        query: Search terms (development name, location, etc.)

    Returns:
        Links to called-in decision resources
    """
    return f"""Called-in Planning Applications

Called-in decisions: {PINS_BASE}/collections/planning-recovered-appeals-and-called-in-planning-applications

Searching for: {query}

Call-in criteria (updated 2024):
The SoS may call in applications which:
- May conflict with national planning policies
- May have significant effects beyond the LPA area
- Give rise to significant regional or national controversy
- May set precedent on significant matters
- Involve significant architectural or urban design issues

The call-in process:
1. LPA receives application
2. Direction issued to refer to SoS (instead of determining locally)
3. Written reps/hearing/inquiry held
4. Inspector reports to SoS
5. SoS decides (allows or refuses)

Called-in decisions are fully reasoned and represent government
policy application. They are persuasive in future appeals.

Statistics on call-ins:
https://www.gov.uk/government/statistics/planning-inspectorate-statistics

Related resources:
- Planning policy: https://www.gov.uk/government/collections/planning-practice-guidance
- NPPF: https://www.gov.uk/government/publications/national-planning-policy-framework--2"""


def get_national_infrastructure() -> str:
    """
    Get information about Nationally Significant Infrastructure Projects.

    Returns:
        Links to NSIP database and resources
    """
    return f"""Nationally Significant Infrastructure Projects (NSIPs)

NSIP Database: {NATIONAL_INFRASTRUCTURE}

NSIPs include:
- Power stations (over 50MW onshore, 100MW offshore)
- Electricity lines (132kV and above)
- Gas pipelines (over 48")
- Harbours (over £250m)
- Railways
- Highways
- Airports
- Water transfers and reservoirs
- Hazardous waste facilities

Process:
1. Pre-application consultation
2. Acceptance of application
3. Pre-examination
4. Examination (6 months)
5. Recommendation
6. Decision by SoS

All documents, representations, and examinations are published:
{NATIONAL_INFRASTRUCTURE}

Key documents:
- Application documents
- Examining Authority reports
- SoS decision letters
- Development Consent Orders (DCOs)

Planning Act 2008 governs NSIPs.

Search projects:
{NATIONAL_INFRASTRUCTURE}/projects"""


def get_planning_inspectorate_guidance() -> str:
    """
    Get Planning Inspectorate procedural guidance.

    Returns:
        Links to PINS guidance documents
    """
    return f"""Planning Inspectorate Guidance

Procedural guidance:
{PINS_BASE}/publications?keywords=procedural+guide

Key guidance documents:

Appeals:
- Procedural Guide: Planning Appeals - England
- Householder appeals guidance
- Enforcement appeals guidance

Hearings and Inquiries:
- Guide to hearings and inquiries
- Inquiry procedure rules

Costs:
- Award of costs guidance
- Unreasonable behaviour guidance

Statement of case:
- How to prepare your appeal
- What to include in statements

Timetables:
- Householder appeals: 8 weeks
- Written representations: 12-16 weeks
- Hearings: 16-20 weeks
- Inquiries: 24+ weeks (depending on complexity)

Statistics and performance:
{PINS_BASE}/statistics

National Planning Policy:
- NPPF: https://www.gov.uk/government/publications/national-planning-policy-framework--2
- Planning Practice Guidance: https://www.gov.uk/government/collections/planning-practice-guidance

Use Our Land registry: https://www.gov.uk/search-property-information-land-registry"""


def list_planning_resources() -> str:
    """
    List all available planning resources.

    Returns:
        Index of planning law resources
    """
    return f"""Planning Law Resources Index

PLANNING INSPECTORATE
Main site: {PINS_BASE}
Appeals search: {APPEALS_SEARCH}/pap/search
NSIPs: {NATIONAL_INFRASTRUCTURE}

APPEAL DECISIONS
- search_planning_appeals() - Search appeal decisions
- get_planning_decision() - Get specific appeal decision

SECRETARY OF STATE DECISIONS
- search_sos_planning_decisions() - Called-in and recovered appeals
- search_called_in_decisions() - Called-in applications

NATIONAL INFRASTRUCTURE
- get_national_infrastructure() - NSIP database

GUIDANCE
- get_planning_inspectorate_guidance() - Procedural guides

LEGISLATION
- Town and Country Planning Act 1990
  https://www.legislation.gov.uk/ukpga/1990/8/contents
- Planning Act 2008 (NSIPs)
  https://www.legislation.gov.uk/ukpga/2008/29/contents
- Planning and Compulsory Purchase Act 2004
  https://www.legislation.gov.uk/ukpga/2004/5/contents

POLICY
- National Planning Policy Framework (NPPF)
  https://www.gov.uk/government/publications/national-planning-policy-framework--2
- Planning Practice Guidance
  https://www.gov.uk/government/collections/planning-practice-guidance

LOCAL PLANS
- Search local authority websites for:
  - Local Plans / Development Plan Documents
  - Supplementary Planning Documents
  - Neighbourhood Plans

CASE LAW
For planning judicial reviews, search:
- EWHC (Admin): https://caselaw.nationalarchives.gov.uk/courts/ewhc/admin
- Court of Appeal: https://caselaw.nationalarchives.gov.uk/courts/ewca/civ

Common grounds for JR:
- Failure to take material consideration into account
- Taking irrelevant consideration into account
- Failure to give adequate reasons
- Irrationality (Wednesbury unreasonableness)"""
