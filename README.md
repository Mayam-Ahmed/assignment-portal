# Assignment Submission Portal

Flask web app where students submit assignment links, with automated tests and CI that reports results to a local receiver.

## Run the application
    pip install -r requirements.txt
    python app.py
Open http://127.0.0.1:5000

## Run the tests
    python -m pytest -v

## Start the local report receiver
    python receiver/receiver.py
The receiver listens on http://127.0.0.1:5001/report and saves each report to `receiver/test-report.json`.

## CI pipeline
GitHub Actions (`.github/workflows/ci.yml`) runs on every push using a self-hosted runner on my computer.
It installs dependencies, runs pytest, builds a JSON report and POSTs it to the receiver
(also when tests fail). Bonus: deploys `demo/` to GitHub Pages on `main` only if tests pass, and emails the report.

## Self-hosted runner
GitHub repo -> Settings -> Actions -> Runners -> New self-hosted runner (Windows), then run `run.cmd`.
Demo run 1: passing pipeline