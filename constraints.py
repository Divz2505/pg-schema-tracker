def get_constraints(cursor):
    cursor.execute("""
        SELECT
            tc.table_name,
            tc.constraint_type,
            kcu.column_name,
            ccu.table_name AS foreign_table,
            ccu.column_name AS foreign_column
        FROM information_schema.table_constraints tc
        LEFT JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
        LEFT JOIN information_schema.constraint_column_usage ccu
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.table_schema = 'public';
    """)

    constraints = {}

    for row in cursor.fetchall():
        table, ctype, column, f_table, f_column = row

        if table not in constraints:
            constraints[table] = []

        constraints[table].append({
            "type": ctype,
            "column": column,
            "references": {
                "table": f_table,
                "column": f_column
            } if ctype == "FOREIGN KEY" else None
        })

    return constraints