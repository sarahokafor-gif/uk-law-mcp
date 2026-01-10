"""
UK Law MCP Server

Gives Claude access to free official UK legal sources:
- legislation.gov.uk (statutes and regulations)
- caselaw.nationalarchives.gov.uk (court judgments 2003+)
- bailii.org (older cases, tribunals)
- judiciary.uk (practice directions, court rules)
- gov.uk (statutory guidance, codes of practice)
"""

from fastmcp import FastMCP
from typing import Optional

# Existing modules
from legislation import search_legislation_api, get_legislation_section, get_legislation_pdf
from caselaw import search_cases_api, get_judgment_api, get_judgment_pdf

# New modules
from bailii import search_bailii as bailii_search, get_bailii_case as bailii_case, get_recent_decisions as bailii_recent
from judiciary import search_practice_directions as pd_search, get_practice_direction as pd_get, get_court_guide as guide_get, get_recent_judgments
from guidance import search_guidance as gov_search, get_guidance as gov_get, get_forms as forms_get
from supremecourt import (
    search_supreme_court as uksc_search, 
    search_privy_council as jcpc_search,
    get_uksc_case as uksc_case,
    get_jcpc_case as jcpc_case,
    get_uksc_recent as uksc_recent,
    get_jcpc_recent as jcpc_recent
)

mcp = FastMCP("UK Law Research")


# ============================================================
# LEGISLATION (legislation.gov.uk)
# ============================================================

@mcp.tool
def get_legislation(
    act_title: str,
    section: str,
    year: Optional[int] = None
) -> str:
    """
    Fetch a specific section of UK legislation from legislation.gov.uk.
    
    Args:
        act_title: Name of the Act (e.g., "Mental Capacity Act")
        section: Section number (e.g., "3" or "21A")
        year: Year of the Act (e.g., 2005)
    
    Example:
        get_legislation("Mental Capacity Act", "3", 2005)
    """
    return get_legislation_section(act_title, section, year)


@mcp.tool
def search_legislation(
    query: str,
    legislation_type: Optional[str] = None
) -> str:
    """
    Search all UK legislation on legislation.gov.uk.
    
    Args:
        query: Search terms (e.g., "deprivation of liberty")
        legislation_type: Optional - "primary" for Acts, "secondary" for SIs
    
    Example:
        search_legislation("mental capacity")
    """
    return search_legislation_api(query, legislation_type)


@mcp.tool
def get_legislation_pdf_url(
    act_title: str,
    section: str,
    year: Optional[int] = None
) -> str:
    """
    Get PDF download URL for a legislation section.
    
    Args:
        act_title: Name of the Act
        section: Section number
        year: Year of the Act
    
    Example:
        get_legislation_pdf_url("Mental Capacity Act", "3", 2005)
    """
    return get_legislation_pdf(act_title, section, year)


# ============================================================
# CASE LAW - National Archives (2003+)
# ============================================================

