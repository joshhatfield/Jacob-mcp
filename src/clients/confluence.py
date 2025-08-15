from typing import Optional, Dict, Any, List
import requests

class ConfluenceError(RuntimeError):
    pass

class ConfluenceClient:
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

    def search(self, cql: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Search pages using CQL. Returns metadata and basic page info.
        """
        url = f"{self.base_url}/rest/api/content/search"
        params = {
            "cql": cql,
            "limit": limit,
            "expand": "space,body.view"
        }
        resp = self.sess.get(url, params=params, timeout=self.timeout)
        if resp.status_code != 200:
            raise ConfluenceError(f"Search failed [{resp.status_code}]: {resp.text}")
        return resp.json().get("results", [])

    def get_page(self, page_id: str, expand: str = "body.storage") -> Dict[str, Any]:
        """
        Retrieve a page by ID, with full content in the chosen format.
        """
        url = f"{self.base_url}/rest/api/content/{page_id}"
        params = {"expand": expand}
        resp = self.sess.get(url, params=params, timeout=self.timeout)
        if resp.status_code != 200:
            raise ConfluenceError(f"Get page failed [{resp.status_code}]: {resp.text}")
        return resp.json()
