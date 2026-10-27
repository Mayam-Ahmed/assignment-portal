import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone


def parse_results(xml_path):
    tests = []
    if not os.path.exists(xml_path):
        return tests
    root = ET.parse(xml_path).getroot()
    for tc in root.iter("testcase"):
        result, message = "passed", None
        for tag in ("failure", "error"):
            el = tc.find(tag)
            if el is not None:
                result = "failed"
                message = (el.get("message") or el.text or "").strip()[:500]
        if tc.find("skipped") is not None:
            result = "skipped"
        tests.append({"name": tc.get("name"), "result": result, "failure_message": message})
    return tests


def main():
    tests = parse_results("ci-results.xml")
    passed = sum(1 for t in tests if t["result"] == "passed")
    failed = sum(1 for t in tests if t["result"] == "failed")
    report = {
        "repository": os.environ.get("REPO_NAME", "local-run"),
        "branch": os.environ.get("BRANCH", "local"),
        "commit_sha": os.environ.get("COMMIT_SHA", "local"),
        "run_id": os.environ.get("RUN_ID", "local"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overall_status": "passed" if tests and failed == 0 else "failed",
        "summary": {"total": len(tests), "passed": passed, "failed": failed},
        "tests": tests,
    }

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    url = os.environ.get("RECEIVER_URL", "http://127.0.0.1:5001/report")
    req = urllib.request.Request(
        url, data=json.dumps(report).encode(), headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print("Report sent to receiver, HTTP", resp.status)
    except Exception as e:
        print("FAILED to send report:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()