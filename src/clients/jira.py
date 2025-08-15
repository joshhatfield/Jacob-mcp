from typing import Optional, Iterable, Dict, Any, List
import requests


class JiraError(RuntimeError):
    pass

class JiraClient:
    def __init__(
        self,
        base_url: str,
        pat: str,
        auth_mode: str = "bearer",  # "bearer" or "basic"
        username: Optional[str] = None,
        verify_tls: bool = True,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = (timeout, timeout)
        self.sess = requests.Session()
        self.sess.headers.update({"Accept": "application/json"})
        self.sess.verify = verify_tls
        if auth_mode == "bearer":
            self.sess.headers.update({"Authorization": f"Bearer {pat}"})
        elif auth_mode == "basic":
            if not username:
                raise ValueError("username required for auth_mode='basic'")
            self.sess.auth = (username, pat)
        else:
            raise ValueError("auth_mode must be 'bearer' or 'basic'")

    def search(
        self,
        jql: str,
        fields: Optional[Iterable[str]] = None,
        expand: Optional[Iterable[str]] = None,
        batch_size: int = 100,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        if batch_size < 1 or batch_size > 1000:
            raise ValueError("batch_size must be 1..1000")

        params: Dict[str, Any] = {
            "jql": jql,
            "startAt": 0,
            "maxResults": min(batch_size, limit) if limit else batch_size,
        }
        if fields is not None:
            params["fields"] = ",".join(fields)
        if expand is not None:
            params["expand"] = ",".join(expand)

        issues: List[Dict[str, Any]] = []
        url = f"{self.base_url}/rest/api/2/search"

        while True:
            resp = self.sess.get(url, params=params, timeout=self.timeout)
            if resp.status_code != 200:
                raise JiraError(f"Search failed [{resp.status_code}]: {resp.text}")
            data = resp.json()
            batch = data.get("issues", [])
            issues.extend(batch)

            if limit is not None and len(issues) >= limit:
                return issues[:limit]

            start_at = data.get("startAt", 0)
            max_results = data.get("maxResults", len(batch))
            total = data.get("total", start_at + len(batch))
            next_start = start_at + max_results

            if next_start >= total or not batch:
                break

            params["startAt"] = next_start
            if limit is not None:
                params["maxResults"] = min(batch_size, limit - len(issues))
        return issues

    def get_issue(
        self,
        issue_key: str,
        fields: Optional[Iterable[str]] = None,
        expand: Optional[Iterable[str]] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if fields is not None:
            params["fields"] = ",".join(fields)
        if expand is not None:
            params["expand"] = ",".join(expand)

        url = f"{self.base_url}/rest/api/2/issue/{issue_key}"
        resp = self.sess.get(url, params=params, timeout=self.timeout)
        if resp.status_code != 200:
            raise JiraError(f"Get issue failed [{resp.status_code}]: {resp.text}")
        return resp.json()