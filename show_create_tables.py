from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    for table in ['precio', 'textos']:
        cursor.execute(f"SHOW CREATE TABLE {table}")
        result = cursor.fetchone()
        print(f"--- {table} ---")
        print(result[1])
    conn.close()
