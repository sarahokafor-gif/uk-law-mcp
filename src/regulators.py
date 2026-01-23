"""
Regulators Module

Connects to UK regulatory body websites:
- CQC (Care Quality Commission)
- ICO (Information Commissioner's Office)
- SRA (Solicitors Regulation Authority)
- BSB (Bar Standards Board)
- LAA (Legal Aid Agency)
- Ofsted
"""

import httpx
from typing import Optional
from urllib.parse import quote, urlencode

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# Base URLs
CQC_BASE = "https://www.cqc.org.uk"
CQC_API = "https://api.cqc.org.uk/public/v1"
ICO_BASE = "https://ico.org.uk"
SRA_BASE = "https://www.sra.org.uk"
BSB_BASE = "https://www.barstandardsboard.org.uk"
LAA_BASE = "https://www.gov.uk/government/organisations/legal-aid-agency"
OFSTED_BASE = "https://reports.ofsted.gov.uk"


# ============================================================
# CQC (Care Quality Commission)
# ============================================================

def search_cqc(provider_name: str, location: Optional[str] = None) -> str:
    """
    Search CQC for care provider inspection reports.

    Args:
        provider_name: Name of the provider (e.g., care home name)
        location: Optional location filter (town, city, or postcode)

    Returns:
        Search URL and guidance on using CQC

    Note: CQC has a public API at api.cqc.org.uk for programmatic access
    """
    # Build search URL
    params = {"q": provider_name}
    if location:
        params["location"] = location

    search_url = f"{CQC_BASE}/search/providers?{urlencode(params)}"

    result = f"""CQC Provider Search

Search: {search_url}

Searching for: {provider_name}"""

    if location:
        result += f"\nLocation: {location}"

    result += f"""

The CQC regulates and inspects:
- Care homes (residential and nursing)
- Domiciliary care agencies
- Hospitals and clinics
- GP practices
- Dental practices

CQC API (for programmatic access):
- API docs: {CQC_API}
- Locations endpoint: {CQC_API}/locations
- Providers endpoint: {CQC_API}/providers

Ratings explained:
- Outstanding: Exceptionally good
- Good: Performing well and meeting expectations
- Requires improvement: Not performing as well as expected
- Inadequate: Performing badly; enforcement action taken

CQC inspection reports include:
- Overall rating and ratings for each key area
- What the service does well
- What the service must improve
- Evidence from inspection"""

    return result


def get_cqc_report(provider_id: str) -> str:
    """
    Get a specific CQC inspection report.

    Args:
        provider_id: CQC location ID (found in URLs, e.g., "1-123456789")

    Returns:
        Direct link to the provider's CQC page
    """
    # CQC location pages
    url = f"{CQC_BASE}/location/{provider_id}"

    return f"""CQC Provider Page

URL: {url}

The page will show:
- Current rating and date of last inspection
- Full inspection report (PDF available)
- Rating history
- Services provided
- Contact information

If the ID is incorrect, search for the provider:
{CQC_BASE}/search/providers

CQC API endpoint for this location:
{CQC_API}/locations/{provider_id}"""


def get_cqc_api_info() -> str:
    """
    Get information about the CQC public API.

    Returns:
        API documentation and endpoint information
    """
    return f"""CQC Public API

Base URL: {CQC_API}

Endpoints:
- GET /locations - Search locations (care homes, services, etc.)
- GET /locations/{{locationId}} - Get specific location details
- GET /providers - Search providers (organisations)
- GET /providers/{{providerId}} - Get specific provider details
- GET /changes/locations - Get recent changes to locations
- GET /changes/providers - Get recent changes to providers

Example searches:
- Care homes in London: {CQC_API}/locations?careHome=Y&localAuthority=London
- Nursing homes: {CQC_API}/locations?nursingHome=Y
- By postcode area: {CQC_API}/locations?postalCode=SW1

Response includes:
- Location/provider details
- Current ratings
- Inspection dates
- Registration details
- Contact information

Rate limits apply. For high-volume access, contact CQC.

Documentation: https://www.cqc.org.uk/about-us/transparency/using-cqc-data"""


# ============================================================
# ICO (Information Commissioner's Office)
# ============================================================

