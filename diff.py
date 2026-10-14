import json
import os

SCHEMA_DIR = "schemas"
LATEST_FILE = os.path.join(SCHEMA_DIR, "latest_schema.json")


def get_previous_file():
    files = sorted([
        f for f in os.listdir(SCHEMA_DIR)
        if f.startswith("schema_") and f.endswith(".json")
    ])

    if len(files) < 2:
        return None

    return os.path.join(SCHEMA_DIR, files[-2])  # second latest


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def compare_schemas(old, new):
    changes = []

    old_tables = old.get("tables", {})
    new_tables = new.get("tables", {})

    # 🔥 Detect new tables
    for table in new_tables:
        if table not in old_tables:
            changes.append(f"🆕 New table added: {table}")

    # 🔥 Detect removed tables
    for table in old_tables:
        if table not in new_tables:
            changes.append(f"❌ Table removed: {table}")

    # 🔥 Compare tables
    for table in new_tables:
        if table in old_tables:
            old_cols = old_tables[table]["columns"]
            new_cols = new_tables[table]["columns"]

            old_cols_set = {c["column"] for c in old_cols}
            new_cols_set = {c["column"] for c in new_cols}

            # ➕ New columns
            for col in new_cols_set - old_cols_set:
                changes.append(f"➕ Column added: {table}.{col}")

            # ➖ Removed columns
            for col in old_cols_set - new_cols_set:
                changes.append(f"➖ Column removed: {table}.{col}")

            # 🔄 Type changes
            old_cols_dict = {c["column"]: c["type"] for c in old_cols}
            new_cols_dict = {c["column"]: c["type"] for c in new_cols}

            for col in old_cols_dict:
                if col in new_cols_dict:
                    if old_cols_dict[col] != new_cols_dict[col]:
                        changes.append(
                            f"🔄 Column type changed: {table}.{col} "
                            f"({old_cols_dict[col]} → {new_cols_dict[col]})"
                        )

            # 🔥 INDEX DIFF
            old_indexes = {idx["index"] for idx in old_tables[table].get("indexes", [])}
            new_indexes = {idx["index"] for idx in new_tables[table].get("indexes", [])}

            for idx in new_indexes - old_indexes:
                changes.append(f"📈 Index added: {table}.{idx}")

            for idx in old_indexes - new_indexes:
                changes.append(f"📉 Index removed: {table}.{idx}")

            # 🔥 CONSTRAINT DIFF
            def normalize_constraint(c):
                if c["type"] == "FOREIGN KEY":
                    ref = c.get("references") or {}
                    return f"{c['type']}:{c['column']}->{ref.get('table')}.{ref.get('column')}"
                else:
                    return f"{c['type']}:{c['column']}"

            old_constraints = {
                normalize_constraint(c)
                for c in old_tables[table].get("constraints", [])
            }

            new_constraints = {
                normalize_constraint(c)
                for c in new_tables[table].get("constraints", [])
            }

            for c in new_constraints - old_constraints:
                changes.append(f"🔗 Constraint added: {table} [{c}]")

            for c in old_constraints - new_constraints:
                changes.append(f"❌ Constraint removed: {table} [{c}]")

    # 🔥 FUNCTION DIFF (GLOBAL, not per-table)
    def normalize_functions(func_list):
        normalized = {}

        for f in func_list:
            # Old format (string)
            if isinstance(f, str):
                normalized[f] = ""
            # New format (dict)
            elif isinstance(f, dict):
                normalized[f.get("name")] = f.get("definition", "")

        return normalized


    old_funcs = normalize_functions(old.get("functions", []))
    new_funcs = normalize_functions(new.get("functions", []))
    
    # ➕ New functions
    for f in new_funcs:
        if f not in old_funcs:
            changes.append(f"🆕 Function added: {f}")

    # ➖ Removed functions
    for f in old_funcs:
        if f not in new_funcs:
            changes.append(f"❌ Function removed: {f}")

    # 🔄 Modified functions
    for f in old_funcs:
        if f in new_funcs:
            if old_funcs[f] != new_funcs[f]:
                changes.append(f"🔄 Function modified: {f}")

        # 🔥 VIEW DIFF
    old_views = {v["name"]: v["definition"] for v in old.get("views", [])}
    new_views = {v["name"]: v["definition"] for v in new.get("views", [])}

    # ➕ New views
    for v in new_views:
        if v not in old_views:
            changes.append(f"🆕 View added: {v}")

    # ➖ Removed views
    for v in old_views:
        if v not in new_views:
            changes.append(f"❌ View removed: {v}")

    # 🔄 Modified views
    for v in old_views:
        if v in new_views:
            if old_views[v] != new_views[v]:
                changes.append(f"🔄 View modified: {v}")

    return changes


def run_diff():
    prev_file = get_previous_file()

    if not prev_file:
        print("⚠️ Not enough schema versions to compare.")
        return

    print(f"📂 Previous schema: {prev_file}")
    print(f"📂 Current schema: {LATEST_FILE}")

    old_schema = load_json(prev_file)
    new_schema = load_json(LATEST_FILE)

    changes = compare_schemas(old_schema, new_schema)

    print("\n🔍 Schema Changes:\n")

    if not changes:
        print("✅ No changes detected")
    else:
        for change in changes:
            print(change)


if __name__ == "__main__":
    run_diff()