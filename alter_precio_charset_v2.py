from connection import get_connection

def alter_precio_charset_v2():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        commands = [
            "SET FOREIGN_KEY_CHECKS = 0;",
            "ALTER TABLE precio CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
            "SET FOREIGN_KEY_CHECKS = 1;"
        ]
        
        for cmd in commands:
            print(f"Executing: {cmd}")
            cursor.execute(cmd)
            
        print("Table precio altered to utf8mb4.")
        
    except Exception as e:
        print(f"Error altering table: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    alter_precio_charset_v2()
