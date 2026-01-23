"""
Forms Module

Connects to HMCTS and gov.uk for official court forms.
"""

import httpx
from typing import Optional
from urllib.parse import quote

GOV_UK_BASE = "https://www.gov.uk"
HMCTS_FORMS = f"{GOV_UK_BASE}/government/collections/court-and-tribunal-forms"

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# Court of Protection forms
COP_FORMS = {
    "cop1": {
        "title": "Application form",
        "description": "Main application to the Court of Protection",
        "url": f"{GOV_UK_BASE}/government/publications/make-a-court-of-protection-application-form-cop1",
    },
    "cop1a": {
        "title": "Annex A - Supporting information for property and affairs applications",
        "description": "Property and affairs application supplement",
        "url": f"{GOV_UK_BASE}/government/publications/apply-to-make-decisions-on-someones-property-and-financial-affairs-cop1a",
    },
    "cop1b": {
        "title": "Annex B - Supporting information for personal welfare applications",
        "description": "Personal welfare application supplement",
        "url": f"{GOV_UK_BASE}/government/publications/apply-to-make-decisions-on-someones-personal-welfare-cop1b",
    },
    "cop3": {
        "title": "Assessment of capacity",
        "description": "Capacity assessment by practitioner",
        "url": f"{GOV_UK_BASE}/government/publications/assessment-of-capacity-form-cop3",
    },
    "cop4": {
        "title": "Deputy's declaration",
        "description": "Declaration by proposed deputy",
        "url": f"{GOV_UK_BASE}/government/publications/deputys-declaration-form-cop4",
    },
    "cop5": {
        "title": "Acknowledgment of notification / service",
        "description": "Acknowledgment of being served/notified",
        "url": f"{GOV_UK_BASE}/government/publications/acknowledgment-of-notification-service-cop5",
    },
    "cop9": {
        "title": "Application relating to statutory wills, codicils, settlements and other dealings with P's property",
        "description": "Applications for statutory wills, gifts, settlements",
        "url": f"{GOV_UK_BASE}/government/publications/application-relating-to-a-statutory-will-codicil-or-other-dealing-with-ps-property-cop9",
    },
    "cop14": {
        "title": "Application to be joined as a party",
        "description": "Application to be joined as party to proceedings",
        "url": f"{GOV_UK_BASE}/government/publications/apply-to-be-joined-as-party-to-court-of-protection-proceedings-cop14",
    },
    "cop15": {
        "title": "Application for permission",
        "description": "Request permission to make application",
        "url": f"{GOV_UK_BASE}/government/publications/apply-for-permission-to-make-a-court-of-protection-application-cop15",
    },
    "cop24": {
        "title": "Witness statement",
        "description": "Template for witness statements",
        "url": f"{GOV_UK_BASE}/government/publications/witness-statement-form-cop24",
    },
    "copdol11": {
        "title": "Application to authorise deprivation of liberty",
        "description": "Re X / COPDOL application for welfare DoL",
        "url": f"{GOV_UK_BASE}/government/publications/apply-for-authorisation-to-deprive-someone-of-their-liberty-copdol11",
    },
    "copdol10": {
        "title": "P's representative appointment under s.21A",
        "description": "Appointment of representative in s.21A case",
        "url": f"{GOV_UK_BASE}/government/publications/appoint-a-representative-for-someone-applying-to-the-court-of-protection-copdol10",
    },
}

