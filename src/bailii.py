"""
BAILII Module

Connects to bailii.org - British and Irish Legal Information Institute.
Best for older cases (pre-2003) and tribunal decisions.
"""

import httpx
from typing import Optional
from urllib.parse import quote, urlencode
import re

BAILII_BASE = "https://www.bailii.org"

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# BAILII database codes for England & Wales
BAILII_DATABASES = {
    # Supreme Court & House of Lords
    "uksc": "/uk/cases/UKSC/",
    "supreme court": "/uk/cases/UKSC/",
    "ukhl": "/uk/cases/UKHL/",
    "house of lords": "/uk/cases/UKHL/",

    # Privy Council
    "ukpc": "/uk/cases/UKPC/",
    "privy council": "/uk/cases/UKPC/",

    # Court of Appeal
    "ewca/civ": "/ew/cases/EWCA/Civ/",
    "ewca civ": "/ew/cases/EWCA/Civ/",
    "court of appeal civil": "/ew/cases/EWCA/Civ/",
    "ewca/crim": "/ew/cases/EWCA/Crim/",
    "ewca crim": "/ew/cases/EWCA/Crim/",
    "court of appeal criminal": "/ew/cases/EWCA/Crim/",

    # High Court divisions
    "ewhc/admin": "/ew/cases/EWHC/Admin/",
    "ewhc admin": "/ew/cases/EWHC/Admin/",
    "admin court": "/ew/cases/EWHC/Admin/",
    "administrative court": "/ew/cases/EWHC/Admin/",
    "ewhc/ch": "/ew/cases/EWHC/Ch/",
    "ewhc ch": "/ew/cases/EWHC/Ch/",
    "chancery": "/ew/cases/EWHC/Ch/",
    "ewhc/comm": "/ew/cases/EWHC/Comm/",
    "commercial court": "/ew/cases/EWHC/Comm/",
    "ewhc/fam": "/ew/cases/EWHC/Fam/",
    "ewhc fam": "/ew/cases/EWHC/Fam/",
    "family division": "/ew/cases/EWHC/Fam/",
    "ewhc/kb": "/ew/cases/EWHC/KB/",
    "ewhc/qb": "/ew/cases/EWHC/QB/",
    "kings bench": "/ew/cases/EWHC/KB/",
    "queens bench": "/ew/cases/EWHC/QB/",
    "ewhc/tcc": "/ew/cases/EWHC/TCC/",
    "technology and construction": "/ew/cases/EWHC/TCC/",

    # Court of Protection
    "ewcop": "/ew/cases/EWCOP/",
    "court of protection": "/ew/cases/EWCOP/",
    "cop": "/ew/cases/EWCOP/",

    # Family Court
    "ewfc": "/ew/cases/EWFC/",
    "family court": "/ew/cases/EWFC/",

    # Upper Tribunal
    "ukut": "/uk/cases/UKUT/",
    "upper tribunal": "/uk/cases/UKUT/",
    "ukut/aac": "/uk/cases/UKUT/AAC/",
    "upper tribunal aac": "/uk/cases/UKUT/AAC/",
    "administrative appeals chamber": "/uk/cases/UKUT/AAC/",
    "ukut/iac": "/uk/cases/UKUT/IAC/",
    "immigration tribunal": "/uk/cases/UKUT/IAC/",
    "ukut/lc": "/uk/cases/UKUT/LC/",
    "lands chamber": "/uk/cases/UKUT/LC/",
    "ukut/tcc": "/uk/cases/UKUT/TCC/",
    "tax chamber": "/uk/cases/UKUT/TCC/",

    # First-tier Tribunal
    "ukftt": "/uk/cases/UKFTT/",
    "first-tier tribunal": "/uk/cases/UKFTT/",
    "ukftt/tc": "/uk/cases/UKFTT/TC/",
    "tax tribunal": "/uk/cases/UKFTT/TC/",
    "ukftt/grc": "/uk/cases/UKFTT/GRC/",
    "general regulatory chamber": "/uk/cases/UKFTT/GRC/",

    # Employment tribunals
    "eat": "/uk/cases/UKEAT/",
    "employment appeal tribunal": "/uk/cases/UKEAT/",

    # Mental Health
    "mhlo": "/uk/cases/UKMHLO/",
    "mental health": "/uk/cases/UKMHLO/",
    "mental health tribunal": "/uk/cases/UKMHLO/",
}

