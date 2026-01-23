"""
Land Registry Module

Connects to HM Land Registry services:
- Property price paid data (free)
- Title information (requires account/payment for full data)
- INSPIRE Index Polygons (free)
"""

import httpx
from typing import Optional
from urllib.parse import quote, urlencode

# Land Registry URLs
LR_BASE = "https://www.gov.uk/government/organisations/land-registry"
LR_SEARCH = "https://search-property-information.service.gov.uk"
LR_DATA = "https://landregistry.data.gov.uk"
PRICE_PAID_API = "https://landregistry.data.gov.uk/data/ppi"

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "application/json"
}


def search_price_paid(
    postcode: Optional[str] = None,
    street: Optional[str] = None,
    town: Optional[str] = None,
    property_type: Optional[str] = None
) -> str:
    """
    Search Land Registry Price Paid Data.

    Args:
        postcode: Full or partial postcode (e.g., "SW1A 1AA" or "SW1A")
        street: Street name
        town: Town or city name
        property_type: D (detached), S (semi), T (terraced), F (flat)

    Returns:
        Search URL and data access information

    Note: Price Paid Data is free and open data
    """
    # Build SPARQL-style query parameters
    params = {}
    if postcode:
        params["postcode"] = postcode.upper().strip()
    if street:
        params["street"] = street
    if town:
        params["town"] = town
    if property_type:
        type_map = {
            "d": "detached",
            "detached": "detached",
            "s": "semi-detached",
            "semi": "semi-detached",
            "t": "terraced",
            "terraced": "terraced",
            "f": "flat",
            "flat": "flat",
        }
        params["propertyType"] = type_map.get(property_type.lower(), property_type)

    # Web search URL
    web_search = "https://www.gov.uk/search-property-information-land-registry"

    # API search (linked data)
    api_url = f"{PRICE_PAID_API}/transaction-record.json"
    if params:
        api_url += "?" + urlencode(params)

    result = f"""Land Registry Price Paid Data

Web search: {web_search}
Data API: {LR_DATA}

Search criteria:"""
    if postcode:
        result += f"\n  Postcode: {postcode}"
    if street:
        result += f"\n  Street: {street}"
    if town:
        result += f"\n  Town: {town}"
    if property_type:
        result += f"\n  Property type: {property_type}"

    result += f"""

PRICE PAID DATA
Free dataset of property sales in England and Wales:
- Transaction price
- Transaction date
- Property type (detached, semi, terraced, flat)
- Old/new build
- Freehold/leasehold
- Address

Access options:
1. Download bulk data: {LR_DATA}/app/ppd
2. Query via SPARQL: {LR_DATA}/app/qonsole
3. Use the linked data API

Property types:
- D: Detached
- S: Semi-detached
- T: Terraced
- F: Flat/maisonette
- O: Other

Transaction categories:
- A: Standard price paid (open market)
- B: Additional price paid (not open market - e.g., transfers between family)

Limitations:
- Does not include commercial property
- Does not include sales below £100 (Right to Buy)
- Some transactions excluded for legal reasons"""

    return result


def get_title_summary(title_number: str) -> str:
    """
    Get Land Registry title information guidance.

    Args:
        title_number: Title number (e.g., "DN123456")

    Returns:
        Guidance on obtaining title information

    Note: Full title information requires account and payment
    """
    return f"""Land Registry Title Information

Title number: {title_number}

HOW TO GET TITLE INFORMATION

1. Title Summary (£3 per title):
   {LR_SEARCH}/search/search-by-title-number
   - Shows current owner name
   - Property address
   - Price paid (if available)
   - Whether there are documents

2. Title Register (£3 per title):
   Full register with:
   - Property description
   - Ownership details (proprietor)
   - Restrictions
   - Charges (mortgages)
   - Easements and covenants affecting the property

3. Title Plan (£3 per plan):
   Map showing property boundaries

4. Official Copies (£7 per document):
   Certified copies for legal proceedings

ORDER ONLINE
{LR_SEARCH}

You will need:
- Address or title number
- Government Gateway account or create one
- Payment card

UNDERSTANDING TITLE NUMBERS
Format: [Letters][Numbers]
- DN: Devon (some areas)
- GR: Gloucestershire (some areas)
- HD: Hull
- LN: Lincolnshire
- SY: Shropshire
- WS: West Sussex
- etc.

Newer titles have different formats depending on registration date.

FOR LEGAL PROCEEDINGS
Order official copies for court evidence.
Title registers admissible under Civil Evidence Act 1995."""


