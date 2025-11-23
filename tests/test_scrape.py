from src.techcrunch_py.scraper import get_latest
import pytest
from unittest.mock import Mock, patch
import requests


@pytest.fixture
def mock_html():
    return """
    <html>
        <a class="loop-card__title-link" href="/article-1">First Article</a>
        <a class="loop-card__title-link" href="/article-2">Second Article</a>
    </html>
    """

@pytest.fixture
def mock_html_5_articles():
    return """
    <html>
        <a class="loop-card__title-link" href="/article-1">First Article</a>
        <a class="loop-card__title-link" href="/article-2">Second Article</a>
        <a class="loop-card__title-link" href="/article-3">Third Article</a>
        <a class="loop-card__title-link" href="/article-4">Fourth Article</a>
        <a class="loop-card__title-link" href="/article-5">Fifth Article</a>
        <a class="other-class" href="/not-this">Ignored</a>
    </html>
    """

@pytest.fixture
def mock_html_empty():
    return """
    <a class="other-class" href="/not-this">Ignored</a>
    """


@pytest.fixture
def mock_response(mock_html):
    resp = Mock()
    resp.text = mock_html
    return resp

@pytest.fixture
def mock_response_5_articles(mock_html_5_articles):
    resp = Mock()
    resp.text = mock_html_5_articles
    return resp

@pytest.fixture
def mock_empty_response(mock_html_empty):
    resp = Mock()
    resp.text = mock_html_empty
    return resp

@pytest.fixture
def mock_client():
    mock_client = Mock()
    return mock_client


