from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from connection import get_connection
from models import (
    Conjunto, ConjuntoCreate, Pais, PaisCreate, Producto, ProductoCreate, 
    Linea, LineaCreate, LineaDetallada, Precio, PrecioCreate, PrecioDetallado,
    GenericResponse, ListResponse
)
from typing import List
from mysql.connector import Error

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
            "conjuntos": "/conjuntos",
            "paises": "/paises",
            "productos": "/productos",
            "lineas": "/lineas",
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
            cursor.fetchone()  # Leer el resultado
            cursor.close()
            conn.close()
            return {"status": "healthy", "database": "connected"}
        else:
            return {"status": "unhealthy", "database": "disconnected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ ENDPOINTS CONJUNTO ============

@app.get("/conjuntos", response_model=ListResponse)
async def get_conjuntos(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener lista de conjuntos con paginación"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Contar total de conjuntos
        cursor.execute("SELECT COUNT(*) FROM conjunto")
        total = cursor.fetchone()[0]
        
        # Obtener conjuntos con paginación
        query = "SELECT id, sitio, nombre FROM conjunto LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, skip))
        
        conjuntos = []
        for row in cursor.fetchall():
            conjunto = {
                "id": row[0],
                "sitio": row[1],
                "nombre": row[2]
            }
            conjuntos.append(conjunto)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(conjuntos)} conjuntos",
            data=conjuntos,
            total=total
        )
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/conjuntos/{conjunto_id}", response_model=GenericResponse)
async def get_conjunto(conjunto_id: int):
    """Obtener un conjunto específico por ID"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, sitio, nombre FROM conjunto WHERE id = %s", (conjunto_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Conjunto con ID {conjunto_id} no encontrado")
        
        conjunto = {
            "id": row[0],
            "sitio": row[1],
            "nombre": row[2]
        }
        
        return GenericResponse(
            success=True,
            message="Conjunto obtenido correctamente",
            data=conjunto
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

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
        query = "SELECT id, nombre, unidad, unidades, moneda, moneda_tic, simbolo FROM pais LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, skip))
        
        paises = []
        for row in cursor.fetchall():
            pais = {
                "id": row[0],
                "nombre": row[1],
                "unidad": row[2],
                "unidades": row[3],
                "moneda": row[4],
                "moneda_tic": row[5],
                "simbolo": row[6]
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
    
    except Error as e:
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
        cursor.execute("SELECT id, nombre, unidad, unidades, moneda, moneda_tic, simbolo FROM pais WHERE id = %s", (pais_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"País con ID {pais_id} no encontrado")
        
        pais = {
            "id": row[0],
            "nombre": row[1],
            "unidad": row[2],
            "unidades": row[3],
            "moneda": row[4],
            "moneda_tic": row[5],
            "simbolo": row[6]
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
        query = "SELECT id, nombre, cantidad, unidad_general, precio_base FROM producto LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, skip))
        
        productos = []
        for row in cursor.fetchall():
            producto = {
                "id": row[0],
                "nombre": row[1],
                "cantidad": row[2],
                "unidad_general": row[3],
                "precio_base": row[4]
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
    
    except Error as e:
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
        cursor.execute("SELECT id, nombre, cantidad, unidad_general, precio_base FROM producto WHERE id = %s", (producto_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Producto con ID {producto_id} no encontrado")
        
        producto = {
            "id": row[0],
            "nombre": row[1],
            "cantidad": row[2],
            "unidad_general": row[3],
            "precio_base": row[4]
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

# ============ ENDPOINTS LINEA ============

@app.get("/lineas", response_model=ListResponse)
async def get_lineas(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener lista de líneas con información detallada"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Contar total de líneas
        cursor.execute("SELECT COUNT(*) FROM linea")
        total = cursor.fetchone()[0]
        
        # Obtener líneas con información detallada
        query = """
            SELECT 
                l.id, l.id_conjunto, l.id_producto,
                c.nombre, c.sitio,
                p.nombre, p.cantidad
            FROM linea l
            LEFT JOIN conjunto c ON l.id_conjunto = c.id
            LEFT JOIN producto p ON l.id_producto = p.id
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, skip))
        
        lineas = []
        for row in cursor.fetchall():
            linea = {
                "id": row[0],
                "id_conjunto": row[1],
                "id_producto": row[2],
                "conjunto_nombre": row[3],
                "conjunto_sitio": row[4],
                "producto_nombre": row[5],
                "producto_cantidad": row[6]
            }
            lineas.append(linea)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(lineas)} líneas",
            data=lineas,
            total=total
        )
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/lineas/{linea_id}", response_model=GenericResponse)
async def get_linea(linea_id: int):
    """Obtener una línea específica con información detallada"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        query = """
            SELECT 
                l.id, l.id_conjunto, l.id_producto,
                c.nombre, c.sitio,
                p.nombre, p.cantidad
            FROM linea l
            LEFT JOIN conjunto c ON l.id_conjunto = c.id
            LEFT JOIN producto p ON l.id_producto = p.id
            WHERE l.id = %s
        """
        cursor.execute(query, (linea_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Línea con ID {linea_id} no encontrada")
        
        linea = {
            "id": row[0],
            "id_conjunto": row[1],
            "id_producto": row[2],
            "conjunto_nombre": row[3],
            "conjunto_sitio": row[4],
            "producto_nombre": row[5],
            "producto_cantidad": row[6]
        }
        
        return GenericResponse(
            success=True,
            message="Línea obtenida correctamente",
            data=linea
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/lineas/conjunto/{conjunto_id}", response_model=ListResponse)
async def get_lineas_by_conjunto(conjunto_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener todas las líneas de un conjunto específico"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Contar total de líneas
        cursor.execute("SELECT COUNT(*) FROM linea WHERE id_conjunto = %s", (conjunto_id,))
        total = cursor.fetchone()[0]
        
        # Obtener líneas
        query = """
            SELECT 
                l.id, l.id_conjunto, l.id_producto,
                c.nombre, c.sitio,
                p.nombre, p.cantidad
            FROM linea l
            LEFT JOIN conjunto c ON l.id_conjunto = c.id
            LEFT JOIN producto p ON l.id_producto = p.id
            WHERE l.id_conjunto = %s
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (conjunto_id, limit, skip))
        
        lineas = []
        for row in cursor.fetchall():
            linea = {
                "id": row[0],
                "id_conjunto": row[1],
                "id_producto": row[2],
                "conjunto_nombre": row[3],
                "conjunto_sitio": row[4],
                "producto_nombre": row[5],
                "producto_cantidad": row[6]
            }
            lineas.append(linea)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(lineas)} líneas del conjunto ID {conjunto_id}",
            data=lineas,
            total=total
        )
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# ============ ENDPOINTS PRECIO ============

