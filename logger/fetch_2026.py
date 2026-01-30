import requests
import os
from datetime import datetime, timedelta
import pytz


# ==========================
# CONFIG
# ==========================

IST = pytz.timezone("Asia/Kolkata")

START_DATE = "2026-01-01"

# New Source
SUMMARY_URL = "https://raw.githubusercontent.com/unknownman2024/assetz/refs/heads/main/advance/data/{compact}/finalsummary.json"

DETAILED_URL = "https://raw.githubusercontent.com/unknownman2024/assetz/refs/heads/main/advance/data/{compact}/finaldetailed.json"


# ==========================
# UTILS
# ==========================

def make_dir(path):
    os.makedirs(path, exist_ok=True)


def download(url, path):

    try:
        r = requests.get(url, timeout=30)

        if r.status_code == 200:

            with open(path, "wb") as f:
                f.write(r.content)

            print("Saved:", path)
            return True

        return False

    except Exception as e:
        print("Error:", url, e)
        return False


def get_last_allowed_date():
    now_ist = datetime.now(IST)
    return (now_ist - timedelta(days=1)).date()


# ==========================
# MAIN
# ==========================

def main():

    start = datetime.strptime(START_DATE, "%Y-%m-%d").date()

    end = get_last_allowed_date()

    print("Fetch till:", end)

    cur = start

    while cur <= end:

        year = cur.strftime("%Y")
        md = cur.strftime("%m-%d")
        compact = cur.strftime("%Y%m%d")

        print("\nProcessing:", cur)

        # ======================
        # BOXOFFICE
        # ======================

        box_dir = f"daily/data/{year}"
        make_dir(box_dir)

        box_sum = f"{box_dir}/{md}_finalsummary.json"
        box_det = f"{box_dir}/{md}_finaldetailed.json"

        # Skip if already exists
        if os.path.exists(box_sum) and os.path.exists(box_det):
            print("Skip boxoffice (exists)")
        else:

            s_url = SUMMARY_URL.format(compact=compact)
            d_url = DETAILED_URL.format(compact=compact)

            if not os.path.exists(box_sum):
                download(s_url, box_sum)

            if not os.path.exists(box_det):
                download(d_url, box_det)


        # ======================
        # ADVANCE
        # ======================

        adv_dir = f"advance/data/{year}"
        make_dir(adv_dir)

        adv_sum = f"{adv_dir}/{md}_finalsummary.json"
        adv_det = f"{adv_dir}/{md}_finaldetailed.json"

        if os.path.exists(adv_sum) and os.path.exists(adv_det):
            print("Skip advance (exists)")
        else:

            s_url = SUMMARY_URL.format(compact=compact)
            d_url = DETAILED_URL.format(compact=compact)

            if not os.path.exists(adv_sum):
                download(s_url, adv_sum)

            if not os.path.exists(adv_det):
                download(d_url, adv_det)


        cur += timedelta(days=1)


# ==========================
# RUN
# ==========================

if __name__ == "__main__":
    main()
