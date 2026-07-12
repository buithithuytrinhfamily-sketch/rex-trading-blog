#!/usr/bin/env python3
"""
Helper: turn a SHORT-lived token into a LONG-lived Page Access Token.

You need (all from developers.facebook.com):
  - App ID and App Secret  (App → Settings → Basic)
  - A short-lived User token with permissions:
        pages_show_list, pages_manage_posts, pages_read_engagement
    (grab it from the Graph API Explorer)

Run:
    python scripts/get_page_token.py <APP_ID> <APP_SECRET> <SHORT_USER_TOKEN>

It prints a long-lived Page Access Token for each page you manage.
Copy the token for the page you want and paste it into GitHub Secrets.
(Page tokens derived from a long-lived user token typically do not expire
while you remain an admin — but if posting ever 401s, just re-run this.)
"""
import sys, json, urllib.request, urllib.parse

GRAPH = "https://graph.facebook.com/v21.0"


def get(path, params):
    url = f"{GRAPH}/{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    app_id, app_secret, short_token = sys.argv[1], sys.argv[2], sys.argv[3]

    # 1) short-lived user token -> long-lived user token (~60 days)
    ll = get("oauth/access_token", {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token,
    })
    ll_user = ll["access_token"]
    print("\n✅ Long-lived USER token acquired.\n")

    # 2) list pages -> each has its own long-lived Page token
    pages = get("me/accounts", {"access_token": ll_user})
    data = pages.get("data", [])
    if not data:
        print("No pages found. Make sure the token has pages_show_list and you admin a page.")
        return
    print("Pages you manage (use the token of the one you want):\n")
    for p in data:
        print(f"  • {p.get('name')}")
        print(f"    PAGE_ID   = {p.get('id')}")
        print(f"    PAGE_TOKEN= {p.get('access_token')}\n")


if __name__ == "__main__":
    main()