def search_ico_guidance(query: str) -> str:
    """
    Search ICO for data protection guidance.

    Args:
        query: Search terms (e.g., "subject access request", "GDPR", "data breach")

    Returns:
        Search URL and key guidance links
    """
    search_url = f"{ICO_BASE}/for-organisations/search/?q={quote(query)}"

    result = f"""ICO Guidance Search

Search: {search_url}

Searching for: {query}

Key ICO Guidance Resources:

UK GDPR / Data Protection Act 2018:
- Guide to UK GDPR: {ICO_BASE}/for-organisations/uk-gdpr-guidance-and-resources/
- Lawful basis for processing: {ICO_BASE}/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis-for-processing/
- Individual rights: {ICO_BASE}/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/

Subject Access Requests (SAR):
- SAR guidance: {ICO_BASE}/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/right-of-access/

Data Breaches:
- Breach reporting: {ICO_BASE}/for-organisations/report-a-breach/
- Breach guidance: {ICO_BASE}/for-organisations/uk-gdpr-guidance-and-resources/personal-data-breaches/

Freedom of Information:
- FOI guidance: {ICO_BASE}/for-organisations/foi/
- Section 14 vexatious requests: {ICO_BASE}/for-organisations/foi/section-14/

Decision Notices:
- ICO decisions database: {ICO_BASE}/action-weve-taken/decision-notices/"""

    return result


def get_ico_decisions(topic: Optional[str] = None) -> str:
    """
    Get ICO enforcement decisions and decision notices.

    Args:
        topic: Optional topic filter (e.g., "health", "local authority", "FOI")

    Returns:
        Links to ICO decision databases
    """
    result = f"""ICO Decisions and Enforcement

Decision Notices (FOI/EIR):
{ICO_BASE}/action-weve-taken/decision-notices/

Enforcement Action:
{ICO_BASE}/action-weve-taken/enforcement/

Monetary Penalties:
{ICO_BASE}/action-weve-taken/enforcement/

Undertakings:
{ICO_BASE}/action-weve-taken/enforcement/

"""
    if topic:
        result += f"""Filtered by topic: {topic}

Use the search/filter functions on the ICO website to narrow by:
- Organisation type
- Sector
- Type of breach
- Date range
"""

    result += """
ICO decisions are important for:
- Understanding ICO interpretation of data protection law
- FOI exemption application
- Proportionality in SAR responses
- Regulatory expectations for data controllers

Appeals from ICO decisions go to the First-tier Tribunal (Information Rights)."""

    return result


# ============================================================
# SRA (Solicitors Regulation Authority)
# ============================================================

def get_sra_rules(section: Optional[str] = None) -> str:
    """
    Get SRA Standards and Regulations.

    Args:
        section: Optional section (e.g., "code", "accounts", "transparency")

    Returns:
        Links to SRA rules and guidance
    """
    result = f"""SRA Standards and Regulations

SRA Handbook (current standards):
{SRA_BASE}/solicitors/standards-regulations/

Key Documents:

SRA Principles:
{SRA_BASE}/solicitors/standards-regulations/principles/
- Act in a way that upholds the constitutional principle of the rule of law
- Act in a way that upholds public trust and confidence
- Act with independence
- Act with honesty
- Act with integrity
- Act in a way that encourages equality, diversity and inclusion
- Act in the best interests of each client

SRA Code of Conduct for Solicitors:
{SRA_BASE}/solicitors/standards-regulations/code-conduct-solicitors/

SRA Code of Conduct for Firms:
{SRA_BASE}/solicitors/standards-regulations/code-conduct-firms/

SRA Accounts Rules:
{SRA_BASE}/solicitors/standards-regulations/accounts-rules/

SRA Transparency Rules:
{SRA_BASE}/solicitors/standards-regulations/transparency-rules/
"""

    if section:
        section_lower = section.lower()
        if "code" in section_lower:
            result += f"""
Specific: Code of Conduct

Individual solicitors: {SRA_BASE}/solicitors/standards-regulations/code-conduct-solicitors/
Firms: {SRA_BASE}/solicitors/standards-regulations/code-conduct-firms/"""
        elif "account" in section_lower:
            result += f"""
Specific: Accounts Rules

{SRA_BASE}/solicitors/standards-regulations/accounts-rules/

Key requirements:
- Client money handling
- Reconciliations
- Accountant's reports"""
        elif "transparency" in section_lower:
            result += f"""
Specific: Transparency Rules

{SRA_BASE}/solicitors/standards-regulations/transparency-rules/

Requirements for publishing:
- Pricing information for certain services
- Complaint handling procedures
- Regulatory status"""

    result += f"""

Find a solicitor:
{SRA_BASE}/consumers/using-solicitor/solicitor-firm-search/

Check solicitor/firm status:
{SRA_BASE}/consumers/using-solicitor/solicitor-firm-search/

Report a concern:
{SRA_BASE}/consumers/problems-solicitor/"""

    return result


