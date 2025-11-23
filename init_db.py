import mariadb
from connection import get_connection

def create_tables():
    """Crear las tablas necesarias en la base de datos desde el archivo SQL"""
    try:
        conn = get_connection()
        if not conn:
            print("Error: No se pudo conectar a la base de datos")
            return False
        
        cursor = conn.cursor()
        
        # Crear tabla PAIS
        create_pais_table = """
        CREATE TABLE IF NOT EXISTS pais (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR(255),
            moneda VARCHAR(255),
            moneda_tic VARCHAR(255),
            simbolo VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_pais_table)
        print("✓ Tabla 'pais' lista")
        
        # Crear tabla PRODUCTO
        create_producto_table = """
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR(255),
            precio_mxn VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_producto_table)
        print("✓ Tabla 'producto' lista")
        
        # Crear tabla PRECIO
        create_precio_table = """
        CREATE TABLE IF NOT EXISTS precio (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR(255),
            id_producto INTEGER NOT NULL,
            id_pais INTEGER NOT NULL,
            status VARCHAR(255),
            price_id VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_precio_table)
        print("✓ Tabla 'precio' lista")
        
        # Agregar foreign keys si no existen
        try:
            cursor.execute("ALTER TABLE precio ADD FOREIGN KEY (id_producto) REFERENCES producto (id)")
            print("✓ Foreign key precio -> producto creada")
        except mariadb.Error:
            print("✓ Foreign key precio -> producto ya existe")
        
        try:
            cursor.execute("ALTER TABLE precio ADD FOREIGN KEY (id_pais) REFERENCES pais (id)")
            print("✓ Foreign key precio -> pais creada")
        except mariadb.Error:
            print("✓ Foreign key precio -> pais ya existe")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    except mariadb.Error as e:
        print(f"Error MariaDB: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Creando tablas en la base de datos...")
    print("=" * 50)
    if create_tables():
        print("=" * 50)
        print("✓ Base de datos lista para usar")
    else:
        print("=" * 50)
        print("✗ Error al crear las tablas")
