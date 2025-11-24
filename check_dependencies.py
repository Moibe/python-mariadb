from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    tables = ['textos', 'precio']
    for table in tables:
        print(f"--- {table} ---")
        try:
            cursor.execute(f"DESCRIBE {table}")
            columns = cursor.fetchall()
            for col in columns:
                if 'id_pais' in col[0]:
                    print(col)
        except Exception as e:
            print(f"Error describing {table}: {e}")
    conn.close()
