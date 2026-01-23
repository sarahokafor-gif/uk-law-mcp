"""
International Law Module

Connects to international legal sources:
- EUR-Lex (EU law, retained EU law)
- HUDOC (European Court of Human Rights)
- UK Treaties
- UN Treaty Collection
"""

import httpx
from typing import Optional
from urllib.parse import quote, urlencode

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# Base URLs
EURLEX_BASE = "https://eur-lex.europa.eu"
HUDOC_BASE = "https://hudoc.echr.coe.int"
UK_TREATIES = "https://treaties.fcdo.gov.uk"
UN_TREATIES = "https://treaties.un.org"


# ============================================================
# EUR-Lex (EU Law / Retained EU Law)
# ============================================================

def search_eurlex(query: str, doc_type: Optional[str] = None) -> str:
    """
    Search EUR-Lex for EU law.

    Args:
        query: Search terms
        doc_type: Optional document type (regulation, directive, decision, etc.)

    Returns:
        Search URL and guidance

    Note: Relevant for retained EU law in UK post-Brexit
    """
    params = {
        "text": query,
        "scope": "EURLEX",
        "type": "quick"
    }

    search_url = f"{EURLEX_BASE}/search.html?{urlencode(params)}"

    result = f"""EUR-Lex Search

Search: {search_url}

Searching for: {query}

EUR-Lex contains:
- EU Treaties
- Regulations (directly applicable)
- Directives (require implementation)
- Decisions
- Case law (CJEU)
- Preparatory documents

POST-BREXIT RELEVANCE (UK)

Retained EU Law:
EU law in force on 31 December 2020 was retained in UK law.
See: European Union (Withdrawal) Act 2018

UK Retained EU Law:
{EURLEX_BASE}/summary/chapter/recast.html (understanding EU law types)
https://www.legislation.gov.uk/eu-origin (UK legislation.gov.uk)

Common EU law areas still relevant:
- Data protection (GDPR origins)
- Employment law
- Environmental law
- Consumer protection
- Competition law

To find retained EU law on legislation.gov.uk:
https://www.legislation.gov.uk/eu-origin

CELEX Numbers:
EU documents have CELEX identifiers:
- 3: Legislation (32018R0001 = Reg 2018/1)
- 6: Case law (62015CJ0001 = Case C-1/15)"""

    if doc_type:
        result += f"\n\nFiltered by: {doc_type}"

    return result


def get_eu_legislation(celex_or_number: str) -> str:
    """
    Get specific EU legislation.

    Args:
        celex_or_number: CELEX number or common citation (e.g., "Regulation 2016/679" for GDPR)

    Returns:
        Link to the legislation
    """
    # Common regulations
    common_refs = {
        "gdpr": "32016R0679",
        "2016/679": "32016R0679",
        "regulation 2016/679": "32016R0679",
        "data protection": "32016R0679",
        "brussels i": "32012R1215",
        "brussels recast": "32012R1215",
        "rome i": "32008R0593",
        "rome ii": "32007R0864",
        "insolvency": "32015R0848",
    }

    # Check for common references
    ref_lower = celex_or_number.lower().strip()
    celex = common_refs.get(ref_lower, celex_or_number)

    # If it looks like a CELEX number (starts with number)
    if celex[0].isdigit():
        url = f"{EURLEX_BASE}/legal-content/EN/TXT/?uri=CELEX:{celex}"
    else:
        # Search instead
        url = f"{EURLEX_BASE}/search.html?text={quote(celex_or_number)}"

    return f"""EUR-Lex Document

Reference: {celex_or_number}
URL: {url}

The page will show:
- Full text of the legislation
- Consolidated versions
- Related documents
- Implementation measures
- Case law citing this provision

For UK retained version:
Search: https://www.legislation.gov.uk/eu-origin

Understanding CELEX:
- 32016R0679 = Regulation (EU) 2016/679
  - 3 = Legislation
  - 2016 = Year
  - R = Regulation (L = Directive, D = Decision)
  - 0679 = Number"""


# ============================================================
# HUDOC (European Court of Human Rights)
# ============================================================

