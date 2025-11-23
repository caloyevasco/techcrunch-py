# techcrunch-py

Small library to scrape latest headlines from TechCrunch.

Quick start

- Create a virtualenv and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pip install pytest
```

- Run tests:

```powershell
pytest -q
```

Usage example

```python
from techcrunch_py.scraper import get_latest_headlines

for article in get_latest_headlines(limit=5):
    print(article.title, article.full_article_link)
```

Notes

- Respect site terms and robots.txt when scraping.
- This project uses `requests` + `beautifulsoup4` and returns Pydantic models.
