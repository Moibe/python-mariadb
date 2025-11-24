import pandas as pd
from connection import get_connection
from datetime import datetime

def populate_productos():
    file_path = 'productos.xlsx'
    
    try:
        # Read with header=1 based on previous check
        df = pd.read_excel(file_path, header=1)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    conn = get_connection()
    if not conn:
        print("Could not connect to database")
        return

    cursor = conn.cursor()
    
    rows_inserted = 0
    rows_errors = 0

    for index, row in df.iterrows():
        try:
            # Mapping
            # We will use the ID from Excel to ensure consistency if referenced elsewhere
            p_id = row['id']
            nombre = row['nombre']
            cantidad = row['cantidad']
            id_tipo_producto = row['id_tipo_producto']
            id_conjunto = row['id_conjunto']
            precio_base = row['precio_base']
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # SQL Query
            # Including ID in insert
            sql = """
                INSERT INTO producto (id, nombre, cantidad, id_tipo_producto, id_conjunto, precio_base, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                nombre = VALUES(nombre),
                cantidad = VALUES(cantidad),
                id_tipo_producto = VALUES(id_tipo_producto),
                id_conjunto = VALUES(id_conjunto),
                precio_base = VALUES(precio_base),
                created_at = VALUES(created_at)
            """
            
            values = (p_id, nombre, cantidad, id_tipo_producto, id_conjunto, precio_base, created_at)
            
            cursor.execute(sql, values)
            rows_inserted += 1
            
        except Exception as e:
            print(f"Error inserting row {index} (ID: {row.get('id')}): {e}")
            rows_errors += 1

    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Finished. Inserted/Updated: {rows_inserted}, Errors: {rows_errors}")

if __name__ == "__main__":
    populate_productos()
