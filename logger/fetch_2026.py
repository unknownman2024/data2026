import requests
import os
from datetime import datetime, timedelta
import pytz
import time

# ==========================
# CONFIG
# ==========================

IST = pytz.timezone("Asia/Kolkata")

START_DATE = "2026-02-02"

# Force overwrite
FORCE_DOWNLOAD = True

# Sources
SOURCES = {
    "daily": {
        "summary": "https://raw.githubusercontent.com/unknownman2024/assetz/refs/heads/main/daily/data/{compact}/finalsummary.json",
        "detailed": "https://raw.githubusercontent.com/unknownman2024/assetz/refs/heads/main/daily/data/{compact}/finaldetailed.json"
    },
    "advance": {
        "summary": "https://raw.githubusercontent.com/unknownman2024/assetz/refs/heads/main/advance/data/{compact}/finalsummary.json",
        "detailed": "https://raw.githubusercontent.com/unknownman2024/assetz/refs/heads/main/advance/data/{compact}/finaldetailed.json"
    }
}

MAX_RETRIES = 3
TIMEOUT = 30


# ==========================
# UTILS
# ==========================

def make_dir(path):
    os.makedirs(path, exist_ok=True)


def download(url, path):
    """Force download (overwrite always)"""

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(url, timeout=TIMEOUT)

            if r.status_code == 200:
                with open(path, "wb") as f:
                    f.write(r.content)

                print(f"🔁 Overwritten: {path}")
                return True

            else:
                print(f"⚠️ {r.status_code} for {url}")

        except Exception as e:
            print(f"❌ Error ({attempt}):", url, e)

        time.sleep(1.5 * attempt)

    print(f"🚫 Failed after retries: {url}")
    return False


def get_last_allowed_date():
    now_ist = datetime.now(IST)
    return (now_ist - timedelta(days=1)).date()


# ==========================
# CORE FETCH
# ==========================

def process_date(cur):

    year = cur.strftime("%Y")
    md = cur.strftime("%m-%d")
    compact = cur.strftime("%Y%m%d")

    print(f"\n📅 Processing: {cur}")

    for mode in ["daily", "advance"]:

        base_dir = f"{mode}/data/{year}"
        make_dir(base_dir)

        sum_path = f"{base_dir}/{md}_finalsummary.json"
        det_path = f"{base_dir}/{md}_finaldetailed.json"

        summary_url = SOURCES[mode]["summary"].format(compact=compact)
        detailed_url = SOURCES[mode]["detailed"].format(compact=compact)

        print(f"🔹 {mode.upper()} Overwriting...")

        # Always overwrite
        download(summary_url, sum_path)
        download(detailed_url, det_path)


# ==========================
# MAIN
# ==========================

def main():

    start = datetime.strptime(START_DATE, "%Y-%m-%d").date()
    end = get_last_allowed_date()

    print("🚀 Overwriting till:", end)

    cur = start

    while cur <= end:
        process_date(cur)
        cur += timedelta(days=1)


# ==========================
# RUN
# ==========================

if __name__ == "__main__":
    main()
