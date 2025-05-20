import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

LOG_FILE = "output/log.txt"
RULE_FILE = "output/extracted_rules.json"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} - {msg}\n")
    print(msg)

def extract_rules(text):
    rules = []
    if "Henson trust" in text or "absolute discretion" in text or "disability" in text:
        rules.append({
            "source": "S.A. v. Metro Vancouver Housing Corp., 2019 SCC 4",
            "rule": "Henson trusts give absolute discretion to the trustee and are not counted as assets of the beneficiary for eligibility purposes unless policies explicitly include them.",
            "tags": ["Henson trust", "disability", "estate planning"]
        })
    return rules

def fetch_case_text():
    url = "https://scc-csc.lexum.com/scc-csc/scc-csc/en/item/17484/index.do"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            log(f"Failed to fetch case: HTTP {res.status_code}")
            return

        soup = BeautifulSoup(res.content, "html.parser")
        paragraphs = soup.select("div#decision p")
        full_text = "\n".join(p.get_text() for p in paragraphs)
        if not full_text:
            log("Could not extract decision text from page.")
            return

        log("Successfully fetched case content.")
        rules = extract_rules(full_text)
        with open(RULE_FILE, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2)
        log(f"Extracted {len(rules)} rules from case.")
    except Exception as e:
        log(f"Error fetching case: {e}")

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    fetch_case_text()
