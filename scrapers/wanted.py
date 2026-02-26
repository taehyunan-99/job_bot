import requests

WANTED_API = "https://www.wanted.co.kr/api/v4/jobs"
QUERIES = ["데이터 사이언티스트", "데이터 엔지니어", "머신러닝 엔지니어"]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "wanted-user-language": "ko",
    "Accept": "application/json",
}

MAX_PER_SOURCE = 5

def scrape_wanted():
    jobs = []
    for query in QUERIES:
        params = {
            "job_sort": "job.latest_order",
            "limit": 10,
            "offset": 0,
            "country": "kr",
            "query": query,
        }
        resp = requests.get(WANTED_API, params=params, headers=HEADERS)
        if resp.status_code != 200:
            continue
        data = resp.json().get("data", [])
        for item in data:
            jobs.append({
                "id": f"wanted-{item['id']}",
                "title": item.get("position", ""),
                "company": item["company"]["name"],
                "skills": [],
                "url": f"https://www.wanted.co.kr/wd/{item['id']}",
                "source": "원티드",
            })
    seen_ids = set()
    unique = []
    for j in jobs:
        if j["id"] not in seen_ids:
            seen_ids.add(j["id"])
            unique.append(j)
    return unique[:MAX_PER_SOURCE]
