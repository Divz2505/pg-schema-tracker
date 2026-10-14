def get_tables(cursor):
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE';
    """)
    return [row[0] for row in cursor.fetchall()]


def get_columns(cursor):
    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    
    data = {}
    for table, column, dtype in cursor.fetchall():
        if table not in data:
            data[table] = []
        data[table].append({
            "column": column,
            "type": dtype
        })
    
    return data