@app.get("/precios", response_model=ListResponse)
async def get_precios(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener lista de precios con información detallada"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Contar total de precios
        cursor.execute("SELECT COUNT(*) FROM precio")
        total = cursor.fetchone()[0]
        
        # Obtener precios con información detallada (línea → conjunto → producto, país)
        query = """
            SELECT 
                pr.id, pr.nombre, pr.id_linea, pr.id_pais, pr.price_id, 
                pr.cantidad_precio, pr.ratio_imagen, pr.status,
                l.id, p.nombre, p.cantidad,
                c.nombre, 
                pa.nombre, pa.moneda, pa.simbolo
            FROM precio pr
            LEFT JOIN linea l ON pr.id_linea = l.id
            LEFT JOIN producto p ON l.id_producto = p.id
            LEFT JOIN conjunto c ON l.id_conjunto = c.id
            LEFT JOIN pais pa ON pr.id_pais = pa.id
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, skip))
        
        precios = []
        for row in cursor.fetchall():
            precio = {
                "id": row[0],
                "nombre": row[1],
                "id_linea": row[2],
                "id_pais": row[3],
                "price_id": row[4],
                "cantidad_precio": row[5],
                "ratio_imagen": row[6],
                "status": row[7],
                "linea_id": row[8],
                "producto_nombre": row[9],
                "producto_cantidad": row[10],
                "conjunto_nombre": row[11],
                "pais_nombre": row[12],
                "pais_moneda": row[13],
                "pais_simbolo": row[14]
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
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/precios/{precio_id}", response_model=GenericResponse)
async def get_precio(precio_id: int):
    """Obtener un precio específico con información detallada"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        query = """
            SELECT 
                pr.id, pr.nombre, pr.id_linea, pr.id_pais, pr.price_id, 
                pr.cantidad_precio, pr.ratio_imagen, pr.status,
                l.id, p.nombre, p.cantidad,
                c.nombre, 
                pa.nombre, pa.moneda, pa.simbolo
            FROM precio pr
            LEFT JOIN linea l ON pr.id_linea = l.id
            LEFT JOIN producto p ON l.id_producto = p.id
            LEFT JOIN conjunto c ON l.id_conjunto = c.id
            LEFT JOIN pais pa ON pr.id_pais = pa.id
            WHERE pr.id = %s
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
            "id_linea": row[2],
            "id_pais": row[3],
            "price_id": row[4],
            "cantidad_precio": row[5],
            "ratio_imagen": row[6],
            "status": row[7],
            "linea_id": row[8],
            "producto_nombre": row[9],
            "producto_cantidad": row[10],
            "conjunto_nombre": row[11],
            "pais_nombre": row[12],
            "pais_moneda": row[13],
            "pais_simbolo": row[14]
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

@app.get("/precios/linea/{linea_id}", response_model=ListResponse)
async def get_precios_by_linea(linea_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener todos los precios de una línea específica en diferentes países"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Contar total de precios para esta línea
        cursor.execute("SELECT COUNT(*) FROM precio WHERE id_linea = %s", (linea_id,))
        total = cursor.fetchone()[0]
        
        # Obtener precios
        query = """
            SELECT 
                pr.id, pr.nombre, pr.id_linea, pr.id_pais, pr.price_id, 
                pr.cantidad_precio, pr.ratio_imagen, pr.status,
                l.id, p.nombre, p.cantidad,
                c.nombre, 
                pa.nombre, pa.moneda, pa.simbolo
            FROM precio pr
            LEFT JOIN linea l ON pr.id_linea = l.id
            LEFT JOIN producto p ON l.id_producto = p.id
            LEFT JOIN conjunto c ON l.id_conjunto = c.id
            LEFT JOIN pais pa ON pr.id_pais = pa.id
            WHERE pr.id_linea = %s
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (linea_id, limit, skip))
        
        precios = []
        for row in cursor.fetchall():
            precio = {
                "id": row[0],
                "nombre": row[1],
                "id_linea": row[2],
                "id_pais": row[3],
                "price_id": row[4],
                "cantidad_precio": row[5],
                "ratio_imagen": row[6],
                "status": row[7],
                "linea_id": row[8],
                "producto_nombre": row[9],
                "producto_cantidad": row[10],
                "conjunto_nombre": row[11],
                "pais_nombre": row[12],
                "pais_moneda": row[13],
                "pais_simbolo": row[14]
            }
            precios.append(precio)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(precios)} precios para la línea ID {linea_id}",
            data=precios,
            total=total
        )
    
    except Error as e:
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
        cursor.execute("SELECT COUNT(*) FROM precio WHERE id_pais = %s", (pais_id,))
        total = cursor.fetchone()[0]
        
        # Obtener precios
        query = """
            SELECT 
                pr.id, pr.nombre, pr.id_linea, pr.id_pais, pr.price_id, 
                pr.cantidad_precio, pr.ratio_imagen, pr.status,
                l.id, p.nombre, p.cantidad,
                c.nombre, 
                pa.nombre, pa.moneda, pa.simbolo
            FROM precio pr
            LEFT JOIN linea l ON pr.id_linea = l.id
            LEFT JOIN producto p ON l.id_producto = p.id
            LEFT JOIN conjunto c ON l.id_conjunto = c.id
            LEFT JOIN pais pa ON pr.id_pais = pa.id
            WHERE pr.id_pais = %s
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (pais_id, limit, skip))
        
        precios = []
        for row in cursor.fetchall():
            precio = {
                "id": row[0],
                "nombre": row[1],
                "id_linea": row[2],
                "id_pais": row[3],
                "price_id": row[4],
                "cantidad_precio": row[5],
                "ratio_imagen": row[6],
                "status": row[7],
                "linea_id": row[8],
                "producto_nombre": row[9],
                "producto_cantidad": row[10],
                "conjunto_nombre": row[11],
                "pais_nombre": row[12],
                "pais_moneda": row[13],
                "pais_simbolo": row[14]
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
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
