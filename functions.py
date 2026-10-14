def get_functions(cursor):
    cursor.execute("""
        SELECT 
            p.proname,
            pg_get_functiondef(p.oid)
        FROM pg_proc p
        JOIN pg_namespace n ON p.pronamespace = n.oid
        WHERE n.nspname = 'public';
    """)

    return [
        {
            "name": row[0],
            "definition": row[1]
        }
        for row in cursor.fetchall()
    ]