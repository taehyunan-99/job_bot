from unittest.mock import patch
from scrapers.saramin import scrape_saramin

def test_scrape_saramin_returns_list():
    mock_html = """
    <div class="item_recruit">
        <div class="area_job">
            <h2 class="job_tit"><a href="/zf_user/jobs/relay/view?rec_idx=99999" title="데이터 분석가">데이터 분석가</a></h2>
            <div class="job_condition">
                <span><a href="#">네이버</a></span>
            </div>
            <div class="job_sector">
                <a>Python</a><a>SQL</a>
            </div>
        </div>
    </div>
    """
    with patch("scrapers.saramin.requests.get") as mock_get:
        mock_get.return_value.text = mock_html
        mock_get.return_value.status_code = 200
        jobs = scrape_saramin()
    assert isinstance(jobs, list)
