from connection import get_connection

def populate_conjunto():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Insert the row
        # ID will be 1 (auto_increment)
        # created_at will be current timestamp (default)
        sql = "INSERT INTO conjunto (sitio, nombre) VALUES (%s, %s)"
        values = ("splashmix", "normal")
        
        print(f"Executing: {sql} with values {values}")
        cursor.execute(sql, values)
        conn.commit()
        print("Row inserted successfully.")
        
        # Verify
        cursor.execute("SELECT * FROM conjunto")
        row = cursor.fetchone()
        print(f"Inserted row: {row}")
        
    except Exception as e:
        print(f"Error inserting row: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    populate_conjunto()