@mcp.tool
def search_cases(
    query: str,
    court: Optional[str] = None,
    year: Optional[int] = None,
    party: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> str:
    """
    Search UK case law on caselaw.nationalarchives.gov.uk.

    Args:
        query: Search terms (e.g., "best interests")
        court: Court code (e.g., "ewcop", "uksc", "ewca/civ")
        year: Filter by year (e.g., 2024)
        party: Party name to search for
        from_date: Start date as "YYYY-MM-DD" (e.g., "2024-01-01")
        to_date: End date as "YYYY-MM-DD" (e.g., "2024-06-30")

    Courts: uksc, ewca/civ, ewca/crim, ewhc, ewcop, ewfc, ukut

    Examples:
        search_cases("deprivation of liberty", court="ewcop")
        search_cases("best interests", court="ewcop", from_date="2024-01-01", to_date="2024-12-31")
    """
    return search_cases_api(query, court, year, party, from_date, to_date)


@mcp.tool
def get_judgment(citation: str) -> str:
    """
    Fetch a specific judgment by neutral citation.
    
    Args:
        citation: Neutral citation (e.g., "[2024] EWCOP 15")
    
    Example:
        get_judgment("[2024] EWCOP 15")
    """
    return get_judgment_api(citation)


@mcp.tool
def get_judgment_pdf_url(citation: str) -> str:
    """
    Get PDF download URL for a judgment.
    
    Args:
        citation: Neutral citation (e.g., "[2024] EWCOP 15")
    
    Example:
        get_judgment_pdf_url("[2024] EWCOP 15")
    """
    return get_judgment_pdf(citation)


# ============================================================
# CASE LAW - BAILII (older cases, tribunals)
# ============================================================

@mcp.tool
def search_bailii(
    query: str,
    database: Optional[str] = None,
    title_only: bool = False
) -> str:
    """
    Search BAILII for UK case law (especially older cases and tribunals).
    
    Args:
        query: Search terms
        database: Optional database filter (e.g., "ewcop", "mental health tribunal", "ukhl")
        title_only: If True, search case titles only
    
    Databases: uksc, ukhl, ewca/civ, ewca/crim, ewcop, ewfc, eat, 
               mental health tribunal, upper tribunal aac
    
    Example:
        search_bailii("best interests", database="ewcop")
    """
    return bailii_search(query, database, title_only)


@mcp.tool
def get_bailii_case(citation: str) -> str:
    """
    Get BAILII URL for a case by neutral citation.
    
    Best for older cases (pre-2003) and tribunal decisions.
    
    Args:
        citation: Neutral citation (e.g., "[1999] UKHL 30", "[2020] UKUT 123 (AAC)")
    
    Example:
        get_bailii_case("[1999] UKHL 30")
    """
    return bailii_case(citation)


@mcp.tool
def get_bailii_recent(jurisdiction: str = "ew") -> str:
    """
    Get link to recent decisions on BAILII.
    
    Args:
        jurisdiction: "ew" (England & Wales), "scot" (Scotland), "nie" (Northern Ireland)
    
    Example:
        get_bailii_recent("ew")
    """
    return bailii_recent(jurisdiction)


# ============================================================
# PRACTICE DIRECTIONS & COURT RULES (judiciary.uk)
# ============================================================

@mcp.tool
def search_practice_directions(
    court: str,
    topic: Optional[str] = None
) -> str:
    """
    Search for Practice Directions for a court.
    
    Args:
        court: Court type - "cop", "fpr", "cpr", "coa"
        topic: Optional topic to filter by
    
    Courts:
        - cop / court of protection / copr
        - fpr / family (Family Procedure Rules)
        - cpr / civil (Civil Procedure Rules)
        - coa / court of appeal
    
    Example:
        search_practice_directions("cop")
    """
    return pd_search(court, topic)


@mcp.tool
def get_practice_direction(court: str, pd_number: str) -> str:
    """
    Get direct link to a specific Practice Direction PDF.
    
    Args:
        court: Court type (currently "cop" has direct PDF links)
        pd_number: Practice Direction number (e.g., "4b", "10aa")
    
    CoP Practice Directions: 1a, 2a, 2b, 4b, 9e, 9f, 10aa, 10b, 
                             14a, 14e, 15a, 17a, 19b, 20a, 20b
    
    Example:
        get_practice_direction("cop", "4b")
    """
    return pd_get(court, pd_number)


@mcp.tool
def get_court_guide(guide: str) -> str:
    """
    Get link to a court guide or key judicial resource.
    
    Args:
        guide: Guide name (e.g., "admin court", "cop rules", "experts")
    
    Available: admin court, cop rules, copr 2017, expert guidance
    
    Example:
        get_court_guide("cop rules")
    """
    return guide_get(guide)


# ============================================================
# STATUTORY GUIDANCE (gov.uk)
# ============================================================

@mcp.tool
def search_gov_guidance(topic: str) -> str:
    """
    Search gov.uk for statutory guidance on a topic.
    
    Args:
        topic: Topic to search (e.g., "mental capacity", "care act", "safeguarding")
    
    Example:
        search_gov_guidance("mental capacity")
    """
    return gov_search(topic)


@mcp.tool
def get_statutory_guidance(name: str) -> str:
    """
    Get direct link to a statutory guidance document.
    
    Args:
        name: Guidance name
    
    Available:
        - mca code / mental capacity code
        - care act guidance
        - dols code / deprivation of liberty code
        - mha code / mental health code
        - working together (children safeguarding)
        - opg guidance / deputy guidance / lpa guidance
    
    Example:
        get_statutory_guidance("mca code")
    """
    return gov_get(name)


@mcp.tool
def get_court_forms(form_type: str) -> str:
    """
    Get links to official court forms.
    
    Args:
        form_type: Type of form (e.g., "cop", "lpa", "dols", "family")
    
    Example:
        get_court_forms("cop")
    """
    return forms_get(form_type)


# ============================================================
# SUPREME COURT (supremecourt.uk)
# ============================================================

@mcp.tool
def search_supreme_court(
    query: Optional[str] = None,
    year: Optional[int] = None,
    status: str = "decided"
) -> str:
    """
    Search UK Supreme Court cases on supremecourt.uk.
    
    Args:
        query: Optional search terms
        year: Optional year filter (2009-present)
        status: "decided", "pending", or "all"
    
    Note: UKSC was established October 2009. For pre-2009, search House of Lords.
    
    Example:
        search_supreme_court("human rights", year=2024)
    """
    return uksc_search(query, year, status)


@mcp.tool
def get_supreme_court_case(citation: str) -> str:
    """
    Get UK Supreme Court case by citation.
    
    Args:
        citation: Neutral citation (e.g., "[2024] UKSC 1") or
                  case reference (e.g., "UKSC/2022/0038")
    
    Returns links to case page, press summary, and full judgment.
    
    Example:
        get_supreme_court_case("[2024] UKSC 1")
    """
    return uksc_case(citation)


@mcp.tool
def get_supreme_court_recent() -> str:
    """
    Get links to recent UK Supreme Court judgments.
    
    Returns links to latest judgments, press summaries, and
    forthcoming hearings on supremecourt.uk.
    
    Example:
        get_supreme_court_recent()
    """
    return uksc_recent()


# ============================================================
# PRIVY COUNCIL (jcpc.uk)
# ============================================================

@mcp.tool
def search_privy_council(
    query: Optional[str] = None,
    year: Optional[int] = None,
    jurisdiction: Optional[str] = None
) -> str:
    """
    Search Judicial Committee of the Privy Council cases.
    
    The JCPC is the final court of appeal for:
    - UK overseas territories
    - Crown dependencies (Jersey, Guernsey, Isle of Man)
    - Some Commonwealth countries
    
    Args:
        query: Optional search terms
        year: Optional year filter (2009+ on jcpc.uk)
        jurisdiction: Optional jurisdiction (e.g., "Jersey", "Trinidad")
    
    Example:
        search_privy_council("constitutional", jurisdiction="Jersey")
    """
    return jcpc_search(query, year, jurisdiction)


@mcp.tool
def get_privy_council_case(citation: str) -> str:
    """
    Get Privy Council case by citation.
    
    Args:
        citation: Neutral citation (e.g., "[2024] UKPC 1") or
                  case reference (e.g., "JCPC/2022/0038")
    
    Example:
        get_privy_council_case("[2024] UKPC 1")
    """
    return jcpc_case(citation)


@mcp.tool
def get_privy_council_recent() -> str:
    """
    Get links to recent Privy Council judgments.
    
    Example:
        get_privy_council_recent()
    """
    return jcpc_recent()


if __name__ == "__main__":
    mcp.run()
