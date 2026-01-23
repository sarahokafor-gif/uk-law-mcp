"""
Court Rules Module

Connects to justice.gov.uk for court procedural rules:
- Civil Procedure Rules (CPR)
- Family Procedure Rules (FPR)
- Court of Protection Rules (COPR)
- Tribunal Procedure Rules
"""

import httpx
from typing import Optional
from urllib.parse import quote

JUSTICE_BASE = "https://www.justice.gov.uk"

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# Base URLs for different rule sets
RULE_BASES = {
    "cpr": f"{JUSTICE_BASE}/courts/procedure-rules/civil",
    "fpr": f"{JUSTICE_BASE}/courts/procedure-rules/family",
    "copr": f"{JUSTICE_BASE}/courts/procedure-rules/court-of-protection",
    "crpr": f"{JUSTICE_BASE}/courts/procedure-rules/criminal",
}

# Tribunal procedure rules (different structure)
TRIBUNAL_RULES_BASE = "https://www.gov.uk/government/collections"
TRIBUNAL_RULES = {
    "grc": f"{TRIBUNAL_RULES_BASE}/tribunal-procedure-rules#general-regulatory-chamber",
    "iac": f"{TRIBUNAL_RULES_BASE}/tribunal-procedure-rules#immigration-and-asylum-chamber",
    "sec": f"{TRIBUNAL_RULES_BASE}/tribunal-procedure-rules#social-entitlement-chamber",
    "hesc": f"{TRIBUNAL_RULES_BASE}/tribunal-procedure-rules#health-education-and-social-care-chamber",
    "pc": f"{TRIBUNAL_RULES_BASE}/tribunal-procedure-rules#property-chamber",
    "tc": f"{TRIBUNAL_RULES_BASE}/tribunal-procedure-rules#tax-chamber",
    "wpc": f"{TRIBUNAL_RULES_BASE}/tribunal-procedure-rules#war-pensions-and-armed-forces-compensation-chamber",
    "ut-aac": f"{TRIBUNAL_RULES_BASE}/tribunal-procedure-rules#upper-tribunal-administrative-appeals-chamber",
    "ut-iac": f"{TRIBUNAL_RULES_BASE}/tribunal-procedure-rules#upper-tribunal-immigration-and-asylum-chamber",
    "ut-lc": f"{TRIBUNAL_RULES_BASE}/tribunal-procedure-rules#upper-tribunal-lands-chamber",
    "ut-tcc": f"{TRIBUNAL_RULES_BASE}/tribunal-procedure-rules#upper-tribunal-tax-and-chancery-chamber",
    "eat": f"{TRIBUNAL_RULES_BASE}/employment-appeal-tribunal-rules-and-legislation",
}


def get_cpr(part: str, rule: Optional[str] = None) -> str:
    """
    Get Civil Procedure Rules.

    Args:
        part: CPR Part number (e.g., "1", "3", "24", "54")
        rule: Optional specific rule within the part (e.g., "3.4", "24.2")

    Returns:
        URL to the CPR part and guidance

    Examples:
        get_cpr("3") - Part 3 (Case Management)
        get_cpr("24") - Part 24 (Summary Judgment)
        get_cpr("54") - Part 54 (Judicial Review)
    """
    part_clean = part.strip().lstrip("0")

    # Direct URL to CPR part
    url = f"{RULE_BASES['cpr']}/rules/part{part_clean.zfill(2)}"

    result = f"""Civil Procedure Rules - Part {part_clean}

Rules: {url}
Practice Direction: {url}#pd

CPR Contents: {RULE_BASES['cpr']}/rules

Key CPR Parts:
- Part 1: Overriding objective
- Part 3: Case management
- Part 6: Service
- Part 7: Starting proceedings
- Part 23: Applications
- Part 24: Summary judgment
- Part 25: Interim remedies
- Part 31: Disclosure
- Part 32: Evidence
- Part 35: Experts
- Part 36: Offers to settle
- Part 44: Costs
- Part 52: Appeals
- Part 54: Judicial review"""

    if rule:
        result += f"\n\nSpecific rule {rule}: Check the page above and search for 'Rule {rule}'"

    return result


