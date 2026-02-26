from utils.dedup import filter_new_jobs

def test_filters_seen_jobs():
    jobs = [
        {"id": "wanted-123", "title": "DS", "company": "카카오"},
        {"id": "saramin-456", "title": "MLE", "company": "네이버"},
    ]
    seen = {"wanted-123"}
    new_jobs, updated_seen = filter_new_jobs(jobs, seen)
    assert len(new_jobs) == 1
    assert new_jobs[0]["id"] == "saramin-456"
    assert "saramin-456" in updated_seen
    assert "wanted-123" in updated_seen

def test_empty_jobs():
    new_jobs, updated_seen = filter_new_jobs([], set())
    assert new_jobs == []
    assert updated_seen == set()
