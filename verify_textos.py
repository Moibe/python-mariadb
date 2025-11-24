from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM textos LIMIT 5")
    rows = cursor.fetchall()
    print("First 5 rows in 'textos' table:")
    for row in rows:
        print(row)
    conn.close()