def search_sra_decisions(query: str) -> str:
    """
    Search SRA disciplinary decisions.

    Args:
        query: Search terms (e.g., solicitor name, firm name, conduct issue)

    Returns:
        Link to SRA decisions database
    """
    search_url = f"{SRA_BASE}/consumers/solicitor-check/"

    return f"""SRA Disciplinary Decisions

Search solicitor records: {search_url}

Searching for: {query}

The SRA publishes:
- Regulatory decisions
- Tribunal decisions (referred to SDT)
- Conditions on practice
- Interventions

Solicitors Disciplinary Tribunal (SDT):
https://www.solicitorstribunal.org.uk/
- Full tribunal judgments
- Searchable database of decisions

For individual solicitor records, use the solicitor checker to view:
- Current practising status
- Any regulatory history
- Firm associations"""


# ============================================================
# BSB (Bar Standards Board)
# ============================================================

def get_bsb_rules(section: Optional[str] = None) -> str:
    """
    Get Bar Standards Board rules and guidance.

    Args:
        section: Optional section (e.g., "conduct", "equality", "training")

    Returns:
        Links to BSB rules
    """
    result = f"""Bar Standards Board Rules and Guidance

BSB Handbook:
{BSB_BASE}/for-barristers/bsb-handbook-and-code-guidance/

Core Documents:

Code of Conduct:
{BSB_BASE}/for-barristers/bsb-handbook-and-code-guidance/code-of-conduct/

Core Duties:
CD1: Act with honesty and integrity
CD2: Do not behave in a way likely to diminish public trust
CD3: Act in the best interests of each client
CD4: Maintain your independence
CD5: Do not behave in a way likely to diminish confidence in the legal profession
CD6: Keep your affairs of clients confidential
CD7: Provide a competent standard of work
CD8: Do not discriminate unlawfully
CD9: Be open and cooperative with regulators
CD10: Take reasonable steps to manage your practice competently

Guidance on:
- Cab rank rule
- Conflicts of interest
- Complaints handling
- Continuing professional development

"""

    if section:
        section_lower = section.lower()
        if "conduct" in section_lower:
            result += f"""
Specific: Code of Conduct
{BSB_BASE}/for-barristers/bsb-handbook-and-code-guidance/code-of-conduct/"""
        elif "equality" in section_lower or "discrimination" in section_lower:
            result += f"""
Specific: Equality Rules
{BSB_BASE}/for-barristers/bsb-handbook-and-code-guidance/equality-rules/"""

    result += f"""

Find a barrister:
{BSB_BASE}/for-the-public/search-a-barrister/

Report a concern:
{BSB_BASE}/for-the-public/reporting-concerns/

Disciplinary decisions:
{BSB_BASE}/for-the-public/search-a-barrister/ (includes disciplinary history)"""

    return result


# ============================================================
# LAA (Legal Aid Agency)
# ============================================================

def search_laa(query: str) -> str:
    """
    Search Legal Aid Agency guidance.

    Args:
        query: Search terms (e.g., "means test", "merits", "scope", "exceptional funding")

    Returns:
        Search URL and key guidance links
    """
    search_url = f"https://www.gov.uk/search/all?q={quote(query)}&filter_organisations%5B%5D=legal-aid-agency"

    result = f"""Legal Aid Agency Guidance Search

Search: {search_url}

Searching for: {query}

Key LAA Resources:

Legal Aid Legislation:
- LASPO 2012: https://www.legislation.gov.uk/ukpga/2012/10/contents
- Civil Legal Aid Regulations: https://www.legislation.gov.uk/uksi/2013/480/contents
- Criminal Legal Aid Regulations: https://www.legislation.gov.uk/uksi/2013/435/contents

Guidance and Manuals:

Civil Legal Aid:
- Scope of civil legal aid: {LAA_BASE}/collections/civil-legal-aid
- Means assessment guidance: {LAA_BASE}/collections/civil-legal-aid
- Merits criteria: {LAA_BASE}/collections/civil-legal-aid

Exceptional Case Funding (ECF):
- ECF guidance: {LAA_BASE}/collections/civil-legal-aid
- ECF application form: https://www.gov.uk/guidance/exceptional-case-funding-ecf-how-to-apply

Family Legal Aid:
- Family scope: {LAA_BASE}/collections/civil-legal-aid
- MIAM exemptions
- Domestic abuse evidence requirements

Provider Guidance:
- Contract specifications
- Billing guidance
- Quality standards

Find legal aid:
https://www.gov.uk/check-legal-aid
https://www.gov.uk/find-legal-advice"""

    return result


