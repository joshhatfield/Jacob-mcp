import unittest
from unittest.mock import Mock, patch
from clients.confluence import ConfluenceClient, ConfluenceError

class TestConfluenceClient(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://test.atlassian.net/wiki"
        self.pat = "test-token"
        self.client = ConfluenceClient(self.base_url, self.pat)

    @patch('clients.confluence.requests.Session.get')
    def test_search_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"id": "123", "title": "Test Page"}
            ]
        }
        mock_get.return_value = mock_response

        result = self.client.search("type=page AND title~'test'")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Test Page")
        mock_get.assert_called_once()

    @patch('clients.confluence.requests.Session.get')
    def test_search_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response

        with self.assertRaises(ConfluenceError):
            self.client.search("type=page")

    @patch('clients.confluence.requests.Session.get')
    def test_get_page_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "123",
            "title": "Test Page",
            "body": {"storage": {"value": "<p>Content</p>"}}
        }
        mock_get.return_value = mock_response

        result = self.client.get_page("123")
        
        self.assertEqual(result["title"], "Test Page")
        mock_get.assert_called_once()

    @patch('clients.confluence.requests.Session.get')
    def test_get_page_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        with self.assertRaises(ConfluenceError):
            self.client.get_page("999")

if __name__ == '__main__':
    unittest.main()