"""
Script para agregar campos 'side' y 'decs' a la tabla 'pais'
"""

from alter_db import add_column

if __name__ == "__main__":
    print("Agregando campos a tabla 'pais'")
    print("=" * 60)
    
    # Agregar campo 'side' (booleano)
    result1 = add_column('pais', 'side', 'BOOLEAN DEFAULT 0', 'simbolo')
    
    # Agregar campo 'decs' (entero)
    result2 = add_column('pais', 'decs', 'INT DEFAULT 0', 'side')
    
    print("=" * 60)
    if result1 and result2:
        print("✓ Todos los campos fueron agregados exitosamente")
    else:
        print("✗ Hubo un error al agregar los campos")
