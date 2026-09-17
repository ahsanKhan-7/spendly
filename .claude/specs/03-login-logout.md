# Spec: Login and Logout

## Overview
Implements session-based authentication for Spendly. The `/login` route
currently only renders the sign-in form (GET); this step adds the POST
handler that verifies the submitted email/password against the `users`
table and starts a Flask session. It also implements `/logout`, which
currently returns a placeholder string, so it clears that session. This is
the first step that reads from the `users` table to authenticate someone
(rather than write to it, as Step 2 did), and it introduces the concept of
"logged in" to the app, which the shared nav in `base.html` needs to reflect.

## Depends on
- Step 1 (database setup) — `users` table, `get_db()`, `init_db()`.
- Step 2 (registration) — the `/register` flow that creates the accounts
  being signed into here.

## Routes
- `GET /login` — renders the sign-in form — public (already implemented, unchanged)
- `POST /login` — validates credentials, starts a session, redirects — public
- `GET /logout` — clears the session, redirects to landing — logged-in (route signature unchanged; safe to hit while logged out, just redirects)

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`,
`password_hash`, `created_at`) already supports login — the route only
needs to `SELECT` by email and verify the hash. Verified against
`database/db.py` — no new columns or tables required.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — reuse the existing `{% if error %}` block to
    surface invalid-credentials errors returned by the route. No structural
    changes needed.
  - `templates/base.html` — the nav currently hardcodes "Sign in" /
    "Get started" links for every visitor. Make it session-aware: when
    `session.get('user_id')` is set, show a "Profile" link (to the existing
    `/profile` placeholder) and a "Logout" link (`url_for('logout')`)
    instead of the sign-in/register links.

## Files to change
- `app.py` — set `app.secret_key` (required for Flask sessions), extend
  `/login` to accept `GET` and `POST` with credential validation and
  session creation, and implement `/logout` to clear the session.
- `templates/login.html` — display the invalid-credentials error.
- `templates/base.html` — conditionally render nav links based on session
  state.

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only — no string-formatted SQL.
- Passwords verified with `werkzeug.security.check_password_hash` against
  the stored hash; never compare plaintext passwords.
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- Use Flask's built-in `session` (cookie-based) to track the logged-in
  user — store only `user_id`, nothing sensitive like the password hash.
- `app.secret_key` must be set for sessions to work; read it from an
  environment variable with a hardcoded fallback for local dev (documented
  inline as dev-only, not committed as a production secret).
- On successful login, redirect (302) to `url_for('profile')` — the next
  placeholder page in the roadmap; do not build a dashboard here.
- On invalid email or password, re-render `login.html` with a single
  generic error (e.g. "Invalid email or password.") — do not reveal
  whether the email exists, to avoid user enumeration.
- `GET /logout` clears the session (`session.clear()`) and redirects to
  `url_for('landing')`; it must not error if no one is logged in.
- Keep all logic in the existing `login()` / `logout()` views in `app.py`
  (no blueprints, no new modules), consistent with current architecture.

## Definition of done
- [ ] `GET /login` still renders the form with no errors.
- [ ] Submitting the seeded demo credentials (`demo@spendly.com` /
      `demo123`) logs in successfully and redirects to `/profile`.
- [ ] Submitting a correct email with the wrong password re-renders
      `login.html` with a generic invalid-credentials error and does not
      start a session.
- [ ] Submitting an email that doesn't exist re-renders `login.html` with
      the same generic error (no user-enumeration hint).
- [ ] After logging in, the nav in `base.html` shows "Profile" and
      "Logout" instead of "Sign in" / "Get started" on every page.
- [ ] Visiting `/logout` while logged in clears the session and redirects
      to `/`, after which the nav reverts to "Sign in" / "Get started".
- [ ] Visiting `/logout` while already logged out does not error and
      redirects to `/`.
- [ ] `python app.py` starts without errors and existing routes
      (`/`, `/register`, `/terms`, `/privacy`) are unaffected.
