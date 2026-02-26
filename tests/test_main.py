from unittest.mock import patch
from main import main

def test_main_runs_without_error():
    mock_jobs = [
        {"id": "wanted-1", "title": "DS", "company": "A", "skills": ["Python"], "description": "분석", "url": "http://x", "source": "원티드"}
    ]
    with patch("main.scrape_wanted", return_value=mock_jobs), \
         patch("main.scrape_saramin", return_value=[]), \
         patch("main.scrape_linkedin", return_value=[]), \
         patch("main.send_slack_message") as mock_slack:
        main()
        mock_slack.assert_called_once()
