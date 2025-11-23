import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import socket
import sys

# Cargar variables de entorno
load_dotenv()

def get_connection():
    """Crea y retorna una conexión a la base de datos MariaDB"""
    try:
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")
        port = int(os.getenv("DB_PORT", 3306))
        
        print(f"Intentando conectar con:")
        print(f"  Host: {host}")
        print(f"  Puerto: {port}")
        print(f"  Usuario: {user}")
        print(f"  Base de datos: {database}")
        print()
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            autocommit=True
        )
        return connection
    except Error as e:
        print(f"Error de conexión (código {e.errno}): {e.msg}")
        return None
    except Exception as e:
        print(f"Error general: {type(e).__name__}: {e}")
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("Probando conexión a MariaDB...")
    print("=" * 50)
    print()
    
    conn = get_connection()
    
    if conn:
        print("✓ Conexión exitosa!")
        print()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Versión de MariaDB: {version[0]}")
            
            cursor.execute("SELECT DATABASE()")
            db = cursor.fetchone()
            print(f"Base de datos actual: {db[0]}")
            
            cursor.close()
        except Exception as e:
            print(f"Error al ejecutar queries: {e}")
        finally:
            conn.close()
    else:
        print("✗ No se pudo conectar a la base de datos")
