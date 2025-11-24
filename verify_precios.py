from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, cantidad_precio, ratio_imagen, ambiente FROM precio")
    rows = cursor.fetchall()
    print("Rows in 'precio' table:")
    for row in rows:
        print(row)
    conn.close()
