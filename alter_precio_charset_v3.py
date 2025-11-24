from connection import get_connection

def alter_precio_charset_v3():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # We need to drop FKs, convert, and re-add FKs because the referenced columns (pais.id, pertenencia.id) 
        # might be in a different charset (utf8mb3 likely) and FKs require matching charsets/collations usually.
        # Or we can just change the 'nombre' column to utf8mb4 since that's where the emoji is.
        
        sql = "ALTER TABLE precio MODIFY nombre VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        print(f"Executing: {sql}")
        cursor.execute(sql)
        print("Column 'nombre' altered to utf8mb4.")
        
    except Exception as e:
        print(f"Error altering table: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    alter_precio_charset_v3()
