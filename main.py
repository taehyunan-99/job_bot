from scrapers.wanted import scrape_wanted
from scrapers.saramin import scrape_saramin
from notifier.slack import send_slack_message

def main():
    all_jobs = []

    try:
        all_jobs += scrape_wanted()
    except Exception as e:
        print(f"원티드 크롤링 실패: {e}")

    try:
        all_jobs += scrape_saramin()
    except Exception as e:
        print(f"사람인 크롤링 실패: {e}")

    if all_jobs:
        send_slack_message(all_jobs)
    else:
        print("공고 없음")

if __name__ == "__main__":
    main()
