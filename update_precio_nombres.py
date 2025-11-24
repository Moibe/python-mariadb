from connection import get_connection

def update_precio_nombres():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    
    try:
        # Fetch necessary data to construct the name
        query = """
            SELECT 
                pr.id,
                pr.id_pais,
                c.sitio,
                p.cantidad,
                tp.nombre as tipo_producto_nombre,
                pr.ambiente
            FROM precio pr
            JOIN pertenencia pe ON pr.id_pertenencia = pe.id
            JOIN conjunto c ON pe.id_conjunto = c.id
            JOIN producto p ON pe.id_producto = p.id
            JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        updated_count = 0
        
        for row in rows:
            price_id = row[0]
            pais_iso = row[1].lower() # mxn
            sitio = row[2] # splashmix
            cantidad = row[3] # 1, 10, etc
            tipo_prod = row[4] # imagen
            ambiente = row[5] # sandbox
            
            # Construct new name: pais-sitio-cantidad-tipo_producto-ambiente
            new_name = f"{pais_iso}-{sitio}-{cantidad}-{tipo_prod}-{ambiente}"
            
            # Update
            update_sql = "UPDATE precio SET nombre = %s WHERE id = %s"
            cursor.execute(update_sql, (new_name, price_id))
            updated_count += 1
            print(f"Updated ID {price_id} to: {new_name}")
            
        conn.commit()
        print(f"Finished. Updated {updated_count} rows.")

    except Exception as e:
        print(f"Error updating names: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    update_precio_nombres.py = update_precio_nombres
    update_precio_nombres()