def get_fpr(part: str, rule: Optional[str] = None) -> str:
    """
    Get Family Procedure Rules.

    Args:
        part: FPR Part number (e.g., "1", "12", "29")
        rule: Optional specific rule within the part

    Returns:
        URL to the FPR part and guidance

    Examples:
        get_fpr("12") - Part 12 (Children proceedings)
        get_fpr("29") - Part 29 (Appeals)
    """
    part_clean = part.strip().lstrip("0")

    url = f"{RULE_BASES['fpr']}/rules/part_number"  # FPR uses different URL structure

    # FPR actual structure
    fpr_contents = f"{RULE_BASES['fpr']}/rules"

    result = f"""Family Procedure Rules - Part {part_clean}

FPR Contents: {fpr_contents}

The FPR governs:
- Divorce and financial remedies (Parts 7-9)
- Children Act proceedings (Part 12)
- Adoption proceedings (Part 14)
- Enforcement (Part 33)
- Appeals (Part 30)

Key FPR Parts:
- Part 1: Overriding objective
- Part 4: General case management
- Part 7: Divorce, dissolution, etc.
- Part 9: Financial remedies
- Part 12: Children proceedings (private law)
- Part 14: Adoption
- Part 18: Applications
- Part 22: Evidence
- Part 25: Experts
- Part 27: Hearings and directions
- Part 28: Costs
- Part 30: Appeals"""

    if rule:
        result += f"\n\nFor rule {rule}, navigate to Part {part_clean} on the contents page."

    return result


def get_copr(part: str, rule: Optional[str] = None) -> str:
    """
    Get Court of Protection Rules 2017.

    Args:
        part: COPR Part number (e.g., "1", "10", "14")
        rule: Optional specific rule within the part

    Returns:
        URL to the COPR part and guidance

    Examples:
        get_copr("1") - Part 1 (Preliminary)
        get_copr("10") - Part 10 (Permission)
        get_copr("14") - Part 14 (Admissions, evidence, depositions)
    """
    part_clean = part.strip().lstrip("0")

    # COPR URL structure
    copr_rules = f"{RULE_BASES['copr']}/rules"
    legislation_url = "https://www.legislation.gov.uk/uksi/2017/1035/contents"

    result = f"""Court of Protection Rules 2017 - Part {part_clean}

Rules index: {copr_rules}
Legislation.gov.uk: {legislation_url}

Practice Directions:
- PD 1A: Participation of P
- PD 2A: Court documents
- PD 4B: Statements of truth
- PD 9E: Applications within proceedings
- PD 10AA: Deprivation of liberty applications
- PD 10B: Urgent and interim applications
- PD 14A: Written evidence
- PD 14E: Section 49 reports
- PD 17A: Litigation friend

Key COPR Parts:
- Part 1: Preliminary (rules 1.1-1.4)
- Part 3: Interpretation and general provisions
- Part 7: Notifying P
- Part 8: Permission
- Part 9: Starting proceedings (COP1)
- Part 10: Applications within proceedings
- Part 11: Human rights and deprivation of liberty
- Part 12: Dealing with applications
- Part 14: Admissions, evidence, depositions
- Part 17: Litigation friends
- Part 19: Costs
- Part 20: Appeals"""

    if rule:
        result += f"\n\nFor rule {rule}, check legislation.gov.uk: {legislation_url}/part/{part_clean}"

    return result


