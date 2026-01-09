"""
UK Law MCP Server

Gives Claude access to free official UK legal sources:
- legislation.gov.uk (statutes and regulations)
- caselaw.nationalarchives.gov.uk (court judgments)
"""

from fastmcp import FastMCP
from typing import Optional

from legislation import search_legislation_api, get_legislation_section, get_legislation_pdf
from caselaw import search_cases_api, get_judgment_api, get_judgment_pdf

mcp = FastMCP("UK Law Research")


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
def search_cases(
    query: str,
    court: Optional[str] = None,
    year: Optional[int] = None,
    party: Optional[str] = None
) -> str:
    """
    Search UK case law on caselaw.nationalarchives.gov.uk.
    
    Args:
        query: Search terms (e.g., "best interests")
        court: Court code (e.g., "ewcop", "uksc", "ewca/civ")
        year: Filter by year
        party: Party name to search for
    
    Courts: uksc, ewca/civ, ewca/crim, ewhc, ewcop, ewfc, ukut
    
    Example:
        search_cases("deprivation of liberty", court="ewcop")
    """
    return search_cases_api(query, court, year, party)


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


if __name__ == "__main__":
    mcp.run()
