import mysql.connector
from mysql.connector import Error
from connection import get_connection

def create_tables():
    """Crear las tablas necesarias en la base de datos desde el archivo SQL"""
    try:
        conn = get_connection()
        if not conn:
            print("Error: No se pudo conectar a la base de datos")
            return False
        
        cursor = conn.cursor()
        
        # Crear tabla CONJUNTO
        create_conjunto_table = """
        CREATE TABLE IF NOT EXISTS conjunto (
            id INTEGER PRIMARY KEY,
            sitio VARCHAR(255),
            nombre VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_conjunto_table)
        print("✓ Tabla 'conjunto' lista")
        
        # Crear tabla PAIS
        create_pais_table = """
        CREATE TABLE IF NOT EXISTS pais (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR(255),
            unidad VARCHAR(255),
            unidades VARCHAR(255),
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
            cantidad INT,
            unidad_general VARCHAR(255),
            precio_base VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_producto_table)
        print("✓ Tabla 'producto' lista")
        
        # Crear tabla LINEA (relación entre conjunto y producto)
        create_linea_table = """
        CREATE TABLE IF NOT EXISTS linea (
            id INTEGER PRIMARY KEY,
            id_conjunto INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_linea_table)
        print("✓ Tabla 'linea' lista")
        
        # Crear tabla PRECIO
        create_precio_table = """
        CREATE TABLE IF NOT EXISTS precio (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR(255),
            id_linea INTEGER NOT NULL,
            id_pais INTEGER NOT NULL,
            price_id VARCHAR(255),
            cantidad_precio INT,
            ratio_imagen INT,
            status VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_precio_table)
        print("✓ Tabla 'precio' lista")
        
        # Agregar foreign keys si no existen
        try:
            cursor.execute("ALTER TABLE linea ADD FOREIGN KEY (id_conjunto) REFERENCES conjunto (id)")
            print("✓ Foreign key linea -> conjunto creada")
        except Error:
            print("✓ Foreign key linea -> conjunto ya existe")
        
        try:
            cursor.execute("ALTER TABLE linea ADD FOREIGN KEY (id_producto) REFERENCES producto (id)")
            print("✓ Foreign key linea -> producto creada")
        except Error:
            print("✓ Foreign key linea -> producto ya existe")
        
        try:
            cursor.execute("ALTER TABLE precio ADD FOREIGN KEY (id_linea) REFERENCES linea (id)")
            print("✓ Foreign key precio -> linea creada")
        except Error:
            print("✓ Foreign key precio -> linea ya existe")
        
        try:
            cursor.execute("ALTER TABLE precio ADD FOREIGN KEY (id_pais) REFERENCES pais (id)")
            print("✓ Foreign key precio -> pais creada")
        except Error:
            print("✓ Foreign key precio -> pais ya existe")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    except Error as e:
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
