"""
Parliament Module

Connects to UK Parliament APIs:
- Bills (current and past)
- Hansard (parliamentary debates)
- Committees (reports and evidence)
- Written Questions and Statements
"""

import httpx
from typing import Optional
from urllib.parse import quote, urlencode

HEADERS = {
    "User-Agent": "UK-Law-MCP/1.0 (Legal Research Tool)",
    "Accept": "application/json"
}

# Parliament API endpoints
BILLS_API = "https://bills-api.parliament.uk"
BILLS_WEB = "https://bills.parliament.uk"
HANSARD_WEB = "https://hansard.parliament.uk"
COMMITTEES_WEB = "https://committees.parliament.uk"
QUESTIONS_WEB = "https://questions-statements.parliament.uk"
PARLIAMENT_WEB = "https://www.parliament.uk"
MEMBERS_API = "https://members-api.parliament.uk"


def search_bills(query: str, session: Optional[str] = None, status: Optional[str] = None) -> str:
    """
    Search current and past parliamentary bills.

    Args:
        query: Search terms or bill title
        session: Parliamentary session (e.g., "2023-24")
        status: Bill status (e.g., "current", "enacted", "failed")

    Returns:
        Search URL and bill information
    """
    params = {"q": query}
    if session:
        params["session"] = session
    if status:
        params["status"] = status

    search_url = f"{BILLS_WEB}/bills?{urlencode(params)}"
    api_url = f"{BILLS_API}/api/v1/Bills?SearchTerm={quote(query)}"

    result = f"""UK Parliament Bills Search

Web search: {search_url}
API: {api_url}

Searching for: {query}"""

    if session:
        result += f"\nSession: {session}"
    if status:
        result += f"\nStatus: {status}"

    result += f"""

Bill types:
- Government Bills (introduced by Ministers)
- Private Members' Bills (introduced by backbenchers)
- Private Bills (affecting specific persons/bodies)
- Hybrid Bills (mix of public and private)

Bill stages:
1. First Reading (formal introduction)
2. Second Reading (principle debate)
3. Committee Stage (detailed examination)
4. Report Stage (amendments)
5. Third Reading (final debate)
6. Same stages in the other House
7. Royal Assent (becomes Act)

Bill status:
- Current: Progressing through Parliament
- Enacted: Received Royal Assent (now an Act)
- Failed: Did not complete passage
- Withdrawn: Removed by sponsor

Bills API documentation:
{BILLS_API}/index.html

For Acts (passed legislation):
https://www.legislation.gov.uk"""

    return result


def get_bill(bill_id: str) -> str:
    """
    Get specific bill details and progress.

    Args:
        bill_id: Bill ID or short title

    Returns:
        Bill information and links
    """
    # Try to construct bill URL
    bill_url = f"{BILLS_WEB}/bills/{quote(bill_id.lower().replace(' ', '-'))}"

    return f"""Parliament Bill

Searching for: {bill_id}

Bill page: {bill_url}

If the URL doesn't work, search at: {BILLS_WEB}/bills

Bill page includes:
- Bill status and current stage
- Bill documents (as introduced, as amended)
- Explanatory notes
- Impact assessments
- Committee reports
- Hansard debates
- Voting records

For bill documents:
{BILLS_WEB} > Select bill > Documents

For debates on the bill:
{HANSARD_WEB} > Search for bill name

For committee consideration:
{COMMITTEES_WEB} > Search for bill name

Amendment papers:
Published during Committee and Report stages."""


def search_hansard(
    query: str,
    date: Optional[str] = None,
    house: Optional[str] = None,
    member: Optional[str] = None
) -> str:
    """
    Search Hansard parliamentary debates.

    Args:
        query: Search terms
        date: Optional date or date range (YYYY-MM-DD)
        house: Optional "Commons" or "Lords"
        member: Optional MP/Lord name

    Returns:
        Search URL and guidance
    """
    params = {"query": query}
    if house:
        params["house"] = house
    if member:
        params["member"] = member

    search_url = f"{HANSARD_WEB}/search?{urlencode(params)}"

    result = f"""Hansard - Parliamentary Debates

Search: {search_url}

Searching for: {query}"""

    if date:
        result += f"\nDate: {date}"
    if house:
        result += f"\nHouse: {house}"
    if member:
        result += f"\nMember: {member}"

    result += f"""

Hansard contains:
- Debates in the Chamber
- Westminster Hall debates
- Grand Committee (Lords)
- Written Statements
- Written Answers
- Petitions

Debate types:
- Main Chamber debates
- Westminster Hall (adjournment debates)
- Opposition Day debates
- Backbench Business debates
- Urgent Questions
- Points of Order
- Ministerial Statements

Uses in legal research:
- Pepper v Hart [1993]: Parliamentary statements may be used
  to interpret ambiguous legislation if:
  - Clear statement by promoter
  - On the mischief or purpose of provision
  - Legislation remains ambiguous

Search tips:
- Use quotes for exact phrases
- Use MP/Lord name for their contributions
- Filter by date range
- Filter by House

Historical Hansard (pre-2010):
{HANSARD_WEB}/historic-hansard"""

    return result


