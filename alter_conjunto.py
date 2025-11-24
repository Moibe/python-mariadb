from connection import get_connection

def alter_conjunto():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Modify id to be AUTO_INCREMENT
        sql = "ALTER TABLE conjunto MODIFY id INT(11) NOT NULL AUTO_INCREMENT;"
        print(f"Executing: {sql}")
        cursor.execute(sql)
        print("Table conjunto altered to AUTO_INCREMENT.")
    except Exception as e:
        print(f"Error altering table: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    alter_conjunto()
