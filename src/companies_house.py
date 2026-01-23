"""
Companies House Module

Connects to Companies House API for company information.
Note: The API is free but requires an API key for some endpoints.
Basic company search and public data is available without a key.
"""

import httpx
from typing import Optional
from urllib.parse import quote, urlencode

# Companies House API (free, some endpoints need API key)
CH_API_BASE = "https://api.company-information.service.gov.uk"
CH_WEB_BASE = "https://find-and-update.company-information.service.gov.uk"
CH_BETA = "https://beta.companieshouse.gov.uk"

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "application/json"
}


def search_companies(query: str) -> str:
    """
    Search Companies House for companies.

    Args:
        query: Company name or number to search for

    Returns:
        Search URL and guidance

    Note: For API access, register at https://developer.company-information.service.gov.uk
    """
    # Web search (no API key needed)
    web_search_url = f"{CH_WEB_BASE}/search?q={quote(query)}"

    # API endpoint (needs API key for programmatic access)
    api_search_url = f"{CH_API_BASE}/search/companies?q={quote(query)}"

    return f"""Companies House Search

Web search: {web_search_url}
API endpoint: {api_search_url} (requires API key)

Searching for: {query}

The search will return:
- Company name
- Company number
- Registered office address
- Company status (active, dissolved, etc.)
- Company type (Ltd, PLC, LLP, etc.)

To search by company number directly, use get_company("12345678")

Company types:
- ltd / private-limited-shares-section-30-exemption
- plc / public-limited-company
- llp / limited-liability-partnership
- charitable-incorporated-organisation
- registered-society
- scottish-partnership
- and others

Free API access:
Register at https://developer.company-information.service.gov.uk
- 600 requests per 5 minutes
- No cost for public data

Companies House web services:
- Search: {CH_WEB_BASE}
- Filing history
- Accounts
- Officers
- Persons with significant control"""


def get_company(company_number: str) -> str:
    """
    Get company details by company number.

    Args:
        company_number: 8-character company number (e.g., "00000001" or "SC123456")

    Returns:
        Direct links to company information
    """
    # Normalise company number (pad with zeros if needed)
    cn = company_number.strip().upper()
    if cn.isdigit():
        cn = cn.zfill(8)

    # Direct link to company page
    web_url = f"{CH_WEB_BASE}/company/{cn}"
    api_url = f"{CH_API_BASE}/company/{cn}"

    return f"""Companies House - Company {cn}

Company page: {web_url}
API endpoint: {api_url} (requires API key)

The company page shows:
- Company overview (status, type, incorporation date)
- Registered office address
- Nature of business (SIC codes)
- Previous company names

Related pages:
- Filing history: {web_url}/filing-history
- Officers: {web_url}/officers
- Persons with significant control: {web_url}/persons-with-significant-control
- Accounts: Available in filing history
- Charges: {web_url}/charges
- Insolvency: {web_url}/insolvency (if applicable)

Company prefixes:
- No prefix: England & Wales
- SC: Scotland
- NI: Northern Ireland
- FC/SF: Overseas companies
- OC: LLPs
- IP: Industrial and Provident Societies
- CE/GE: European companies"""


def get_company_filings(company_number: str) -> str:
    """
    Get company filing history.

    Args:
        company_number: Company number

    Returns:
        Link to filing history
    """
    cn = company_number.strip().upper()
    if cn.isdigit():
        cn = cn.zfill(8)

    web_url = f"{CH_WEB_BASE}/company/{cn}/filing-history"
    api_url = f"{CH_API_BASE}/company/{cn}/filing-history"

    return f"""Companies House - Filing History

Company: {cn}
Filing history: {web_url}
API endpoint: {api_url}

Filing history includes:
- Annual accounts
- Confirmation statements (previously annual returns)
- Appointment/termination of directors
- Changes of registered office
- Resolutions and minutes
- Charges (mortgages and debentures)
- Articles of association changes

Document types:
- AA: Annual accounts
- CS01: Confirmation statement
- AP01-04: Appointment of director/secretary
- TM01-02: Termination of director/secretary
- AD01: Change of registered office
- MR01-05: Charge documents
- IN01: First gazette notice (insolvency)
- SH01: Share allotment

Most documents are free to download as PDFs.
Some older documents require payment for certified copies."""


def get_officers(company_number: str) -> str:
    """
    Get company officers (directors, secretaries).

    Args:
        company_number: Company number

    Returns:
        Link to officers list
    """
    cn = company_number.strip().upper()
    if cn.isdigit():
        cn = cn.zfill(8)

    web_url = f"{CH_WEB_BASE}/company/{cn}/officers"
    api_url = f"{CH_API_BASE}/company/{cn}/officers"

    return f"""Companies House - Officers

Company: {cn}
Officers page: {web_url}
API endpoint: {api_url}

Officers information includes:
- Current and resigned directors
- Company secretaries
- LLP designated members
- Appointment and resignation dates
- Occupation
- Nationality
- Date of birth (month/year only for privacy)
- Country of residence

Officer search (find all directorships):
{CH_WEB_BASE}/search/officers

Disqualified directors:
{CH_WEB_BASE}/search/disqualified-officers

Note: Directors' home addresses are protected.
Service addresses are shown instead."""