def search_registered_titles(address: str) -> str:
    """
    Search for registered titles by address.

    Args:
        address: Property address to search

    Returns:
        Guidance on searching by address
    """
    search_url = f"{LR_SEARCH}/search/search-by-address"

    return f"""Land Registry Address Search

Search page: {search_url}

Searching for: {address}

SEARCH BY ADDRESS
Enter the property address to find:
- Whether the property is registered
- Title number(s) for the property
- Option to purchase title documents

UNREGISTERED LAND
Not all land in England and Wales is registered.
Registration became compulsory in stages:
- 1990: Compulsory on sale in England and Wales
- Some land still unregistered if not sold since

MULTIPLE TITLES
One property may have multiple titles:
- Freehold title
- Leasehold title (if applicable)
- Separate titles for different parts

COSTS
- Search by address: Free
- View title summary: £3
- Download title register: £3
- Download title plan: £3
- Official copies: £7

BULK SEARCHES
For commercial searches (conveyancing, etc.):
{LR_BASE}/using-the-business-e-services"""


def get_inspire_index() -> str:
    """
    Get INSPIRE Index Polygon data information.

    Returns:
        Information about free spatial data
    """
    return f"""Land Registry INSPIRE Index Polygons

FREE SPATIAL DATA
{LR_DATA}/app/root/doc/inspire

The INSPIRE Index Polygon dataset shows:
- Boundaries of all registered titles
- Title numbers
- Tenure (freehold/leasehold)
- Date of last update

This is FREE and OPEN data.

ACCESS OPTIONS

1. Download bulk data (GeoPackage, GML):
   {LR_DATA}/app/root/doc/inspire

2. WFS (Web Feature Service):
   For GIS applications

3. Via QGIS or similar GIS software

USE CASES
- Identifying registered titles in an area
- Property boundary research
- Planning and development analysis
- Land ownership mapping

LIMITATIONS
- Shows boundaries, not owners
- To get owner information, use title search service
- Accuracy varies (based on original deed plans)
- Does not show unregistered land

SUPPLEMENTARY DATA
Land Registry also publishes:
- UK House Price Index: {LR_DATA}/app/ukhpi
- Price Paid Data: {LR_DATA}/app/ppd
- Transaction Data: {LR_DATA}/app/root/doc/td
- Standard Reports: {LR_DATA}/app/root/doc/sr"""


def land_registry_services_index() -> str:
    """
    Index of Land Registry services.

    Returns:
        Complete guide to LR services
    """
    return f"""HM Land Registry Services Index

FREE DATA AND SEARCHES

Price Paid Data:
- What properties sold for
- {LR_DATA}/app/ppd
- Use: search_price_paid()

INSPIRE Index Polygons:
- Title boundaries (no owner info)
- {LR_DATA}/app/root/doc/inspire
- Use: get_inspire_index()

UK House Price Index:
- Monthly price statistics
- {LR_DATA}/app/ukhpi

PAID SEARCHES (via account)

Search Property Information:
{LR_SEARCH}

Costs:
- Title summary: £3
- Title register: £3
- Title plan: £3
- Official copies: £7

BUSINESS SERVICES

Business Gateway (for professionals):
{LR_BASE}/using-the-business-e-services

Portal:
- Conveyancers
- Mortgage lenders
- Solicitors

GUIDANCE

Practice guides:
{LR_BASE}/publications?publication_filter_option=guidance

Key guides:
- Practice Guide 1: First registrations
- Practice Guide 4: Restrictions
- Practice Guide 40: Land Registry plans
- Practice Guide 52: Adverse possession
- Practice Guide 67: Leases

LEGISLATION
- Land Registration Act 2002
- Land Registration Rules 2003

ADJUDICATOR
HM Land Registry Adjudicator handles disputes:
https://www.gov.uk/government/organisations/hm-land-registry/about/complaints-procedure

For boundary disputes, see:
Property Chamber (First-tier Tribunal)"""


def get_ownership_search_options() -> str:
    """
    Get options for searching property ownership.

    Returns:
        Guide to ownership research
    """
    return f"""Property Ownership Search Options

1. SEARCH BY ADDRESS
{LR_SEARCH}/search/search-by-address
- Enter property address
- Get title number
- Purchase title documents

2. SEARCH BY TITLE NUMBER
{LR_SEARCH}/search/search-by-title-number
- If you know the title number
- Direct access to documents

3. SEARCH BY MAP
{LR_SEARCH}/search/search-by-map
- Click on map to find titles
- Useful for land without street address

4. BULK SEARCHES
For multiple properties:
- Business Gateway (account required)
- Data services

WHAT YOU GET

Title Summary (£3):
- Owner name
- Address
- Price paid
- Tenure type

Title Register (£3):
- Full ownership details
- Property description
- Restrictions
- Charges (mortgages)
- Easements references

Title Plan (£3):
- Property boundary on OS map
- Coloured edging shows extent

UNREGISTERED LAND
If property not registered:
- Check with local authority for council tax records
- Electoral register (voters)
- Historical deed searches (conveyancers)
- Land Charges search

COMPANY OWNERSHIP
If owner is a company:
- Title shows company name
- Check Companies House for company details
- May show registered office, not beneficial owner

OVERSEAS COMPANIES
Register of Overseas Entities:
https://www.gov.uk/government/organisations/register-of-overseas-entities
- Owners of UK property
- From 2022 onwards"""