class TestGetLatest:

    @patch('src.techcrunch_py.scraper.create_client')
    def test_returns_list_of_latest_articles(self, mock_create, mock_response, mock_client):
        mock_client.get.return_value = mock_response
        mock_create.return_value = mock_client
        result = get_latest()
        assert len(result) == 2
        assert result[0].href == "/article-1"
        assert result[0].text == "First Article"
        assert result[0].element_class == "loop-card__title-link"
        assert result[1].href == "/article-2"
        assert result[1].text == "Second Article"
        assert result[1].element_class == "loop-card__title-link"

    @patch('src.techcrunch_py.scraper.create_client')
    def test_returns_list_of_latest_articles_by_limit_5(self, mock_create, mock_response_5_articles, mock_client):
        mock_client.get.return_value = mock_response_5_articles
        mock_create.return_value = mock_client
        result = get_latest(limit=5)
        assert len(result) == 5

    @patch('src.techcrunch_py.scraper.create_client')
    def test_returns_list_of_latest_articles_by_limit_0(self, mock_create, mock_response_5_articles, mock_client):
        mock_client.get.return_value = mock_response_5_articles
        mock_create.return_value = mock_client
        result = get_latest(limit=0)
        assert len(result) == 0

    @patch('src.techcrunch_py.scraper.create_client')
    def test_returns_empty_list_of_latest_articles(self, mock_create, mock_empty_response, mock_client):
        mock_client.get.return_value = mock_empty_response
        mock_create.return_value = mock_client
        result = get_latest()
        assert len(result) == 0

    @patch('src.techcrunch_py.scraper.create_client')
    def test_timeout_error(self, mock_create, mock_client):
        mock_client.get.side_effect = requests.Timeout("connection timed out")
        mock_create.return_value = mock_client
        
        with pytest.raises(requests.Timeout):
            get_latest()
    
    @patch('src.techcrunch_py.scraper.create_client')
    def test_connection_error(self, mock_create, mock_client):
        mock_client.get.side_effect = requests.ConnectionError("no internet")
        mock_create.return_value = mock_client
        
        with pytest.raises(requests.ConnectionError):
            get_latest()
    
    @patch('src.techcrunch_py.scraper.create_client')
    def test_http_404_error(self, mock_create, mock_client):
        mock_resp = Mock()
        mock_resp.raise_for_status.side_effect = requests.HTTPError("404")
        mock_client.get.return_value = mock_resp
        mock_create.return_value = mock_client
        
        with pytest.raises(requests.HTTPError):
            get_latest()

    @patch('src.techcrunch_py.scraper.create_client')
    def test_http_500_error(self, mock_create, mock_client):
        mock_resp = Mock()
        mock_resp.raise_for_status.side_effect = requests.HTTPError("500")
        mock_client.get.return_value = mock_resp
        mock_create.return_value = mock_client
        
        with pytest.raises(requests.HTTPError):
            get_latest()

    @patch("src.techcrunch_py.scraper.create_client")
    def test_returns_empty_list_when_no_articles(self, mock_create):
        mock_client = Mock()
        mock_resp = Mock()
        mock_resp.text = "<html><div>nothing here</div></html>"
        mock_client.get.return_value = mock_resp
        mock_create.return_value = mock_client

        result = get_latest()

        assert result == []

    @patch("src.techcrunch_py.scraper.create_client")
    def test_limit_greater_than_available_articles(self, mock_create, mock_response):
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_create.return_value = mock_client

        result = get_latest(limit=100)

        assert len(result) == 2

    @patch("src.techcrunch_py.scraper.create_client")
    def test_negative_limit_returns_empty(self, mock_create, mock_response):
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_create.return_value = mock_client

        result = get_latest(limit=-5)

        assert len(result) == 0

    @patch("src.techcrunch_py.scraper.create_client")
    def test_calls_client_with_home(self, mock_create, mock_response):
        from src.techcrunch_py.client import home
        
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_create.return_value = mock_client

        get_latest()

        mock_client.get.assert_called_once_with(home)

    @patch('src.techcrunch_py.scraper.create_client')
    def test_whitespace_in_article_text_is_preserved(self, mock_create, mock_client):
        mock_resp = Mock()
        mock_resp.text = """
        <html>
            <a class="loop-card__title-link" href="/test">  Spaces  Everywhere  </a>
        </html>
        """
        mock_client.get.return_value = mock_resp
        mock_create.return_value = mock_client
        
        result = get_latest()
        assert result[0].text == "  Spaces  Everywhere  "

    @patch('src.techcrunch_py.scraper.create_client')
    def test_special_characters_in_urls(self, mock_create, mock_client):
        mock_resp = Mock()
        mock_resp.text = """
        <html>
            <a class="loop-card__title-link" href="/article?id=123&sort=new">Article</a>
        </html>
        """
        mock_client.get.return_value = mock_resp
        mock_create.return_value = mock_client
        
        result = get_latest()
        assert result[0].href == "/article?id=123&sort=new"

    @patch('src.techcrunch_py.scraper.create_client')
    def test_empty_response_text(self, mock_create, mock_client):
        mock_resp = Mock()
        mock_resp.text = ""
        mock_client.get.return_value = mock_resp
        mock_create.return_value = mock_client
        
        result = get_latest()
        assert result == []

    @patch('src.techcrunch_py.scraper.create_client')
    def test_articles_with_multiple_classes(self, mock_create, mock_client):
        mock_resp = Mock()
        mock_resp.text = """
        <html>
            <a class="loop-card__title-link featured" href="/test">Featured Article</a>
        </html>
        """
        mock_client.get.return_value = mock_resp
        mock_create.return_value = mock_client
        
        result = get_latest()
        assert result[0].element_class == "loop-card__title-link"

    @patch('src.techcrunch_py.scraper.create_client')
    def test_unicode_in_article_titles(self, mock_create, mock_client):
        mock_resp = Mock()
        mock_resp.text = """
        <html>
            <a class="loop-card__title-link" href="/test">Article 日本語 🚀</a>
        </html>
        """
        mock_client.get.return_value = mock_resp
        mock_create.return_value = mock_client
        
        result = get_latest()
        assert "日本語" in result[0].text
        assert "🚀" in result[0].text

    @patch('src.techcrunch_py.scraper.create_client')
    def test_nested_html_in_link_text(self, mock_create, mock_client):
        mock_resp = Mock()
        mock_resp.text = """
        <html>
            <a class="loop-card__title-link" href="/test">
                <span>Nested</span> Text
            </a>
        </html>
        """
        mock_client.get.return_value = mock_resp
        mock_create.return_value = mock_client
        
        result = get_latest()
        assert "Nested" in result[0].text
        assert "Text" in result[0].text