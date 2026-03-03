def deduplicate(jobs: list) -> list:
    """Return jobs with duplicate IDs removed, preserving order."""
    seen = set()
    unique = []
    for job in jobs:
        if job["id"] not in seen:
            seen.add(job["id"])
            unique.append(job)
    return unique
