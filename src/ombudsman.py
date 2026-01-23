"""
Ombudsman Module

Connects to UK Ombudsman decision databases:
- LGO (Local Government and Social Care Ombudsman)
- Housing Ombudsman
- PHSO (Parliamentary and Health Service Ombudsman)
- Financial Ombudsman Service
- Legal Ombudsman
"""

import httpx
from typing import Optional
from urllib.parse import quote, urlencode

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# Base URLs
LGO_BASE = "https://www.lgo.org.uk"
HOUSING_OMB_BASE = "https://www.housing-ombudsman.org.uk"
PHSO_BASE = "https://www.ombudsman.org.uk"
FOS_BASE = "https://www.financial-ombudsman.org.uk"
LEO_BASE = "https://www.legalombudsman.org.uk"


# ============================================================
# LGO (Local Government and Social Care Ombudsman)
# ============================================================

def search_lgo(query: str, council: Optional[str] = None, category: Optional[str] = None) -> str:
    """
    Search Local Government Ombudsman decisions.

    Args:
        query: Search terms (e.g., "care assessment", "safeguarding", "housing")
        council: Optional council name filter
        category: Optional category (e.g., "adult care services", "education", "housing")

    Returns:
        Search URL and guidance

    Note: LGO decisions are important for local authority practice
    """
    # LGO decisions search
    params = {"q": query}

    search_url = f"{LGO_BASE}/decisions/?{urlencode(params)}"

    result = f"""Local Government and Social Care Ombudsman (LGO) Decisions

Search: {search_url}

Searching for: {query}"""

    if council:
        result += f"\nCouncil: {council}"
    if category:
        result += f"\nCategory: {category}"

    result += f"""

The LGO investigates complaints about:
- Council services (all departments)
- Adult social care (care homes, home care, assessments)
- Children's services
- Education (school admissions, SEND)
- Housing (homelessness, allocations, repairs)
- Planning and building control
- Environmental health
- Benefits administration
- Complaint handling

Categories for filtering:
- Adult care services
- Benefits and tax
- Children's services
- Corporate and other services
- Education
- Environment services
- Highways and transport
- Housing
- Planning and development

Decision database: {LGO_BASE}/decisions/
Statistics and reports: {LGO_BASE}/information-centre/

Note: LGO decisions establish good administrative practice standards.
Finding of 'maladministration causing injustice' requires remedy."""

    return result


def get_lgo_decision(case_reference: str) -> str:
    """
    Get a specific LGO decision.

    Args:
        case_reference: LGO case reference number (e.g., "22 001 234")

    Returns:
        Link to search for the specific decision
    """
    # Clean reference
    ref_clean = case_reference.strip().replace(" ", "+")

    search_url = f"{LGO_BASE}/decisions/?q={ref_clean}"

    return f"""LGO Decision Search

Reference: {case_reference}
Search: {search_url}

If the reference is correct, the decision should appear in search results.

LGO decisions include:
- Summary of complaint
- What the Ombudsman found
- Whether there was fault/maladministration
- Whether fault caused injustice
- Recommended remedy

To cite an LGO decision:
"LGO Decision [reference], [date]"

Decisions are persuasive but not binding - they establish standards
of good administrative practice for local authorities."""


def get_lgo_focus_reports() -> str:
    """
    Get LGO focus reports and guidance.

    Returns:
        Links to key LGO publications
    """
    return f"""LGO Focus Reports and Guidance

Focus Reports (thematic reviews):
{LGO_BASE}/information-centre/focus-reports/

Key recent focus reports include topics like:
- Adult social care
- Children's services
- Homelessness
- School admissions
- Complaint handling

Annual Review:
{LGO_BASE}/information-centre/annual-reviews/

Council statistics:
{LGO_BASE}/information-centre/councils-performance/

Guidance for councils:
{LGO_BASE}/information-centre/

Good practice guides on:
- Running a complaints procedure
- Handling remedies
- Learning from complaints

These reports are useful for:
- Understanding LGO expectations
- Defending judicial reviews
- Improving council practices
- Training staff"""


# ============================================================
# Housing Ombudsman
# ============================================================

def search_housing_ombudsman(query: str) -> str:
    """
    Search Housing Ombudsman decisions.

    Args:
        query: Search terms (e.g., "repairs", "antisocial behaviour", "damp")

    Returns:
        Search URL and guidance
    """
    search_url = f"{HOUSING_OMB_BASE}/decisions/"

    result = f"""Housing Ombudsman Decisions

Decisions database: {search_url}

Searching for: {query}

The Housing Ombudsman investigates complaints about:
- Social landlords (housing associations, councils as landlords)
- Repairs and maintenance
- Antisocial behaviour handling
- Complaint handling
- Service charges (for some tenancies)
- Tenant engagement

NOT covered:
- Private landlords (use local authority/courts)
- Right to Buy disputes
- Rent levels

Categories:
- Repairs
- Antisocial behaviour
- Complaint handling
- Property condition
- Staff conduct
- Communication
- Record keeping

The Housing Ombudsman uses a severity scale:
- No maladministration
- Service failure (minor issues)
- Maladministration
- Severe maladministration

Landlord performance reports:
{HOUSING_OMB_BASE}/landlords/

Complaint handling code:
{HOUSING_OMB_BASE}/landlords/complaint-handling-code/"""

    return result


