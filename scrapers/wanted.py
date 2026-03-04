import requests
from utils.dedup import deduplicate
from scrapers.config import MAX_PER_SOURCE, REQUEST_TIMEOUT

WANTED_API = "https://www.wanted.co.kr/api/v4/jobs"
QUERIES = ["데이터 사이언티스트", "데이터 엔지니어", "머신러닝 엔지니어"]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "wanted-user-language": "ko",
    "Accept": "application/json",
}

def _fetch_detail(job_id: int) -> dict:
    resp = requests.get(f"{WANTED_API}/{job_id}", headers=HEADERS, timeout=REQUEST_TIMEOUT)
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
        resp = requests.get(WANTED_API, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            continue
        for item in resp.json().get("data", []):
            raw_id = item["id"]
            jobs.append((raw_id, {
                "id": f"wanted-{raw_id}",
                "title": item.get("position", ""),
                "company": item.get("company", {}).get("name", ""),
                "url": f"https://www.wanted.co.kr/wd/{raw_id}",
                "source": "원티드",
            }))

    deduped = deduplicate([job for _, job in jobs])[:MAX_PER_SOURCE]
    id_map = {job["id"]: raw_id for raw_id, job in jobs}

    result = []
    for job in deduped:
        job.update(_fetch_detail(id_map[job["id"]]))
        result.append(job)
    return result
