from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("DESCRIBE pais")
    columns = cursor.fetchall()
    for col in columns:
        print(col)
    conn.close()
