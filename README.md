# Flames BDC App — Hockey Explorer (Big Data Cup 2021)

A lightweight Flask web app for exploring Stathletes’ Big Data Cup women’s hockey data with clean, coach-friendly visuals (Plotly) and a simple Bootstrap UI.

**Live demo:** https://flames-bdc-app-f3ec259a4741.herokuapp.com/

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup (Local)](#setup-local)
- [Usage](#usage)
- [Data](#data)
- [Development Notes](#development-notes)
- [Roadmap / Ideas](#roadmap--ideas)
- [Acknowledgements/Credits](#acknowledgements--credits)

---

## Features
- 🔎 Filterable views: team, event type, player, and more (via `/coach` route).
- 📈 Interactive Plotly charts (pan/zoom, hover, tooltips).
- 🧹 Small helpers for quick stats/aggregations (Python).
- 🧱 Simple, responsive UI using Bootstrap 5.
- 🚀 One-click deploy to Heroku (Procfile/runtime included).

---

## Tech Stack
- **Backend:** Python, Flask, Jinja2 templates  
- **Data:** pandas  
- **Viz:** Plotly  
- **UI:** HTML, JS, Bootstrap 5  
- **Deploy:** Heroku (Procfile + runtime)

---

## Project Structure
```plaintext
flames-bdc-app/
├─ app.py                 # Flask app + routes
├─ charts.py              # Plot/figure helpers
├─ stats.py               # Small stat/aggregation helpers
├─ requirements.txt
├─ Procfile               # Heroku process type
├─ runtime.txt            # Heroku Python version
├─ templates/             # Jinja2 templates (e.g., index.html, coach.html)
├─ static/                # CSS/JS/img assets
├─ data/
│  └─ files/              # CSVs (e.g., hackathon_nwhl.csv, olympic_womens_dataset.csv)
├─ notebooks/             # (Optional) exploration notebooks
└─ scripts/               # (Optional) data prep utilities
```
## Setup (Local)
### Prerequisties
- Python 3.x (match runtime.txt if deploying to Heroku)
- pip and a virtual environment tool (venv or conda)

### 1) Clone and create an environment
``` plaintext
git clone https://github.com/Granatire97/flames-bdc-app.git
cd flames-bdc-app

python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```
### 2) Install Dependencies & Run the app
``` plaintext
pip install -r requirements.txt

# Option A: Flask runner
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

# Option B: plain Python
python app.py
```
## Usage
- Home: /

- Coach view: /coach
  - Select Team, Event, and/or Player, then submit.
  - Visuals are Plotly—use the toolbar to pan/zoom/save PNG.
  - Some panels display static placeholders if a chart isn’t available yet.

## Data
This app is designed around the Big Data Cup (Stathletes) women’s hockey datasets (e.g., NWHL/NCAA/Olympics CSVs).
Place the CSVs under data/files/ and point the app to the correct file(s) in app.py (examples: hackathon_nwhl.csv, olympic_womens_dataset.csv).
👉 Original dataset & documentation: Big Data Cup 2021 (Stathletes) - https://github.com/bigdatacup/Big-Data-Cup-2021

## Development Notes
- Templates: Jinja2/JS/HTML (templates/) with Bootstrap 5 for layout/components.
- Charts: Plotly figures rendered into HTML and embedded in template blocks.
- Static assets: Images/CSS/JS go into static/.
- Data cleaning: Team-name normalization + date parsing in app.py and helpers.

## Roadmap / Ideas
- Add more event types & drill-down views.
- Player cards with per-60 stats and shot maps.
- Heatmap of shots in an ice rink image
- Export views (CSV/PNG).
- Add tests + CI (GitHub Actions).
- Dockerfile for local dev parity.

## Acknowledgements / Credits
- Stathletes & the Big Data Cup organizers for open data
- https://teamusa.usahockey.com/2019rivalryseries
- https://en.wikipedia.org/wiki/2019_IIHF_Women%27s_World_Championship




