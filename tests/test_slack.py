from unittest.mock import patch
from notifier.slack import format_message, send_slack_message

def test_format_message_contains_title():
    jobs = [
        {
            "source": "원티드",
            "title": "데이터 사이언티스트",
            "company": "카카오",
            "skills": ["Python", "SQL"],
            "description": "추천 시스템 개발",
            "url": "https://www.wanted.co.kr/wd/12345",
        }
    ]
    msg = format_message(jobs)
    assert "데이터 사이언티스트" in msg
    assert "카카오" in msg
    assert "Python" in msg

def test_send_slack_message_calls_webhook():
    jobs = [{"source": "원티드", "title": "DS", "company": "A", "skills": [], "description": "", "url": "http://x"}]
    with patch("notifier.slack.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        with patch.dict("os.environ", {"SLACK_WEBHOOK_URL": "https://hooks.slack.com/test"}):
            send_slack_message(jobs)
        mock_post.assert_called_once()
