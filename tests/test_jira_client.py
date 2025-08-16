import pytest
import responses
from src.clients.jira import JiraClient, JiraError


class TestJiraClient:
    def test_init_bearer_auth(self):
        client = JiraClient(
            base_url="https://test.atlassian.net",
            pat="test-token",
            auth_mode="bearer"
        )
        assert client.base_url == "https://test.atlassian.net"
        assert client.sess.headers["Authorization"] == "Bearer test-token"

    def test_init_basic_auth(self):
        client = JiraClient(
            base_url="https://test.atlassian.net",
            pat="test-token",
            auth_mode="basic",
            username="testuser"
        )
        assert client.sess.auth == ("testuser", "test-token")

    def test_init_invalid_auth_mode(self):
        with pytest.raises(ValueError):
            JiraClient(
                base_url="https://test.atlassian.net",
                pat="test-token",
                auth_mode="invalid"
            )

    @responses.activate
    def test_search_success(self):
        responses.add(
            responses.GET,
            "https://test.atlassian.net/rest/api/2/search",
            json={"issues": [{"key": "TEST-1"}], "startAt": 0, "maxResults": 1, "total": 1},
            status=200
        )
        
        client = JiraClient(
            base_url="https://test.atlassian.net",
            pat="test-token"
        )
        result = client.search(jql="project = TEST")
        assert len(result) == 1
        assert result[0]["key"] == "TEST-1"

    @responses.activate
    def test_search_failure(self):
        responses.add(
            responses.GET,
            "https://test.atlassian.net/rest/api/2/search",
            json={"error": "Not found"},
            status=404
        )
        
        client = JiraClient(
            base_url="https://test.atlassian.net",
            pat="test-token"
        )
        with pytest.raises(JiraError):
            client.search(jql="project = TEST")

    @responses.activate
    def test_get_issue_success(self):
        responses.add(
            responses.GET,
            "https://test.atlassian.net/rest/api/2/issue/TEST-1",
            json={"key": "TEST-1", "fields": {"summary": "Test issue"}},
            status=200
        )
        
        client = JiraClient(
            base_url="https://test.atlassian.net",
            pat="test-token"
        )
        result = client.get_issue("TEST-1")
        assert result["key"] == "TEST-1"
        assert result["fields"]["summary"] == "Test issue"

    @responses.activate
    def test_get_issue_failure(self):
        responses.add(
            responses.GET,
            "https://test.atlassian.net/rest/api/2/issue/TEST-1",
            json={"error": "Not found"},
            status=404
        )
        
        client = JiraClient(
            base_url="https://test.atlassian.net",
            pat="test-token"
        )
        with pytest.raises(JiraError):
            client.get_issue("TEST-1")