"""
Secretary of State Decisions Module

Connects to gov.uk for Secretary of State determinations across departments:
- Ordinary residence disputes (DHSC)
- Education disputes (DfE)
- Housing decisions (DLUHC)
- Immigration decisions (Home Office)
"""

import httpx
from typing import Optional
from urllib.parse import quote, urlencode

GOV_UK_BASE = "https://www.gov.uk"

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# Government departments
DEPARTMENTS = {
    "dhsc": {
        "name": "Department of Health and Social Care",
        "slug": "department-of-health-and-social-care",
        "decisions": [
            "ordinary-residence-disputes",
            "s117-disputes",
        ],
    },
    "dfe": {
        "name": "Department for Education",
        "slug": "department-for-education",
        "decisions": [
            "academy-complaints",
            "school-organisation",
        ],
    },
    "dluhc": {
        "name": "Department for Levelling Up, Housing and Communities",
        "slug": "department-for-levelling-up-housing-and-communities",
        "decisions": [
            "planning-called-in",
            "compulsory-purchase",
            "local-government",
        ],
    },
    "moj": {
        "name": "Ministry of Justice",
        "slug": "ministry-of-justice",
        "decisions": [
            "parole-decisions",
        ],
    },
    "ho": {
        "name": "Home Office",
        "slug": "home-office",
        "decisions": [
            "immigration-rules",
            "deportation",
        ],
    },
    "dwp": {
        "name": "Department for Work and Pensions",
        "slug": "department-for-work-pensions",
        "decisions": [
            "benefit-regulations",
        ],
    },
}


def search_sos_decisions(query: str, department: Optional[str] = None) -> str:
    """
    Search Secretary of State determinations.

    Args:
        query: Search terms (e.g., "ordinary residence", "s117")
        department: Optional department filter (dhsc, dfe, dluhc, moj, ho, dwp)

    Returns:
        Search URL and guidance
    """
    params = {
        "q": query,
        "filter_content_purpose_supergroup": "government",
    }

    if department:
        dept_lower = department.lower().strip()
        if dept_lower in DEPARTMENTS:
            params["filter_organisations[]"] = DEPARTMENTS[dept_lower]["slug"]

    search_url = f"{GOV_UK_BASE}/search/all?{urlencode(params, doseq=True)}"

    result = f"""Secretary of State Decisions Search

Search: {search_url}

Searching for: {query}"""

    if department and department.lower() in DEPARTMENTS:
        dept = DEPARTMENTS[department.lower()]
        result += f"\nDepartment: {dept['name']}"

    result += """

SoS decisions arise in various statutory contexts where disputes
or appeals are referred to central government for determination.

Key areas:

HEALTH AND SOCIAL CARE (DHSC)
- Ordinary residence disputes (s.40 Care Act 2014)
- s.117 MHA ordinary residence disputes
- NHS Continuing Healthcare disputes

EDUCATION (DfE)
- Academy complaints (where ESFA involved)
- School organisation decisions
- SEND Tribunal enforcement

HOUSING AND PLANNING (DLUHC)
- Called-in planning applications
- Recovered planning appeals
- Compulsory purchase orders
- Local government disputes

HOME OFFICE
- Immigration and nationality
- Deportation appeals (national security)

Note: Many SoS decisions are not routinely published.
For specific decision types, use the topic-specific functions."""

    return result


def get_sos_decision(reference: str) -> str:
    """
    Get a specific SoS decision by reference.

    Args:
        reference: Decision reference number or identifier

    Returns:
        Search guidance
    """
    search_url = f"{GOV_UK_BASE}/search/all?q={quote(reference)}"

    return f"""Secretary of State Decision Search

Reference: {reference}
Search: {search_url}

SoS decisions may be published:
1. On gov.uk publications pages
2. In departmental decision letters
3. Through Freedom of Information requests

If searching for ordinary residence decisions:
- DHSC publishes some determinations
- Search: "ordinary residence determination" on gov.uk

If searching for planning decisions:
- Search Planning Inspectorate: https://acp.planninginspectorate.gov.uk

If searching for education decisions:
- DfE decisions database: https://www.gov.uk/government/organisations/department-for-education

If the decision is not published:
- Consider FOI request to relevant department
- Check tribunal decisions if appeal pursued"""


