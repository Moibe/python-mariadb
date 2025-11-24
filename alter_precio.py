from connection import get_connection

def add_ambiente_to_precio():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Add ambiente column after status
        sql = "ALTER TABLE precio ADD COLUMN ambiente VARCHAR(255) AFTER status;"
        print(f"Executing: {sql}")
        cursor.execute(sql)
        print("Column 'ambiente' added to table 'precio'.")
        
        # Also ensure id is AUTO_INCREMENT if not already (it wasn't checked/altered yet for this table specifically in this session, though likely is int)
        # Let's check describe output from previous step: ('id', 'int(11)', 'NO', 'PRI', None, '')
        # It doesn't explicitly say auto_increment in the tuple output of mysql connector usually unless we check 'Extra'.
        # But for consistency with other tables, I will run the modify id command too.
        
        sql_ai = "ALTER TABLE precio MODIFY id INT(11) NOT NULL AUTO_INCREMENT;"
        print(f"Executing: {sql_ai}")
        cursor.execute(sql_ai)
        print("Table precio altered to AUTO_INCREMENT.")

    except Exception as e:
        print(f"Error altering table: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    add_ambiente_to_precio()
