import requests
import json
from tqdm import tqdm

BASE_URL = "https://issues.apache.org/jira/rest/api/2/search"


def fetch_issues(project_key, start=0, max_results=50):
    """Fetch issues from a Jira project with pagination + retry."""
    params = {
        "jql": f"project={project_key}",
        "startAt": start,
        "maxResults": max_results
    }

    for retry in range(3):
        try:
            r = requests.get(BASE_URL, params=params, timeout=10)

            # Too many requests
            if r.status_code == 429:
                print("Rate limit hit. Waiting 5 seconds...")
                import time; time.sleep(5)
                continue

            # Server error
            if r.status_code >= 500:
                continue

            return r.json()

        except Exception as e:
            print("Network error, retrying:", e)

    return {"issues": []}


def scrape_project(project_key):
    print(f"\n Scraping project: {project_key}")

    all_issues = []
    start = 0
    total = 1

    while start < total:
        data = fetch_issues(project_key, start)
        issues = data.get("issues", [])
        total = data.get("total", 0)

        all_issues.extend(issues)
        start += 50


    # Save raw file
    with open(f"{project_key.lower()}_raw.json", "w", encoding="utf-8") as f:
        json.dump(all_issues, f, indent=2)

 
    return all_issues


if __name__ == "__main__":
    PROJECTS = ["SPARK", "HADOOP", "KAFKA"]

    for proj in PROJECTS:
        scrape_project(proj)

    print(" Scraping complete")
