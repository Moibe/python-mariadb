from connection import get_connection

def populate_tipo_producto():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Insert the row
        # We don't specify ID, so it will be 1 (since table is empty and we just added auto_increment)
        sql = "INSERT INTO tipo_producto (nombre, unidad_base) VALUES (%s, %s)"
        values = ("imagen", "imagen")
        
        print(f"Executing: {sql} with values {values}")
        cursor.execute(sql, values)
        conn.commit()
        print("Row inserted successfully.")
        
        # Verify
        cursor.execute("SELECT * FROM tipo_producto")
        row = cursor.fetchone()
        print(f"Inserted row: {row}")
        
    except Exception as e:
        print(f"Error inserting row: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    populate_tipo_producto()
