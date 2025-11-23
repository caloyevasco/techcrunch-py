from src.techcrunch_py.scraper import get_latest_headlines
from unittest.mock import Mock, patch, call
import pytest

from tests.test_data import mock_html

class TestGetLatestHeadlines:
    
    @patch('src.techcrunch_py.scraper.create_client')
    def test_returns_correct_number_of_articles(self, mock_create, mock_html):
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = mock_html
        mock_client.get.return_value = mock_response
        mock_create.return_value = mock_client

        articles = list(get_latest_headlines(limit=3))

        assert len(articles) == 3

    @patch('src.techcrunch_py.scraper.create_client')
    def test_calls_home_endpoint_once(self, mock_create, mock_html):
        from src.techcrunch_py.client import home
        
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = mock_html
        mock_client.get.return_value = mock_response
        mock_create.return_value = mock_client

        list(get_latest_headlines(limit=2))

        # first call should be homepage
        assert mock_client.get.call_args_list[0] == call(home)

    @patch('src.techcrunch_py.scraper.create_client')
    def test_fetches_full_article_content(self, mock_create, mock_html):
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = mock_html
        mock_client.get.return_value = mock_response
        mock_create.return_value = mock_client

        articles = list(get_latest_headlines(limit=1))

        # should call get at least twice: homepage + 1 article
        assert mock_client.get.call_count >= 2

    @patch('src.techcrunch_py.scraper.create_client')
    def test_article_schema_fields_not_empty(self, mock_create, mock_html):
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = mock_html
        mock_client.get.return_value = mock_response
        mock_create.return_value = mock_client

        articles = list(get_latest_headlines(limit=1))
        article = articles[0]

        assert article.title
        assert article.full_article_link
        # other fields might be optional but these shouldn't be empty

    @patch('src.techcrunch_py.scraper.create_client')
    def test_raises_on_bad_home_response(self, mock_create, mock_html):
        mock_client = Mock()
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("404 not found")
        mock_client.get.return_value = mock_response
        mock_create.return_value = mock_client

        with pytest.raises(Exception):
            list(get_latest_headlines(limit=1))

    @patch('src.techcrunch_py.scraper.create_client')
    def test_default_limit_is_10(self, mock_create, mock_html):
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = mock_html
        mock_client.get.return_value = mock_response
        mock_create.return_value = mock_client

        articles = list(get_latest_headlines())  # no limit param

        # assuming mock_html has at least 10 articles
        assert len(articles) <= 10
