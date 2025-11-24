from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM producto")
    count = cursor.fetchone()[0]
    print(f"Count: {count}")
    conn.close()
