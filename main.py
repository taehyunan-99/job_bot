from scrapers.wanted import scrape_wanted
from scrapers.saramin import scrape_saramin
from notifier.slack import send_slack_message

def main():
    all_jobs = []
    all_jobs += scrape_wanted()
    all_jobs += scrape_saramin()

    if all_jobs:
        send_slack_message(all_jobs)
    else:
        print("공고 없음")

if __name__ == "__main__":
    main()
