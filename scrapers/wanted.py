import requests

# 원티드 직무 카테고리 ID (데이터 관련)
# 872: 데이터 엔지니어, 873: 데이터 사이언티스트, 874: BI 엔지니어, 10110: AI/ML
WANTED_API = "https://www.wanted.co.kr/api/v4/jobs"
CATEGORY_IDS = [872, 873, 874, 10110]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "wanted-user-language": "ko",
    "Accept": "application/json",
}

def scrape_wanted():
    jobs = []
    for category_id in CATEGORY_IDS:
        params = {
            "job_sort": "job.latest_order",
            "limit": 20,
            "offset": 0,
            "job_category_tags": category_id,
            "country": "kr",
        }
        resp = requests.get(WANTED_API, params=params, headers=HEADERS)
        if resp.status_code != 200:
            continue
        data = resp.json().get("data", [])
        for item in data:
            jobs.append({
                "id": f"wanted-{item['id']}",
                "title": item["position"]["name"],
                "company": item["company"]["name"],
                "skills": [t["keyword"] for t in item.get("skill_tags", [])],
                "description": item.get("job_category", {}).get("name", ""),
                "url": f"https://www.wanted.co.kr/wd/{item['id']}",
                "source": "원티드",
            })
    seen_ids = set()
    unique = []
    for j in jobs:
        if j["id"] not in seen_ids:
            seen_ids.add(j["id"])
            unique.append(j)
    return unique
