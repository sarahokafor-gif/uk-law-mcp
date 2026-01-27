# UK Law MCP Server

A comprehensive Model Context Protocol server providing AI assistants with access to free official UK legal sources. Built for legal research, case preparation, and practice management.

## Features

- **60+ research tools** covering legislation, case law, court rules, guidance, and more
- **Free official sources only** - no paywalled databases required
- **Designed for legal practice** - Court of Protection, Family, Civil, and Tribunal work

## Data Sources

| Source | Coverage |
|--------|----------|
| legislation.gov.uk | All UK statutes, SIs, regulations |
| caselaw.nationalarchives.gov.uk | Court judgments 2003+ |
| bailii.org | Older cases, tribunals, House of Lords |
| justice.gov.uk | CPR, FPR, COPR, Tribunal Rules |
| judiciary.uk | Practice Directions |
| gov.uk | Statutory guidance, codes of practice |
| CQC, Ofsted | Inspection reports |
| ICO | Data protection guidance |
| SRA, BSB | Professional regulation |
| Ombudsman services | LGO, Housing, PHSO, FOS, Legal |
| Planning Inspectorate | Appeals, called-in decisions |
| Companies House | Company information |
| Land Registry | Property data (Price Paid) |
| EUR-Lex, HUDOC | EU law, ECHR case law |
| Parliament | Bills, Hansard, committees |
| HMCTS | Court forms |

## Tools Reference

### Legislation

| Tool | Description |
|------|-------------|
| `get_legislation` | Fetch specific statute section |
| `search_legislation` | Search all UK legislation |

### Case Law - National Archives (2003+)

| Tool | Description |
|------|-------------|
| `search_cases` | Search court judgments with filters |
| `get_judgment` | Fetch case by neutral citation |

### Case Law - BAILII (older cases, tribunals)

| Tool | Description |
|------|-------------|
| `search_bailii` | Search BAILII databases |
| `search_tribunal_decisions` | Search tribunal decisions |
| `get_bailii_case` | Get case by citation |

### Court Rules

| Tool | Description |
|------|-------------|
| `get_civil_procedure_rules` | Get CPR part/rule |
| `get_family_procedure_rules` | Get FPR part/rule |
| `get_cop_rules` | Get COPR 2017 part/rule |
| `get_tribunal_procedure_rules` | Get Tribunal rules |
| `search_court_rules` | Search across all rulesets |

### Practice Directions

| Tool | Description |
|------|-------------|
| `get_practice_direction_link` | Get specific PD |
| `search_practice_directions_all` | Search all PDs |

### Statutory Guidance

| Tool | Description |
|------|-------------|
| `search_gov_guidance` | Search gov.uk guidance |
| `get_statutory_guidance` | Get specific guidance document |

### Codes of Practice

| Tool | Description |
|------|-------------|
| `get_mca_code_of_practice` | Mental Capacity Act Code |
| `get_dols_code_of_practice` | DoLS Code of Practice |
| `get_care_act_statutory_guidance` | Care Act 2014 guidance |
| `get_mha_code_of_practice` | Mental Health Act Code |
| `search_codes_of_practice` | Search all codes |

### Regulators

| Tool | Description |
|------|-------------|
| `search_cqc_providers` | Search CQC inspection reports |
| `get_cqc_provider_report` | Get specific CQC report |
| `search_ico` | Search ICO guidance |
| `get_sra_standards` | SRA Standards and Regulations |
| `get_bsb_handbook` | BSB rules and guidance |
| `search_legal_aid_guidance` | Search LAA guidance |
| `search_ofsted_reports` | Search Ofsted reports |

### Ombudsman Services

| Tool | Description |
|------|-------------|
| `search_lgo_decisions` | Local Government Ombudsman |
| `search_housing_ombudsman_decisions` | Housing Ombudsman |
| `search_phso_decisions` | Parliamentary & Health Service Ombudsman |
| `search_financial_ombudsman_decisions` | Financial Ombudsman |
| `search_legal_ombudsman_info` | Legal Ombudsman |

