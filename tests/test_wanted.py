from unittest.mock import patch, MagicMock
from scrapers.wanted import scrape_wanted

def test_scrape_wanted_returns_list():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "data": [
            {
                "id": 12345,
                "position": "데이터 사이언티스트",
                "company": {"name": "카카오"},
            }
        ]
    }
    empty_resp = MagicMock()
    empty_resp.status_code = 200
    empty_resp.json.return_value = {"data": []}

    with patch("scrapers.wanted.requests.get") as mock_get:
        mock_get.side_effect = [mock_resp, empty_resp, empty_resp]
        jobs = scrape_wanted()

    assert len(jobs) == 1
    assert jobs[0]["id"] == "wanted-12345"
    assert jobs[0]["company"] == "카카오"
