#main.py
import os
from datetime import datetime
import json
from db import get_connection

from extractors.tables import get_tables, get_columns
from extractors.views import get_views
from extractors.indexes import get_indexes
from extractors.functions import get_functions
from extractors.constraints import get_constraints


SCHEMA_DIR = "schemas"
LATEST_FILE = os.path.join(SCHEMA_DIR, "latest_schema.json")


def run():
    print("🔌 Connecting to database...")
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("📦 Extracting tables...")
        tables = get_tables(cursor)

        print("📊 Extracting columns...")
        columns = get_columns(cursor)

        print("👁️ Extracting views...")
        views = get_views(cursor)

        print("⚡ Extracting indexes...")
        indexes = get_indexes(cursor)

        print("🧠 Extracting functions...")
        functions = get_functions(cursor)

        print("🔗 Extracting constraints...")
        constraints = get_constraints(cursor)

        # 🔥 Structure per table
        structured_tables = {}
        for table in tables:
            structured_tables[table] = {
                "columns": columns.get(table, []),
                "indexes": [idx for idx in indexes if idx["table"] == table],
                "constraints": constraints.get(table, [])
            }

        schema = {
            "tables": structured_tables,
            "views": views,
            "functions": functions
        }

        print("💾 Saving schema version...")

        # Ensure folder exists
        os.makedirs(SCHEMA_DIR, exist_ok=True)

        # Timestamp file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_file = os.path.join(SCHEMA_DIR, f"schema_{timestamp}.json")

        # Save versioned file
        with open(version_file, "w") as f:
            json.dump(schema, f, indent=4)

        # 🔥 Save/update latest schema
        with open(LATEST_FILE, "w") as f:
            json.dump(schema, f, indent=4)

        print(f"📁 Version saved: {version_file}")
        print(f"📌 Updated latest schema: {LATEST_FILE}")

    finally:
        cursor.close()
        conn.close()
        print("🔒 Connection closed")

    print("✅ Schema extraction completed successfully!")


if __name__ == "__main__":
    run()