def search_ministerial_decisions(query: str, department: Optional[str] = None) -> str:
    """
    Search ministerial decisions and directions.

    Args:
        query: Search terms
        department: Optional department filter

    Returns:
        Search URL and resources
    """
    params = {
        "q": query,
        "filter_content_purpose_supergroup": "government",
    }

    if department:
        dept_lower = department.lower().strip()
        if dept_lower in DEPARTMENTS:
            params["filter_organisations[]"] = DEPARTMENTS[dept_lower]["slug"]

    search_url = f"{GOV_UK_BASE}/search/all?{urlencode(params, doseq=True)}"

    result = f"""Ministerial Decisions Search

Search: {search_url}

Searching for: {query}

Ministerial decisions include:
- Written ministerial statements (Commons/Lords)
- Ministerial directions
- Regulatory decisions
- Statutory determinations

Written Ministerial Statements:
https://questions-statements.parliament.uk/written-statements

Parliamentary Questions:
https://questions-statements.parliament.uk/written-questions

Ministerial decisions affecting legal rights usually:
- Are published on gov.uk
- Appear in Hansard (if announced to Parliament)
- May be obtained via FOI

For judicial review of ministerial decisions:
- Time limit: promptly, at most 3 months
- Pre-action protocol applies
- Permission required"""

    return result


def list_departments() -> str:
    """
    List government departments with decision-making functions.

    Returns:
        Index of departments and their roles
    """
    result = "Government Departments - Decision Functions\n\n"

    for code, dept in DEPARTMENTS.items():
        result += f"{code.upper()}: {dept['name']}\n"
        result += f"  Gov.uk: {GOV_UK_BASE}/government/organisations/{dept['slug']}\n"
        result += f"  Publications: {GOV_UK_BASE}/government/publications?organisations[]={dept['slug']}\n\n"

    result += """
Other relevant bodies:

HMCTS (Courts and Tribunals):
https://www.gov.uk/government/organisations/hm-courts-and-tribunals-service

Planning Inspectorate:
https://www.gov.uk/government/organisations/planning-inspectorate

Office of the Public Guardian:
https://www.gov.uk/government/organisations/office-of-the-public-guardian

Legal Aid Agency:
https://www.gov.uk/government/organisations/legal-aid-agency

CQC (Care Quality Commission):
https://www.cqc.org.uk"""

    return result


# ============================================================
# Specific Decision Types
# ============================================================

def get_ordinary_residence_decisions() -> str:
    """
    Get information about ordinary residence dispute determinations.

    Returns:
        Links and guidance on OR decisions
    """
    return f"""Ordinary Residence Determinations

DHSC determines disputes about:
- Which local authority is responsible under Care Act 2014
- Which area is responsible for s.117 MHA aftercare

Legal framework:
- Care Act 2014, s.40 (Care Act disputes)
- Mental Health Act 1983, s.117 (aftercare disputes)
- Care Act Statutory Guidance, Chapter 17

Key principles (Shah v Barnet):
- Ordinary residence = voluntarily adopted abode
- Settled purpose for the time being
- Part of regular order of life

DHSC determinations:
{GOV_UK_BASE}/government/collections/ordinary-residence-guidance

Published determinations provide precedent for:
- Application of deeming provisions
- Treatment of hospital placements
- Effect of care home placements
- Cross-border issues

Related case law:
- R (Cornwall Council) v SoS for Health [2015] UKSC 46
- R (Worcestershire CC) v SoS for Health [2023] UKSC 31 (s.117)

Process:
1. Dispute arises between authorities
2. Both authorities provide evidence
3. SoS (DHSC) determines which authority is responsible
4. Decision is binding (subject to JR)

For live disputes:
Contact DHSC ordinary residence team"""


