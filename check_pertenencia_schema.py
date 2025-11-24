from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("DESCRIBE pertenencia")
    columns = cursor.fetchall()
    print("--- pertenencia ---")
    for col in columns:
        print(col)
    conn.close()
