# Jacob-mcp
Jira And Confluence On-prem Bridge MCP or J.A.C.O.B

## Running
written on python 3.12

Reccomended to run with MCPO

```shell
export JIRA_BASE_URL="https://your-jira.example.com"
export JIRA_PAT="your_pat_token"
export CONFLUENCE_BASE_URL="https://your-confluence.example.com"
export CONFLUENCE_PAT="your_pat_token"

# Optional jira vars:
export JIRA_AUTH_MODE="bearer"      # or "basic"
export JIRA_USERNAME="your_user"    # only if JIRA_AUTH_MODE=basic
export JIRA_VERIFY_TLS="true"       # "false" to skip TLS verify (dev only)
export JIRA_TIMEOUT="30"

# Optional confluence vars:
export CONFLUENCE_AUTH_MODE="bearer"       # or "basic"
export CONFLUENCE_USERNAME="your_user"     # if basic
export CONFLUENCE_VERIFY_TLS="true"        # false to skip TLS verify (dev only)
export CONFLUENCE_TIMEOUT="30"


# pip install mcpo 
mcpo --port 8000 -- python main.py
```
