from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SHOW CREATE TABLE tipo_producto")
    result = cursor.fetchone()
    print(result[1])
    conn.close()