# Family Court forms
FAMILY_FORMS = {
    "c1": {
        "title": "Application for an order",
        "description": "Section 8 orders (contact, specific issue, prohibited steps)",
        "url": f"{GOV_UK_BASE}/government/publications/form-c1-application-for-an-order",
    },
    "c2": {
        "title": "Application in existing proceedings",
        "description": "Application within existing proceedings",
        "url": f"{GOV_UK_BASE}/government/publications/form-c2-application-for-permission-or-an-order-in-proceedings",
    },
    "c100": {
        "title": "Application under the Children Act 1989 for a child arrangements, prohibited steps, specific issue section 8 order",
        "description": "Main private law children application",
        "url": f"{GOV_UK_BASE}/government/publications/form-c100-application-under-the-children-act-1989-for-a-child-arrangements-prohibited-steps-specific-issue-section-8-order",
    },
    "c1a": {
        "title": "Allegations of harm and domestic abuse",
        "description": "Supplement for domestic abuse/harm allegations",
        "url": f"{GOV_UK_BASE}/government/publications/form-c1a-supplement-for-allegations-of-harm-form-c100",
    },
    "d8": {
        "title": "Divorce/dissolution petition",
        "description": "Application for divorce or dissolution",
        "url": f"{GOV_UK_BASE}/government/publications/form-d8-application-for-a-divorce-dissolution-or-judicial-separation",
    },
    "fl401": {
        "title": "Non-molestation order / occupation order",
        "description": "Application for protective injunctions",
        "url": f"{GOV_UK_BASE}/government/publications/form-fl401-application-for-a-non-molestation-order-occupation-order",
    },
    "fl403": {
        "title": "Application to vary, extend or discharge an order",
        "description": "Vary non-molestation/occupation orders",
        "url": f"{GOV_UK_BASE}/government/publications/form-fl403-application-to-vary-extend-or-discharge-an-order",
    },
    "a1": {
        "title": "Application for a matrimonial or civil partnership order",
        "description": "Financial remedy application",
        "url": f"{GOV_UK_BASE}/government/publications/form-a1-application-for-a-matrimonial-or-civil-partnership-order",
    },
}

# Civil Court forms
CIVIL_FORMS = {
    "n1": {
        "title": "Claim form",
        "description": "Starting a civil claim",
        "url": f"{GOV_UK_BASE}/government/publications/form-n1-claim-form-cpr-part-7",
    },
    "n244": {
        "title": "Application notice",
        "description": "General application in proceedings",
        "url": f"{GOV_UK_BASE}/government/publications/form-n244-application-notice",
    },
    "n215": {
        "title": "Certificate of service",
        "description": "Certificate confirming service",
        "url": f"{GOV_UK_BASE}/government/publications/form-n215-certificate-of-service",
    },
    "n161": {
        "title": "Appellant's notice",
        "description": "Notice of appeal",
        "url": f"{GOV_UK_BASE}/government/publications/form-n161-appellants-notice",
    },
    "n180": {
        "title": "Directions questionnaire",
        "description": "Case management information",
        "url": f"{GOV_UK_BASE}/government/publications/form-n180-directions-questionnaire-small-claims-track",
    },
    "n251": {
        "title": "Notice of funding",
        "description": "Notice of funding (CFAs, legal aid)",
        "url": f"{GOV_UK_BASE}/government/publications/form-n251-notice-of-funding-of-case-or-claim",
    },
    "n461": {
        "title": "Application for judicial review",
        "description": "Judicial review claim form",
        "url": f"{GOV_UK_BASE}/government/publications/form-n461-claim-form-for-judicial-review",
    },
}

# LPA forms
LPA_FORMS = {
    "lp1f": {
        "title": "Lasting Power of Attorney for property and financial affairs",
        "description": "Property and financial affairs LPA",
        "url": f"{GOV_UK_BASE}/government/publications/make-a-lasting-power-of-attorney-property-and-financial-affairs",
    },
    "lp1h": {
        "title": "Lasting Power of Attorney for health and welfare",
        "description": "Health and welfare LPA",
        "url": f"{GOV_UK_BASE}/government/publications/make-a-lasting-power-of-attorney-health-and-welfare",
    },
    "lpa002": {
        "title": "Object to an LPA registration",
        "description": "Objection to LPA registration",
        "url": f"{GOV_UK_BASE}/government/publications/object-to-an-lpa-registration-lpa002",
    },
    "lp3": {
        "title": "Search the OPG register",
        "description": "Request search of LPA/EPA register",
        "url": f"{GOV_UK_BASE}/government/publications/search-the-opg-register-lp3",
    },
}


