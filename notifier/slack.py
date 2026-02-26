import os
import requests
from datetime import date
from collections import defaultdict

def _get_webhook_url():
    return os.environ.get("SLACK_WEBHOOK_URL", "")

def format_message(jobs: list) -> str:
    today = date.today().strftime("%Y-%m-%d")
    lines = [f"📊 *[데이터 직무 주간 브리핑]* {today}\n"]

    by_source = defaultdict(list)
    for job in jobs:
        by_source[job["source"]].append(job)

    for source, source_jobs in by_source.items():
        lines.append(f"\n✅ *{source}* ({len(source_jobs)}건)")
        for job in source_jobs:
            skills = ", ".join(job["skills"]) if job["skills"] else "정보 없음"
            desc = job["description"] if job["description"] else "정보 없음"
            lines.append(
                f"• *{job['company']}* - {job['title']}\n"
                f"  🛠 {skills}\n"
                f"  📋 {desc}\n"
                f"  🔗 {job['url']}"
            )

    return "\n".join(lines)

def send_slack_message(jobs: list):
    webhook_url = _get_webhook_url()
    if not webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL 환경변수가 설정되지 않았습니다")
    message = format_message(jobs)
    payload = {"text": message}
    resp = requests.post(webhook_url, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(f"슬랙 발송 실패: {resp.status_code} {resp.text}")
