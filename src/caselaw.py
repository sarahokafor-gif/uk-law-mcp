"""
Case Law Module

Connects to caselaw.nationalarchives.gov.uk - the official UK court judgments database.
"""

import httpx
from typing import Optional, Tuple
import re
from urllib.parse import quote

CASELAW_BASE = "https://caselaw.nationalarchives.gov.uk"

# Headers to identify as a legitimate bot
HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool; +https://github.com/uk-law-mcp)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

COURT_CODES = {
    "uksc": "uksc",
    "supreme court": "uksc",
    "ewca": "ewca",
    "court of appeal": "ewca",
    "ewca/civ": "ewca/civ",
    "court of appeal civil": "ewca/civ",
    "ewca/crim": "ewca/crim",
    "court of appeal criminal": "ewca/crim",
    "ewhc": "ewhc",
    "high court": "ewhc",
    "ewhc/admin": "ewhc/admin",
    "admin court": "ewhc/admin",
    "administrative court": "ewhc/admin",
    "judicial review": "ewhc/admin",
    "ewhc/ch": "ewhc/ch",
    "chancery": "ewhc/ch",
    "ewhc/comm": "ewhc/comm",
    "commercial court": "ewhc/comm",
    "ewhc/fam": "ewhc/fam",
    "family division": "ewhc/fam",
    "high court family": "ewhc/fam",
    "ewhc/kb": "ewhc/kb",
    "kings bench": "ewhc/kb",
    "queens bench": "ewhc/kb",
    "qb": "ewhc/kb",
    "ewhc/tcc": "ewhc/tcc",
    "technology and construction": "ewhc/tcc",
    "ewcop": "ewcop",
    "court of protection": "ewcop",
    "cop": "ewcop",
    "ewfc": "ewfc",
    "family court": "ewfc",
    "ukut": "ukut",
    "upper tribunal": "ukut",
    "ukftt": "ukftt",
    "first-tier tribunal": "ukftt",
    "eat": "eat",
    "employment appeal tribunal": "eat",
}


def normalise_court(court: str) -> Optional[str]:
    if not court:
        return None
    court_lower = court.lower().strip()
    return COURT_CODES.get(court_lower)


def parse_date_to_params(date_str: str) -> Tuple[str, str, str]:
    """
    Parse a date string (YYYY-MM-DD) into split parameters for National Archives.

    Args:
        date_str: Date in format "2024-01-15" or "2024-1-5"

    Returns:
        Tuple of (day, month, year) as zero-padded strings
        e.g., ("15", "01", "2024")

    Raises:
        ValueError: If date format is invalid
    """
    # Try YYYY-MM-DD format
    match = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})$', date_str.strip())
    if match:
        year, month, day = match.groups()
        return (day.zfill(2), month.zfill(2), year)

    # Try DD/MM/YYYY format (UK style)
    match = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', date_str.strip())
    if match:
        day, month, year = match.groups()
        return (day.zfill(2), month.zfill(2), year)

    raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD or DD/MM/YYYY")


def build_date_params(from_date: Optional[str] = None, to_date: Optional[str] = None, year: Optional[int] = None) -> str:
    """
    Build date filter URL parameters for National Archives search.

    National Archives uses split date parameters:
    - from_date_0 = From Day (DD)
    - from_date_1 = From Month (MM)
    - from_date_2 = From Year (YYYY)
    - to_date_0 = To Day (DD)
    - to_date_1 = To Month (MM)
    - to_date_2 = To Year (YYYY)

    Args:
        from_date: Start date as "YYYY-MM-DD" or "DD/MM/YYYY"
        to_date: End date as "YYYY-MM-DD" or "DD/MM/YYYY"
        year: Year filter (used if from_date/to_date not provided)

    Returns:
        URL parameter string like "&from_date_0=01&from_date_1=01&from_date_2=2024..."
    """
    params = ""

    if from_date:
        day, month, yr = parse_date_to_params(from_date)
        params += f"&from_date_0={day}&from_date_1={month}&from_date_2={yr}"
    elif year:
        # Default to January 1st of the year
        params += f"&from_date_0=01&from_date_1=01&from_date_2={year}"

    if to_date:
        day, month, yr = parse_date_to_params(to_date)
        params += f"&to_date_0={day}&to_date_1={month}&to_date_2={yr}"
    elif year:
        # Default to December 31st of the year
        params += f"&to_date_0=31&to_date_1=12&to_date_2={year}"

    return params


def parse_citation(citation: str) -> Optional[dict]:
    """Parse neutral citation like [2024] EWCOP 15"""
    pattern = r'\[(\d{4})\]\s*([A-Za-z/]+)\s*(\d+)'
    match = re.search(pattern, citation)
    
    if not match:
        return None
    
    year = match.group(1)
    court = match.group(2).lower()
    number = match.group(3)
    
    return {
        "year": year,
        "court": court,
        "number": number
    }


def construct_judgment_url(year: str, court: str, number: str) -> str:
    return f"{CASELAW_BASE}/{court}/{year}/{number}"


def search_cases_api(
    query: str,
    court: Optional[str] = None,
    year: Optional[int] = None,
    party: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> str:
    """
    Search case law on National Archives.

    Args:
        query: Search terms
        court: Court code (e.g., "ewcop", "uksc")
        year: Filter by year (e.g., 2024)
        party: Party name to search for
        from_date: Start date as "YYYY-MM-DD" (e.g., "2024-01-01")
        to_date: End date as "YYYY-MM-DD" (e.g., "2024-12-31")

    Returns:
        Search URL and instructions
    """
    search_url = f"{CASELAW_BASE}/judgments/search?query={quote(query)}"

    if court:
        normalised = normalise_court(court)
        if normalised:
            search_url += f"&court={normalised}"

    # Add date parameters using the helper function
    # from_date/to_date take priority over year
    if from_date or to_date:
        search_url += build_date_params(from_date=from_date, to_date=to_date)
    elif year:
        search_url += build_date_params(year=year)

    if party:
        search_url += f"&party={quote(party)}"

    result = f"Search: {search_url}\n\n"
    result += "Click the link above to see matching judgments.\n\n"
    result += "Tip: Use get_judgment('[YEAR] COURT NUMBER') to fetch a specific case."

    return result


def get_judgment_api(citation: str) -> str:
    parsed = parse_citation(citation)
    
    if not parsed:
        return f"Could not parse citation: {citation}\n\nExpected format: [YEAR] COURT NUMBER\nExamples: [2024] EWCOP 15, [2023] UKSC 1"
    
    url = construct_judgment_url(parsed["year"], parsed["court"], parsed["number"])
    
    try:
        response = httpx.get(url, headers=HEADERS, follow_redirects=True, timeout=30.0)
        
        if response.status_code == 404:
            return f"Judgment not found: {citation}\n\nTry search_cases to find it."
        
        if response.status_code != 200:
            return f"Error: HTTP {response.status_code}"
        
        return f"""Found: {citation}

View: {url}
PDF: {url}/data.pdf
XML: {url}/data.xml

Visit the link above for full judgment."""
        
    except httpx.TimeoutException:
        return "Request timed out. Try again."
    except Exception as e:
        return f"Error: {str(e)}"


def get_judgment_pdf(citation: str) -> str:
    parsed = parse_citation(citation)
    
    if not parsed:
        return f"Could not parse citation: {citation}"
    
    url = construct_judgment_url(parsed["year"], parsed["court"], parsed["number"])
    return f"{url}/data.pdf"
