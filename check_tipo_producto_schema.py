from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("DESCRIBE tipo_producto")
    columns = cursor.fetchall()
    print("--- tipo_producto ---")
    for col in columns:
        print(col)
    conn.close()
