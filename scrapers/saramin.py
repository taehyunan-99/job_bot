import requests
from bs4 import BeautifulSoup

SARAMIN_URL = "https://www.saramin.co.kr/zf_user/search/recruit"
KEYWORDS = ["데이터사이언티스트", "데이터엔지니어", "머신러닝엔지니어"]

HEADERS = {"User-Agent": "Mozilla/5.0"}

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
        resp = requests.get(SARAMIN_URL, params=params, headers=HEADERS)
        if resp.status_code != 200:
            continue
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select(".item_recruit")
        for item in items:
            title_el = item.select_one(".job_tit a")
            company_el = item.select_one(".job_condition span a")
            skill_els = item.select(".job_sector a")
            if not title_el:
                continue
            href = title_el.get("href", "")
            rec_idx = href.split("rec_idx=")[-1].split("&")[0] if "rec_idx=" in href else href
            jobs.append({
                "id": f"saramin-{rec_idx}",
                "title": title_el.get_text(strip=True),
                "company": company_el.get_text(strip=True) if company_el else "",
                "skills": [s.get_text(strip=True) for s in skill_els],
                "description": "",
                "url": f"https://www.saramin.co.kr{href}",
                "source": "사람인",
            })
    seen_ids = set()
    unique = []
    for j in jobs:
        if j["id"] not in seen_ids:
            seen_ids.add(j["id"])
            unique.append(j)
    return unique
