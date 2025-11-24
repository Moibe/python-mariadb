from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    rows = cursor.fetchall()
    print("Rows in 'producto' table:")
    for row in rows:
        print(row)
    conn.close()
