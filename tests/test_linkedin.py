from unittest.mock import patch
from scrapers.linkedin import scrape_linkedin

def test_scrape_linkedin_returns_list():
    mock_html = """
    <ul class="jobs-search__results-list">
      <li>
        <a class="base-card__full-link" href="https://www.linkedin.com/jobs/view/123456">
        </a>
        <h3 class="base-search-card__title">Data Scientist</h3>
        <h4 class="base-search-card__subtitle">Kakao</h4>
      </li>
    </ul>
    """
    with patch("scrapers.linkedin.requests.get") as mock_get:
        mock_get.return_value.text = mock_html
        mock_get.return_value.status_code = 200
        jobs = scrape_linkedin()
    assert isinstance(jobs, list)
