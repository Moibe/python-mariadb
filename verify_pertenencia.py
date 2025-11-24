from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pertenencia")
    rows = cursor.fetchall()
    print("Rows in 'pertenencia' table:")
    for row in rows:
        print(row)
    conn.close()