def get_tribunal_rules(tribunal: str, part: Optional[str] = None) -> str:
    """
    Get Tribunal Procedure Rules.

    Args:
        tribunal: Tribunal code (e.g., "grc", "iac", "sec", "hesc", "ut-aac")
        part: Optional part number

    Returns:
        URL to the tribunal rules

    Examples:
        get_tribunal_rules("grc") - General Regulatory Chamber
        get_tribunal_rules("iac") - Immigration and Asylum Chamber
        get_tribunal_rules("hesc") - Health, Education and Social Care Chamber
        get_tribunal_rules("ut-aac") - Upper Tribunal AAC
    """
    trib_lower = tribunal.lower().strip()

    # Map common names to codes
    tribunal_names = {
        "general regulatory": "grc",
        "general regulatory chamber": "grc",
        "immigration": "iac",
        "immigration and asylum": "iac",
        "immigration and asylum chamber": "iac",
        "social entitlement": "sec",
        "social entitlement chamber": "sec",
        "health education": "hesc",
        "health education and social care": "hesc",
        "mental health": "hesc",
        "property": "pc",
        "property chamber": "pc",
        "tax": "tc",
        "tax chamber": "tc",
        "war pensions": "wpc",
        "employment": "eat",
        "employment appeal": "eat",
        "upper tribunal aac": "ut-aac",
        "aac": "ut-aac",
        "administrative appeals": "ut-aac",
        "upper tribunal iac": "ut-iac",
        "upper tribunal lc": "ut-lc",
        "lands": "ut-lc",
        "upper tribunal tcc": "ut-tcc",
    }

    if trib_lower in tribunal_names:
        trib_lower = tribunal_names[trib_lower]

    if trib_lower in TRIBUNAL_RULES:
        url = TRIBUNAL_RULES[trib_lower]

        tribunal_full_names = {
            "grc": "General Regulatory Chamber",
            "iac": "Immigration and Asylum Chamber",
            "sec": "Social Entitlement Chamber",
            "hesc": "Health, Education and Social Care Chamber",
            "pc": "Property Chamber",
            "tc": "Tax Chamber",
            "wpc": "War Pensions and Armed Forces Compensation Chamber",
            "ut-aac": "Upper Tribunal - Administrative Appeals Chamber",
            "ut-iac": "Upper Tribunal - Immigration and Asylum Chamber",
            "ut-lc": "Upper Tribunal - Lands Chamber",
            "ut-tcc": "Upper Tribunal - Tax and Chancery Chamber",
            "eat": "Employment Appeal Tribunal",
        }

        result = f"""Tribunal Procedure Rules - {tribunal_full_names.get(trib_lower, tribunal)}

Rules: {url}

All Tribunal Procedure Rules: {TRIBUNAL_RULES_BASE}/tribunal-procedure-rules

Note: Tribunal rules are consolidated on legislation.gov.uk:
- First-tier Tribunal rules by chamber
- Upper Tribunal rules by chamber
- Employment Appeal Tribunal rules"""

        if part:
            result += f"\n\nFor Part {part}, navigate to the rules page and search within the document."

        return result

    # Unknown tribunal
    return f"""Tribunal '{tribunal}' not recognised.

Available tribunals:
- grc: General Regulatory Chamber
- iac: Immigration and Asylum Chamber
- sec: Social Entitlement Chamber
- hesc: Health, Education and Social Care Chamber (including Mental Health)
- pc: Property Chamber
- tc: Tax Chamber
- wpc: War Pensions Chamber
- ut-aac: Upper Tribunal Administrative Appeals Chamber
- ut-iac: Upper Tribunal Immigration and Asylum Chamber
- ut-lc: Upper Tribunal Lands Chamber
- ut-tcc: Upper Tribunal Tax and Chancery Chamber
- eat: Employment Appeal Tribunal

All rules: {TRIBUNAL_RULES_BASE}/tribunal-procedure-rules"""