# Tribunal-specific databases
TRIBUNAL_DATABASES = {
    "aac": "/uk/cases/UKUT/AAC/",
    "iac": "/uk/cases/UKUT/IAC/",
    "lc": "/uk/cases/UKUT/LC/",
    "tcc": "/uk/cases/UKUT/TCC/",
    "eat": "/uk/cases/UKEAT/",
    "tax": "/uk/cases/UKFTT/TC/",
    "grc": "/uk/cases/UKFTT/GRC/",
    "mhlo": "/uk/cases/UKMHLO/",
    "mental health": "/uk/cases/UKMHLO/",
    "information tribunal": "/uk/cases/UKFTT/GRC/",
}


def get_bailii_search_url(query: str, database: Optional[str] = None, title_only: bool = False) -> str:
    """Build BAILII search URL."""
    params = {
        "method": "boolean",
        "query": query,
    }

    if title_only:
        params["mask_path"] = ""  # Search titles only

    # Add database restriction if specified
    if database:
        db_lower = database.lower().strip()
        if db_lower in BAILII_DATABASES:
            params["mask_path"] = BAILII_DATABASES[db_lower]

    search_url = f"{BAILII_BASE}/cgi-bin/find.cgi?{urlencode(params)}"
    return search_url


def search_bailii(query: str, database: Optional[str] = None, title_only: bool = False) -> str:
    """
    Search BAILII for UK case law.

    Args:
        query: Search terms
        database: Optional database filter (e.g., "ewcop", "ukhl", "eat")
        title_only: If True, search case titles only

    Returns:
        Search URL and guidance
    """
    search_url = get_bailii_search_url(query, database, title_only)

    result = f"BAILII Search: {search_url}\n\n"

    if database:
        db_lower = database.lower().strip()
        if db_lower in BAILII_DATABASES:
            result += f"Searching: {db_lower.upper()} database\n"
        else:
            result += f"Note: '{database}' not recognised. Searching all databases.\n"
            result += "Available databases: uksc, ukhl, ewca/civ, ewca/crim, ewcop, ewfc, "
            result += "ukut/aac, ukut/iac, eat, mental health tribunal\n"

    result += "\nTip: Use get_bailii_case('[YEAR] COURT NUMBER') to fetch a specific case."

    return result


def search_tribunals(query: str, tribunal: Optional[str] = None, year: Optional[int] = None) -> str:
    """
    Search BAILII specifically for tribunal decisions.

    Args:
        query: Search terms
        tribunal: Tribunal type (e.g., "eat", "aac", "iac", "mental health")
        year: Optional year filter

    Returns:
        Search URL and guidance
    """
    # Map tribunal name to database
    db_path = None
    if tribunal:
        trib_lower = tribunal.lower().strip()
        if trib_lower in TRIBUNAL_DATABASES:
            db_path = TRIBUNAL_DATABASES[trib_lower]
        elif trib_lower in BAILII_DATABASES:
            db_path = BAILII_DATABASES[trib_lower]

    params = {
        "method": "boolean",
        "query": query,
    }

    if db_path:
        params["mask_path"] = db_path
    else:
        # Default to all UK tribunals
        params["mask_path"] = "/uk/cases/UK"

    search_url = f"{BAILII_BASE}/cgi-bin/find.cgi?{urlencode(params)}"

    result = f"BAILII Tribunal Search: {search_url}\n\n"

    if tribunal:
        result += f"Searching: {tribunal.upper()} decisions\n"
    else:
        result += "Searching: All UK tribunal decisions\n"

    result += "\nAvailable tribunals:\n"
    result += "- eat (Employment Appeal Tribunal)\n"
    result += "- aac (Administrative Appeals Chamber)\n"
    result += "- iac (Immigration and Asylum Chamber)\n"
    result += "- lc (Lands Chamber)\n"
    result += "- tax / tcc (Tax Chamber)\n"
    result += "- grc (General Regulatory Chamber)\n"
    result += "- mental health (Mental Health Tribunal)\n"

    if year:
        result += f"\nNote: Filter by year {year} on the results page.\n"

    return result


