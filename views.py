def get_views(cursor):
    cursor.execute("""
        SELECT table_name, view_definition
        FROM information_schema.views
        WHERE table_schema = 'public';
    """)
    
    return [
        {"name": row[0], "definition": row[1]}
        for row in cursor.fetchall()
    ]