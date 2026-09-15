# REX Trading Signal

## Existing production site

- Static HTML published by GitHub Pages from `main`, repository root `/`.
- Keep `CNAME` set to `rextradingsignal.com`. Do not migrate hosting or move article URLs.
- A separate daily publisher adds articles. Run `git pull --ff-only` before editing. Before pushing, fetch and rebase your committed changes onto the latest `origin/main`; resolve conflicts without dropping the publisher's work.

## Daily publishing compatibility

- Articles live as `.html` files in the repository root.
- Keep the home-page `section#blog`, `.blog__grid`, and `.post` links. New cards belong first inside `.blog__grid` and should contain `.post__cat`, `.post__body`, `h3`, and `.post__more` as existing cards do.
- The homepage displays the first six cards. Keep all older cards in the markup; the full article library is linked below the feed.
- `articles/index.html` has a complete static fallback and search. `assets/article-library.js` reads the home-page cards to discover newly published articles if the static archive has not yet been refreshed.
- Update `articles/_danh-sach.json` and the static list in `articles/index.html` when practical. Preserve fields `url`, `title`, `desc`, and `date`; `category` and `image` are optional additions.
- New article pages should link `/assets/reading.css` after their inline styles and include a navigation link to `/articles/`.
- Do not replace `/assets/editorial.css`, `/assets/reading.css`, or `/assets/article-library.js` with the old draft theme. `index-improved.html` is an unused draft.

## Validation

- Check local links and assets, JavaScript syntax, navigation, and the article list.
- Preserve article copy, canonical URLs, analytics, subscription endpoint, Telegram destinations, prices, guarantee terms, and testimonials unless explicitly asked to change them.
- Never submit test email addresses to the live subscription endpoint.
