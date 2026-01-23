"""
UK Law MCP Server

Gives Claude access to free official UK legal sources:
- legislation.gov.uk (statutes and regulations)
- caselaw.nationalarchives.gov.uk (court judgments 2003+)
- bailii.org (older cases, tribunals)
- judiciary.uk (practice directions, court rules)
- gov.uk (statutory guidance, codes of practice)
- Regulators (CQC, ICO, SRA, BSB, LAA, Ofsted)
- Ombudsman services (LGO, Housing, PHSO, FOS, LeO)
- Planning Inspectorate (appeals, called-in decisions)
- Companies House (company information)
- Land Registry (property data)
- International (EUR-Lex, HUDOC, UK Treaties)
- Parliament (bills, Hansard, committees)
- Court forms (HMCTS forms)
"""

from fastmcp import FastMCP
from typing import Optional

# Core modules
from legislation import search_legislation_api, get_legislation_section, get_legislation_pdf
from caselaw import search_cases_api, get_judgment_api, get_judgment_pdf

# BAILII module
from bailii import (
    search_bailii as bailii_search,
    search_tribunals as bailii_tribunals,
    get_bailii_case as bailii_get_case,
    get_recent_decisions as bailii_recent,
    get_bailii_database_list as bailii_databases,
)

# Court rules module
from court_rules import (
    get_cpr,
    get_fpr,
    get_copr,
    get_tribunal_rules,
    search_rules,
    get_rules_index,
)

# Practice directions module
from practice_directions import (
    get_practice_direction,
    search_practice_directions,
    list_practice_directions,
    get_judiciary_guidance,
    get_court_of_protection_guidance,
)

# Guidance module
from guidance import (
    search_guidance as gov_guidance_search,
    get_guidance as gov_guidance_get,
    get_forms as gov_forms_get,
    get_department_publications,
)

# Codes of practice module
from codes_of_practice import (
    get_mca_code,
    get_dols_guidance,
    get_care_act_guidance,
    get_mha_code,
    get_send_code,
    search_codes,
    list_all_codes,
)

# Regulators module
from regulators import (
    search_cqc,
    get_cqc_report,
    get_cqc_api_info,
    search_ico_guidance,
    get_ico_decisions,
    get_sra_rules,
    search_sra_decisions,
    get_bsb_rules,
    search_laa,
    get_laa_rates,
    search_ofsted,
    get_ofsted_report,
    list_regulators,
)

# Ombudsman module
from ombudsman import (
    search_lgo,
    get_lgo_decision,
    get_lgo_focus_reports,
    search_housing_ombudsman,
    get_housing_ombudsman_decision,
    search_phso,
    get_phso_decision,
    search_financial_ombudsman,
    get_fos_decision,
    search_legal_ombudsman,
    get_leo_decision,
    list_ombudsman_services,
)

# Planning module
from planning import (
    search_planning_appeals,
    get_planning_decision,
    search_sos_planning_decisions,
    search_called_in_decisions,
    get_national_infrastructure,
    get_planning_inspectorate_guidance,
    list_planning_resources,
)

# Secretary of State decisions module
from sos_decisions import (
    search_sos_decisions,
    get_sos_decision,
    search_ministerial_decisions,
    list_departments,
    get_ordinary_residence_decisions,
    get_s117_dispute_guidance,
    get_education_decisions,
    get_dluhc_decisions,
    sos_decisions_index,
)

# Companies House module
from companies_house import (
    search_companies,
    get_company,
    get_company_filings,
    get_officers,
    get_charges,
    get_psc,
    search_disqualified_directors,
    companies_house_api_info,
)

# Land Registry module
from land_registry import (
    search_price_paid,
    get_title_summary,
    search_registered_titles,
    get_inspire_index,
    land_registry_services_index,
    get_ownership_search_options,
)

# International law module
from international import (
    search_eurlex,
    get_eu_legislation,
    search_hudoc,
    get_echr_case,
    get_echr_article_caselaw,
    search_uk_treaties,
    get_uk_treaty,
    international_law_index,
)

