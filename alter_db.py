"""
Script para alterar la estructura de la base de datos en Opalstack
Ejecuta alteraciones (ADD COLUMN, MODIFY, etc.) directamente
"""

import mysql.connector
from mysql.connector import Error
from connection import get_connection

def add_column(table_name: str, column_name: str, column_definition: str, after_column: str = None):
    """
    Agregar una columna a una tabla
    
    Args:
        table_name: Nombre de la tabla
        column_name: Nombre de la nueva columna
        column_definition: Definición (ej: "VARCHAR(255)", "INT", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        after_column: (Opcional) Posicionar después de esta columna
    
    Ejemplo:
        add_column('pais', 'codigo_pais', 'VARCHAR(10)', 'nombre')
    """
    try:
        conn = get_connection()
        if not conn:
            print("Error: No se pudo conectar a la base de datos")
            return False
        
        cursor = conn.cursor()
        
        if after_column:
            query = f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {column_definition} AFTER `{after_column}`"
        else:
            query = f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {column_definition}"
        
        print(f"Ejecutando: {query}")
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✓ Columna '{column_name}' agregada a tabla '{table_name}'")
        return True
    
    except Error as e:
        print(f"Error MariaDB: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def modify_column(table_name: str, column_name: str, new_definition: str):
    """
    Modificar definición de una columna existente
    
    Args:
        table_name: Nombre de la tabla
        column_name: Nombre de la columna a modificar
        new_definition: Nueva definición (ej: "VARCHAR(500) NOT NULL")
    
    Ejemplo:
        modify_column('pais', 'id', 'INT AUTO_INCREMENT PRIMARY KEY')
    """
    try:
        conn = get_connection()
        if not conn:
            print("Error: No se pudo conectar a la base de datos")
            return False
        
        cursor = conn.cursor()
        query = f"ALTER TABLE `{table_name}` MODIFY COLUMN `{column_name}` {new_definition}"
        
        print(f"Ejecutando: {query}")
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✓ Columna '{column_name}' modificada en tabla '{table_name}'")
        return True
    
    except Error as e:
        print(f"Error MariaDB: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def drop_column(table_name: str, column_name: str):
    """
    Eliminar una columna de una tabla
    
    Args:
        table_name: Nombre de la tabla
        column_name: Nombre de la columna a eliminar
    
    Ejemplo:
        drop_column('pais', 'campo_viejo')
    """
    try:
        conn = get_connection()
        if not conn:
            print("Error: No se pudo conectar a la base de datos")
            return False
        
        cursor = conn.cursor()
        query = f"ALTER TABLE `{table_name}` DROP COLUMN `{column_name}`"
        
        print(f"Ejecutando: {query}")
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✓ Columna '{column_name}' eliminada de tabla '{table_name}'")
        return True
    
    except Error as e:
        print(f"Error MariaDB: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def rename_column(table_name: str, old_name: str, new_name: str, column_definition: str):
    """
    Renombrar una columna
    
    Args:
        table_name: Nombre de la tabla
        old_name: Nombre actual de la columna
        new_name: Nuevo nombre
        column_definition: Definición completa (ej: "VARCHAR(255)")
    
    Ejemplo:
        rename_column('pais', 'nombre_viejo', 'nombre_nuevo', 'VARCHAR(255)')
    """
    try:
        conn = get_connection()
        if not conn:
            print("Error: No se pudo conectar a la base de datos")
            return False
        
        cursor = conn.cursor()
        query = f"ALTER TABLE `{table_name}` CHANGE COLUMN `{old_name}` `{new_name}` {column_definition}"
        
        print(f"Ejecutando: {query}")
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✓ Columna '{old_name}' renombrada a '{new_name}' en tabla '{table_name}'")
        return True
    
    except Error as e:
        print(f"Error MariaDB: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def execute_custom_query(query: str):
    """
    Ejecutar una query personalizada
    
    Args:
        query: Query SQL personalizada
    
    Ejemplo:
        execute_custom_query("ALTER TABLE pais ADD INDEX idx_nombre (nombre)")
    """
    try:
        conn = get_connection()
        if not conn:
            print("Error: No se pudo conectar a la base de datos")
            return False
        
        cursor = conn.cursor()
        
        print(f"Ejecutando: {query}")
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Query ejecutada exitosamente")
        return True
    
    except Error as e:
        print(f"Error MariaDB: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Script de alteraciones de base de datos")
    print("=" * 60)
    
    # Ejemplo de uso (descomenta lo que necesites):
    
    # add_column('pais', 'codigo_pais', 'VARCHAR(10)', 'nombre')
    # modify_column('pais', 'id', 'INT AUTO_INCREMENT PRIMARY KEY')
    # drop_column('pais', 'campo_viejo')
    # rename_column('pais', 'nombre_viejo', 'nombre_nuevo', 'VARCHAR(255)')
    # execute_custom_query("ALTER TABLE pais ADD INDEX idx_nombre (nombre)")
    
    print("\nPara usar este script, llama las funciones directamente:")
    print("- add_column(table, column, definition, after_column)")
    print("- modify_column(table, column, new_definition)")
    print("- drop_column(table, column)")
    print("- rename_column(table, old_name, new_name, definition)")
    print("- execute_custom_query(query)")
