import requests

WANTED_API = "https://www.wanted.co.kr/api/v4/jobs"
QUERIES = ["데이터 사이언티스트", "데이터 엔지니어", "머신러닝 엔지니어"]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "wanted-user-language": "ko",
    "Accept": "application/json",
}

MAX_PER_SOURCE = 5

def _fetch_detail(job_id: int) -> dict:
    resp = requests.get(f"{WANTED_API}/{job_id}", headers=HEADERS)
    if resp.status_code != 200:
        return {}
    job = resp.json().get("job", {})
    detail = job.get("detail", {})
    address = job.get("address", {})
    return {
        "skills": [t["title"] for t in job.get("skill_tags", [])],
        "requirements": detail.get("requirements", "").strip()[:200],
        "main_tasks": detail.get("main_tasks", "").strip()[:200],
        "location": address.get("location_key", "") or address.get("full_location", ""),
    }

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
        for item in resp.json().get("data", []):
            jobs.append({
                "id": f"wanted-{item['id']}",
                "_raw_id": item["id"],
                "title": item.get("position", ""),
                "company": item["company"]["name"],
                "url": f"https://www.wanted.co.kr/wd/{item['id']}",
                "source": "원티드",
            })

    seen_ids = set()
    unique = []
    for j in jobs:
        if j["id"] not in seen_ids:
            seen_ids.add(j["id"])
            unique.append(j)
    unique = unique[:MAX_PER_SOURCE]

    for j in unique:
        detail = _fetch_detail(j.pop("_raw_id"))
        j.update(detail)

    return unique
