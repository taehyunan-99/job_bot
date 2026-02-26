import requests
from bs4 import BeautifulSoup

LINKEDIN_URL = "https://www.linkedin.com/jobs/search/"
KEYWORDS = ["data scientist", "data engineer", "machine learning engineer"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
}

def scrape_linkedin():
    jobs = []
    for keyword in KEYWORDS:
        params = {
            "keywords": keyword,
            "location": "South Korea",
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
            if not link_el or not title_el:
                continue
            url = link_el.get("href", "").split("?")[0]
            job_id = url.rstrip("/").split("/")[-1]
            jobs.append({
                "id": f"linkedin-{job_id}",
                "title": title_el.get_text(strip=True),
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
    return unique
