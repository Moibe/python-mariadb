from connection import get_connection

def alter_precio_charset():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Change table charset to utf8mb4 to support emojis
        sql = "ALTER TABLE precio CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        print(f"Executing: {sql}")
        cursor.execute(sql)
        print("Table precio altered to utf8mb4.")
        
    except Exception as e:
        print(f"Error altering table: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    alter_precio_charset()
