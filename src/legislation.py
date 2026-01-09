"""
Legislation Module

Connects to legislation.gov.uk - the official UK government legislation database.
"""

import httpx
from typing import Optional
import re

LEGISLATION_BASE = "https://www.legislation.gov.uk"

KNOWN_ACTS = {
    "mental capacity act": ("ukpga", 2005, 9),
    "mca": ("ukpga", 2005, 9),
    "mca 2005": ("ukpga", 2005, 9),
    "children act": ("ukpga", 1989, 41),
    "children act 1989": ("ukpga", 1989, 41),
    "children act 2004": ("ukpga", 2004, 31),
    "family law act": ("ukpga", 1996, 27),
    "family law act 1996": ("ukpga", 1996, 27),
    "adoption and children act": ("ukpga", 2002, 38),
    "matrimonial causes act": ("ukpga", 1973, 18),
    "human rights act": ("ukpga", 1998, 42),
    "hra": ("ukpga", 1998, 42),
    "equality act": ("ukpga", 2010, 15),
    "care act": ("ukpga", 2014, 23),
    "care act 2014": ("ukpga", 2014, 23),
    "police and criminal evidence act": ("ukpga", 1984, 60),
    "pace": ("ukpga", 1984, 60),
    "criminal justice act 2003": ("ukpga", 2003, 44),
    "sentencing act": ("ukpga", 2020, 17),
    "sentencing act 2020": ("ukpga", 2020, 17),
    "trusts of land act": ("ukpga", 1996, 47),
    "tolata": ("ukpga", 1996, 47),
    "land registration act": ("ukpga", 2002, 9),
    "employment rights act": ("ukpga", 1996, 18),
    "era": ("ukpga", 1996, 18),
    "immigration act 1971": ("ukpga", 1971, 77),
    "immigration act 2014": ("ukpga", 2014, 22),
    "senior courts act": ("ukpga", 1981, 54),
    "tribunals courts and enforcement act": ("ukpga", 2007, 15),
}


def normalise_act_name(name: str) -> str:
    return name.lower().strip()


def find_act_details(act_title: str, year: Optional[int] = None):
    normalised = normalise_act_name(act_title)
    
    if normalised in KNOWN_ACTS:
        return KNOWN_ACTS[normalised]
    
    if year:
        with_year = f"{normalised} {year}"
        if with_year in KNOWN_ACTS:
            return KNOWN_ACTS[with_year]
    
    for known_name, details in KNOWN_ACTS.items():
        if normalised in known_name or known_name in normalised:
            if year and details[1] != year:
                continue
            return details
    
    return None


def construct_legislation_url(leg_type: str, year: int, number: int, section: str) -> str:
    section_clean = re.sub(r'^section\s*', '', section.lower()).strip()
    return f"{LEGISLATION_BASE}/{leg_type}/{year}/{number}/section/{section_clean}"


def get_legislation_section(act_title: str, section: str, year: Optional[int] = None) -> str:
    act_details = find_act_details(act_title, year)
    
    if not act_details:
        return f"Could not find '{act_title}'. Try search_legislation('{act_title}') to find it."
    
    leg_type, act_year, chapter = act_details
    url = construct_legislation_url(leg_type, act_year, chapter, section)
    
    try:
        response = httpx.get(url, follow_redirects=True, timeout=30.0)
        
        if response.status_code == 404:
            return f"Section {section} not found. View full Act: {LEGISLATION_BASE}/{leg_type}/{act_year}/{chapter}/contents"
        
        if response.status_code != 200:
            return f"Error: HTTP {response.status_code}"
        
        return f"""Found: {act_title.title()} {act_year} - Section {section}

Source: {url}
PDF: {url}/data.pdf

Visit the link above for full text."""
        
    except httpx.TimeoutException:
        return "Request timed out. Try again."
    except Exception as e:
        return f"Error: {str(e)}"


def search_legislation_api(query: str, legislation_type: Optional[str] = None) -> str:
    search_url = f"{LEGISLATION_BASE}/search?text={query.replace(' ', '+')}"
    
    result = f"Search: {search_url}\n\nMatching known acts:\n"
    
    query_lower = query.lower()
    matches = []
    
    for name, (leg_type, year, chapter) in KNOWN_ACTS.items():
        if query_lower in name:
            matches.append((name.title(), year, f"{LEGISLATION_BASE}/{leg_type}/{year}/{chapter}"))
    
    if matches:
        for name, year, url in matches[:5]:
            result += f"- {name} ({year}): {url}\n"
    else:
        result += "None in quick lookup. Use the search link above."
    
    return result


def get_legislation_pdf(act_title: str, section: str, year: Optional[int] = None) -> str:
    act_details = find_act_details(act_title, year)
    
    if not act_details:
        return f"Could not find '{act_title}'."
    
    leg_type, act_year, chapter = act_details
    section_clean = re.sub(r'^section\s*', '', section.lower()).strip()
    
    return f"{LEGISLATION_BASE}/{leg_type}/{act_year}/{chapter}/section/{section_clean}/data.pdf"
