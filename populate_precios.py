import json
from connection import get_connection
from datetime import datetime

precios_dev = [
    {"id":0, "nombre":"🃏1 imagen", "precio":"$30 mxn", "cxt":"($30/imagen)",  "mode": "payment", "price_id": "price_1SDXvuROVpWRmEfBsAGp37kf",  "imagenes": 1},
    {"id":1, "nombre":"🃏10 imágenes", "precio":"$190 mxn", "cxt":"($19/imagen)",  "mode": "payment", "price_id": "price_1S1GF3ROVpWRmEfB6hRtG5Cy",  "imagenes": 10},
    {"id":2, "nombre":"🃏40 imágenes", "precio":"$580 mxn", "cxt":"($14.5/imagen)",  "mode": "payment", "price_id": "price_1S1GLEROVpWRmEfBVlVTsuPC", "imagenes": 40},
    {"id":3, "nombre":"🃏80 imágenes", "precio":"$780 mxn", "cxt":"($9.75)/imagen",  "mode": "payment", "price_id": "price_1S1GMrROVpWRmEfBVqnTwG9g", "imagenes": 80},
    {"id":4, "nombre":"🃏320 imágenes", "precio":"$1600 mxn", "cxt":"($5/imagen)",  "mode": "payment", "price_id": "price_1S1GOSROVpWRmEfBvnjSrhQ9", "imagenes": 320},
    {"id":5, "nombre":"🃏1000 imágenes", "precio":"$1900 mxn", "cxt":"($1.9/imagen)",  "mode": "payment", "price_id": "price_1S1GQPROVpWRmEfBYv6SoeuO", "imagenes": 1000},
]

def populate_precios():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    
    rows_inserted = 0
    id_pais = "MXN"
    status = "activo"
    ambiente = "sandbox"
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Check if MXN exists
        cursor.execute("SELECT id FROM pais WHERE id = %s", (id_pais,))
        if not cursor.fetchone():
            print(f"Error: Pais {id_pais} not found.")
            return

        for item in precios_dev:
            imagenes = item["imagenes"]
            price_id = item["price_id"]
            nombre = item["nombre"]
            
            # Find product by cantidad (imagenes)
            # Assuming unique quantity per product for now or taking the first one
            cursor.execute("SELECT id, precio_base, cantidad FROM producto WHERE cantidad = %s", (imagenes,))
            prod_row = cursor.fetchone()
            
            if not prod_row:
                print(f"Warning: No product found for {imagenes} images. Skipping.")
                continue
                
            prod_id = prod_row[0]
            precio_base = prod_row[1] # This is int now
            cantidad = prod_row[2]
            
            # Find pertenencia for this product
            # Assuming we want the pertenencia for the 'splashmix' conjunto (id 1) or just any pertenencia for this product
            # The user said "tenemos 5 pertenencias que a su vez están relacionadas a un producto".
            # I'll search for pertenencia by product_id
            cursor.execute("SELECT id FROM pertenencia WHERE id_producto = %s", (prod_id,))
            pert_row = cursor.fetchone()
            
            if not pert_row:
                print(f"Warning: No pertenencia found for product {prod_id}. Skipping.")
                continue
                
            id_pertenencia = pert_row[0]
            
            # Calculate fields
            cantidad_precio = precio_base
            ratio_imagen = int(cantidad_precio / cantidad)
            
            # Insert
            sql = """
                INSERT INTO precio (nombre, id_pertenencia, id_pais, price_id, cantidad_precio, ratio_imagen, status, ambiente, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (nombre, id_pertenencia, id_pais, price_id, cantidad_precio, ratio_imagen, status, ambiente, created_at)
            
            cursor.execute(sql, values)
            rows_inserted += 1
            print(f"Inserted price for {imagenes} images (Product ID: {prod_id}, Pertenencia ID: {id_pertenencia})")

        conn.commit()
        print(f"Finished. Inserted: {rows_inserted} rows.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    populate_precios()
