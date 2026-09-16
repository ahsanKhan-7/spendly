# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

"Spendly" is a Flask expense tracker built incrementally as a step-by-step learning project. Many files are intentionally stubbed with `# Step N` comments or placeholder route bodies (e.g. `return "Logout — coming in Step 3"`) — this is expected scaffolding, not broken code. When asked to implement a feature, check whether a stub already describes the intended shape (see `database/db.py`'s docstring-style comment for `get_db()`/`init_db()`/`seed_db()`) and follow it rather than inventing a different structure.

## Commands

- Run the dev server: `python app.py` (Flask runs on port 5001, debug mode on)
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `pytest` (test suite not yet written; `pytest` and `pytest-flask` are in requirements.txt for when it is added)

There is no build step, linter, or frontend bundler configured — templates and static assets are served directly by Flask.

## Architecture

- `app.py` — single Flask application object with all routes defined directly on it (no blueprints). Routes for implemented pages (`/`, `/register`, `/login`, `/terms`, `/privacy`) render templates; routes for unbuilt features (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`) return plain placeholder strings. When implementing one of these, replace the placeholder body but keep the route signature.
- `database/db.py` — intended to hold `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (idempotent `CREATE TABLE IF NOT EXISTS` schema setup), and `seed_db()` (sample data for dev). Not yet implemented. The SQLite file (`expense_tracker.db`) is gitignored and created locally, not committed.
- `templates/` — Jinja2 templates. `base.html` defines the shared layout (nav, footer, font imports) with `{% block title %}`, `{% block head %}`, `{% block content %}`, and `{% block scripts %}` for child templates to override. All page templates (`landing.html`, `login.html`, `register.html`, `terms.html`, `privacy.html`) extend `base.html`.
- `static/css/style.css` — single global stylesheet (no preprocessor/build step) covering all pages.
- `static/js/main.js` — single global script file; currently handles the landing page's "how it works" YouTube modal. New JS should be added here or as additional plain `<script>` files unless a build tool is introduced.

## Conventions

- Currency/copy uses Pakistani Rupee framing (e.g. footer tagline "Track every rupee"); keep placeholder content/locale consistent with this when adding copy.
- Routes are named after their template/purpose (`landing`, `register`, `login`, `terms`, `privacy`) and are referenced via `url_for()` in templates rather than hardcoded paths.
