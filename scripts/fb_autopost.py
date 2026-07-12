#!/usr/bin/env python3
"""
Auto-post to Facebook Pages via the Graph API.

- Reads pages.json (list of pages + their schedule CSV + secret env names).
- For each page whose secrets are present, posts every row whose Date is due
  (<= today in Asia/Ho_Chi_Minh) and not already posted.
- Supports multi-photo posts (comma-separated Media URL), plain text, and links.
- Tracks posted rows in a small JSON state file so nothing is posted twice.

Only uses the Python standard library — no pip install needed.
"""
import os, csv, json, sys, time, hashlib, datetime, urllib.request, urllib.parse, urllib.error

GRAPH = "https://graph.facebook.com/v21.0"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root


def vn_today():
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).date()


def _post(url, data, tries=3):
    body = urllib.parse.urlencode(data).encode()
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=body, method="POST")
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = e.read().decode("utf-8", "replace")
            print(f"  ! HTTP {e.code}: {last}")
            if e.code in (400, 401, 403):  # bad token / permission — don't retry
                break
        except Exception as e:
            last = str(e)
            print(f"  ! error: {last}")
        time.sleep(2 * (i + 1))
    raise RuntimeError(f"POST failed: {last}")


def upload_unpublished_photo(page_id, token, image_url):
    res = _post(f"{GRAPH}/{page_id}/photos",
                {"url": image_url, "published": "false", "access_token": token})
    return res["id"]


def post_row(page_id, token, message, link, media_urls):
    media = [u.strip() for u in media_urls if u.strip()]
    if not media:
        data = {"message": message, "access_token": token}
        if link:
            data["link"] = link
        return _post(f"{GRAPH}/{page_id}/feed", data)
    # upload each image unpublished, then publish one feed post attaching them all
    ids = [upload_unpublished_photo(page_id, token, u) for u in media]
    data = {"message": message, "access_token": token}
    for i, pid in enumerate(ids):
        data[f"attached_media[{i}]"] = json.dumps({"media_fbid": pid})
    return _post(f"{GRAPH}/{page_id}/feed", data)


def row_key(row):
    raw = (row.get("Date", "") + row.get("Time", "") + row.get("Content", "")[:60])
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def run_page(page):
    name = page["name"]
    page_id = os.environ.get(page["page_id_env"], "").strip()
    token = os.environ.get(page["token_env"], "").strip()
    if not page_id or not token:
        print(f"[{name}] secrets missing ({page['page_id_env']}/{page['token_env']}) — skipping")
        return 0
    csv_path = os.path.join(HERE, page["csv"])
    if not os.path.exists(csv_path):
        print(f"[{name}] schedule not found: {page['csv']} — skipping")
        return 0
    state_path = os.path.join(HERE, page["state"])
    posted = set(json.load(open(state_path))) if os.path.exists(state_path) else set()

    today = vn_today()
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
    n = 0
    for row in rows:
        try:
            d = datetime.date.fromisoformat(row["Date"].strip())
        except Exception:
            continue
        if d > today:
            continue                      # not due yet
        k = row_key(row)
        if k in posted:
            continue                      # already posted
        media = row.get("Media URL", "").split(",")
        print(f"[{name}] posting row dated {row['Date']} ({len(media)} media)…")
        res = post_row(page_id, token, row.get("Content", ""), row.get("Link", "").strip(), media)
        print(f"[{name}]   -> {res}")
        posted.add(k)
        n += 1
    json.dump(sorted(posted), open(state_path, "w"), indent=0)
    print(f"[{name}] done — {n} new post(s)")
    return n


def main():
    cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages.json")))
    total = 0
    for page in cfg:
        try:
            total += run_page(page)
        except Exception as e:
            print(f"[{page.get('name','?')}] FAILED: {e}")
    print(f"TOTAL new posts: {total}")


if __name__ == "__main__":
    main()
