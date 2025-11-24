from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("DESCRIBE textos")
    columns = cursor.fetchall()
    print("--- textos ---")
    for col in columns:
        print(col)
    conn.close()
