import requests

WANTED_API = "https://www.wanted.co.kr/api/v4/jobs"
KEYWORDS = ["데이터 사이언티스트", "데이터 엔지니어", "ML 엔지니어", "머신러닝", "data scientist"]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "wanted-user-language": "ko",
}

def scrape_wanted():
    jobs = []
    for keyword in KEYWORDS:
        params = {
            "job_sort": "job.latest_order",
            "years": -1,
            "limit": 20,
            "offset": 0,
            "tag_type_names": keyword,
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
