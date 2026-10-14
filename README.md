# schema-connector

Python tool that extracts PostgreSQL schema metadata (tables, columns, views, indexes, functions, constraints) into versioned JSON snapshots and diffs them to detect schema changes.

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows (use source venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
cp .env.example .env         # then edit .env with your DB credentials
```

## Usage

Extract the current schema:

```bash
python main.py
```

This writes a timestamped snapshot `schemas/schema_<YYYYMMDD_HHMMSS>.json` and updates `schemas/latest_schema.json`.

Compare the two most recent snapshots:

```bash
python diff.py
```

## Project layout

- `main.py` – runs all extractors and saves the snapshot
- `diff.py` – compares snapshots and reports changes
- `db.py` / `config.py` – connection setup (settings come from `.env`)
- `extractors/` – one module each for tables/columns, views, indexes, functions, constraints
- `schemas/` – saved snapshots (timestamped files are git-ignored)
