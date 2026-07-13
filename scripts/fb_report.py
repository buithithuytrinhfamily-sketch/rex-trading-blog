#!/usr/bin/env python3
"""
Weekly performance report for a Facebook Page.

Pulls every PUBLISHED post's engagement (reactions + comments + shares, and reach
where available), ranks them, and prints what's working so you can double down.

Env: FB_PAGE_ID, FB_TOKEN (page token with pages_read_engagement).
Optional arg: number of posts to scan (default 50).

Only uses the Python standard library.
"""
import os, sys, json, urllib.request, urllib.parse, urllib.error, datetime

GRAPH = "https://graph.facebook.com/v21.0"
PAGE = os.environ["FB_PAGE_ID"]
TOKEN = os.environ["FB_TOKEN"]
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 50


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def reach_of(post_id):
    try:
        u = f"{GRAPH}/{post_id}/insights/post_impressions_unique?access_token={urllib.parse.quote(TOKEN)}"
        d = get(u)
        vals = d.get("data", [])
        if vals and vals[0].get("values"):
            return vals[0]["values"][0].get("value", 0)
    except Exception:
        pass
    return None


def main():
    fields = "id,created_time,message,permalink_url,reactions.summary(true),comments.summary(true),shares"
    u = (f"{GRAPH}/{PAGE}/published_posts?fields={urllib.parse.quote(fields)}"
         f"&limit={LIMIT}&access_token={urllib.parse.quote(TOKEN)}")
    try:
        data = get(u).get("data", [])
    except urllib.error.HTTPError as e:
        print("ERROR:", e.read().decode("utf-8", "replace")); return

    if not data:
        print("Chưa có bài nào ĐÃ ĐĂNG (published) trên trang.")
        print("→ Các bài đang ở dạng LÊN LỊCH sẽ có số liệu sau khi Facebook tự đăng.")
        return

    rows = []
    for p in data:
        rx = p.get("reactions", {}).get("summary", {}).get("total_count", 0)
        cm = p.get("comments", {}).get("summary", {}).get("total_count", 0)
        sh = p.get("shares", {}).get("count", 0)
        eng = rx + cm + sh
        rows.append({
            "id": p["id"], "date": p.get("created_time", "")[:10],
            "msg": (p.get("message", "") or "").replace("\n", " ")[:55],
            "rx": rx, "cm": cm, "sh": sh, "eng": eng,
            "url": p.get("permalink_url", ""),
        })
    rows.sort(key=lambda r: r["eng"], reverse=True)

    print(f"\n===== REX — BÁO CÁO HIỆU QUẢ ({len(rows)} bài đã đăng) =====\n")
    tot = {k: sum(r[k] for r in rows) for k in ("rx", "cm", "sh", "eng")}
    print(f"Tổng: {tot['rx']} reactions · {tot['cm']} comments · {tot['sh']} shares "
          f"· {tot['eng']} tương tác\n")
    print("TOP bài tương tác cao nhất:")
    for i, r in enumerate(rows[:10], 1):
        reach = reach_of(r["id"])
        rtxt = f" · reach {reach}" if reach is not None else ""
        print(f"{i:2}. [{r['date']}] 👍{r['rx']} 💬{r['cm']} 🔁{r['sh']}{rtxt}  | {r['msg']}")
    print("\n💡 Nhân bản công thức của các bài top: định dạng, hook, chủ đề, giờ đăng.")


if __name__ == "__main__":
    main()
