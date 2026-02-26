def filter_new_jobs(jobs, seen: set):
    new_jobs = []
    for job in jobs:
        if job["id"] not in seen:
            new_jobs.append(job)
            seen.add(job["id"])
    return new_jobs, seen
