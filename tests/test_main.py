import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add src to path so we can import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import main
from clients.jira import JiraClient
from clients.confluence import ConfluenceClient

class TestMain(unittest.TestCase):
    
    def setUp(self):
        # Clear environment variables
        for key in ['JIRA_BASE_URL', 'JIRA_PAT', 'CONFLUENCE_BASE_URL', 'CONFLUENCE_PAT']:
            if key in os.environ:
                del os.environ[key]

    @patch.dict(os.environ, {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_PAT': 'test-token'
    })
    def test_jira_client_from_env_bearer(self):
        client = main.jira_client_from_env()
        self.assertIsInstance(client, JiraClient)
        self.assertEqual(client.base_url, 'https://test.atlassian.net')

    @patch.dict(os.environ, {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_PAT': 'test-pass',
        'JIRA_AUTH_MODE': 'basic',
        'JIRA_USERNAME': 'test-user'
    })
    def test_jira_client_from_env_basic(self):
        client = main.jira_client_from_env()
        self.assertIsInstance(client, JiraClient)
        self.assertEqual(client.sess.auth, ('test-user', 'test-pass'))

    @patch.dict(os.environ, {
        'CONFLUENCE_BASE_URL': 'https://test.atlassian.net/wiki',
        'CONFLUENCE_PAT': 'test-token'
    })
    def test_confluence_client_from_env(self):
        client = main.confluence_client_from_env()
        self.assertIsInstance(client, ConfluenceClient)
        self.assertEqual(client.base_url, 'https://test.atlassian.net/wiki')

    @patch('main.JiraClient')
    def test_jira_search(self, mock_jira_client_class):
        mock_client_instance = Mock()
        mock_jira_client_class.return_value = mock_client_instance
        mock_client_instance.search.return_value = [{'key': 'TEST-1'}]
        
        with patch.dict(os.environ, {
            'JIRA_BASE_URL': 'https://test.atlassian.net',
            'JIRA_PAT': 'test-token'
        }):
            result = main.jira_search('project = TEST', ['summary'], 10)
            
        self.assertEqual(result, [{'key': 'TEST-1'}])
        mock_client_instance.search.assert_called_once_with(jql='project = TEST', fields=['summary'], limit=10)

    @patch('main.ConfluenceClient')
    def test_confluence_search(self, mock_confluence_client_class):
        mock_client_instance = Mock()
        mock_confluence_client_class.return_value = mock_client_instance
        mock_client_instance.search.return_value = [{'id': '123'}]
        
        with patch.dict(os.environ, {
            'CONFLUENCE_BASE_URL': 'https://test.atlassian.net/wiki',
            'CONFLUENCE_PAT': 'test-token'
        }):
            result = main.confluence_search('type = page', 5)
            
        self.assertEqual(result, [{'id': '123'}])
        mock_client_instance.search.assert_called_once_with(cql='type = page', limit=5)

if __name__ == '__main__':
    unittest.main()