def get_indexes(cursor):
    cursor.execute("""
        SELECT tablename, indexname, indexdef
        FROM pg_indexes
        WHERE schemaname = 'public';
    """)
    
    return [
        {
            "table": row[0],
            "index": row[1],
            "definition": row[2]
        }
        for row in cursor.fetchall()
    ]