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

## Learning and tools portal

- New portal pages are generated with `python3 scripts/build_portal.py` from `content/academy.json`, `content/glossary.json`, the existing article index and the generator's curated course/category definitions.
- Edit the generator or content files before rebuilding; do not hand-edit generated route files and then run the generator over those edits.
- Keep all existing articles in the home-page blog grid. The generator changes the shared header but does not rewrite article bodies or remove daily posts.
- The portal uses `/assets/portal.css`, `portal.js`, `portal-math.js`, `portal-tools.js`, `portal-markets.js` and `portal-widgets.js`.
- Run `python3 scripts/validate_portal.py` and `node --test tests/portal-math.test.cjs` after changes. Check any changed data integrations in a browser; an inserted iframe alone does not prove the provider display is working.
- Forex comparison tables use Frankfurter daily reference rates and must retain effective dates and methodology. Do not relabel them as real-time executable quotes.
- TradingView's generic screener uses `market: 'crypto'` for crypto pairs, not `crypto_mkt` (which can silently show the wrong market). The asset market-cap display instead uses `screener_type: 'crypto_mkt'` with `displayCurrency: 'USD'` on the same embed script.
- Learning progress and scores are local-device data, with export/import. No server-side authentication or independent forum exists. Do not add a fake login, claim cloud sync, or label a manual score as live data.
- Preserve attribution for external data displays. Paid features continue to use the original Kit terms; the portal does not introduce a new billing arrangement.

## Homepage banner
- `scripts/build_home_banner.py` builds the three-slide banner and curated Forex (33) / gold (9) paths. It is also called by the portal generator.
- Keep auto-rotation at 6500 ms on load and after manual slide selection. Only the explicit pause control stops rotation.
