import os
from clients.jira import JiraClient
from clients.confluence import ConfluenceClient

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