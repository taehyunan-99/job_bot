from unittest.mock import patch, MagicMock
from scrapers.wanted import scrape_wanted

def test_scrape_wanted_returns_list():
    mock_list_resp = MagicMock()
    mock_list_resp.status_code = 200
    mock_list_resp.json.return_value = {
        "data": [{"id": 12345, "position": "데이터 사이언티스트", "company": {"name": "카카오"}}]
    }
    empty_resp = MagicMock()
    empty_resp.status_code = 200
    empty_resp.json.return_value = {"data": []}

    mock_detail_resp = MagicMock()
    mock_detail_resp.status_code = 200
    mock_detail_resp.json.return_value = {
        "job": {
            "skill_tags": [{"title": "Python"}, {"title": "SQL"}],
            "detail": {"requirements": "3년 이상", "main_tasks": "모델 개발"},
            "address": {"location_key": "서울"},
        }
    }

    with patch("scrapers.wanted.requests.get") as mock_get:
        mock_get.side_effect = [mock_list_resp, empty_resp, empty_resp, mock_detail_resp]
        jobs = scrape_wanted()

    assert len(jobs) == 1
    assert jobs[0]["id"] == "wanted-12345"
    assert jobs[0]["company"] == "카카오"
    assert "Python" in jobs[0]["skills"]
    assert jobs[0]["location"] == "서울"
