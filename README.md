# Kaplun Financial Group website

Static site for kaplunfinancial.com.

- Edit content in `build.py`, `pages_unique.py`, `faq_data.py`, `growth.py` and `src/styles.css`.
- `growth.py` holds SEO (page titles/descriptions, schema, sitemap), city pages, free tools and lead forms. `SITE_URL`, `HOURS` and `FORM_ACTION` are set at its top.
- Favicons and the social share image live in `img/brand/` (delete them and rebuild with Pillow installed to redraw).
- `python build.py` writes the deployable site to `site/` (and a single-file preview to `preview/`).
- Every push to `main` builds and deploys to GitHub Pages automatically (`.github/workflows/pages.yml`).
