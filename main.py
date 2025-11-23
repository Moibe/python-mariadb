from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from connection import get_connection
from models import (
    Pais, PaisCreate, Producto, ProductoCreate, 
    Precio, PrecioCreate, PrecioDetallado,
    GenericResponse, ListResponse
)
from typing import List
import mariadb

# Crear la aplicación FastAPI
app = FastAPI(
    title="Splashmix API",
    description="API para consumir datos de Splashmix (Pais, Producto, Precio)",
    version="1.0.0"
)

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint de bienvenida"""
    return {
        "mensaje": "Bienvenido a la API de Splashmix",
        "version": "1.0.0",
        "documentación": "/docs",
        "endpoints": {
            "paises": "/paises",
            "productos": "/productos",
            "precios": "/precios"
        }
    }

@app.get("/health")
async def health_check():
    """Verificar que la API y la base de datos están activas"""
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            return {"status": "healthy", "database": "connected"}
        else:
            return {"status": "unhealthy", "database": "disconnected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ ENDPOINTS PAIS ============

@app.get("/paises", response_model=ListResponse)
async def get_paises(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener lista de países con paginación"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Contar total de países
        cursor.execute("SELECT COUNT(*) FROM pais")
        total = cursor.fetchone()[0]
        
        # Obtener países con paginación
        query = "SELECT id, nombre, moneda, moneda_tic, simbolo FROM pais LIMIT ? OFFSET ?"
        cursor.execute(query, (limit, skip))
        
        paises = []
        for row in cursor.fetchall():
            pais = {
                "id": row[0],
                "nombre": row[1],
                "moneda": row[2],
                "moneda_tic": row[3],
                "simbolo": row[4]
            }
            paises.append(pais)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(paises)} países",
            data=paises,
            total=total
        )
    
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/paises/{pais_id}", response_model=GenericResponse)
async def get_pais(pais_id: int):
    """Obtener un país específico por ID"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, moneda, moneda_tic, simbolo FROM pais WHERE id = ?", (pais_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"País con ID {pais_id} no encontrado")
        
        pais = {
            "id": row[0],
            "nombre": row[1],
            "moneda": row[2],
            "moneda_tic": row[3],
            "simbolo": row[4]
        }
        
        return GenericResponse(
            success=True,
            message="País obtenido correctamente",
            data=pais
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============ ENDPOINTS PRODUCTO ============

@app.get("/productos", response_model=ListResponse)
async def get_productos(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener lista de productos con paginación"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Contar total de productos
        cursor.execute("SELECT COUNT(*) FROM producto")
        total = cursor.fetchone()[0]
        
        # Obtener productos con paginación
        query = "SELECT id, nombre, precio_mxn FROM producto LIMIT ? OFFSET ?"
        cursor.execute(query, (limit, skip))
        
        productos = []
        for row in cursor.fetchall():
            producto = {
                "id": row[0],
                "nombre": row[1],
                "precio_mxn": row[2]
            }
            productos.append(producto)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(productos)} productos",
            data=productos,
            total=total
        )
    
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/productos/{producto_id}", response_model=GenericResponse)
async def get_producto(producto_id: int):
    """Obtener un producto específico por ID"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio_mxn FROM producto WHERE id = ?", (producto_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Producto con ID {producto_id} no encontrado")
        
        producto = {
            "id": row[0],
            "nombre": row[1],
            "precio_mxn": row[2]
        }
        
        return GenericResponse(
            success=True,
            message="Producto obtenido correctamente",
            data=producto
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============ ENDPOINTS PRECIO ============

@app.get("/precios", response_model=ListResponse)
async def get_precios(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener lista de precios con paginación y información detallada"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Contar total de precios
        cursor.execute("SELECT COUNT(*) FROM precio")
        total = cursor.fetchone()[0]
        
        # Obtener precios con información de producto y país
        query = """
            SELECT 
                p.id, p.nombre, p.id_producto, p.id_pais, p.status, p.price_id,
                prod.nombre, pais.nombre, pais.moneda
            FROM precio p
            LEFT JOIN producto prod ON p.id_producto = prod.id
            LEFT JOIN pais pais ON p.id_pais = pais.id
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, (limit, skip))
        
        precios = []
        for row in cursor.fetchall():
            precio = {
                "id": row[0],
                "nombre": row[1],
                "id_producto": row[2],
                "id_pais": row[3],
                "status": row[4],
                "price_id": row[5],
                "producto_nombre": row[6],
                "pais_nombre": row[7],
                "pais_moneda": row[8]
            }
            precios.append(precio)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(precios)} precios",
            data=precios,
            total=total
        )
    
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/precios/{precio_id}", response_model=GenericResponse)
async def get_precio(precio_id: int):
    """Obtener un precio específico por ID con información detallada"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        query = """
            SELECT 
                p.id, p.nombre, p.id_producto, p.id_pais, p.status, p.price_id,
                prod.nombre, pais.nombre, pais.moneda
            FROM precio p
            LEFT JOIN producto prod ON p.id_producto = prod.id
            LEFT JOIN pais pais ON p.id_pais = pais.id
            WHERE p.id = ?
        """
        cursor.execute(query, (precio_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Precio con ID {precio_id} no encontrado")
        
        precio = {
            "id": row[0],
            "nombre": row[1],
            "id_producto": row[2],
            "id_pais": row[3],
            "status": row[4],
            "price_id": row[5],
            "producto_nombre": row[6],
            "pais_nombre": row[7],
            "pais_moneda": row[8]
        }
        
        return GenericResponse(
            success=True,
            message="Precio obtenido correctamente",
            data=precio
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/precios/producto/{producto_id}", response_model=ListResponse)
async def get_precios_by_producto(producto_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener todos los precios de un producto específico"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Contar total de precios para este producto
        cursor.execute("SELECT COUNT(*) FROM precio WHERE id_producto = ?", (producto_id,))
        total = cursor.fetchone()[0]
        
        # Obtener precios
        query = """
            SELECT 
                p.id, p.nombre, p.id_producto, p.id_pais, p.status, p.price_id,
                prod.nombre, pais.nombre, pais.moneda
            FROM precio p
            LEFT JOIN producto prod ON p.id_producto = prod.id
            LEFT JOIN pais pais ON p.id_pais = pais.id
            WHERE p.id_producto = ?
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, (producto_id, limit, skip))
        
        precios = []
        for row in cursor.fetchall():
            precio = {
                "id": row[0],
                "nombre": row[1],
                "id_producto": row[2],
                "id_pais": row[3],
                "status": row[4],
                "price_id": row[5],
                "producto_nombre": row[6],
                "pais_nombre": row[7],
                "pais_moneda": row[8]
            }
            precios.append(precio)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(precios)} precios para el producto ID {producto_id}",
            data=precios,
            total=total
        )
    
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/precios/pais/{pais_id}", response_model=ListResponse)
async def get_precios_by_pais(pais_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener todos los precios para un país específico"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Contar total de precios para este país
        cursor.execute("SELECT COUNT(*) FROM precio WHERE id_pais = ?", (pais_id,))
        total = cursor.fetchone()[0]
        
        # Obtener precios
        query = """
            SELECT 
                p.id, p.nombre, p.id_producto, p.id_pais, p.status, p.price_id,
                prod.nombre, pais.nombre, pais.moneda
            FROM precio p
            LEFT JOIN producto prod ON p.id_producto = prod.id
            LEFT JOIN pais pais ON p.id_pais = pais.id
            WHERE p.id_pais = ?
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, (pais_id, limit, skip))
        
        precios = []
        for row in cursor.fetchall():
            precio = {
                "id": row[0],
                "nombre": row[1],
                "id_producto": row[2],
                "id_pais": row[3],
                "status": row[4],
                "price_id": row[5],
                "producto_nombre": row[6],
                "pais_nombre": row[7],
                "pais_moneda": row[8]
            }
            precios.append(precio)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(precios)} precios para el país ID {pais_id}",
            data=precios,
            total=total
        )
    
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
