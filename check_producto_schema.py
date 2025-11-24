from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("DESCRIBE producto")
    columns = cursor.fetchall()
    print("--- producto ---")
    for col in columns:
        print(col)
    conn.close()
