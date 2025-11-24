from connection import get_connection

conn = get_connection()
if conn:
    cursor = conn.cursor()
    # Test query similar to API
    query = """
        SELECT 
            pr.id, pr.nombre, pr.id_pertenencia, pr.id_pais, pr.price_id,
            pr.cantidad_precio, pr.ratio_imagen, pr.status, pr.ambiente,
            pe.id, p.nombre, p.cantidad,
            tp.nombre,
            c.nombre,
            pa.nombre, pa.moneda, pa.simbolo, pa.side, pa.decs
        FROM precio pr
        LEFT JOIN pertenencia pe ON pr.id_pertenencia = pe.id
        LEFT JOIN producto p ON pe.id_producto = p.id
        LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
        LEFT JOIN conjunto c ON pe.id_conjunto = c.id
        LEFT JOIN pais pa ON pr.id_pais = pa.id
        LIMIT 1
    """
    cursor.execute(query)
    row = cursor.fetchone()
    print("API Query Test Result:")
    print(row)
    conn.close()
