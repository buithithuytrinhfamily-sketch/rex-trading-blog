# -*- coding: utf-8 -*-
"""Create scheduled posts on a Facebook Page from july_full.csv via Graph API.

Env: FB_PAGE_ID, FB_TOKEN
Args: 'test' = only schedule the first pending row (dry validation of timing).
State file (.scheduled_july.json) records already-scheduled rows so re-runs skip them.
"""
import os, sys, csv, json, time, calendar, hashlib, datetime
import urllib.request, urllib.parse, urllib.error

GRAPH = "https://graph.facebook.com/v21.0"
ROOT = "/home/user/rex-trading-blog"
CSV = os.path.join(ROOT, "facebook/schedule/july_full.csv")
STATE = os.path.join(ROOT, "facebook/schedule/.scheduled_july.json")

PAGE_ID = os.environ["FB_PAGE_ID"]
TOKEN = os.environ["FB_TOKEN"]
TEST = len(sys.argv) > 1 and sys.argv[1] == "test"


def api(path, data):
    body = urllib.parse.urlencode(data).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request(f"{GRAPH}/{path}", data=body, method="POST")
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")
            # rate limit codes -> back off and retry
            if e.code in (429, 500, 503) or '"code":4' in msg or '"code":17' in msg or '"code":32' in msg or '"code":613' in msg:
                wait = 20 * (attempt + 1)
                print(f"    rate/limit, wait {wait}s… ({msg[:120]})")
                time.sleep(wait)
                continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")
    raise RuntimeError("gave up after retries")


def sched_ts(date, tm):
    dt_vn = datetime.datetime.strptime(f"{date} {tm}", "%Y-%m-%d %H:%M")
    dt_utc = dt_vn - datetime.timedelta(hours=7)  # VN = UTC+7
    return calendar.timegm(dt_utc.timetuple())


def key(row):
    return hashlib.sha1((row["Date"] + row["Time"] + row["Content"][:50]).encode()).hexdigest()[:12]


def schedule_row(row):
    ts = sched_ts(row["Date"], row["Time"])
    media = [u.strip() for u in row.get("Media URL", "").split(",") if u.strip()]
    if media:
        ids = []
        for u in media:
            res = api(f"{PAGE_ID}/photos", {"url": u, "published": "false", "access_token": TOKEN})
            ids.append(res["id"])
        data = {"message": row["Content"], "published": "false",
                "scheduled_publish_time": str(ts), "access_token": TOKEN}
        for i, pid in enumerate(ids):
            data[f"attached_media[{i}]"] = json.dumps({"media_fbid": pid})
        return api(f"{PAGE_ID}/feed", data)
    else:
        return api(f"{PAGE_ID}/feed", {"message": row["Content"], "published": "false",
                                       "scheduled_publish_time": str(ts), "access_token": TOKEN})


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    done = json.load(open(STATE)) if os.path.exists(STATE) else {}
    ok = fail = 0
    for row in rows:
        k = key(row)
        if k in done:
            continue
        label = f"{row['Date']} {row['Time']} {'[IMG]' if row.get('Media URL') else '[TXT]'}"
        try:
            res = schedule_row(row)
            done[k] = {"id": res.get("id"), "when": f"{row['Date']} {row['Time']}"}
            ok += 1
            print(f"✅ {label} -> {res.get('id')}")
        except Exception as e:
            fail += 1
            print(f"❌ {label} -> {e}")
        json.dump(done, open(STATE, "w"), indent=0)
        if TEST:
            print("TEST mode: stopping after 1 post.")
            break
        time.sleep(1.5)
    print(f"\nDONE — scheduled OK: {ok}, failed: {fail}, total in state: {len(done)}")


if __name__ == "__main__":
    main()
