from connection import get_connection

def alter_producto():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Modify precio_base to INT
        sql = "ALTER TABLE producto MODIFY COLUMN precio_base INT(11);"
        print(f"Executing: {sql}")
        cursor.execute(sql)
        print("Table producto altered: precio_base is now INT.")
        
        # Also ensure id is AUTO_INCREMENT while we are at it, as we did for others
        sql_ai = "ALTER TABLE producto MODIFY id INT(11) NOT NULL AUTO_INCREMENT;"
        print(f"Executing: {sql_ai}")
        cursor.execute(sql_ai)
        print("Table producto altered: id is now AUTO_INCREMENT.")
        
    except Exception as e:
        print(f"Error altering table: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    alter_producto()
