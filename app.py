import os
from datetime import date, datetime

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
# Dev-only fallback secret — set the SECRET_KEY env var for anything real.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-for-production")

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    error = None
    if not name:
        error = "Please enter your full name."
    elif not email or "@" not in email:
        error = "Please enter a valid email address."
    elif len(password) < 8:
        error = "Password must be at least 8 characters."

    if error:
        return render_template("register.html", error=error)

    conn = get_db()
    try:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            return render_template(
                "register.html",
                error="An account with that email already exists.",
            )

        password_hash = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("login", registered=1))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    error = "Invalid email or password."

    conn = get_db()
    try:
        user = conn.execute(
            "SELECT id, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()
    finally:
        conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error=error)

    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    month_start = date.today().replace(day=1).isoformat()

    conn = get_db()
    try:
        user = conn.execute(
            "SELECT name, email, created_at FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            session.clear()
            return redirect(url_for("login"))

        totals = conn.execute(
            "SELECT COUNT(*) AS n, COALESCE(SUM(amount), 0) AS total "
            "FROM expenses WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        month_total = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses "
            "WHERE user_id = ? AND date >= ?",
            (user_id, month_start),
        ).fetchone()[0]
        category_rows = conn.execute(
            "SELECT category, SUM(amount) AS total FROM expenses "
            "WHERE user_id = ? GROUP BY category ORDER BY total DESC",
            (user_id,),
        ).fetchall()
        recent = conn.execute(
            "SELECT date, category, description, amount FROM expenses "
            "WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT 8",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()

    grand_total = totals["total"]
    categories = [
        {
            "name": row["category"],
            "total": row["total"],
            "pct": round(row["total"] / grand_total * 100) if grand_total else 0,
        }
        for row in category_rows
    ]

    try:
        member_since = datetime.strptime(
            user["created_at"], "%Y-%m-%d %H:%M:%S"
        ).strftime("%B %Y")
    except (TypeError, ValueError):
        member_since = None

    stats = {
        "total": grand_total,
        "month": month_total,
        "count": totals["n"],
        "top_category": categories[0]["name"] if categories else "—",
    }

    return render_template(
        "profile.html",
        user=user,
        initial=user["name"][:1].upper(),
        member_since=member_since,
        stats=stats,
        categories=categories,
        recent=recent,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
