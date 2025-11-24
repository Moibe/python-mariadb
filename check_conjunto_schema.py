from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("DESCRIBE conjunto")
    columns = cursor.fetchall()
    print("--- conjunto ---")
    for col in columns:
        print(col)
    conn.close()
