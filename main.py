import json
from scrapers.wanted import scrape_wanted
from scrapers.saramin import scrape_saramin

from notifier.slack import send_slack_message
from utils.dedup import filter_new_jobs

SEEN_JOBS_PATH = "seen_jobs.json"

def load_seen_jobs():
    with open(SEEN_JOBS_PATH, "r") as f:
        return set(json.load(f))

def save_seen_jobs(seen):
    with open(SEEN_JOBS_PATH, "w") as f:
        json.dump(list(seen), f)

def main():
    seen = load_seen_jobs()

    all_jobs = []
    all_jobs += scrape_wanted()
    all_jobs += scrape_saramin()


    new_jobs, updated_seen = filter_new_jobs(all_jobs, seen)
    save_seen_jobs(updated_seen)

    if new_jobs:
        send_slack_message(new_jobs)
    else:
        print("새 공고 없음")

if __name__ == "__main__":
    main()
