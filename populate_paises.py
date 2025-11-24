import pandas as pd
from connection import get_connection
from datetime import datetime
import sys

def populate_paises():
    file_path = 'paises.xlsx'
    
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    conn = get_connection()
    if not conn:
        print("Could not connect to database")
        return

    cursor = conn.cursor()
    
    # Check if table is empty or if we should update?
    # User said "poblaré", usually means insert.
    # I will use INSERT IGNORE or REPLACE or just INSERT and handle errors.
    # Since we are setting ID explicitly, we should probably use INSERT INTO ...
    
    rows_inserted = 0
    rows_errors = 0

    for index, row in df.iterrows():
        try:
            # Mapping
            # User said: "iso sea el id". 
            
            p_id = row['iso'] 
            nombre = row['nombre']
            moneda = row['moneda']
            moneda_tic = row['iso'] # User said "iso es moneda_tic también"
            simbolo = row['simbolo']
            side = 1 if row['side'] else 0 # Ensure it's 0 or 1
            decs = row['decs']
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # SQL Query
            sql = """
                INSERT INTO pais (id, nombre, moneda, moneda_tic, simbolo, side, decs, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                nombre = VALUES(nombre),
                moneda = VALUES(moneda),
                moneda_tic = VALUES(moneda_tic),
                simbolo = VALUES(simbolo),
                side = VALUES(side),
                decs = VALUES(decs),
                created_at = VALUES(created_at)
            """
            
            values = (p_id, nombre, moneda, moneda_tic, simbolo, side, decs, created_at)
            
            cursor.execute(sql, values)
            rows_inserted += 1
            
        except Exception as e:
            print(f"Error inserting row {index}: {e}")
            rows_errors += 1

    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Finished. Inserted/Updated: {rows_inserted}, Errors: {rows_errors}")

if __name__ == "__main__":
    populate_paises()