def parse_bailii_citation(citation: str) -> Optional[dict]:
    """
    Parse neutral citation to construct BAILII URL.

    Supports formats like:
    - [2024] EWCOP 15
    - [1999] UKHL 30
    - [2020] UKUT 123 (AAC)
    """
    # Pattern for standard citation: [YEAR] COURT NUMBER
    pattern = r'\[(\d{4})\]\s*([A-Za-z]+(?:/[A-Za-z]+)?)\s*(\d+)'
    match = re.search(pattern, citation)

    if not match:
        return None

    year = match.group(1)
    court = match.group(2).upper()
    number = match.group(3)

    # Check for chamber suffix like (AAC)
    chamber_pattern = r'\(([A-Za-z]+)\)'
    chamber_match = re.search(chamber_pattern, citation)
    chamber = chamber_match.group(1).upper() if chamber_match else None

    return {
        "year": year,
        "court": court,
        "number": number,
        "chamber": chamber
    }


def construct_bailii_url(year: str, court: str, number: str, chamber: Optional[str] = None) -> str:
    """Construct BAILII URL from citation components."""
    court_upper = court.upper()

    # Map court codes to BAILII paths
    court_paths = {
        "UKSC": "/uk/cases/UKSC",
        "UKHL": "/uk/cases/UKHL",
        "UKPC": "/uk/cases/UKPC",
        "EWCA": "/ew/cases/EWCA",
        "EWCA/CIV": "/ew/cases/EWCA/Civ",
        "EWCA/CRIM": "/ew/cases/EWCA/Crim",
        "EWHC": "/ew/cases/EWHC",
        "EWHC/ADMIN": "/ew/cases/EWHC/Admin",
        "EWHC/CH": "/ew/cases/EWHC/Ch",
        "EWHC/COMM": "/ew/cases/EWHC/Comm",
        "EWHC/FAM": "/ew/cases/EWHC/Fam",
        "EWHC/KB": "/ew/cases/EWHC/KB",
        "EWHC/QB": "/ew/cases/EWHC/QB",
        "EWHC/TCC": "/ew/cases/EWHC/TCC",
        "EWCOP": "/ew/cases/EWCOP",
        "EWFC": "/ew/cases/EWFC",
        "UKUT": "/uk/cases/UKUT",
        "UKFTT": "/uk/cases/UKFTT",
        "UKEAT": "/uk/cases/UKEAT",
        "EAT": "/uk/cases/UKEAT",
    }

    # Handle UKUT with chamber
    if court_upper == "UKUT" and chamber:
        chamber_paths = {
            "AAC": "/uk/cases/UKUT/AAC",
            "IAC": "/uk/cases/UKUT/IAC",
            "LC": "/uk/cases/UKUT/LC",
            "TCC": "/uk/cases/UKUT/TCC",
        }
        if chamber in chamber_paths:
            return f"{BAILII_BASE}{chamber_paths[chamber]}/{year}/{number}.html"

    # Handle UKFTT with chamber
    if court_upper == "UKFTT" and chamber:
        chamber_paths = {
            "TC": "/uk/cases/UKFTT/TC",
            "GRC": "/uk/cases/UKFTT/GRC",
        }
        if chamber in chamber_paths:
            return f"{BAILII_BASE}{chamber_paths[chamber]}/{year}/{number}.html"

    if court_upper in court_paths:
        return f"{BAILII_BASE}{court_paths[court_upper]}/{year}/{number}.html"

    # Try constructing URL anyway
    return f"{BAILII_BASE}/cgi-bin/find.cgi?method=boolean&query={quote(f'[{year}] {court} {number}')}"


def get_bailii_case(citation_or_url: str) -> str:
    """
    Get BAILII case by neutral citation or URL.

    Args:
        citation_or_url: Either a neutral citation (e.g., "[1999] UKHL 30")
                        or a BAILII URL

    Returns:
        Case URL and access information
    """
    # If it's already a BAILII URL, return it
    if citation_or_url.startswith("http") and "bailii.org" in citation_or_url:
        return f"BAILII Case: {citation_or_url}\n\nVisit the link above for the full judgment."

    # Parse the citation
    parsed = parse_bailii_citation(citation_or_url)

    if not parsed:
        # Try a search instead
        search_url = get_bailii_search_url(citation_or_url, title_only=True)
        return f"Could not parse citation: {citation_or_url}\n\nTry searching: {search_url}"

    url = construct_bailii_url(
        parsed["year"],
        parsed["court"],
        parsed["number"],
        parsed.get("chamber")
    )

    # Try to verify the URL exists
    try:
        response = httpx.head(url, headers=HEADERS, follow_redirects=True, timeout=10.0)
        if response.status_code == 200:
            return f"""BAILII Case: {citation_or_url}

URL: {url}

Visit the link above for the full judgment.

Note: BAILII is best for:
- House of Lords cases (pre-2009)
- Older Court of Appeal decisions
- Tribunal decisions not on National Archives"""
        else:
            # URL doesn't exist, provide search link
            search_url = get_bailii_search_url(citation_or_url, title_only=True)
            return f"""Case URL not found: {url}

The case may be under a different path. Try searching:
{search_url}

Alternatively, try caselaw.nationalarchives.gov.uk for recent cases (2003+)."""

    except httpx.TimeoutException:
        return f"""BAILII Case URL (unverified): {url}

Could not verify the URL (timeout). The link may still work.
If not, try searching on BAILII directly."""
    except Exception as e:
        return f"""BAILII Case URL (unverified): {url}

Could not verify: {str(e)}
The link may still work. Try it directly."""


