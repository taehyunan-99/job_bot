import requests

WANTED_API = "https://www.wanted.co.kr/api/v4/jobs"
KEYWORDS = ["데이터 사이언티스트", "데이터 엔지니어", "머신러닝", "AI 엔지니어"]

RELEVANT_KEYWORDS = [
    "데이터", "data", "ml", "ai", "머신러닝", "machine learning",
    "딥러닝", "deep learning", "분석가", "사이언티스트", "scientist",
    "data engineer", "mlops", "llm"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "wanted-user-language": "ko",
    "Accept": "application/json",
}

MAX_PER_SOURCE = 5

def _is_relevant(title: str) -> bool:
    t = title.lower()
    return any(kw in t for kw in RELEVANT_KEYWORDS)

def _fetch_skills(job_id: int) -> list:
    resp = requests.get(f"{WANTED_API}/{job_id}", headers=HEADERS)
    if resp.status_code != 200:
        return []
    job = resp.json().get("job", {})
    return [t["keyword"] for t in job.get("skill_tags", [])]

def scrape_wanted():
    jobs = []
    for keyword in KEYWORDS:
        params = {
            "job_sort": "job.latest_order",
            "limit": 20,
            "offset": 0,
            "country": "kr",
            "tag_type_names": keyword,
        }
        resp = requests.get(WANTED_API, params=params, headers=HEADERS)
        if resp.status_code != 200:
            continue
        data = resp.json().get("data", [])
        for item in data:
            title = item.get("position", "")
            if not _is_relevant(title):
                continue
            jobs.append({
                "id": f"wanted-{item['id']}",
                "_raw_id": item["id"],
                "title": title,
                "company": item["company"]["name"],
                "skills": [],
                "description": "",
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
        j["skills"] = _fetch_skills(j.pop("_raw_id"))
    return unique
