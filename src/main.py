import os
import requests
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP
from clients.jira import JiraClient
from clients.confluence import ConfluenceClient




mcp = FastMCP("Jira MCP")

def jira_client_from_env() -> JiraClient:
    base = os.environ["JIRA_BASE_URL"]
    pat = os.environ["JIRA_PAT"]
    auth_mode = os.environ.get("JIRA_AUTH_MODE", "bearer").lower()
    username = os.environ.get("JIRA_USERNAME") if auth_mode == "basic" else None
    verify_tls_env = os.environ.get("JIRA_VERIFY_TLS", "true").lower()
    verify_tls = verify_tls_env not in ("false", "0", "no")
    timeout = int(os.environ.get("JIRA_TIMEOUT", "30"))
    return JiraClient(base, pat, auth_mode=auth_mode, username=username,
                      verify_tls=verify_tls, timeout=timeout)

def confluence_client_from_env() -> ConfluenceClient:
    base = os.environ["CONFLUENCE_BASE_URL"]
    pat = os.environ["CONFLUENCE_PAT"]
    auth_mode = os.environ.get("CONFLUENCE_AUTH_MODE", "bearer").lower()
    username = os.environ.get("CONFLUENCE_USERNAME") if auth_mode == "basic" else None
    verify_tls_env = os.environ.get("CONFLUENCE_VERIFY_TLS", "true").lower()
    verify_tls = verify_tls_env not in ("false", "0", "no")
    timeout = int(os.environ.get("CONFLUENCE_TIMEOUT", "30"))
    return ConfluenceClient(
        base, pat,
        auth_mode=auth_mode,
        username=username,
        verify_tls=verify_tls,
        timeout=timeout
    )

@mcp.tool
def jira_search(jql: str,
                fields: Optional[List[str]] = None,
                limit: Optional[int] = 50) -> List[Dict[str, Any]]:
    """
    Search Jira issues via JQL.
    - jql: e.g. 'project = "ENG" AND statusCategory != Done ORDER BY updated DESC'
    - fields: list of field names (e.g. ["summary","assignee","status"])
    - limit: max number of issues to return (pagination handled server-side)
    Returns: list of issue objects (subset of Jira REST v2)
    """
    client = jira_client_from_env()
    return client.search(jql=jql, fields=fields, limit=limit)

@mcp.tool
def jira_get_issue(key: str,
                   fields: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Get a single issue by key (e.g. 'PROJ-123').
    - fields: list of field names to include
    Returns: issue object (Jira REST v2)
    """
    client = jira_client_from_env()
    return client.get_issue(issue_key=key, fields=fields)


@mcp.tool
def confluence_search(cql: str, limit: int = 25) -> List[Dict[str, Any]]:
    """
    Search Confluence pages using CQL.
    - cql: e.g. 'type=page AND space=ENG AND title~"design"'
    - limit: number of results to return
    Returns: list of pages with metadata and rendered view HTML.
    """
    client = confluence_client_from_env()
    return client.search(cql=cql, limit=limit)

@mcp.tool
def confluence_get_page(page_id: str, expand: str = "body.storage") -> Dict[str, Any]:
    """
    Get a single Confluence page by its ID.
    - page_id: numeric ID (string)
    - expand: fields to expand (default: 'body.storage')
      Common values:
        - body.storage (raw storage format)
        - body.view (rendered HTML)
    Returns: page object with expanded content.
    """
    client = confluence_client_from_env()
    return client.get_page(page_id=page_id, expand=expand)


if __name__ == "__main__":
    mcp.run()
