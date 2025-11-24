from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("DESCRIBE precio")
    columns = cursor.fetchall()
    print("--- precio ---")
    for col in columns:
        print(col)
    conn.close()
