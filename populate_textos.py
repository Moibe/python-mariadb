import pandas as pd
from connection import get_connection
from datetime import datetime

def populate_textos():
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
    
    rows_inserted = 0
    rows_errors = 0
    
    # Fixed value for id_tipo_producto
    id_tipo_producto = 1

    for index, row in df.iterrows():
        try:
            # Mapping
            id_pais = row['iso'] # Using ISO as ID for pais
            unidad = row['singular']
            unidades = row['plural']
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # SQL Query
            sql = """
                INSERT INTO textos (id_tipo_producto, id_pais, unidad, unidades, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            values = (id_tipo_producto, id_pais, unidad, unidades, created_at)
            
            cursor.execute(sql, values)
            rows_inserted += 1
            
        except Exception as e:
            print(f"Error inserting row {index} (Pais: {row.get('iso')}): {e}")
            rows_errors += 1

    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Finished. Inserted: {rows_inserted}, Errors: {rows_errors}")

if __name__ == "__main__":
    populate_textos()
