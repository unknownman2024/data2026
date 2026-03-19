import requests
import json
import os
from datetime import datetime, timedelta

BASE_URL = "https://filmynewsnetwork.com/api/all-box-office?date={}"

START_DATE = "20260101"
END_DATE = "20260201"

OUTPUT_BASE = "advance/data/2026"


def to_float(val):
    if isinstance(val, (int, float)):
        return float(val)
    return val


def convert_json1_to_json2(data):
    output = {
        "last_updated": data.get("last_updated"),
        "movies": {}
    }

    for movie in data.get("movies", []):
        movie_name = movie.get("movie")
        movie_data = {}

        for key, value in movie.items():
            if key == "movie":
                continue

            if key in ["gross", "occupancy"]:
                value = to_float(value)

            if key in ["details", "Chain_details"] and isinstance(value, list):
                new_list = []
                for item in value:
                    new_item = {}
                    for k, v in item.items():
                        if k in ["gross", "occupancy"]:
                            v = to_float(v)
                        new_item[k] = v
                    new_list.append(new_item)
                value = new_list

            movie_data[key] = value

        output["movies"][movie_name] = movie_data

    return output


def daterange(start_date, end_date):
    start = datetime.strptime(start_date, "%Y%m%d")
    end = datetime.strptime(end_date, "%Y%m%d")

    while start <= end:
        yield start
        start += timedelta(days=1)


def main():
    os.makedirs(OUTPUT_BASE, exist_ok=True)

    for date_obj in daterange(START_DATE, END_DATE):
        date_str = date_obj.strftime("%Y%m%d")
        display_date = date_obj.strftime("%m-%d")

        url = BASE_URL.format(date_str)

        try:
            print(f"📡 Fetching {date_str}...")
            res = requests.get(url, timeout=20)
            res.raise_for_status()

            json1 = res.json()
            json2 = convert_json1_to_json2(json1)

            output_file = f"{OUTPUT_BASE}/{display_date}_finalsummary.json"

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(json2, f, indent=2, ensure_ascii=False)

            print(f"✅ Saved: {output_file}")

        except Exception as e:
            print(f"❌ Failed for {date_str}: {e}")


if __name__ == "__main__":
    main()