def get_recent_decisions(jurisdiction: str = "ew") -> str:
    """
    Get link to recent decisions on BAILII.

    Args:
        jurisdiction: "ew" (England & Wales), "scot" (Scotland),
                     "nie" (Northern Ireland), "uk" (UK-wide)

    Returns:
        Links to recent decision pages
    """
    jur_lower = jurisdiction.lower().strip()

    jurisdiction_urls = {
        "ew": f"{BAILII_BASE}/recent/ew.html",
        "england": f"{BAILII_BASE}/recent/ew.html",
        "england and wales": f"{BAILII_BASE}/recent/ew.html",
        "scot": f"{BAILII_BASE}/recent/scot.html",
        "scotland": f"{BAILII_BASE}/recent/scot.html",
        "nie": f"{BAILII_BASE}/recent/nie.html",
        "ni": f"{BAILII_BASE}/recent/nie.html",
        "northern ireland": f"{BAILII_BASE}/recent/nie.html",
        "uk": f"{BAILII_BASE}/recent/uk.html",
    }

    if jur_lower in jurisdiction_urls:
        url = jurisdiction_urls[jur_lower]
        jur_name = {
            "ew": "England & Wales",
            "england": "England & Wales",
            "england and wales": "England & Wales",
            "scot": "Scotland",
            "scotland": "Scotland",
            "nie": "Northern Ireland",
            "ni": "Northern Ireland",
            "northern ireland": "Northern Ireland",
            "uk": "UK-wide",
        }[jur_lower]

        return f"""BAILII Recent Decisions - {jur_name}

URL: {url}

This page shows recently added decisions.

Other jurisdictions:
- England & Wales: {BAILII_BASE}/recent/ew.html
- Scotland: {BAILII_BASE}/recent/scot.html
- Northern Ireland: {BAILII_BASE}/recent/nie.html
- UK-wide: {BAILII_BASE}/recent/uk.html"""

    return f"""Jurisdiction not recognised: {jurisdiction}

Available jurisdictions:
- ew / england / england and wales
- scot / scotland
- nie / ni / northern ireland
- uk (UK-wide tribunals)

Recent decisions pages:
- England & Wales: {BAILII_BASE}/recent/ew.html
- Scotland: {BAILII_BASE}/recent/scot.html
- Northern Ireland: {BAILII_BASE}/recent/nie.html"""


def get_bailii_database_list() -> str:
    """Return a list of available BAILII databases."""
    return """BAILII Databases (England & Wales)

Supreme Court & Predecessors:
- uksc: UK Supreme Court (2009+)
- ukhl: House of Lords (pre-2009)
- ukpc: Privy Council

Court of Appeal:
- ewca/civ: Civil Division
- ewca/crim: Criminal Division

High Court:
- ewhc/admin: Administrative Court
- ewhc/ch: Chancery Division
- ewhc/comm: Commercial Court
- ewhc/fam: Family Division
- ewhc/kb: King's Bench Division
- ewhc/tcc: Technology & Construction Court

Specialist Courts:
- ewcop: Court of Protection
- ewfc: Family Court

Upper Tribunal:
- ukut/aac: Administrative Appeals Chamber
- ukut/iac: Immigration and Asylum Chamber
- ukut/lc: Lands Chamber
- ukut/tcc: Tax and Chancery Chamber

First-tier Tribunal:
- ukftt/tc: Tax Chamber
- ukftt/grc: General Regulatory Chamber

Employment:
- eat: Employment Appeal Tribunal

Mental Health:
- mhlo: Mental Health Law Online (Tribunal decisions)

Use these codes with search_bailii(query, database="code")"""
