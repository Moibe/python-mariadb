from connection import get_connection
from datetime import datetime

def populate_pertenencia():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    
    try:
        # Get Conjunto ID (assuming only 1 exists or taking the first one)
        cursor.execute("SELECT id FROM conjunto LIMIT 1")
        conjunto_row = cursor.fetchone()
        if not conjunto_row:
            print("No conjunto found.")
            return
        conjunto_id = conjunto_row[0]
        print(f"Using Conjunto ID: {conjunto_id}")

        # Get all Producto IDs
        cursor.execute("SELECT id FROM producto")
        productos = cursor.fetchall()
        print(f"Found {len(productos)} products.")

        rows_inserted = 0
        for prod in productos:
            prod_id = prod[0]
            
            # Check if already exists to avoid duplicates (optional but good practice)
            cursor.execute("SELECT id FROM pertenencia WHERE id_conjunto = %s AND id_producto = %s", (conjunto_id, prod_id))
            if cursor.fetchone():
                print(f"Pertenencia for Conjunto {conjunto_id} and Producto {prod_id} already exists. Skipping.")
                continue

            sql = "INSERT INTO pertenencia (id_conjunto, id_producto) VALUES (%s, %s)"
            cursor.execute(sql, (conjunto_id, prod_id))
            rows_inserted += 1

        conn.commit()
        print(f"Finished. Inserted: {rows_inserted} rows.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    populate_pertenencia()
