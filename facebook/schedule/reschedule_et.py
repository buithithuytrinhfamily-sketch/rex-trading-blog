# -*- coding: utf-8 -*-
"""Move all scheduled July posts to US Eastern Time (EDT = UTC-4 in July).

The daily slot labels (08:00/12:30/18:00/20:30) are now interpreted as ET.
Env: FB_TOKEN (page token), FB_PAGE_ID (unused for edits, ids come from state).
"""
import os, csv, json, time, calendar, hashlib, datetime
import urllib.request, urllib.parse, urllib.error

GRAPH = "https://graph.facebook.com/v21.0"
ROOT = "/home/user/rex-trading-blog"
CSV = os.path.join(ROOT, "facebook/schedule/july_full.csv")
STATE = os.path.join(ROOT, "facebook/schedule/.scheduled_july.json")
TOKEN = os.environ["FB_TOKEN"]
ET_OFFSET = 4  # EDT = UTC-4 (July)


def key(row):
    return hashlib.sha1((row["Date"] + row["Time"] + row["Content"][:50]).encode()).hexdigest()[:12]


def et_ts(date, tm):
    dt_et = datetime.datetime.strptime(f"{date} {tm}", "%Y-%m-%d %H:%M")
    dt_utc = dt_et + datetime.timedelta(hours=ET_OFFSET)  # UTC = ET + 4
    return calendar.timegm(dt_utc.timetuple())


def api(path, data):
    body = urllib.parse.urlencode(data).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request(f"{GRAPH}/{path}", data=body, method="POST")
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")
            if e.code in (429, 500, 503) or '"code":4' in msg or '"code":17' in msg or '"code":32' in msg:
                time.sleep(15 * (attempt + 1)); continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")
    raise RuntimeError("gave up")


def main():
    state = json.load(open(STATE))
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    ok = fail = 0
    for row in rows:
        k = key(row)
        rec = state.get(k)
        if not rec:
            print(f"? no id for {row['Date']} {row['Time']}"); continue
        pid = rec["id"]
        ts = et_ts(row["Date"], row["Time"])
        try:
            api(pid, {"scheduled_publish_time": str(ts), "access_token": TOKEN})
            ok += 1
            print(f"✅ {row['Date']} {row['Time']} ET  (id …{pid[-6:]})")
        except Exception as e:
            fail += 1
            print(f"❌ {row['Date']} {row['Time']} -> {e}")
        time.sleep(0.8)
    print(f"\nRescheduled to ET — OK: {ok}, failed: {fail}")


if __name__ == "__main__":
    main()
