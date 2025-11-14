import json
import jsonlines


def convert_to_jsonl(raw_file, output_file):
    """Convert Jira issues into JSONL format"""
    
    # Load raw JSON
    with open(raw_file, "r", encoding="utf-8") as f:
        issues = json.load(f)

    # Create JSONL file
    with jsonlines.open(output_file, "w") as writer:
        for issue in issues:
            fields = issue.get("fields", {})

            obj = {
                "id": issue.get("key"),
                "title": fields.get("summary", ""),
                "project": fields.get("project", {}).get("key"),
                "status": fields.get("status", {}).get("name"),
                "priority": fields.get("priority", {}).get("name") if fields.get("priority") else None,
                "reporter": fields.get("reporter", {}).get("displayName") if fields.get("reporter") else None,
                "description": fields.get("description", ""),
                "comments": [
                    c.get("body", "") for c in fields.get("comment", {}).get("comments", [])
                ],
                # LLM tasks
                "task_summarization": f"Summarize the issue: {fields.get('summary', '')}",
                "task_classification": f"Classify issue priority: {fields.get('summary', '')}"
            }

            writer.write(obj)

    print(f"Saved transformed file: {output_file}")


if __name__ == "__main__":
    PROJECTS = ["spark", "hadoop", "kafka"]

    for proj in PROJECTS:
        raw = f"{proj}_raw.json"
        output = f"{proj}_jira.jsonl"
        convert_to_jsonl(raw, output)

    print("\n All JSONL transformation completed!")