def get_s117_dispute_guidance() -> str:
    """
    Get guidance on s.117 MHA aftercare disputes.

    Returns:
        Guidance on s.117 responsibility disputes
    """
    return f"""Section 117 MHA Aftercare Disputes

DHSC determines disputes about s.117 responsibility.

Legal framework:
- Mental Health Act 1983, s.117(3)
- As amended by Care Act 2014

Key question: Where was the patient ordinarily resident
immediately before detention under a qualifying section?

Qualifying sections: 3, 37, 45A, 47, 48

Key case law:
- R (Worcestershire CC) v SoS for Health [2023] UKSC 31
  * Responsibility can transfer if OR changes after discharge
  * "Snapshot at discharge" principle
  * Hospital stay does not establish OR

- R (Sunderland CC) v South Tyneside Council [2012] EWCA Civ 1232

DHSC guidance:
{GOV_UK_BASE}/government/publications/mental-health-act-1983-code-of-practice
(Chapter 22: After-care)

Care Act guidance on OR:
{GOV_UK_BASE}/government/publications/care-act-statutory-guidance
(Chapter 17)

Dispute process:
1. Both CCGs/local authorities refer to DHSC
2. Evidence submitted by both parties
3. DHSC determination issued
4. Binding subject to judicial review

Note: DHSC determinations on s.117 are relatively rare;
many disputes settle through negotiation."""


def get_education_decisions() -> str:
    """
    Get information about DfE education decisions.

    Returns:
        Links to education decision resources
    """
    return f"""Department for Education Decisions

DfE makes decisions on:

School Organisation:
- Academy conversions
- Free school applications
- School closures and openings
- Significant changes to schools

School Complaints:
- Academy complaints (after ESFA review)
- Independent school regulation

SEND:
- Upper Tribunal appeals on points of law
- Compliance with tribunal orders

Published decisions:
{GOV_UK_BASE}/government/publications?organisations[]=department-for-education

Academy complaints:
{GOV_UK_BASE}/government/organisations/education-and-skills-funding-agency

Regional Schools Commissioners:
Now part of regional DfE teams

School organisation decisions include:
- Opening/closing schools
- Changes to age range
- Changes to capacity
- Academy orders

SEND Tribunal (First-tier):
Appeals about EHC plans go to FTT (SEND), not SoS.
{GOV_UK_BASE}/courts-tribunals/first-tier-tribunal-special-educational-needs-and-disability"""


def get_dluhc_decisions() -> str:
    """
    Get information about DLUHC decisions.

    Returns:
        Links to DLUHC decision resources
    """
    return f"""Department for Levelling Up, Housing and Communities Decisions

DLUHC (formerly MHCLG) makes decisions on:

Planning:
- Called-in applications (s.77 TCPA 1990)
- Recovered appeals
- National infrastructure projects
See: Planning Inspectorate tools

Compulsory Purchase:
- CPO confirmations
- Highways orders
{GOV_UK_BASE}/government/collections/compulsory-purchase-system-guidance

Local Government:
- Structural changes
- Electoral arrangements
- Financial matters

Housing:
- Social housing regulation
- Right to Buy matters

Published decisions:
{GOV_UK_BASE}/government/publications?organisations[]=department-for-levelling-up-housing-and-communities

For planning decisions specifically:
https://www.gov.uk/government/organisations/planning-inspectorate

Local Government Boundary Commission:
https://www.lgbce.org.uk"""


def sos_decisions_index() -> str:
    """
    Index of all SoS decision resources.

    Returns:
        Comprehensive index
    """
    return f"""Secretary of State Decisions - Index

SEARCH ALL DECISIONS
- search_sos_decisions(query, department) - General search
- search_ministerial_decisions(query) - Ministerial decisions
- get_sos_decision(reference) - Specific decision lookup

HEALTH AND SOCIAL CARE
- get_ordinary_residence_decisions() - OR disputes
- get_s117_dispute_guidance() - s.117 MHA disputes

EDUCATION
- get_education_decisions() - DfE decisions

HOUSING AND PLANNING
- get_dluhc_decisions() - DLUHC decisions
- (For planning appeals, use planning.py functions)

DEPARTMENT INFORMATION
- list_departments() - All departments

APPEALS FROM SOS DECISIONS
Most SoS decisions can be challenged by judicial review:
- Time limit: Promptly, at most 3 months
- Court: Administrative Court (EWHC Admin)
- Permission required
- Pre-action protocol applies

Published decisions: {GOV_UK_BASE}/government/publications

FOI requests for unpublished decisions:
https://www.gov.uk/make-a-freedom-of-information-request"""