def search_hudoc(query: str, article: Optional[str] = None, respondent: Optional[str] = None) -> str:
    """
    Search HUDOC for ECHR case law.

    Args:
        query: Search terms or case name
        article: Optional ECHR article number (e.g., "5", "8", "3")
        respondent: Optional respondent state (e.g., "United Kingdom")

    Returns:
        Search URL and guidance
    """
    params = {"query": query}

    if article:
        params["article"] = article
    if respondent:
        params["respondent"] = respondent

    # HUDOC uses a specific URL structure
    search_url = f"{HUDOC_BASE}/eng?{urlencode(params)}"

    result = f"""HUDOC - European Court of Human Rights Case Law

Search: {search_url}

Searching for: {query}"""

    if article:
        result += f"\nArticle: {article}"
    if respondent:
        result += f"\nRespondent: {respondent}"

    result += f"""

HUDOC contains:
- Judgments of the Grand Chamber and Chambers
- Decisions on admissibility
- Advisory opinions
- Legal summaries
- Press releases

Convention Articles frequently cited:
- Article 2: Right to life
- Article 3: Prohibition of torture
- Article 5: Right to liberty and security
- Article 6: Right to fair trial
- Article 8: Right to respect for private and family life
- Article 10: Freedom of expression
- Article 14: Prohibition of discrimination
- Protocol 1, Article 1: Protection of property

UK and ECHR:
- Human Rights Act 1998 incorporates Convention rights
- UK courts must "take into account" ECHR case law (s.2 HRA)
- ECtHR judgments against UK are binding

Search tips:
- Use case name: "Smith v United Kingdom"
- Use application number: "12345/67"
- Combine article and keyword: article=8, query="mental capacity"

Advanced search:
{HUDOC_BASE}/#{{"sort":["kpdate Descending"]}}"""

    return result


def get_echr_case(application_number: str) -> str:
    """
    Get ECHR case by application number.

    Args:
        application_number: Application number (e.g., "12345/67")

    Returns:
        Link to the case
    """
    # Clean application number
    app_num = application_number.strip().replace(" ", "")

    search_url = f"{HUDOC_BASE}/eng?appno={quote(app_num)}"

    return f"""ECHR Case Search

Application number: {application_number}
Search: {search_url}

HUDOC will return all documents for this application:
- Judgment (if determined)
- Decision on admissibility
- Communication to respondent government
- Press release

Understanding ECHR procedure:
1. Application lodged
2. Communication to respondent (if not struck out)
3. Admissibility decision (or judgment on merits)
4. Judgment on merits (if admissible)
5. Just satisfaction (Article 41)
6. Execution supervised by Committee of Ministers

Citation format:
[Name] v [State] (Application no. [number])

Example: Smith v United Kingdom (Application no. 12345/67)

For execution of judgments:
https://www.coe.int/en/web/execution"""


def get_echr_article_caselaw(article: str) -> str:
    """
    Get key ECHR cases for a specific article.

    Args:
        article: Article number (e.g., "5", "8", "3")

    Returns:
        Link to cases and key case information
    """
    search_url = f"{HUDOC_BASE}/eng?article={article}"

    # Key cases by article
    key_cases = {
        "2": ["McCann v UK (1995)", "Osman v UK (1998)"],
        "3": ["Ireland v UK (1978)", "Soering v UK (1989)", "MSS v Belgium and Greece (2011)"],
        "5": ["Winterwerp v Netherlands (1979)", "HL v UK (2004) - Bournewood", "Storck v Germany (2005)"],
        "6": ["Golder v UK (1975)", "Salabiaku v France (1988)"],
        "8": ["Goodwin v UK (2002)", "Von Hannover v Germany (2004)", "S and Marper v UK (2008)"],
        "10": ["Handyside v UK (1976)", "Sunday Times v UK (1979)"],
        "14": ["Belgian Linguistics (1968)", "Thlimmenos v Greece (2000)"],
    }

    result = f"""ECHR Article {article} Case Law

Search all Article {article} cases:
{search_url}

"""
    art = str(article).strip()
    if art in key_cases:
        result += f"Key Article {art} cases:\n"
        for case in key_cases[art]:
            result += f"- {case}\n"

    result += f"""
Guide to Article {article}:
{HUDOC_BASE}/eng (select Article {article} from facets)

Case Law Guides (ECHR publications):
https://www.echr.coe.int/case-law-guides

Factsheets by topic:
https://www.echr.coe.int/factsheets"""

    return result