def search_committees(
    query: str,
    committee: Optional[str] = None,
    report_type: Optional[str] = None
) -> str:
    """
    Search parliamentary committee reports and evidence.

    Args:
        query: Search terms
        committee: Optional committee name
        report_type: Optional "report", "evidence", "inquiry"

    Returns:
        Search URL and guidance
    """
    params = {"query": query}
    if committee:
        params["committee"] = committee

    search_url = f"{COMMITTEES_WEB}/search/?{urlencode(params)}"

    result = f"""Parliamentary Committees

Search: {search_url}

Searching for: {query}"""

    if committee:
        result += f"\nCommittee: {committee}"

    result += f"""

Committee types:
- Select Committees (scrutinise government)
- Public Bill Committees (examine bills)
- Joint Committees (both Houses)

Key Select Committees:
Commons:
- Health and Social Care Committee
- Justice Committee
- Home Affairs Committee
- Education Committee
- Work and Pensions Committee
- Housing, Communities and Local Government Committee
- Public Accounts Committee

Lords:
- Constitution Committee
- Delegated Powers Committee
- Secondary Legislation Scrutiny Committee

Committee outputs:
- Inquiry reports
- Oral evidence transcripts
- Written evidence submissions
- Government responses
- Special reports

Reports database:
{COMMITTEES_WEB}

Using committee reports:
- Evidence of policy intent
- Expert views on legislation
- Government commitments on implementation
- Scrutiny of secondary legislation"""

    return result


def get_committee_report(committee: str, inquiry: Optional[str] = None) -> str:
    """
    Get committee reports.

    Args:
        committee: Committee name
        inquiry: Optional inquiry name

    Returns:
        Link to committee page
    """
    # Slugify committee name
    slug = committee.lower().replace(" ", "-").replace("'", "")

    committee_url = f"{COMMITTEES_WEB}/committee/{slug}"

    result = f"""Parliamentary Committee

Committee: {committee}
Committee page: {committee_url}

"""
    if inquiry:
        result += f"Inquiry: {inquiry}\n"
        result += f"Search inquiries on the committee page.\n\n"

    result += f"""Committee page includes:
- Current inquiries
- Recent reports
- Oral evidence sessions
- Written evidence
- Government responses

To find specific reports:
{COMMITTEES_WEB} > Select committee > Publications

For pre-legislative scrutiny:
Draft bills are often examined by select committees before
formal introduction."""

    return result


def search_written_questions(
    query: str,
    department: Optional[str] = None,
    member: Optional[str] = None
) -> str:
    """
    Search parliamentary written questions and answers.

    Args:
        query: Search terms
        department: Optional government department
        member: Optional MP/Lord name

    Returns:
        Search URL
    """
    params = {"SearchTerm": query}
    if department:
        params["Department"] = department
    if member:
        params["Member"] = member

    search_url = f"{QUESTIONS_WEB}/written-questions?{urlencode(params)}"

    return f"""Parliamentary Written Questions

Search: {search_url}

Searching for: {query}

Written Questions:
- Named Day Questions: Answer due by specific date
- Ordinary Questions: Answer due within 7 days
- Priority Questions (Lords): Answer due within 10 days

Departments:
Search by answering department to find policy positions.

Uses:
- Government policy statements
- Statistical information
- Explanation of government position
- Commitments on implementation

Written Statements:
{QUESTIONS_WEB}/written-statements
Ministerial announcements to Parliament.

Oral Questions:
{HANSARD_WEB}
Recorded in Hansard debates."""


def get_member_info(member_name: str) -> str:
    """
    Get information about an MP or Lord.

    Args:
        member_name: Name of MP or Lord

    Returns:
        Search URL and member lookup
    """
    search_url = f"https://members.parliament.uk/members/search?query={quote(member_name)}"

    return f"""Parliament Member Search

Search: {search_url}

Searching for: {member_name}

Member pages include:
- Constituency (MPs)
- Party
- Contact information
- Registered interests
- Voting record
- Spoken contributions (Hansard)
- Written questions asked
- Bills sponsored

Members' Interests:
https://members.parliament.uk/members/interests

Voting Records:
https://votes.parliament.uk

MPs by constituency:
https://members.parliament.uk/members/Commons

Lords by name:
https://members.parliament.uk/members/Lords"""


def parliament_resources_index() -> str:
    """
    Index of all Parliament resources.

    Returns:
        Comprehensive index
    """
    return f"""UK Parliament Resources Index

BILLS
Website: {BILLS_WEB}
API: {BILLS_API}
Use: search_bills(), get_bill()
- Current and past bills
- Bill documents
- Progress tracker

HANSARD (Debates)
Website: {HANSARD_WEB}
Use: search_hansard()
- Chamber debates
- Westminster Hall
- Written statements
- Historical debates

COMMITTEES
Website: {COMMITTEES_WEB}
Use: search_committees(), get_committee_report()
- Select Committee reports
- Inquiry evidence
- Government responses

WRITTEN QUESTIONS
Website: {QUESTIONS_WEB}
Use: search_written_questions()
- Questions and answers
- Written statements

MEMBERS
Website: https://members.parliament.uk
Use: get_member_info()
- MP and Lord information
- Voting records
- Registered interests

LEGISLATION TRACKING
For bill to Act:
1. {BILLS_WEB} - Bill progress
2. {HANSARD_WEB} - Debates
3. {COMMITTEES_WEB} - Committee stage
4. https://www.legislation.gov.uk - Final Act

SECONDARY LEGISLATION
Joint Committee on Statutory Instruments:
{COMMITTEES_WEB}/committee/joint-committee-on-statutory-instruments

Lords Secondary Legislation Scrutiny Committee:
{COMMITTEES_WEB}/committee/secondary-legislation-scrutiny-committee

PARLIAMENT LIVE
Watch debates live:
https://parliamentlive.tv

RESEARCH BRIEFINGS
Commons Library research:
https://commonslibrary.parliament.uk
- Bill briefings
- Topical research
- Statistics

Lords Library research:
https://lordslibrary.parliament.uk"""
