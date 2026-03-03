import requests
from bs4 import BeautifulSoup
from utils.dedup import deduplicate
from scrapers.config import MAX_PER_SOURCE, REQUEST_TIMEOUT, RELEVANT_KEYWORDS, DEFAULT_HEADERS

SARAMIN_URL = "https://www.saramin.co.kr/zf_user/search/recruit"
KEYWORDS = ["데이터사이언티스트", "데이터엔지니어", "머신러닝엔지니어", "데이터분석가"]

def _is_relevant(title: str) -> bool:
    t = title.lower()
    return any(kw in t for kw in RELEVANT_KEYWORDS)

def scrape_saramin():
    jobs = []
    for keyword in KEYWORDS:
        params = {
            "searchType": "search",
            "searchword": keyword,
            "recruitPage": 1,
            "recruitPageCount": 20,
            "recruitSort": "reg_dt",
        }
        resp = requests.get(SARAMIN_URL, params=params, headers=DEFAULT_HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            continue
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select(".item_recruit"):
            title_el = item.select_one(".job_tit a")
            company_el = item.select_one(".corp_name a")
            skill_els = item.select(".job_sector a")
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            if not _is_relevant(title):
                continue
            href = title_el.get("href", "")
            rec_idx = href.split("rec_idx=")[-1].split("&")[0] if "rec_idx=" in href else href
            location_el = item.select_one(".job_condition span a")
            jobs.append({
                "id": f"saramin-{rec_idx}",
                "title": title,
                "company": company_el.get_text(strip=True) if company_el else "",
                "skills": [s.get_text(strip=True) for s in skill_els],
                "location": location_el.get_text(strip=True) if location_el else "",
                "url": f"https://www.saramin.co.kr{href}",
                "source": "사람인",
            })
    return deduplicate(jobs)[:MAX_PER_SOURCE]