# ============================================================
# UK Treaties
# ============================================================

def search_uk_treaties(query: str) -> str:
    """
    Search UK treaties database.

    Args:
        query: Search terms or treaty name

    Returns:
        Search URL and guidance
    """
    search_url = f"{UK_TREATIES}/?query={quote(query)}"

    return f"""UK Treaties Search

Search: {search_url}

Searching for: {query}

The UK Treaties Online database contains:
- Bilateral treaties
- Multilateral treaties
- Treaty status
- Reservations and declarations

Treaty types:
- Bilateral (between UK and one other state)
- Multilateral (multiple states)

Status:
- In force
- Not yet in force
- Terminated

Key UK treaties:
- Trade agreements
- Extradition treaties
- Investment protection
- Tax treaties
- Human rights conventions

Post-Brexit treaties:
{UK_TREATIES} (filter by date for post-2020)

For EU-UK agreements:
- Trade and Cooperation Agreement (TCA)
- Withdrawal Agreement

UN Treaty Collection (global treaties):
{UN_TREATIES}"""


def get_uk_treaty(treaty_name: str) -> str:
    """
    Get specific UK treaty.

    Args:
        treaty_name: Treaty name or description

    Returns:
        Search link
    """
    search_url = f"{UK_TREATIES}/?query={quote(treaty_name)}"

    return f"""UK Treaty Search

Searching for: {treaty_name}
Search: {search_url}

The treaty page will show:
- Full title
- Parties
- Date signed
- Date in force
- UK ratification date
- Text of treaty (if available)
- Any reservations

For treaties requiring legislation:
Check legislation.gov.uk for implementing Act

For tax treaties:
https://www.gov.uk/government/collections/tax-treaties

For extradition treaties:
https://www.gov.uk/government/collections/extradition-treaties

Vienna Convention on the Law of Treaties 1969:
Governs treaty interpretation and application."""


# ============================================================
# Index
# ============================================================

def international_law_index() -> str:
    """
    Index of international law resources.

    Returns:
        Comprehensive index of international sources
    """
    return f"""International Law Resources Index

EU LAW (EUR-Lex)
{EURLEX_BASE}
- EU legislation (regulations, directives)
- EU case law (CJEU)
- Retained EU law guidance
Use: search_eurlex(), get_eu_legislation()

ECHR (HUDOC)
{HUDOC_BASE}
- European Court of Human Rights case law
- Convention articles interpretation
Use: search_hudoc(), get_echr_case(), get_echr_article_caselaw()

UK TREATIES
{UK_TREATIES}
- Bilateral and multilateral treaties
- Treaty status and text
Use: search_uk_treaties(), get_uk_treaty()

OTHER INTERNATIONAL SOURCES

UN Treaty Collection:
{UN_TREATIES}
- Multilateral treaties
- State signatures and ratifications

ICJ (International Court of Justice):
https://www.icj-cij.org
- Inter-state disputes
- Advisory opinions

WTO:
https://www.wto.org/english/docs_e/legal_e/legal_e.htm
- Trade agreements
- Dispute settlement

Hague Conference:
https://www.hcch.net
- Private international law conventions
- Child abduction
- Service of documents

UK AND INTERNATIONAL LAW

Dualist system:
International treaties generally require domestic implementing
legislation to have effect in UK law.

Key legislation:
- Human Rights Act 1998 (ECHR)
- European Union (Withdrawal) Act 2018 (retained EU law)
- State Immunity Act 1978
- Extradition Act 2003

Customary international law:
Part of common law where not inconsistent with statute.

For research on public international law:
- BAILII international materials
- Oxford Public International Law
- Cambridge International Law Journal"""
