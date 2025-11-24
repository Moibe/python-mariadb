from connection import get_connection

def make_id_autoincrement():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Modify id to be AUTO_INCREMENT
        # Note: We must repeat the full definition.
        sql = "ALTER TABLE tipo_producto MODIFY id INT(11) NOT NULL AUTO_INCREMENT;"
        print(f"Executing: {sql}")
        cursor.execute(sql)
        print("Table tipo_producto altered to AUTO_INCREMENT.")
    except Exception as e:
        print(f"Error altering table: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    make_id_autoincrement()