def get_housing_ombudsman_decision(case_reference: str) -> str:
    """
    Get a specific Housing Ombudsman decision.

    Args:
        case_reference: Case reference number

    Returns:
        Link to search for the decision
    """
    return f"""Housing Ombudsman Decision

Reference: {case_reference}

Search the decisions database:
{HOUSING_OMB_BASE}/decisions/

Enter the reference number in the search box to find the specific case.

Housing Ombudsman decisions include:
- Background to the complaint
- Assessment of each issue
- Finding (maladministration/service failure/no maladministration)
- Orders and recommendations

Findings can be used to:
- Support similar complaints
- Evidence systemic failures
- Demonstrate landlord non-compliance with Code"""


# ============================================================
# PHSO (Parliamentary and Health Service Ombudsman)
# ============================================================

def search_phso(query: str) -> str:
    """
    Search Parliamentary and Health Service Ombudsman decisions.

    Args:
        query: Search terms (e.g., "NHS", "treatment delay", "DWP")

    Returns:
        Search URL and guidance
    """
    search_url = f"{PHSO_BASE}/publications/"

    result = f"""Parliamentary and Health Service Ombudsman (PHSO)

Publications and reports: {search_url}

Searching for: {query}

PHSO investigates complaints about:

NHS bodies:
- Hospitals (NHS Trusts and Foundation Trusts)
- GPs, dentists, pharmacists
- Clinical Commissioning Groups / ICBs
- NHS England
- Mental health trusts
- Ambulance services

Government departments and agencies:
- DWP (benefits decisions, PIP, UC)
- HMRC
- Home Office (immigration)
- DVLA
- Passport Office
- Other central government bodies

NOT covered:
- Local authorities (use LGO)
- Private healthcare
- Social care (use LGO)

PHSO's role:
- Final stage of complaints process
- Complainant must exhaust NHS/departmental complaints first
- Can recommend financial remedy
- Can require service improvements

Key publications:
- Case summaries: {PHSO_BASE}/publications/
- Investigation reports
- Systemic investigation reports
- Annual report

Principles of Good Administration:
{PHSO_BASE}/making-a-complaint/"""

    return result


def get_phso_decision(case_reference: str) -> str:
    """
    Get a specific PHSO decision or publication.

    Args:
        case_reference: PHSO reference or publication name

    Returns:
        Link to search for the decision
    """
    search_url = f"{PHSO_BASE}/publications/?search={quote(case_reference)}"

    return f"""PHSO Decision/Publication Search

Reference: {case_reference}
Search: {search_url}

PHSO publishes:
- Individual investigation summaries
- Thematic reports
- Systemic investigation reports

For individual cases, PHSO may not publish full details but provides
summaries on specific topics.

Casework statistics:
{PHSO_BASE}/making-a-complaint/data/

Contact PHSO:
{PHSO_BASE}/making-a-complaint/"""


# ============================================================
# Financial Ombudsman Service
# ============================================================

def search_financial_ombudsman(query: str, firm: Optional[str] = None) -> str:
    """
    Search Financial Ombudsman Service decisions.

    Args:
        query: Search terms (e.g., "PPI", "mortgage", "insurance claim")
        firm: Optional firm name filter

    Returns:
        Search URL and guidance
    """
    params = {"query": query}
    if firm:
        params["firm"] = firm

    search_url = f"{FOS_BASE}/decisions/?{urlencode(params)}"

    result = f"""Financial Ombudsman Service (FOS) Decisions

Search: {search_url}

Searching for: {query}"""

    if firm:
        result += f"\nFirm: {firm}"

    result += f"""

FOS investigates complaints about:
- Banks and building societies
- Insurance companies
- Investment firms
- Pension providers
- Credit and loans
- Payment services
- Debt collection
- Financial advisers

Product types:
- Current accounts
- Savings accounts
- Mortgages
- Credit cards
- Loans
- Pensions
- Investments
- Insurance (all types)
- PPI

Decisions database:
{FOS_BASE}/decisions/

FOS can award up to £415,000 (for complaints after April 2023).

Ombudsman news (case studies and guidance):
{FOS_BASE}/businesses/resolving-complaints/ombudsman-news/

Complaint data by firm:
{FOS_BASE}/data-and-research/our-data/"""

    return result