def search_court_forms(query: str, court: Optional[str] = None) -> str:
    """
    Search for court forms.

    Args:
        query: Search terms (form number or description)
        court: Optional court filter ("cop", "family", "civil", "lpa")

    Returns:
        Matching forms and links
    """
    query_lower = query.lower().strip()

    results = []

    # Search by form number or title
    form_sets = [
        ("Court of Protection", COP_FORMS),
        ("Family", FAMILY_FORMS),
        ("Civil", CIVIL_FORMS),
        ("LPA", LPA_FORMS),
    ]

    for court_name, forms in form_sets:
        if court and court.lower() not in court_name.lower():
            continue

        for form_code, form_data in forms.items():
            if (query_lower in form_code.lower() or
                query_lower in form_data['title'].lower() or
                    query_lower in form_data['description'].lower()):
                results.append(f"{court_name} - {form_code.upper()}: {form_data['title']}\n  {form_data['url']}")

    result = f"""Court Forms Search

Searching for: {query}

"""
    if results:
        result += "Matching forms:\n\n"
        result += "\n\n".join(results[:10])
    else:
        result += "No exact matches found.\n"

    result += f"""

All court forms:
{HMCTS_FORMS}

Form collections:
- Court of Protection: {GOV_UK_BASE}/government/collections/court-of-protection-forms
- Family Court: {GOV_UK_BASE}/government/collections/court-and-tribunal-forms#family-court-forms
- Civil Court: {GOV_UK_BASE}/government/collections/court-and-tribunal-forms#civil-court-forms
- LPA forms: {GOV_UK_BASE}/government/collections/lasting-power-of-attorney-forms"""

    return result


def get_form(form_number: str) -> str:
    """
    Get specific form details and download link.

    Args:
        form_number: Form number (e.g., "COP1", "N244", "C100")

    Returns:
        Form details and URL
    """
    form_lower = form_number.lower().strip().replace(" ", "").replace("-", "")

    # Search all form sets
    all_forms = {**COP_FORMS, **FAMILY_FORMS, **CIVIL_FORMS, **LPA_FORMS}

    if form_lower in all_forms:
        form = all_forms[form_lower]
        return f"""Court Form: {form_number.upper()}

Title: {form['title']}
Description: {form['description']}

Download: {form['url']}

The page will have:
- PDF version for printing
- Instructions and guidance notes
- Related forms

Form finder:
{HMCTS_FORMS}"""

    # Not found
    return f"""Form '{form_number}' not found in quick lookup.

Search all forms:
{HMCTS_FORMS}

Or try search_court_forms("{form_number}")

Common form prefixes:
- COP: Court of Protection
- C: Family Court (children)
- D: Divorce/dissolution
- FL: Family Law Act
- N: Civil claims
- LP: Lasting Power of Attorney"""


def list_forms_by_court(court: str) -> str:
    """
    List all forms for a specific court/jurisdiction.

    Args:
        court: Court type ("cop", "family", "civil", "lpa")

    Returns:
        List of available forms
    """
    court_lower = court.lower().strip()

    if court_lower in ["cop", "court of protection"]:
        result = "Court of Protection Forms\n\n"
        for code, form in COP_FORMS.items():
            result += f"{code.upper()}: {form['title']}\n"
        result += f"\nFull list: {GOV_UK_BASE}/government/collections/court-of-protection-forms"
        return result

    if court_lower in ["family", "family court", "fpr"]:
        result = "Family Court Forms\n\n"
        for code, form in FAMILY_FORMS.items():
            result += f"{code.upper()}: {form['title']}\n"
        result += f"\nFull list: {GOV_UK_BASE}/government/collections/court-and-tribunal-forms#family-court-forms"
        return result

    if court_lower in ["civil", "civil court", "cpr"]:
        result = "Civil Court Forms\n\n"
        for code, form in CIVIL_FORMS.items():
            result += f"{code.upper()}: {form['title']}\n"
        result += f"\nFull list: {GOV_UK_BASE}/government/collections/court-and-tribunal-forms#civil-court-forms"
        return result

    if court_lower in ["lpa", "opg", "lasting power of attorney"]:
        result = "LPA / OPG Forms\n\n"
        for code, form in LPA_FORMS.items():
            result += f"{code.upper()}: {form['title']}\n"
        result += f"\nFull list: {GOV_UK_BASE}/government/collections/lasting-power-of-attorney-forms"
        return result

    # Unknown court
    return f"""Court '{court}' not recognised.

Available courts:
- cop: Court of Protection
- family: Family Court
- civil: Civil Court
- lpa: LPA / OPG forms

All forms: {HMCTS_FORMS}"""