def get_charges(company_number: str) -> str:
    """
    Get company charges (mortgages, debentures).

    Args:
        company_number: Company number

    Returns:
        Link to charges register
    """
    cn = company_number.strip().upper()
    if cn.isdigit():
        cn = cn.zfill(8)

    web_url = f"{CH_WEB_BASE}/company/{cn}/charges"
    api_url = f"{CH_API_BASE}/company/{cn}/charges"

    return f"""Companies House - Charges Register

Company: {cn}
Charges page: {web_url}
API endpoint: {api_url}

Charges information includes:
- Outstanding charges (mortgages, debentures, etc.)
- Satisfied (paid off) charges
- Charge holder (secured creditor)
- Description of charged property
- Date of creation
- Date of satisfaction (if applicable)

Understanding charges:
- A charge is security over company assets
- Must be registered within 21 days of creation
- Fixed charge: over specific assets
- Floating charge: over changing assets (e.g., stock)
- Debenture: typically a floating charge over all assets

Charges affect:
- Lending decisions
- Insolvency priorities
- Asset disposal"""


def get_psc(company_number: str) -> str:
    """
    Get persons with significant control (PSC).

    Args:
        company_number: Company number

    Returns:
        Link to PSC register
    """
    cn = company_number.strip().upper()
    if cn.isdigit():
        cn = cn.zfill(8)

    web_url = f"{CH_WEB_BASE}/company/{cn}/persons-with-significant-control"
    api_url = f"{CH_API_BASE}/company/{cn}/persons-with-significant-control"

    return f"""Companies House - Persons with Significant Control (PSC)

Company: {cn}
PSC page: {web_url}
API endpoint: {api_url}

PSC conditions (any one of):
- Holds more than 25% of shares
- Holds more than 25% of voting rights
- Has the right to appoint/remove majority of directors
- Has the right to exercise significant influence or control
- Has the right to exercise significant influence or control over a trust or firm that meets any of the above

Information shown:
- Name
- Date of birth (month/year)
- Nationality
- Country of residence
- Nature of control
- Date registered

PSC statements:
- Steps to identify PSC
- PSC cannot be identified
- No individual is a PSC (only companies)

This register supports anti-money laundering requirements.
Some exemptions exist (e.g., for traded companies with own disclosure)."""


def search_disqualified_directors(name: str) -> str:
    """
    Search for disqualified directors.

    Args:
        name: Director name to search

    Returns:
        Search URL and guidance
    """
    search_url = f"{CH_WEB_BASE}/search/disqualified-officers?q={quote(name)}"

    return f"""Disqualified Directors Search

Search: {search_url}

Searching for: {name}

Director disqualification means they cannot:
- Be a director of a company
- Be involved in company management
- Act as an insolvency practitioner
- Be a receiver

Disqualification can be:
- By court order (Company Directors Disqualification Act 1986)
- By undertaking (accepted by Secretary of State)
- Automatic on bankruptcy

Disqualification periods: 2-15 years

Grounds include:
- Unfitness following company insolvency
- Persistent breaches of Companies Act
- Fraud
- Wrongful or fraudulent trading

Register shows:
- Name and aliases
- Date of birth
- Disqualification dates
- Reason (court order/undertaking)
- Duration"""


def companies_house_api_info() -> str:
    """
    Get information about Companies House API access.

    Returns:
        API documentation and access information
    """
    return f"""Companies House API

REGISTRATION
Developer portal: https://developer.company-information.service.gov.uk

Free API access:
- 600 requests per 5 minutes
- Public company data only
- No cost

API BASE URL
{CH_API_BASE}

KEY ENDPOINTS

Company:
- GET /company/{{company_number}}
- GET /company/{{company_number}}/filing-history
- GET /company/{{company_number}}/officers
- GET /company/{{company_number}}/charges
- GET /company/{{company_number}}/persons-with-significant-control

Search:
- GET /search/companies?q={{query}}
- GET /search/officers?q={{query}}
- GET /search/disqualified-officers?q={{query}}

Documents:
- GET /company/{{company_number}}/filing-history/{{transaction_id}}/document

AUTHENTICATION
Use HTTP Basic Auth with API key as username, no password:
  curl -u YOUR_API_KEY: {CH_API_BASE}/company/00000001

RESPONSE FORMAT
JSON by default. Accept header can request other formats.

RATE LIMITING
HTTP 429 returned if rate exceeded.
Retry-After header indicates wait time.

STREAMING API
For bulk data, consider the streaming API:
https://developer.company-information.service.gov.uk/streaming-api

BULK DATA PRODUCTS
Free bulk data available:
http://download.companieshouse.gov.uk/en_output.html"""