# Parliament module
from parliament import (
    search_bills,
    get_bill,
    search_hansard,
    search_committees,
    get_committee_report,
    search_written_questions,
    get_member_info,
    parliament_resources_index,
)

# Forms module
from forms import (
    search_court_forms,
    get_form,
    list_forms_by_court,
    get_fee_information,
    forms_index,
)

mcp = FastMCP("UK Law Research")


# ============================================================
# LEGISLATION (legislation.gov.uk)
# ============================================================

@mcp.tool
def get_legislation(
    act_title: str,
    section: str,
    year: Optional[int] = None
) -> str:
    """
    Fetch a specific section of UK legislation from legislation.gov.uk.

    Args:
        act_title: Name of the Act (e.g., "Mental Capacity Act")
        section: Section number (e.g., "3" or "21A")
        year: Year of the Act (e.g., 2005)

    Example:
        get_legislation("Mental Capacity Act", "3", 2005)
    """
    return get_legislation_section(act_title, section, year)


@mcp.tool
def search_legislation(
    query: str,
    legislation_type: Optional[str] = None
) -> str:
    """
    Search all UK legislation on legislation.gov.uk.

    Args:
        query: Search terms (e.g., "deprivation of liberty")
        legislation_type: Optional - "primary" for Acts, "secondary" for SIs

    Example:
        search_legislation("mental capacity")
    """
    return search_legislation_api(query, legislation_type)


# ============================================================
# CASE LAW - National Archives (2003+)
# ============================================================