### Planning

| Tool | Description |
|------|-------------|
| `search_planning_appeal_decisions` | Search PINS appeals |
| `get_planning_appeal_decision` | Get specific appeal decision |
| `search_called_in_planning_decisions` | Search called-in applications |

### Secretary of State Decisions

| Tool | Description |
|------|-------------|
| `search_sos_determinations` | Search SoS determinations |
| `get_ordinary_residence_guidance` | OR dispute guidance |
| `get_s117_guidance` | s.117 MHA dispute guidance |

### Companies House

| Tool | Description |
|------|-------------|
| `search_companies_house` | Search companies |
| `get_company_info` | Company details |
| `get_company_officers` | Directors and secretaries |
| `get_company_charges` | Mortgages and debentures |
| `get_company_psc` | Persons with significant control |

### Land Registry

| Tool | Description |
|------|-------------|
| `search_land_registry_prices` | Price Paid data |
| `get_land_registry_title_info` | Title information guidance |

### International Law

| Tool | Description |
|------|-------------|
| `search_eu_law` | Search EUR-Lex |
| `search_echr_cases` | Search HUDOC |
| `get_echr_case_by_application` | Get ECHR case |
| `search_treaties` | Search UK treaties |

### Parliament

| Tool | Description |
|------|-------------|
| `search_parliament_bills` | Search bills |
| `get_parliament_bill` | Get bill details |
| `search_hansard_debates` | Search Hansard |
| `search_parliament_committees` | Search committee reports |
| `search_written_questions_answers` | Written questions |

### Court Forms

| Tool | Description |
|------|-------------|
| `search_forms` | Search court forms |
| `get_court_form` | Get form details and link |
| `list_court_forms` | List forms by court type |
| `get_court_fees` | Fee information |

### Index

| Tool | Description |
|------|-------------|
| `get_all_resources_index` | Complete resource guide |

## Courts Covered

- Supreme Court (UKSC)
- Court of Appeal (EWCA Civ, EWCA Crim)
- High Court (EWHC - all divisions)
- Court of Protection (EWCOP)
- Family Court (EWFC)
- Upper Tribunal (UKUT)
- First-tier Tribunal (UKFTT)
- Employment Appeal Tribunal (EAT)
- House of Lords (historical - UKHL)

## Installation

```bash
git clone https://github.com/sarahokafor-gif/uk-law-mcp.git
cd uk-law-mcp
pip install -r requirements.txt
```

Or with uv:

```bash
uv pip install -r requirements.txt
```

## Usage

### As MCP Server

```bash
python src/server.py
```

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "uk-law": {
      "command": "python",
      "args": ["/path/to/uk-law-mcp/src/server.py"]
    }
  }
}
```

### Claude Code Configuration

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "uk-law": {
      "command": "python",
      "args": ["/path/to/uk-law-mcp/src/server.py"]
    }
  }
}
```

## Example Queries

```
# Search for Court of Protection cases on best interests
search_cases("best interests", court="ewcop", year=2024)

# Get Mental Capacity Act section 4
get_legislation("Mental Capacity Act", "4", 2005)

# Search BAILII for older tribunal decisions
search_tribunal_decisions("disability discrimination", tribunal="eat")

# Get Care Act statutory guidance on safeguarding
get_care_act_statutory_guidance("14")

# Search CQC for care home reports
search_cqc_providers("Sunrise Care Home", location="London")

# Get Court of Protection Rules Part 10
get_cop_rules("10")

# Search for ECHR Article 5 cases
search_echr_cases("deprivation of liberty", article="5")
```

## Requirements

- Python 3.10+
- httpx
- fastmcp

## Author

Sarah Okafor - Chambers of Sarah Okafor

## Licence

MIT - Free to use, modify, and share.