def search_rules(query: str, ruleset: Optional[str] = None) -> str:
    """
    Search across court procedure rules.

    Args:
        query: Search terms (e.g., "service", "permission", "costs")
        ruleset: Optional ruleset to search ("cpr", "fpr", "copr", "tribunal")

    Returns:
        Search guidance and relevant links
    """
    query_encoded = quote(query)

    result = f"Searching for: '{query}' in court rules\n\n"

    if ruleset:
        rs_lower = ruleset.lower().strip()
        if rs_lower in ["cpr", "civil"]:
            result += f"""CPR Search:
- Justice.gov.uk: {RULE_BASES['cpr']} (use Ctrl+F on parts)
- Legislation.gov.uk: https://www.legislation.gov.uk/uksi/1998/3132/contents (search function)

Key CPR terms related to '{query}' - check:
- Part index for relevant part
- Practice Directions for guidance"""

        elif rs_lower in ["fpr", "family"]:
            result += f"""FPR Search:
- Justice.gov.uk: {RULE_BASES['fpr']}
- Legislation.gov.uk: https://www.legislation.gov.uk/uksi/2010/2955/contents

Navigate to the rules index and use browser search."""

        elif rs_lower in ["copr", "cop", "court of protection"]:
            result += f"""COPR Search:
- Justice.gov.uk: {RULE_BASES['copr']}
- Legislation.gov.uk: https://www.legislation.gov.uk/uksi/2017/1035/contents

Key COPR Practice Directions are indexed separately on the justice.gov.uk page."""

        elif rs_lower in ["tribunal", "tribunals"]:
            result += f"""Tribunal Rules Search:
- All rules: {TRIBUNAL_RULES_BASE}/tribunal-procedure-rules

Each chamber has its own rules - navigate to the specific chamber."""

        else:
            result += f"Ruleset '{ruleset}' not recognised. Searching all rule sets.\n\n"
            ruleset = None

    if not ruleset:
        result += f"""Search across all rule sets:

Civil Procedure Rules (CPR):
- {RULE_BASES['cpr']}
- https://www.legislation.gov.uk/uksi/1998/3132/contents

Family Procedure Rules (FPR):
- {RULE_BASES['fpr']}
- https://www.legislation.gov.uk/uksi/2010/2955/contents

Court of Protection Rules (COPR):
- {RULE_BASES['copr']}
- https://www.legislation.gov.uk/uksi/2017/1035/contents

Criminal Procedure Rules:
- {RULE_BASES['crpr']}

Tribunal Procedure Rules:
- {TRIBUNAL_RULES_BASE}/tribunal-procedure-rules

Tip: Use legislation.gov.uk's search function for precise rule location."""

    return result


def get_rules_index() -> str:
    """Return an index of all available court rules."""
    return f"""Court Procedure Rules Index

CIVIL PROCEDURE RULES (CPR)
- Index: {RULE_BASES['cpr']}/rules
- Legislation: https://www.legislation.gov.uk/uksi/1998/3132/contents
- Applies to: Civil proceedings in County Court, High Court, Court of Appeal

FAMILY PROCEDURE RULES (FPR)
- Index: {RULE_BASES['fpr']}/rules
- Legislation: https://www.legislation.gov.uk/uksi/2010/2955/contents
- Applies to: Family proceedings in Family Court, High Court Family Division

COURT OF PROTECTION RULES (COPR)
- Index: {RULE_BASES['copr']}/rules
- Legislation: https://www.legislation.gov.uk/uksi/2017/1035/contents
- Applies to: All Court of Protection proceedings

CRIMINAL PROCEDURE RULES (CrimPR)
- Index: {RULE_BASES['crpr']}/rules
- Applies to: Criminal proceedings in Magistrates' Court, Crown Court, Court of Appeal

TRIBUNAL PROCEDURE RULES
- Index: {TRIBUNAL_RULES_BASE}/tribunal-procedure-rules
- First-tier Tribunal (by chamber)
- Upper Tribunal (by chamber)
- Employment Appeal Tribunal

Use:
- get_cpr(part) for Civil Procedure Rules
- get_fpr(part) for Family Procedure Rules
- get_copr(part) for Court of Protection Rules
- get_tribunal_rules(tribunal) for Tribunal rules
- search_rules(query) to search across all rules"""
