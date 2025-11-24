from connection import get_connection

def alter_database():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    
    commands = [
        "SET FOREIGN_KEY_CHECKS = 0;",
        # Drop FKs
        "ALTER TABLE precio DROP FOREIGN KEY precio_ibfk_2;",
        "ALTER TABLE precio DROP FOREIGN KEY precio_ibfk_3;",
        "ALTER TABLE textos DROP FOREIGN KEY textos_ibfk_2;",
        
        # Modify Columns
        "ALTER TABLE pais MODIFY COLUMN id VARCHAR(5);",
        "ALTER TABLE textos MODIFY COLUMN id_pais VARCHAR(5);",
        "ALTER TABLE precio MODIFY COLUMN id_pais VARCHAR(5);",
        
        # Truncate
        "TRUNCATE TABLE pais;",
        
        # Re-add FKs
        "ALTER TABLE precio ADD CONSTRAINT precio_ibfk_2 FOREIGN KEY (id_pais) REFERENCES pais(id);",
        "ALTER TABLE textos ADD CONSTRAINT textos_ibfk_2 FOREIGN KEY (id_pais) REFERENCES pais(id);",
        
        "SET FOREIGN_KEY_CHECKS = 1;"
    ]

    try:
        for cmd in commands:
            print(f"Executing: {cmd}")
            cursor.execute(cmd)
        print("Database schema updated successfully.")
    except Exception as e:
        print(f"Error updating schema: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    alter_database()
