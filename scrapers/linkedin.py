import requests
from bs4 import BeautifulSoup
from utils.dedup import deduplicate
from scrapers.config import MAX_PER_SOURCE, REQUEST_TIMEOUT, KOREA_LOCATIONS, DEFAULT_HEADERS, is_relevant

LINKEDIN_URL = "https://www.linkedin.com/jobs/search/"
KEYWORDS = ["데이터 사이언티스트 한국", "데이터 엔지니어 한국", "머신러닝 엔지니어 한국"]
KOREA_GEO_ID = "105149290"

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
        resp = requests.get(LINKEDIN_URL, params=params, headers=DEFAULT_HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            continue
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select(".base-card"):
            link_el = item.select_one("a.base-card__full-link")
            title_el = item.select_one(".base-search-card__title")
            company_el = item.select_one(".base-search-card__subtitle")
            location_el = item.select_one(".job-search-card__location")
            if not link_el or not title_el:
                continue
            title = title_el.get_text(strip=True)
            location = location_el.get_text(strip=True) if location_el else ""
            if location and not any(loc in location for loc in KOREA_LOCATIONS):
                continue
            if not is_relevant(title):
                continue
            url = link_el.get("href", "").split("?")[0]
            job_id = url.rstrip("/").split("/")[-1]
            jobs.append({
                "id": f"linkedin-{job_id}",
                "title": title,
                "company": company_el.get_text(strip=True) if company_el else "",
                "skills": [],
                "location": location,
                "url": url,
                "source": "링크드인",
            })
    return deduplicate(jobs)[:MAX_PER_SOURCE]
