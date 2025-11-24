import json
from connection import get_connection
from datetime import datetime

precios_prod = [
    {"id":0, "nombre":"🃏1 imagen", "precio":"$30 mxn", "cxt":"($30/imagen)",  "mode": "payment", "price_id": "price_1SDYG3IYi36CbmfWqVYGm8LA",  "imagenes": 1},
    {"id":1, "nombre":"🃏10 imágenes", "precio":"$190 mxn", "cxt":"($19/imagen)",  "mode": "payment", "price_id": "price_1SBRWMIYi36CbmfWEVM1T8nC",  "imagenes": 10},
    {"id":2, "nombre":"🃏40 imágenes", "precio":"$580 mxn", "cxt":"($14.5/imagen)",  "mode": "payment", "price_id": "price_1SBRSzIYi36CbmfWDtRx2ic7", "imagenes": 40},
    {"id":3, "nombre":"🃏80 imágenes", "precio":"$780 mxn", "cxt":"($9.75)/imagen",  "mode": "payment", "price_id": "price_1SBRVNIYi36CbmfWsQyoKpTq", "imagenes": 80},
    {"id":4, "nombre":"🃏320 imágenes", "precio":"$1600 mxn", "cxt":"($5/imagen)",  "mode": "payment", "price_id": "price_1SBRRkIYi36CbmfWZwqCQaAk", "imagenes": 320},
    {"id":5, "nombre":"🃏1000 imágenes", "precio":"$1900 mxn", "cxt":"($1.9/imagen)",  "mode": "payment", "price_id": "price_1SBPjIIYi36CbmfWOkNXYLcl", "imagenes": 1000},
]

def populate_precios_prod():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    
    rows_inserted = 0
    id_pais = "MXN"
    status = "activo"
    ambiente = "production" # User said "son los de producción"
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Check if MXN exists
        cursor.execute("SELECT id FROM pais WHERE id = %s", (id_pais,))
        if not cursor.fetchone():
            print(f"Error: Pais {id_pais} not found.")
            return

        for item in precios_prod:
            imagenes = item["imagenes"]
            price_id = item["price_id"]
            
            # Find product by cantidad (imagenes)
            cursor.execute("""
                SELECT p.id, p.precio_base, p.cantidad, tp.nombre, c.sitio 
                FROM producto p
                JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
                JOIN conjunto c ON p.id_conjunto = c.id
                WHERE p.cantidad = %s
            """, (imagenes,))
            prod_row = cursor.fetchone()
            
            if not prod_row:
                print(f"Warning: No product found for {imagenes} images. Skipping.")
                continue
                
            prod_id = prod_row[0]
            precio_base = prod_row[1]
            cantidad = prod_row[2]
            tipo_prod_nombre = prod_row[3]
            sitio_nombre = prod_row[4]
            
            # Find pertenencia for this product
            cursor.execute("SELECT id FROM pertenencia WHERE id_producto = %s", (prod_id,))
            pert_row = cursor.fetchone()
            
            if not pert_row:
                print(f"Warning: No pertenencia found for product {prod_id}. Skipping.")
                continue
                
            id_pertenencia = pert_row[0]
            
            # Calculate fields
            cantidad_precio = precio_base
            ratio_imagen = int(cantidad_precio / cantidad)
            
            # Construct name: pais-sitio-cantidad-tipo_producto-ambiente
            # Example: mxn-splashmix-1-imagen-production
            nombre_construido = f"{id_pais.lower()}-{sitio_nombre}-{cantidad}-{tipo_prod_nombre}-{ambiente}"
            
            # Insert
            sql = """
                INSERT INTO precio (nombre, id_pertenencia, id_pais, price_id, cantidad_precio, ratio_imagen, status, ambiente, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (nombre_construido, id_pertenencia, id_pais, price_id, cantidad_precio, ratio_imagen, status, ambiente, created_at)
            
            cursor.execute(sql, values)
            rows_inserted += 1
            print(f"Inserted price: {nombre_construido}")

        conn.commit()
        print(f"Finished. Inserted: {rows_inserted} rows.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    populate_precios_prod()
