from unittest.mock import patch
from scrapers.wanted import scrape_wanted

def test_scrape_wanted_returns_list():
    mock_response = {
        "data": [
            {
                "id": 12345,
                "position": "데이터 사이언티스트",
                "company": {"name": "카카오"},
                "skill_tags": [{"keyword": "Python"}, {"keyword": "SQL"}],
            }
        ]
    }
    with patch("scrapers.wanted.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        jobs = scrape_wanted()
    assert len(jobs) == 1
    assert jobs[0]["id"] == "wanted-12345"
    assert jobs[0]["company"] == "카카오"
    assert "Python" in jobs[0]["skills"]
