from connection import get_connection

def alter_textos():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Modify id to be AUTO_INCREMENT
        sql = "ALTER TABLE textos MODIFY id INT(11) NOT NULL AUTO_INCREMENT;"
        print(f"Executing: {sql}")
        cursor.execute(sql)
        print("Table textos altered to AUTO_INCREMENT.")
        
        # Add created_at column if it doesn't exist (it wasn't in the describe output)
        # The user asked for created_at to be today's date.
        # Let's check if it exists first, although describe didn't show it.
        # Wait, describe output:
        # ('id', 'int(11)', 'NO', 'PRI', None, '')
        # ('id_tipo_producto', 'int(11)', 'NO', 'MUL', None, '')
        # ('id_pais', 'varchar(5)', 'YES', 'MUL', None, '')
        # ('unidad', 'varchar(255)', 'YES', '', None, '')
        # ('unidades', 'varchar(255)', 'YES', '', None, '')
        # It seems created_at is missing. I should add it.
        
        sql_add_col = "ALTER TABLE textos ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;"
        print(f"Executing: {sql_add_col}")
        cursor.execute(sql_add_col)
        print("Column created_at added to textos.")
        
    except Exception as e:
        print(f"Error altering table: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    alter_textos()
