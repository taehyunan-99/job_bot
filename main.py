import logging
from scrapers.wanted import scrape_wanted
from scrapers.saramin import scrape_saramin
from notifier.slack import send_slack_message

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

SCRAPERS = [
    (scrape_wanted, "원티드"),
    (scrape_saramin, "사람인"),
]

def main():
    all_jobs = []
    for scrape_fn, name in SCRAPERS:
        try:
            all_jobs += scrape_fn()
        except Exception as e:
            log.error("%s 크롤링 실패: %s", name, e)

    if all_jobs:
        send_slack_message(all_jobs)
    else:
        log.info("공고 없음")

if __name__ == "__main__":
    main()
