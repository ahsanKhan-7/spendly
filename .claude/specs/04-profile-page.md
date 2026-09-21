# Spec: Profile Page

## Overview
Replaces the `/profile` placeholder with a real page for the logged-in user: identity header, summary stats (total spent, this month, transaction count, top category), a per-category spending breakdown, and the most recent expenses. Login already redirects here.

## Depends on
- Step 1 (database), Step 2 (registration), Step 3 (login/logout — session `user_id`).

## Routes
- `GET /profile` — renders profile page — logged-in (redirects to `/login` otherwise)

## Database changes
No database changes.

## Templates
- **Create:** `templates/profile.html`
- **Modify:** none

## Files to change
- `app.py`, `static/css/style.css`

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Amounts shown as `Rs.` (Pakistani Rupee framing)

## Definition of done
- [ ] Demo login (`demo@spendly.com` / `demo123`) lands on `/profile` showing name, email, member-since
- [ ] Stats show Rs. 376 total, 8 transactions, top category Bills
- [ ] Category bars and recent expenses render, newest first
- [ ] New user with no expenses sees empty states, no errors
- [ ] Logged-out `/profile` redirects to `/login`
- [ ] Layout stacks correctly at ≤900px and ≤600px