def get_fee_information(court: Optional[str] = None) -> str:
    """
    Get court fee information.

    Args:
        court: Optional court for specific fees

    Returns:
        Fee information and links
    """
    return f"""Court Fees

FEE INFORMATION
{GOV_UK_BASE}/court-fees-what-they-are

COURT OF PROTECTION FEES
Application fee: £371 (2024)
Appeal fee: £234

Fee exemptions/remissions:
{GOV_UK_BASE}/get-help-with-court-fees

FAMILY COURT FEES
Divorce/dissolution: £593
Children Act application: Various (some free)
Financial remedy: £275

CIVIL COURT FEES
Claims vary by value:
- Up to £300: £35
- £300.01 to £500: £50
- £500.01 to £1,000: £70
- £1,000.01 to £1,500: £80
- £1,500.01 to £3,000: £115
- £3,000.01 to £5,000: £205
- £5,000.01 to £10,000: £455
- £10,000.01 to £200,000: 5% of value
- Over £200,000: £10,000

Application notice (N244): £119

FEE HELP (EX160)
Apply for help with fees:
{GOV_UK_BASE}/government/publications/apply-for-help-with-court-and-tribunal-fees

Eligibility:
- Receipt of qualifying benefits, OR
- Low income (disposable capital and income tests)

Note: Legal aid may cover fees in funded cases."""


def forms_index() -> str:
    """
    Complete index of court forms resources.

    Returns:
        Index of all form resources
    """
    return f"""Court and Tribunal Forms Index

MAIN FORMS COLLECTION
{HMCTS_FORMS}

COURT OF PROTECTION
{GOV_UK_BASE}/government/collections/court-of-protection-forms
Key forms: COP1, COP3, COP4, COP9, COP24, COPDOL11
Use: list_forms_by_court("cop")

FAMILY COURT
{GOV_UK_BASE}/government/collections/court-and-tribunal-forms#family-court-forms
Key forms: C100, C1, C2, D8, FL401
Use: list_forms_by_court("family")

CIVIL COURT
{GOV_UK_BASE}/government/collections/court-and-tribunal-forms#civil-court-forms
Key forms: N1, N244, N215, N161, N461
Use: list_forms_by_court("civil")

LPA / OPG
{GOV_UK_BASE}/government/collections/lasting-power-of-attorney-forms
Key forms: LP1F, LP1H, LP3
Use: list_forms_by_court("lpa")

TRIBUNALS
{GOV_UK_BASE}/government/collections/court-and-tribunal-forms#tribunal-forms

SEARCH FUNCTIONS
- search_court_forms(query) - Search all forms
- get_form(number) - Get specific form
- list_forms_by_court(court) - List forms by jurisdiction

FEES
- get_fee_information() - Fee amounts and exemptions
- Form EX160: Apply for help with fees

ONLINE SERVICES
Some forms can be completed online:
- Divorce: {GOV_UK_BASE}/apply-for-divorce
- Money claims: {GOV_UK_BASE}/make-court-claim-for-money
- LPA: {GOV_UK_BASE}/lasting-power-attorney"""