@mcp.tool
def search_cases(
    query: str,
    court: Optional[str] = None,
    year: Optional[int] = None,
    party: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> str:
    """
    Search UK case law on caselaw.nationalarchives.gov.uk.

    Args:
        query: Search terms (e.g., "best interests")
        court: Court code (e.g., "ewcop", "uksc", "ewca/civ")
        year: Filter by year (e.g., 2024)
        party: Party name to search for
        from_date: Start date as "YYYY-MM-DD"
        to_date: End date as "YYYY-MM-DD"

    Courts: uksc, ewca/civ, ewca/crim, ewhc, ewcop, ewfc, ukut

    Example:
        search_cases("deprivation of liberty", court="ewcop")
    """
    return search_cases_api(query, court, year, party, from_date, to_date)


@mcp.tool
def get_judgment(citation: str) -> str:
    """
    Fetch a specific judgment by neutral citation.

    Args:
        citation: Neutral citation (e.g., "[2024] EWCOP 15")

    Example:
        get_judgment("[2024] EWCOP 15")
    """
    return get_judgment_api(citation)


# ============================================================
# CASE LAW - BAILII (older cases, tribunals)
# ============================================================

@mcp.tool
def search_bailii(
    query: str,
    database: Optional[str] = None,
    title_only: bool = False
) -> str:
    """
    Search BAILII for UK case law (especially older cases and tribunals).

    Args:
        query: Search terms
        database: Optional filter (e.g., "ewcop", "ukhl", "eat", "mental health tribunal")
        title_only: If True, search case titles only

    Databases: uksc, ukhl, ewca/civ, ewca/crim, ewcop, ewfc, eat, ukut/aac

    Example:
        search_bailii("best interests", database="ewcop")
    """
    return bailii_search(query, database, title_only)


@mcp.tool
def search_tribunal_decisions(
    query: str,
    tribunal: Optional[str] = None,
    year: Optional[int] = None
) -> str:
    """
    Search BAILII specifically for tribunal decisions.

    Args:
        query: Search terms
        tribunal: Tribunal type (e.g., "eat", "aac", "iac", "mental health")
        year: Optional year filter

    Tribunals: eat, aac, iac, lc, tax, grc, mental health

    Example:
        search_tribunal_decisions("disability discrimination", tribunal="eat")
    """
    return bailii_tribunals(query, tribunal, year)


@mcp.tool
def get_bailii_case(citation: str) -> str:
    """
    Get BAILII case by neutral citation.

    Best for older cases (pre-2003) and tribunal decisions.

    Args:
        citation: Neutral citation (e.g., "[1999] UKHL 30")

    Example:
        get_bailii_case("[1999] UKHL 30")
    """
    return bailii_get_case(citation)


# ============================================================
# COURT RULES (justice.gov.uk)
# ============================================================

@mcp.tool
def get_civil_procedure_rules(part: str, rule: Optional[str] = None) -> str:
    """
    Get Civil Procedure Rules (CPR).

    Args:
        part: CPR Part number (e.g., "24", "54")
        rule: Optional specific rule

    Example:
        get_civil_procedure_rules("54")  # Judicial Review
    """
    return get_cpr(part, rule)


@mcp.tool
def get_family_procedure_rules(part: str, rule: Optional[str] = None) -> str:
    """
    Get Family Procedure Rules (FPR).

    Args:
        part: FPR Part number (e.g., "12", "29")
        rule: Optional specific rule

    Example:
        get_family_procedure_rules("12")  # Children proceedings
    """
    return get_fpr(part, rule)


@mcp.tool
def get_cop_rules(part: str, rule: Optional[str] = None) -> str:
    """
    Get Court of Protection Rules 2017.

    Args:
        part: COPR Part number (e.g., "1", "10", "14")
        rule: Optional specific rule

    Example:
        get_cop_rules("10")  # Applications within proceedings
    """
    return get_copr(part, rule)


@mcp.tool
def get_tribunal_procedure_rules(tribunal: str, part: Optional[str] = None) -> str:
    """
    Get Tribunal Procedure Rules.

    Args:
        tribunal: Tribunal code (e.g., "grc", "iac", "hesc", "ut-aac")
        part: Optional part number

    Example:
        get_tribunal_procedure_rules("hesc")  # Health, Education and Social Care
    """
    return get_tribunal_rules(tribunal, part)


@mcp.tool
def search_court_rules(query: str, ruleset: Optional[str] = None) -> str:
    """
    Search across court procedure rules.

    Args:
        query: Search terms (e.g., "service", "permission")
        ruleset: Optional ruleset ("cpr", "fpr", "copr", "tribunal")

    Example:
        search_court_rules("permission", ruleset="copr")
    """
    return search_rules(query, ruleset)


# ============================================================
# PRACTICE DIRECTIONS (judiciary.uk)
# ============================================================

@mcp.tool
def get_practice_direction_link(pd_number: str, court: Optional[str] = None) -> str:
    """
    Get a specific Practice Direction.

    Args:
        pd_number: Practice Direction number (e.g., "10aa", "35", "12j")
        court: Court type ("cop", "cpr", "fpr") - optional

    CoP Practice Directions: 1a, 2a, 4b, 9e, 9f, 10aa, 10b, 14a, 14e, 15a, 17a

    Example:
        get_practice_direction_link("10aa", court="cop")
    """
    return get_practice_direction(pd_number, court)


@mcp.tool
def search_practice_directions_all(query: str) -> str:
    """
    Search Practice Directions across all courts.

    Args:
        query: Search terms (e.g., "experts", "bundles")

    Example:
        search_practice_directions_all("experts")
    """
    return search_practice_directions(query)


# ============================================================
# STATUTORY GUIDANCE (gov.uk)
# ============================================================

@mcp.tool
def search_gov_guidance(query: str, department: Optional[str] = None) -> str:
    """
    Search gov.uk for statutory guidance.

    Args:
        query: Search terms (e.g., "mental capacity", "safeguarding")
        department: Optional department (e.g., "moj", "dhsc", "dfe")

    Example:
        search_gov_guidance("mental capacity", department="moj")
    """
    return gov_guidance_search(query, department)


@mcp.tool
def get_statutory_guidance(name: str) -> str:
    """
    Get direct link to a statutory guidance document.

    Args:
        name: Guidance name (e.g., "mca code", "care act guidance", "dols")

    Available:
        - mca code: Mental Capacity Act Code
        - dols code: DoLS Code of Practice
        - care act guidance: Care Act 2014 Guidance
        - mha code: Mental Health Act Code
        - working together: Safeguarding Children
        - send code: SEND Code of Practice

    Example:
        get_statutory_guidance("mca code")
    """
    return gov_guidance_get(name)


# ============================================================
# CODES OF PRACTICE
# ============================================================

@mcp.tool
def get_mca_code_of_practice(chapter: Optional[str] = None) -> str:
    """
    Get the Mental Capacity Act Code of Practice.

    Args:
        chapter: Optional chapter number (1-16)

    Example:
        get_mca_code_of_practice("5")  # Best interests
    """
    return get_mca_code(chapter)


@mcp.tool
def get_dols_code_of_practice() -> str:
    """
    Get Deprivation of Liberty Safeguards guidance.

    Returns DoLS Code of Practice and related resources.
    """
    return get_dols_guidance()


@mcp.tool
def get_care_act_statutory_guidance(chapter: Optional[str] = None) -> str:
    """
    Get Care Act 2014 statutory guidance.

    Args:
        chapter: Optional chapter number (1-23)

    Example:
        get_care_act_statutory_guidance("17")  # Ordinary residence
    """
    return get_care_act_guidance(chapter)


@mcp.tool
def get_mha_code_of_practice(chapter: Optional[str] = None) -> str:
    """
    Get Mental Health Act 1983 Code of Practice.

    Args:
        chapter: Optional chapter number (1-34)

    Example:
        get_mha_code_of_practice("22")  # After-care
    """
    return get_mha_code(chapter)


@mcp.tool
def search_codes_of_practice(query: str) -> str:
    """
    Search across all codes of practice.

    Args:
        query: Search terms (e.g., "best interests", "capacity")

    Example:
        search_codes_of_practice("safeguarding")
    """
    return search_codes(query)


# ============================================================
# REGULATORS
# ============================================================

@mcp.tool
def search_cqc_providers(provider_name: str, location: Optional[str] = None) -> str:
    """
    Search CQC for care provider inspection reports.

    Args:
        provider_name: Name of the provider
        location: Optional location filter

    Example:
        search_cqc_providers("Sunrise Care Home", location="London")
    """
    return search_cqc(provider_name, location)


@mcp.tool
def get_cqc_provider_report(provider_id: str) -> str:
    """
    Get a specific CQC inspection report.

    Args:
        provider_id: CQC location ID (e.g., "1-123456789")

    Example:
        get_cqc_provider_report("1-123456789")
    """
    return get_cqc_report(provider_id)


@mcp.tool
def search_ico(query: str) -> str:
    """
    Search ICO for data protection guidance.

    Args:
        query: Search terms (e.g., "subject access request", "GDPR")

    Example:
        search_ico("subject access request")
    """
    return search_ico_guidance(query)


@mcp.tool
def get_sra_standards(section: Optional[str] = None) -> str:
    """
    Get SRA Standards and Regulations.

    Args:
        section: Optional section ("code", "accounts", "transparency")

    Example:
        get_sra_standards("code")
    """
    return get_sra_rules(section)


@mcp.tool
def get_bsb_handbook(section: Optional[str] = None) -> str:
    """
    Get Bar Standards Board rules and guidance.

    Args:
        section: Optional section ("conduct", "equality")

    Example:
        get_bsb_handbook()
    """
    return get_bsb_rules(section)


@mcp.tool
def search_legal_aid_guidance(query: str) -> str:
    """
    Search Legal Aid Agency guidance.

    Args:
        query: Search terms (e.g., "means test", "exceptional funding")

    Example:
        search_legal_aid_guidance("exceptional case funding")
    """
    return search_laa(query)


@mcp.tool
def search_ofsted_reports(provider_name: str, location: Optional[str] = None) -> str:
    """
    Search Ofsted inspection reports.

    Args:
        provider_name: Name of school, nursery, children's home, etc.
        location: Optional location filter

    Example:
        search_ofsted_reports("Oak Primary School")
    """
    return search_ofsted(provider_name, location)


# ============================================================
# OMBUDSMAN SERVICES
# ============================================================

@mcp.tool
def search_lgo_decisions(
    query: str,
    council: Optional[str] = None,
    category: Optional[str] = None
) -> str:
    """
    Search Local Government Ombudsman decisions.

    Args:
        query: Search terms (e.g., "care assessment")
        council: Optional council name
        category: Optional category (e.g., "adult care services", "housing")

    Example:
        search_lgo_decisions("safeguarding", category="adult care services")
    """
    return search_lgo(query, council, category)


@mcp.tool
def search_housing_ombudsman_decisions(query: str) -> str:
    """
    Search Housing Ombudsman decisions.

    Args:
        query: Search terms (e.g., "repairs", "damp")

    Example:
        search_housing_ombudsman_decisions("repairs delay")
    """
    return search_housing_ombudsman(query)


@mcp.tool
def search_phso_decisions(query: str) -> str:
    """
    Search Parliamentary and Health Service Ombudsman decisions.

    Args:
        query: Search terms (e.g., "NHS", "DWP")

    Example:
        search_phso_decisions("hospital discharge")
    """
    return search_phso(query)


@mcp.tool
def search_financial_ombudsman_decisions(
    query: str,
    firm: Optional[str] = None
) -> str:
    """
    Search Financial Ombudsman Service decisions.

    Args:
        query: Search terms (e.g., "PPI", "mortgage")
        firm: Optional firm name filter

    Example:
        search_financial_ombudsman_decisions("insurance claim")
    """
    return search_financial_ombudsman(query, firm)


@mcp.tool
def search_legal_ombudsman_info(query: str) -> str:
    """
    Search Legal Ombudsman information.

    Args:
        query: Search terms (e.g., "costs", "delay")

    Example:
        search_legal_ombudsman_info("poor communication")
    """
    return search_legal_ombudsman(query)


# ============================================================
# PLANNING
# ============================================================

@mcp.tool
def search_planning_appeal_decisions(
    query: str,
    location: Optional[str] = None,
    appeal_type: Optional[str] = None
) -> str:
    """
    Search Planning Inspectorate appeal decisions.

    Args:
        query: Search terms (e.g., "green belt")
        location: Optional location filter
        appeal_type: Optional type (householder, enforcement, etc.)

    Example:
        search_planning_appeal_decisions("green belt", location="Surrey")
    """
    return search_planning_appeals(query, location, appeal_type)


@mcp.tool
def get_planning_appeal_decision(reference: str) -> str:
    """
    Get a specific planning appeal decision.

    Args:
        reference: PINS appeal reference (e.g., "APP/X1234/W/23/1234567")

    Example:
        get_planning_appeal_decision("APP/X1234/W/23/1234567")
    """
    return get_planning_decision(reference)


@mcp.tool
def search_called_in_planning_decisions(query: str) -> str:
    """
    Search called-in planning application decisions.

    Args:
        query: Search terms (development name, location)

    Example:
        search_called_in_planning_decisions("London")
    """
    return search_called_in_decisions(query)


# ============================================================
# SECRETARY OF STATE DECISIONS
# ============================================================

@mcp.tool
def search_sos_determinations(query: str, department: Optional[str] = None) -> str:
    """
    Search Secretary of State determinations.

    Args:
        query: Search terms (e.g., "ordinary residence")
        department: Optional department (dhsc, dfe, dluhc, moj, ho)

    Example:
        search_sos_determinations("ordinary residence", department="dhsc")
    """
    return search_sos_decisions(query, department)


@mcp.tool
def get_ordinary_residence_guidance() -> str:
    """
    Get information about ordinary residence dispute determinations.

    Returns guidance on Care Act and s.117 OR disputes.
    """
    return get_ordinary_residence_decisions()


@mcp.tool
def get_s117_guidance() -> str:
    """
    Get guidance on s.117 MHA aftercare disputes.

    Returns s.117 responsibility dispute guidance.
    """
    return get_s117_dispute_guidance()


# ============================================================
# COMPANIES HOUSE
# ============================================================

@mcp.tool
def search_companies_house(query: str) -> str:
    """
    Search Companies House for companies.

    Args:
        query: Company name or number

    Example:
        search_companies_house("Acme Ltd")
    """
    return search_companies(query)


@mcp.tool
def get_company_info(company_number: str) -> str:
    """
    Get company details by company number.

    Args:
        company_number: 8-character company number

    Example:
        get_company_info("12345678")
    """
    return get_company(company_number)


@mcp.tool
def get_company_officers(company_number: str) -> str:
    """
    Get company officers (directors, secretaries).

    Args:
        company_number: Company number

    Example:
        get_company_officers("12345678")
    """
    return get_officers(company_number)


@mcp.tool
def get_company_charges(company_number: str) -> str:
    """
    Get company charges (mortgages, debentures).

    Args:
        company_number: Company number

    Example:
        get_company_charges("12345678")
    """
    return get_charges(company_number)


@mcp.tool
def get_company_psc(company_number: str) -> str:
    """
    Get persons with significant control (PSC).

    Args:
        company_number: Company number

    Example:
        get_company_psc("12345678")
    """
    return get_psc(company_number)


# ============================================================
# LAND REGISTRY
# ============================================================

@mcp.tool
def search_land_registry_prices(
    postcode: Optional[str] = None,
    street: Optional[str] = None,
    town: Optional[str] = None
) -> str:
    """
    Search Land Registry Price Paid Data.

    Args:
        postcode: Full or partial postcode
        street: Street name
        town: Town or city name

    Example:
        search_land_registry_prices(postcode="SW1A")
    """
    return search_price_paid(postcode, street, town)


@mcp.tool
def get_land_registry_title_info(title_number: str) -> str:
    """
    Get Land Registry title information guidance.

    Args:
        title_number: Title number (e.g., "DN123456")

    Example:
        get_land_registry_title_info("DN123456")
    """
    return get_title_summary(title_number)


# ============================================================
# INTERNATIONAL LAW
# ============================================================

@mcp.tool
def search_eu_law(query: str) -> str:
    """
    Search EUR-Lex for EU law.

    Args:
        query: Search terms

    Example:
        search_eu_law("data protection")
    """
    return search_eurlex(query)


@mcp.tool
def search_echr_cases(
    query: str,
    article: Optional[str] = None,
    respondent: Optional[str] = None
) -> str:
    """
    Search HUDOC for ECHR case law.

    Args:
        query: Search terms or case name
        article: Optional ECHR article number
        respondent: Optional respondent state

    Example:
        search_echr_cases("deprivation of liberty", article="5")
    """
    return search_hudoc(query, article, respondent)


@mcp.tool
def get_echr_case_by_application(application_number: str) -> str:
    """
    Get ECHR case by application number.

    Args:
        application_number: Application number (e.g., "12345/67")

    Example:
        get_echr_case_by_application("12345/67")
    """
    return get_echr_case(application_number)


@mcp.tool
def search_treaties(query: str) -> str:
    """
    Search UK treaties database.

    Args:
        query: Search terms or treaty name

    Example:
        search_treaties("extradition")
    """
    return search_uk_treaties(query)


# ============================================================
# PARLIAMENT
# ============================================================

@mcp.tool
def search_parliament_bills(
    query: str,
    session: Optional[str] = None,
    status: Optional[str] = None
) -> str:
    """
    Search current and past parliamentary bills.

    Args:
        query: Search terms or bill title
        session: Parliamentary session (e.g., "2023-24")
        status: Bill status ("current", "enacted", "failed")

    Example:
        search_parliament_bills("mental health")
    """
    return search_bills(query, session, status)


@mcp.tool
def get_parliament_bill(bill_id: str) -> str:
    """
    Get specific bill details and progress.

    Args:
        bill_id: Bill ID or short title

    Example:
        get_parliament_bill("mental-health-bill")
    """
    return get_bill(bill_id)


@mcp.tool
def search_hansard_debates(
    query: str,
    house: Optional[str] = None,
    member: Optional[str] = None
) -> str:
    """
    Search Hansard parliamentary debates.

    Args:
        query: Search terms
        house: Optional "Commons" or "Lords"
        member: Optional MP/Lord name

    Example:
        search_hansard_debates("mental capacity", house="Lords")
    """
    return search_hansard(query, house=house, member=member)


@mcp.tool
def search_parliament_committees(query: str, committee: Optional[str] = None) -> str:
    """
    Search parliamentary committee reports.

    Args:
        query: Search terms
        committee: Optional committee name

    Example:
        search_parliament_committees("social care")
    """
    return search_committees(query, committee)


@mcp.tool
def search_written_questions_answers(
    query: str,
    department: Optional[str] = None
) -> str:
    """
    Search parliamentary written questions and answers.

    Args:
        query: Search terms
        department: Optional government department

    Example:
        search_written_questions_answers("legal aid", department="Ministry of Justice")
    """
    return search_written_questions(query, department)


# ============================================================
# COURT FORMS
# ============================================================

@mcp.tool
def search_forms(query: str, court: Optional[str] = None) -> str:
    """
    Search for court forms.

    Args:
        query: Search terms (form number or description)
        court: Optional court ("cop", "family", "civil", "lpa")

    Example:
        search_forms("COP1")
    """
    return search_court_forms(query, court)


@mcp.tool
def get_court_form(form_number: str) -> str:
    """
    Get specific form details and download link.

    Args:
        form_number: Form number (e.g., "COP1", "N244", "C100")

    Example:
        get_court_form("COP1")
    """
    return get_form(form_number)


@mcp.tool
def list_court_forms(court: str) -> str:
    """
    List all forms for a specific court.

    Args:
        court: Court type ("cop", "family", "civil", "lpa")

    Example:
        list_court_forms("cop")
    """
    return list_forms_by_court(court)


@mcp.tool
def get_court_fees() -> str:
    """
    Get court fee information.

    Returns fee amounts and exemption information.
    """
    return get_fee_information()


# ============================================================
# INDEX FUNCTIONS
# ============================================================

@mcp.tool
def get_all_resources_index() -> str:
    """
    Get a complete index of all UK law resources available.

    Returns comprehensive guide to all legal sources.
    """
    return """UK Law MCP - Complete Resource Index

LEGISLATION
- search_legislation(query) - Search legislation.gov.uk
- get_legislation(act, section, year) - Get specific section

CASE LAW
- search_cases(query, court, year) - National Archives (2003+)
- get_judgment(citation) - Get case by citation
- search_bailii(query, database) - BAILII (older cases, tribunals)

COURT RULES
- get_civil_procedure_rules(part) - CPR
- get_family_procedure_rules(part) - FPR
- get_cop_rules(part) - Court of Protection Rules
- get_tribunal_procedure_rules(tribunal) - Tribunal rules

PRACTICE DIRECTIONS
- get_practice_direction_link(pd_number, court)
- search_practice_directions_all(query)

CODES OF PRACTICE
- get_mca_code_of_practice(chapter)
- get_dols_code_of_practice()
- get_care_act_statutory_guidance(chapter)
- get_mha_code_of_practice(chapter)

REGULATORS
- search_cqc_providers(name) - Care Quality Commission
- search_ico(query) - Information Commissioner
- get_sra_standards() - Solicitors Regulation Authority
- get_bsb_handbook() - Bar Standards Board
- search_ofsted_reports(name) - Ofsted

OMBUDSMAN
- search_lgo_decisions(query) - Local Government Ombudsman
- search_housing_ombudsman_decisions(query)
- search_phso_decisions(query) - Health Service Ombudsman
- search_financial_ombudsman_decisions(query)
- search_legal_ombudsman_info(query)

PLANNING
- search_planning_appeal_decisions(query)
- search_called_in_planning_decisions(query)

COMPANIES & LAND
- search_companies_house(query)
- get_company_info(number)
- search_land_registry_prices(postcode)

INTERNATIONAL
- search_eu_law(query) - EUR-Lex
- search_echr_cases(query, article) - HUDOC
- search_treaties(query)

PARLIAMENT
- search_parliament_bills(query)
- search_hansard_debates(query)
- search_parliament_committees(query)

FORMS
- search_forms(query)
- get_court_form(number)
- list_court_forms(court)
- get_court_fees()"""


if __name__ == "__main__":
    mcp.run()
