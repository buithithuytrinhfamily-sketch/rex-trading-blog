# -*- coding: utf-8 -*-
"""Convert 18 evenly-spaced TEXT posts into branded CARD image posts.

For each selected slot: delete the old scheduled text post, create a new scheduled
image post (card image + CTA caption) at the SAME Eastern-Time slot. Updates state
and rewrites july_full.csv.
Env: FB_PAGE_ID, FB_TOKEN (page token).
"""
import os, csv, json, time, calendar, hashlib, datetime
import urllib.request, urllib.parse, urllib.error

GRAPH = "https://graph.facebook.com/v21.0"
ROOT = "/home/user/rex-trading-blog"
CSV = os.path.join(ROOT, "facebook/schedule/july_full.csv")
STATE = os.path.join(ROOT, "facebook/schedule/.scheduled_july.json")
CARDS = json.load(open(os.path.join(ROOT, "facebook/infographics/cards/cards.json"), encoding="utf-8"))
CARD_BASE = ("https://raw.githubusercontent.com/buithithuytrinhfamily-sketch/"
             "rex-trading-blog/claude/facebook-channel-scheduling-29clrd/facebook/infographics/cards/")
PAGE = os.environ["FB_PAGE_ID"]
TOKEN = os.environ["FB_TOKEN"]
ET_OFFSET = 4


def key(row):
    return hashlib.sha1((row["Date"] + row["Time"] + row["Content"][:50]).encode()).hexdigest()[:12]


def et_ts(date, tm):
    dt = datetime.datetime.strptime(f"{date} {tm}", "%Y-%m-%d %H:%M") + datetime.timedelta(hours=ET_OFFSET)
    return calendar.timegm(dt.timetuple())


def req(path, data, method="POST"):
    body = urllib.parse.urlencode(data).encode() if data else None
    for attempt in range(4):
        try:
            r = urllib.request.Request(f"{GRAPH}/{path}", data=body, method=method)
            with urllib.request.urlopen(r, timeout=90) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")
            if e.code in (429, 500, 503) or any(f'"code":{c}' in msg for c in (4, 17, 32)):
                time.sleep(15 * (attempt + 1)); continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")
    raise RuntimeError("gave up")


def create_card_post(url, caption, ts):
    photo = req(f"{PAGE}/photos", {"url": url, "published": "false", "access_token": TOKEN})
    data = {"message": caption, "published": "false", "scheduled_publish_time": str(ts),
            "access_token": TOKEN, "attached_media[0]": json.dumps({"media_fbid": photo["id"]})}
    return req(f"{PAGE}/feed", data)


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    state = json.load(open(STATE))
    text_idx = [i for i, r in enumerate(rows) if not r.get("Media URL", "").strip()]
    # pick 18 evenly spaced text slots
    n = len(CARDS)
    pick = [text_idx[round(k * (len(text_idx) - 1) / (n - 1))] for k in range(n)]
    pick = sorted(set(pick))
    print(f"text slots: {len(text_idx)}, converting: {len(pick)}")

    ok = fail = 0
    for card, idx in zip(CARDS, pick):
        row = rows[idx]
        k = key(row)
        old = state.get(k, {}).get("id")
        ts = et_ts(row["Date"], row["Time"])
        url = CARD_BASE + card["file"]
        label = f"{row['Date']} {row['Time']} -> {card['file']}"
        try:
            if old:
                try:
                    req(old, {"access_token": TOKEN}, method="DELETE")
                except Exception as e:
                    print(f"   (delete warn {old[-6:]}: {e})")
            res = create_card_post(url, card["caption"], ts)
            # update row + state
            rows[idx]["Content"] = card["caption"]
            rows[idx]["Media URL"] = url
            if k in state:
                del state[k]
            state[key(rows[idx])] = {"id": res.get("id"), "when": f"{row['Date']} {row['Time']}", "card": card["file"]}
            ok += 1
            print(f"✅ {label} -> {res.get('id')}")
        except Exception as e:
            fail += 1
            print(f"❌ {label} -> {e}")
        json.dump(state, open(STATE, "w"), indent=0)
        time.sleep(1.3)

    with open(CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(["Date", "Time", "Content", "Link", "Media URL"])
        for r in rows:
            w.writerow([r["Date"], r["Time"], r["Content"], r.get("Link", ""), r.get("Media URL", "")])

    imgs = sum(1 for r in rows if r.get("Media URL", "").strip())
    print(f"\nDONE — swapped OK: {ok}, failed: {fail}. Image posts now: {imgs}/{len(rows)}")


if __name__ == "__main__":
    main()
