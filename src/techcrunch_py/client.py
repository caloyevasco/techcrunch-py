import requests

home = 'https://techcrunch.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
}

def create_client() -> requests.Session:
    """Create and return a configured requests Session.

    Uses a Session so callers can call `session.get(...)` and preserve
    cookies/connection pooling. The session's headers are updated with
    default headers. The homepage is optionally requested to populate
    any initial cookies.
    """
    session = requests.Session()
    session.headers.update(headers)

    try:
        # Pre-warm the session (populate cookies) but ignore errors.
        session.get(home, timeout=5)
    except Exception:
        pass

    return session