# Spec: Registration

## Overview
Implements account creation for Spendly. The `/register` route currently only
renders the sign-up form on GET; this step adds the POST handler that
validates the submitted name/email/password, hashes the password, inserts a
new row into the `users` table, and sends the user on to sign in. This is the
first step that writes to the `users` table outside of `seed_db()`, and it
sits directly on top of the schema and `get_db()` helper delivered in Step 1.

## Depends on
- Step 1 (database setup) — `users` table, `get_db()`, `init_db()` must exist
  and work as implemented in `database/db.py`.

## Routes
- `GET /register` — renders the registration form — public (already implemented, unchanged)
- `POST /register` — validates input, creates the user, redirects to login — public

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`,
`password_hash`, `created_at`) already supports registration. Verified
against `database/db.py` — no new columns or tables required.

## Templates
- **Create:** none
- **Modify:**
  - `templates/register.html` — no structural changes required; existing
    `{% if error %}` block is reused to surface validation/duplicate-email
    errors returned by the route.
  - `templates/login.html` — add a success banner (reusing the existing
    `.auth-error`-style pattern, e.g. a new `.auth-success` class) shown when
    redirected from a successful registration, so the user gets confirmation
    their account was created.

## Files to change
- `app.py` — extend the `/register` route to accept `GET` and `POST`,
  implement validation, insertion, and redirect-on-success logic.
- `templates/login.html` — display the post-registration success message.
- `static/css/style.css` — add a `.auth-success` style (reuse existing
  `.auth-error` structure/spacing, differentiate only via CSS variables for
  color).

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only — no string-formatted SQL.
- Passwords hashed with `werkzeug.security.generate_password_hash` before
  insert; never store or log plaintext passwords.
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- Validate on the server even though HTML5 `required`/`type=email` attributes
  exist client-side (name non-empty, email non-empty, password length >= 8).
- Check for an existing email (`SELECT` before `INSERT`, or catch the
  `sqlite3.IntegrityError` from the `UNIQUE` constraint) and show a friendly
  inline error via the `error` template variable rather than a stack trace.
- On success, redirect (302) to `url_for('login')` with a query flag (e.g.
  `?registered=1`) — do not start a session or log the user in; that belongs
  to the login step.
- Keep all logic in the existing `register()` view in `app.py` (no
  blueprints, no new modules) consistent with current architecture.

## Definition of done
- [ ] `GET /register` still renders the form with no errors.
- [ ] Submitting valid name/email/password creates exactly one new row in
      `users` with a bcrypt/werkzeug password hash (not plaintext).
- [ ] Submitting an already-registered email re-renders `register.html` with
      an inline error and does not create a duplicate row.
- [ ] Submitting a password shorter than 8 characters re-renders
      `register.html` with an inline error and creates no row.
- [ ] Submitting an empty name or malformed email re-renders `register.html`
      with an inline error and creates no row.
- [ ] On success, the browser is redirected to `/login` and a success
      message is visible on the login page.
- [ ] `python app.py` starts without errors and existing routes
      (`/`, `/login`, `/terms`, `/privacy`) are unaffected.
