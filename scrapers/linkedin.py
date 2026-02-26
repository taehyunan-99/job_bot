import requests
from bs4 import BeautifulSoup

LINKEDIN_URL = "https://www.linkedin.com/jobs/search/"
KEYWORDS = ["데이터 사이언티스트 한국", "데이터 엔지니어 한국", "머신러닝 엔지니어 한국"]

# 한국 geoId
KOREA_GEO_ID = "105149290"

RELEVANT_KEYWORDS = [
    "데이터", "data", "ml", "ai", "머신러닝", "machine learning",
    "딥러닝", "deep learning", "사이언티스트", "scientist", "mlops", "llm"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

MAX_PER_SOURCE = 5

def _is_relevant(title: str) -> bool:
    t = title.lower()
    return any(kw in t for kw in RELEVANT_KEYWORDS)

def scrape_linkedin():
    jobs = []
    for keyword in KEYWORDS:
        params = {
            "keywords": keyword,
            "location": "대한민국",
            "geoId": KOREA_GEO_ID,
            "f_TPR": "r604800",
            "sortBy": "DD",
        }
        resp = requests.get(LINKEDIN_URL, params=params, headers=HEADERS)
        if resp.status_code != 200:
            continue
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select(".base-card")
        for item in items:
            link_el = item.select_one("a.base-card__full-link")
            title_el = item.select_one(".base-search-card__title")
            company_el = item.select_one(".base-search-card__subtitle")
            location_el = item.select_one(".job-search-card__location")
            if not link_el or not title_el:
                continue
            title = title_el.get_text(strip=True)
            location = location_el.get_text(strip=True) if location_el else ""
            # 한국 공고만 허용
            if location and "한국" not in location and "Korea" not in location and "Seoul" not in location and "서울" not in location and "부산" not in location:
                continue
            if not _is_relevant(title):
                continue
            url = link_el.get("href", "").split("?")[0]
            job_id = url.rstrip("/").split("/")[-1]
            jobs.append({
                "id": f"linkedin-{job_id}",
                "title": title,
                "company": company_el.get_text(strip=True) if company_el else "",
                "skills": [],
                "description": "",
                "url": url,
                "source": "링크드인",
            })
    seen_ids = set()
    unique = []
    for j in jobs:
        if j["id"] not in seen_ids:
            seen_ids.add(j["id"])
            unique.append(j)
    return unique[:MAX_PER_SOURCE]
