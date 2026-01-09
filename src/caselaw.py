"""
Case Law Module

Connects to caselaw.nationalarchives.gov.uk - the official UK court judgments database.
"""

import httpx
from typing import Optional
import re
from urllib.parse import quote

CASELAW_BASE = "https://caselaw.nationalarchives.gov.uk"

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
    party: Optional[str] = None
) -> str:
    search_url = f"{CASELAW_BASE}/judgments/search?query={quote(query)}"
    
    if court:
        normalised = normalise_court(court)
        if normalised:
            search_url += f"&court={normalised}"
    
    if year:
        search_url += f"&from={year}-01-01&to={year}-12-31"
    
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
        response = httpx.get(url, follow_redirects=True, timeout=30.0)
        
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
