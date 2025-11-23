from src.techcrunch_py.scraper import get_latest

def test_scraper():

    scraper = get_latest()
    
    assert len(scraper) > 0