def get_laa_rates() -> str:
    """
    Get Legal Aid remuneration rates.

    Returns:
        Links to current LAA fee schedules
    """
    return f"""Legal Aid Remuneration Rates

Current Rates and Fees:

Civil Legal Aid Rates:
{LAA_BASE}/publications/civil-legal-aid-remuneration-rates

Family Legal Aid Rates:
{LAA_BASE}/publications/civil-legal-aid-remuneration-rates

Criminal Legal Aid Rates:
{LAA_BASE}/publications/criminal-legal-aid-remuneration-rates

The rates are set out in:
- Civil Legal Aid (Remuneration) Regulations 2013
- Criminal Legal Aid (Remuneration) Regulations 2013

Key elements:
- Hourly rates (where applicable)
- Fixed fees
- Graduated fees
- High cost case management

For Court of Protection:
- Non-means tested under Reg 5(1)(g) for DoLS challenges
- Controlled work rates apply
- Licensed work for complex cases

Contract documents:
{LAA_BASE}/collections/legal-aid-agency-contracts"""


# ============================================================
# Ofsted
# ============================================================

def search_ofsted(provider_name: str, location: Optional[str] = None) -> str:
    """
    Search Ofsted inspection reports.

    Args:
        provider_name: Name of school, nursery, children's home, etc.
        location: Optional location filter

    Returns:
        Search URL for Ofsted reports
    """
    params = {"q": provider_name}
    if location:
        params["location"] = location

    search_url = f"{OFSTED_BASE}/search?{urlencode(params)}"

    result = f"""Ofsted Inspection Reports Search

Search: {search_url}

Searching for: {provider_name}"""

    if location:
        result += f"\nLocation: {location}"

    result += f"""

Ofsted inspects and regulates:
- Schools (maintained, academies, independent)
- Early years providers (nurseries, childminders)
- Children's social care (children's homes, fostering, adoption)
- Further education colleges
- Initial teacher training

Ratings:
- Outstanding
- Good
- Requires improvement
- Inadequate

For children's homes and social care:
{OFSTED_BASE}/social-care

Search by URN (Unique Reference Number):
{OFSTED_BASE}/provider/{{urn}}

Download data:
- School performance tables: https://www.gov.uk/school-performance-tables
- Ofsted data: https://www.gov.uk/government/statistical-data-sets/ofsted-annual-reports-statistics"""

    return result


def get_ofsted_report(urn: str) -> str:
    """
    Get a specific Ofsted inspection report by URN.

    Args:
        urn: Unique Reference Number for the provider

    Returns:
        Direct link to the provider's Ofsted page
    """
    url = f"{OFSTED_BASE}/provider/{urn}"

    return f"""Ofsted Provider Page

URL: {url}

The page will show:
- Current rating and date of last inspection
- Full inspection report (PDF available)
- Rating history
- Type of provision
- Contact information

If the URN is incorrect, search for the provider:
{OFSTED_BASE}/search

Find your URN:
- Schools: Check Get Information About Schools (GIAS)
- Early years: On your Ofsted registration documents
- Children's homes: On your Ofsted certificate"""


def list_regulators() -> str:
    """
    List all available regulatory bodies.

    Returns:
        Index of regulators with links
    """
    return f"""UK Regulatory Bodies Index

HEALTH AND SOCIAL CARE

CQC (Care Quality Commission):
- Website: {CQC_BASE}
- API: {CQC_API}
- Regulates: Care homes, hospitals, GPs, dental practices, domiciliary care
- Use: search_cqc(), get_cqc_report()

DATA PROTECTION

ICO (Information Commissioner's Office):
- Website: {ICO_BASE}
- Regulates: Data protection, FOI, privacy
- Use: search_ico_guidance(), get_ico_decisions()

LEGAL PROFESSION

SRA (Solicitors Regulation Authority):
- Website: {SRA_BASE}
- Regulates: Solicitors and law firms in England & Wales
- Use: get_sra_rules(), search_sra_decisions()

BSB (Bar Standards Board):
- Website: {BSB_BASE}
- Regulates: Barristers in England & Wales
- Use: get_bsb_rules()

LAA (Legal Aid Agency):
- Website: {LAA_BASE}
- Manages: Legal aid funding
- Use: search_laa(), get_laa_rates()

EDUCATION

Ofsted:
- Website: {OFSTED_BASE}
- Regulates: Schools, nurseries, children's homes, FE colleges
- Use: search_ofsted(), get_ofsted_report()

OTHER RELEVANT REGULATORS

GMC (General Medical Council): https://www.gmc-uk.org
NMC (Nursing and Midwifery Council): https://www.nmc.org.uk
HCPC (Health and Care Professions Council): https://www.hcpc-uk.org
Social Work England: https://www.socialworkengland.org.uk
FCA (Financial Conduct Authority): https://www.fca.org.uk"""
