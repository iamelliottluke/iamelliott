# IAMELLIOTT

Personal creative portfolio for Elliott Luke: creative direction, film, events, campaigns, writing and practical solutions.

**Live website:** https://iamelliott.me  
**Production source:** `main` (GitHub Pages)  
**Domain management:** Cloudflare DNS; GitHub Pages provides HTTPS  
**Contact form:** Formspree (notification settings managed separately)

## Project structure

- `index.html` — homepage, About, selected work, process and contact.
- `work/*.html` — six portfolio case studies, each with its own visual identity.
- `media.js` — source-of-truth filename map for media referenced across pages.
- `site.js`, `build03.js` — client-side media, navigation and behaviour.
- `site.css`, `build03.css`, `build04.css` — **all three are required** and load in order; do not delete older layers without a verified CSS refactor.
- `shared.css` — retained for older pages.
- `assets readme.txt` — detailed asset inventory and usage documentation.
- `EDITING_GUIDE.md` — safe editing and publishing instructions.
- `tests/site_visual.py` and `.github/workflows/site-qa.yml` — responsive browser regression checks on pull requests.

## Updating the website

1. Create a short-lived branch from `main`.
2. Change copy in the relevant HTML file, or replace an asset and update its filename in `media.js`.
3. Open a pull request targeting `main`. The Site QA workflow checks representative viewport sizes.
4. Review the visual changes, then merge.
5. Check that the **GitHub Pages deployment** for the merged commit succeeds; a merged pull request alone does not prove publication.

For actual file usage, see `assets readme.txt`. Old pages and media files are intentionally retained to avoid breaking external links and historical work. Do not delete assets based solely on their absence from the current homepage.
