# UK Law MCP Server

A Model Context Protocol server providing access to free official UK legal sources.

## Data Sources

| Source | What It Provides |
|--------|------------------|
| legislation.gov.uk | All UK statutes, SIs, regulations |
| caselaw.nationalarchives.gov.uk | Court judgments from 2001 onwards |

## Tools

| Tool | Description |
|------|-------------|
| get_legislation | Fetch a specific statute section |
| search_legislation | Search all UK legislation |
| search_cases | Search court judgments |
| get_judgment | Fetch a specific case by citation |
| get_legislation_pdf_url | Get PDF URL for statute section |
| get_judgment_pdf_url | Get PDF URL for judgment |

## Courts Covered

- Supreme Court (UKSC)
- Court of Appeal (EWCA Civ, EWCA Crim)
- High Court (all divisions)
- Court of Protection (EWCOP)
- Family Court (EWFC)
- Upper Tribunal (UKUT)
- First-tier Tribunal (UKFTT)
- Employment Appeal Tribunal (EAT)

## Installation

```bash
cd uk-law-mcp
pip install -r requirements.txt
```

## Usage

```bash
python3 src/server.py
```

## Author

Sarah Okafor - Chambers of Sarah Okafor

## Licence

MIT - Free to use, modify, and share.
