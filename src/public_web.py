"""Anonymous, bounded-time HTTP requests for the coursework scrapers."""
from urllib.parse import urlsplit
import requests

def get(url):
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
        raise ValueError("Use a public HTTP(S) URL without credentials")
    with requests.Session() as session:
        session.trust_env = False
        session.headers["User-Agent"] = "CourseworkScraper/1.0"
        response = session.get(url, timeout=20, allow_redirects=False)
        response.raise_for_status()
        if response.is_redirect:
            raise ValueError("Use the final public URL instead of a redirect")
        return response