def get_fos_decision(case_reference: str) -> str:
    """
    Get a specific Financial Ombudsman decision.

    Args:
        case_reference: FOS decision reference number

    Returns:
        Link to search for the decision
    """
    search_url = f"{FOS_BASE}/decisions/?query={quote(case_reference)}"

    return f"""Financial Ombudsman Decision

Reference: {case_reference}
Search: {search_url}

FOS decisions include:
- Summary of complaint
- Firm's response
- Ombudsman's findings
- Award (if applicable)

FOS decisions are binding on the firm if accepted by the complainant.
Complainant can reject the decision and pursue court action.

FOS decisions are anonymised but searchable by:
- Product type
- Issue type
- Outcome
- Date range

These decisions establish industry practice standards."""


# ============================================================
# Legal Ombudsman
# ============================================================

def search_legal_ombudsman(query: str) -> str:
    """
    Search Legal Ombudsman information and decisions.

    Args:
        query: Search terms (e.g., "costs", "communication", "delay")

    Returns:
        Search URL and guidance
    """
    search_url = f"{LEO_BASE}/information-centre/"

    result = f"""Legal Ombudsman (LeO)

Information centre: {search_url}

Searching for: {query}

The Legal Ombudsman investigates complaints about:
- Solicitors
- Barristers
- Licensed conveyancers
- Legal executives (CILEx)
- Costs lawyers
- Patent and trade mark attorneys
- Notaries
- Claims management companies

Common complaint types:
- Poor communication
- Costs and bills
- Delay
- Failure to follow instructions
- Poor quality of work
- Loss of documents

LeO can award up to £50,000.

Note: LeO handles service complaints. For professional misconduct,
contact the relevant regulator (SRA for solicitors, BSB for barristers).

Decision data:
{LEO_BASE}/raising-standards/data-and-decisions/

Guidance for legal professionals:
{LEO_BASE}/for-lawyers/

How to complain:
{LEO_BASE}/how-to-complain/

Time limits:
- Within 6 years of the act/omission
- Within 3 years of when complainant knew about it
- Within 1 year of completing the firm's complaints procedure"""

    return result


def get_leo_decision(case_reference: str) -> str:
    """
    Get Legal Ombudsman decision or statistics.

    Args:
        case_reference: LeO reference or search term

    Returns:
        Link to LeO data and decisions
    """
    return f"""Legal Ombudsman Decision Search

Reference: {case_reference}

LeO decision data:
{LEO_BASE}/raising-standards/data-and-decisions/

LeO publishes:
- Annual reports
- Statistical data
- Case studies (anonymised)
- Thematic reports

Individual decisions are not routinely published in full, but
anonymised case studies illustrate LeO's approach.

First-tier Tribunal appeals:
Appeals against LeO decisions go to the First-tier Tribunal
(General Regulatory Chamber).

For specific case information:
Contact LeO directly: {LEO_BASE}/contact-us/"""


# ============================================================
# Index Function
# ============================================================

def list_ombudsman_services() -> str:
    """
    List all available Ombudsman services.

    Returns:
        Index of Ombudsman services with jurisdiction
    """
    return f"""UK Ombudsman Services Index

LOCAL GOVERNMENT AND SOCIAL CARE OMBUDSMAN (LGO)
Website: {LGO_BASE}
Decisions: {LGO_BASE}/decisions/
Jurisdiction: Councils, adult social care, children's services, education, housing (LA)
Use: search_lgo(), get_lgo_decision()

HOUSING OMBUDSMAN
Website: {HOUSING_OMB_BASE}
Decisions: {HOUSING_OMB_BASE}/decisions/
Jurisdiction: Social landlords (housing associations, council housing)
Use: search_housing_ombudsman(), get_housing_ombudsman_decision()

PARLIAMENTARY AND HEALTH SERVICE OMBUDSMAN (PHSO)
Website: {PHSO_BASE}
Publications: {PHSO_BASE}/publications/
Jurisdiction: NHS bodies, government departments and agencies
Use: search_phso(), get_phso_decision()

FINANCIAL OMBUDSMAN SERVICE (FOS)
Website: {FOS_BASE}
Decisions: {FOS_BASE}/decisions/
Jurisdiction: Banks, insurers, investment firms, pension providers
Use: search_financial_ombudsman(), get_fos_decision()

LEGAL OMBUDSMAN (LeO)
Website: {LEO_BASE}
Data: {LEO_BASE}/raising-standards/data-and-decisions/
Jurisdiction: Solicitors, barristers, licensed conveyancers, other legal providers
Use: search_legal_ombudsman(), get_leo_decision()

OTHER OMBUDSMAN SCHEMES

Pensions Ombudsman: https://www.pensions-ombudsman.org.uk
- Workplace and personal pensions

Property Ombudsman: https://www.tpos.co.uk
- Estate agents, lettings agents

Removals Ombudsman: https://www.removalsombudsman.org.uk
- Removals companies

Motor Ombudsman: https://www.themotorombudsman.org
- Vehicle sales and servicing

Energy Ombudsman: https://www.energyombudsman.org
- Gas and electricity suppliers

Communications Ombudsman: https://www.ombudsman-services.org/communications
- Phone, broadband, postal services"""
