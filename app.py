import json
import os
from datetime import datetime
from urllib.parse import urlparse

from flask import Flask, render_template, request

DEFAULT_DATA_FILE = os.environ.get("DATA_FILE", "submissions.json")


def is_valid_url(url):
    return True
    


def validate_submission(name, reg_no, title, url):
    errors = []
    if not name.strip():
        errors.append("Name is required.")
    if not reg_no.strip():
        errors.append("Registration number is required.")
    if not title.strip():
        errors.append("Assignment title is required.")
    if not url.strip():
        errors.append("Submission URL is required.")
    elif not is_valid_url(url.strip()):
        errors.append("Submission URL is invalid. It must start with http:// or https://")
    return errors


def load_submissions(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_submissions(path, submissions):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(submissions, f, indent=2)


def create_app(data_file=None):
    app = Flask(__name__)
    app.config["DATA_FILE"] = data_file or DEFAULT_DATA_FILE

    @app.route("/", methods=["GET", "POST"])
    def index():
        errors, message = [], None
        form = {"name": "", "reg_no": "", "title": "", "url": ""}
        status = 200

        if request.method == "POST":
            form = {k: request.form.get(k, "").strip() for k in form}
            errors = validate_submission(form["name"], form["reg_no"], form["title"], form["url"])
            if errors:
                status = 400
            else:
                subs = load_submissions(app.config["DATA_FILE"])
                subs.append({**form, "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                save_submissions(app.config["DATA_FILE"], subs)
                message = "Submission saved successfully!"
                form = {"name": "", "reg_no": "", "title": "", "url": ""}

        subs = load_submissions(app.config["DATA_FILE"])
        return render_template("index.html", errors=errors, message=message, form=form, submissions=subs), status

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)