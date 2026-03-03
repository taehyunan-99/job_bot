from utils.dedup import deduplicate

def test_filters_duplicate_ids():
    jobs = [
        {"id": "wanted-123", "title": "DS", "company": "카카오"},
        {"id": "saramin-456", "title": "MLE", "company": "네이버"},
        {"id": "wanted-123", "title": "DS", "company": "카카오"},
    ]
    result = deduplicate(jobs)
    assert len(result) == 2
    assert result[0]["id"] == "wanted-123"
    assert result[1]["id"] == "saramin-456"

def test_empty_jobs():
    assert deduplicate([]) == []
