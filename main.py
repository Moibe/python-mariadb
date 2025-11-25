from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from connection import get_connection
from models import (
    Conjunto, ConjuntoCreate, TipoProducto, TipoProductoCreate, Pais, PaisCreate, 
    Producto, ProductoCreate, ProductoDetallado, Pertenencia, PertenenciaCreate, PertenenciaDetallada,
    Textos, TextosCreate, TextosDetallado, Precio, PrecioCreate, PrecioDetallado,
    GenericResponse, ListResponse
)
from typing import List
from mysql.connector import Error

# Crear la aplicación FastAPI
app = FastAPI(
    title="Splashmix API",
    description="API para consumir datos de Splashmix (Conjunto, Tipo Producto, País, Producto, Pertenencia, Textos, Precio)",
    version="2.0.0"
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
        "mensaje": "Bienvenido a la API de Splashmix v2",
        "version": "2.0.0",
        "documentación": "/docs",
        "endpoints": {
            "conjuntos": "/conjuntos",
            "tipos_productos": "/tipos-productos",
            "paises": "/paises",
            "productos": "/productos",
            "pertenencias": "/pertenencias",
            "textos": "/textos",
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
            cursor.fetchone()
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
        cursor.execute("SELECT COUNT(*) FROM conjunto")
        total = cursor.fetchone()[0]
        
        query = "SELECT id, sitio, nombre FROM conjunto LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, skip))
        
        conjuntos = []
        for row in cursor.fetchall():
            conjunto = {"id": row[0], "sitio": row[1], "nombre": row[2]}
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
        
        conjunto = {"id": row[0], "sitio": row[1], "nombre": row[2]}
        
        return GenericResponse(
            success=True,
            message="Conjunto obtenido correctamente",
            data=conjunto
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============ ENDPOINTS TIPO_PRODUCTO ============

@app.get("/tipos-productos", response_model=ListResponse)
async def get_tipos_productos(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener lista de tipos de productos"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tipo_producto")
        total = cursor.fetchone()[0]
        
        query = "SELECT id, nombre, unidad_base FROM tipo_producto LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, skip))
        
        tipos = []
        for row in cursor.fetchall():
            tipo = {"id": row[0], "nombre": row[1], "unidad_base": row[2]}
            tipos.append(tipo)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(tipos)} tipos de productos",
            data=tipos,
            total=total
        )
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/tipos-productos/{tipo_id}", response_model=GenericResponse)
async def get_tipo_producto(tipo_id: int):
    """Obtener un tipo de producto específico"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, unidad_base FROM tipo_producto WHERE id = %s", (tipo_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Tipo de producto con ID {tipo_id} no encontrado")
        
        tipo = {"id": row[0], "nombre": row[1], "unidad_base": row[2]}
        
        return GenericResponse(
            success=True,
            message="Tipo de producto obtenido correctamente",
            data=tipo
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============ ENDPOINTS PAIS ============

@app.get("/paises", response_model=ListResponse)
async def get_paises(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener lista de países"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pais")
        total = cursor.fetchone()[0]
        
        query = "SELECT id, nombre, moneda, moneda_tic, simbolo, side, decs FROM pais LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, skip))
        
        paises = []
        for row in cursor.fetchall():
            pais = {
                "id": row[0], "nombre": row[1], "moneda": row[2], "moneda_tic": row[3],
                "simbolo": row[4], "side": row[5], "decs": row[6]
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
async def get_pais(pais_id: str):
    """Obtener un país específico"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, moneda, moneda_tic, simbolo, side, decs FROM pais WHERE id = %s", (pais_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"País con ID {pais_id} no encontrado")
        
        pais = {
            "id": row[0], "nombre": row[1], "moneda": row[2], "moneda_tic": row[3],
            "simbolo": row[4], "side": row[5], "decs": row[6]
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
    """Obtener lista de productos con información detallada"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM producto")
        total = cursor.fetchone()[0]
        
        query = """
            SELECT 
                p.id, p.nombre, p.cantidad, p.precio_base,
                p.id_tipo_producto, p.id_conjunto,
                tp.nombre, tp.unidad_base,
                c.nombre
            FROM producto p
            LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
            LEFT JOIN conjunto c ON p.id_conjunto = c.id
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, skip))
        
        productos = []
        for row in cursor.fetchall():
            producto = {
                "id": row[0], "nombre": row[1], "cantidad": row[2], "precio_base": row[3],
                "id_tipo_producto": row[4], "id_conjunto": row[5],
                "tipo_producto_nombre": row[6], "tipo_producto_unidad_base": row[7],
                "conjunto_nombre": row[8]
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
    """Obtener un producto específico"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        query = """
            SELECT 
                p.id, p.nombre, p.cantidad, p.precio_base,
                p.id_tipo_producto, p.id_conjunto,
                tp.nombre, tp.unidad_base,
                c.nombre
            FROM producto p
            LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
            LEFT JOIN conjunto c ON p.id_conjunto = c.id
            WHERE p.id = %s
        """
        cursor.execute(query, (producto_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Producto con ID {producto_id} no encontrado")
        
        producto = {
            "id": row[0], "nombre": row[1], "cantidad": row[2], "precio_base": row[3],
            "id_tipo_producto": row[4], "id_conjunto": row[5],
            "tipo_producto_nombre": row[6], "tipo_producto_unidad_base": row[7],
            "conjunto_nombre": row[8]
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

# ============ ENDPOINTS PERTENENCIA ============

@app.get("/pertenencias", response_model=ListResponse)
async def get_pertenencias(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener lista de pertenencias con información detallada"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pertenencia")
        total = cursor.fetchone()[0]
        
        query = """
            SELECT 
                pe.id, pe.id_conjunto, pe.id_producto,
                c.nombre, c.sitio,
                p.nombre, p.cantidad,
                tp.nombre
            FROM pertenencia pe
            LEFT JOIN conjunto c ON pe.id_conjunto = c.id
            LEFT JOIN producto p ON pe.id_producto = p.id
            LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, skip))
        
        pertenencias = []
        for row in cursor.fetchall():
            pertenencia = {
                "id": row[0], "id_conjunto": row[1], "id_producto": row[2],
                "conjunto_nombre": row[3], "conjunto_sitio": row[4],
                "producto_nombre": row[5], "producto_cantidad": row[6],
                "tipo_producto_nombre": row[7]
            }
            pertenencias.append(pertenencia)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(pertenencias)} pertenencias",
            data=pertenencias,
            total=total
        )
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/pertenencias/{pertenencia_id}", response_model=GenericResponse)
async def get_pertenencia(pertenencia_id: int):
    """Obtener una pertenencia específica"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        query = """
            SELECT 
                pe.id, pe.id_conjunto, pe.id_producto,
                c.nombre, c.sitio,
                p.nombre, p.cantidad,
                tp.nombre
            FROM pertenencia pe
            LEFT JOIN conjunto c ON pe.id_conjunto = c.id
            LEFT JOIN producto p ON pe.id_producto = p.id
            LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
            WHERE pe.id = %s
        """
        cursor.execute(query, (pertenencia_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Pertenencia con ID {pertenencia_id} no encontrada")
        
        pertenencia = {
            "id": row[0], "id_conjunto": row[1], "id_producto": row[2],
            "conjunto_nombre": row[3], "conjunto_sitio": row[4],
            "producto_nombre": row[5], "producto_cantidad": row[6],
            "tipo_producto_nombre": row[7]
        }
        
        return GenericResponse(
            success=True,
            message="Pertenencia obtenida correctamente",
            data=pertenencia
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/pertenencias/conjunto/{conjunto_id}", response_model=ListResponse)
async def get_pertenencias_by_conjunto(conjunto_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener todas las pertenencias de un conjunto"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pertenencia WHERE id_conjunto = %s", (conjunto_id,))
        total = cursor.fetchone()[0]
        
        query = """
            SELECT 
                pe.id, pe.id_conjunto, pe.id_producto,
                c.nombre, c.sitio,
                p.nombre, p.cantidad,
                tp.nombre
            FROM pertenencia pe
            LEFT JOIN conjunto c ON pe.id_conjunto = c.id
            LEFT JOIN producto p ON pe.id_producto = p.id
            LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
            WHERE pe.id_conjunto = %s
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (conjunto_id, limit, skip))
        
        pertenencias = []
        for row in cursor.fetchall():
            pertenencia = {
                "id": row[0], "id_conjunto": row[1], "id_producto": row[2],
                "conjunto_nombre": row[3], "conjunto_sitio": row[4],
                "producto_nombre": row[5], "producto_cantidad": row[6],
                "tipo_producto_nombre": row[7]
            }
            pertenencias.append(pertenencia)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(pertenencias)} pertenencias del conjunto",
            data=pertenencias,
            total=total
        )
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# ============ ENDPOINTS TEXTOS ============

@app.get("/textos", response_model=ListResponse)
async def get_textos(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """Obtener lista de textos localizados"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM textos")
        total = cursor.fetchone()[0]
        
        query = """
            SELECT 
                t.id, t.id_tipo_producto, t.id_pais, t.unidad, t.unidades,
                tp.nombre, p.nombre
            FROM textos t
            LEFT JOIN tipo_producto tp ON t.id_tipo_producto = tp.id
            LEFT JOIN pais p ON t.id_pais = p.id
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, skip))
        
        textos = []
        for row in cursor.fetchall():
            texto = {
                "id": row[0], "id_tipo_producto": row[1], "id_pais": row[2],
                "unidad": row[3], "unidades": row[4],
                "tipo_producto_nombre": row[5], "pais_nombre": row[6]
            }
            textos.append(texto)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(textos)} textos",
            data=textos,
            total=total
        )
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/textos/{texto_id}", response_model=GenericResponse)
async def get_texto(texto_id: int):
    """Obtener un texto específico"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        query = """
            SELECT 
                t.id, t.id_tipo_producto, t.id_pais, t.unidad, t.unidades,
                tp.nombre, p.nombre
            FROM textos t
            LEFT JOIN tipo_producto tp ON t.id_tipo_producto = tp.id
            LEFT JOIN pais p ON t.id_pais = p.id
            WHERE t.id = %s
        """
        cursor.execute(query, (texto_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Texto con ID {texto_id} no encontrado")
        
        texto = {
            "id": row[0], "id_tipo_producto": row[1], "id_pais": row[2],
            "unidad": row[3], "unidades": row[4],
            "tipo_producto_nombre": row[5], "pais_nombre": row[6]
        }
        
        return GenericResponse(
            success=True,
            message="Texto obtenido correctamente",
            data=texto
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/textos/tipo-pais/{tipo_id}/{pais_id}", response_model=GenericResponse)
async def get_texto_by_tipo_pais(tipo_id: int, pais_id: str):
    """Obtener textos para un tipo de producto y país específicos"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        query = """
            SELECT 
                t.id, t.id_tipo_producto, t.id_pais, t.unidad, t.unidades,
                tp.nombre, p.nombre
            FROM textos t
            LEFT JOIN tipo_producto tp ON t.id_tipo_producto = tp.id
            LEFT JOIN pais p ON t.id_pais = p.id
            WHERE t.id_tipo_producto = %s AND t.id_pais = %s
        """
        cursor.execute(query, (tipo_id, pais_id))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Texto para tipo {tipo_id} y país {pais_id} no encontrado")
        
        texto = {
            "id": row[0], "id_tipo_producto": row[1], "id_pais": row[2],
            "unidad": row[3], "unidades": row[4],
            "tipo_producto_nombre": row[5], "pais_nombre": row[6]
        }
        
        return GenericResponse(
            success=True,
            message="Texto obtenido correctamente",
            data=texto
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============ ENDPOINTS PRECIO ============

@app.get("/precios", response_model=ListResponse)
async def get_precios(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), ambiente: str = Query(None)):
    """Obtener lista de precios con información completa. Filtrar por ambiente opcional (sandbox/production)"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        # Query de conteo
        if ambiente:
            cursor.execute("SELECT COUNT(*) FROM precio WHERE ambiente = %s", (ambiente,))
        else:
            cursor.execute("SELECT COUNT(*) FROM precio")
        total = cursor.fetchone()[0]
        
        # Query principal - SIEMPRE igual, solo cambiar los parámetros
        query = """
            SELECT 
                pr.id, pr.nombre, pr.id_pertenencia, pr.id_pais, pr.price_id,
                pr.cantidad_precio, pr.ratio_imagen, pr.status, pr.ambiente,
                pe.id, p.nombre, p.cantidad,
                tp.nombre,
                c.nombre,
                pa.nombre, pa.moneda, pa.simbolo, pa.side, pa.decs
            FROM precio pr
            LEFT JOIN pertenencia pe ON pr.id_pertenencia = pe.id
            LEFT JOIN producto p ON pe.id_producto = p.id
            LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
            LEFT JOIN conjunto c ON pe.id_conjunto = c.id
            LEFT JOIN pais pa ON pr.id_pais = pa.id
        """
        
        # Construir condición WHERE si hay ambiente
        if ambiente:
            query += " WHERE pr.ambiente = %s"
            query += " LIMIT %s OFFSET %s"
            cursor.execute(query, (ambiente, limit, skip))
        else:
            query += " LIMIT %s OFFSET %s"
            cursor.execute(query, (limit, skip))
        
        precios = []
        for row in cursor.fetchall():
            precio = {
                "id": row[0], "nombre": row[1], "id_pertenencia": row[2], "id_pais": row[3],
                "price_id": row[4], "cantidad_precio": row[5], "ratio_imagen": row[6], "status": row[7], "ambiente": row[8],
                "pertenencia_id": row[9], "producto_nombre": row[10], "producto_cantidad": row[11],
                "tipo_producto_nombre": row[12], "conjunto_nombre": row[13],
                "pais_nombre": row[14], "pais_moneda": row[15], "pais_simbolo": row[16],
                "pais_side": row[17], "pais_decs": row[18]
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
    """Obtener un precio específico"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        query = """
            SELECT 
                pr.id, pr.nombre, pr.id_pertenencia, pr.id_pais, pr.price_id,
                pr.cantidad_precio, pr.ratio_imagen, pr.status, pr.ambiente,
                pe.id, p.nombre, p.cantidad,
                tp.nombre,
                c.nombre,
                pa.nombre, pa.moneda, pa.simbolo, pa.side, pa.decs
            FROM precio pr
            LEFT JOIN pertenencia pe ON pr.id_pertenencia = pe.id
            LEFT JOIN producto p ON pe.id_producto = p.id
            LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
            LEFT JOIN conjunto c ON pe.id_conjunto = c.id
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
            "id": row[0], "nombre": row[1], "id_pertenencia": row[2], "id_pais": row[3],
            "price_id": row[4], "cantidad_precio": row[5], "ratio_imagen": row[6], "status": row[7], "ambiente": row[8],
            "pertenencia_id": row[9], "producto_nombre": row[10], "producto_cantidad": row[11],
            "tipo_producto_nombre": row[12], "conjunto_nombre": row[13],
            "pais_nombre": row[14], "pais_moneda": row[15], "pais_simbolo": row[16],
            "pais_side": row[17], "pais_decs": row[18]
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

@app.get("/precios/pertenencia/{pertenencia_id}", response_model=ListResponse)
async def get_precios_by_pertenencia(pertenencia_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), ambiente: str = Query(None)):
    """Obtener todos los precios de una pertenencia en diferentes países. Filtrar por ambiente opcional (sandbox/production)"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        count_query = "SELECT COUNT(*) FROM precio WHERE id_pertenencia = %s"
        if ambiente:
            count_query += " AND ambiente = %s"
            cursor.execute(count_query, (pertenencia_id, ambiente))
        else:
            cursor.execute(count_query, (pertenencia_id,))
        total = cursor.fetchone()[0]
        
        if ambiente:
            query = """
                SELECT 
                    pr.id, pr.nombre, pr.id_pertenencia, pr.id_pais, pr.price_id,
                    pr.cantidad_precio, pr.ratio_imagen, pr.status, pr.ambiente,
                    pe.id, p.nombre, p.cantidad,
                    tp.nombre,
                    c.nombre,
                    pa.nombre, pa.moneda, pa.simbolo, pa.side, pa.decs
                FROM precio pr
                LEFT JOIN pertenencia pe ON pr.id_pertenencia = pe.id
                LEFT JOIN producto p ON pe.id_producto = p.id
                LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
                LEFT JOIN conjunto c ON pe.id_conjunto = c.id
                LEFT JOIN pais pa ON pr.id_pais = pa.id
                WHERE pr.id_pertenencia = %s AND pr.ambiente = %s
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (pertenencia_id, ambiente, limit, skip))
        else:
            query = """
                SELECT 
                    pr.id, pr.nombre, pr.id_pertenencia, pr.id_pais, pr.price_id,
                    pr.cantidad_precio, pr.ratio_imagen, pr.status, pr.ambiente,
                    pe.id, p.nombre, p.cantidad,
                    tp.nombre,
                    c.nombre,
                    pa.nombre, pa.moneda, pa.simbolo, pa.side, pa.decs
                FROM precio pr
                LEFT JOIN pertenencia pe ON pr.id_pertenencia = pe.id
                LEFT JOIN producto p ON pe.id_producto = p.id
                LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
                LEFT JOIN conjunto c ON pe.id_conjunto = c.id
                LEFT JOIN pais pa ON pr.id_pais = pa.id
                WHERE pr.id_pertenencia = %s
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (pertenencia_id, limit, skip))
        
        precios = []
        for row in cursor.fetchall():
            precio = {
                "id": row[0], "nombre": row[1], "id_pertenencia": row[2], "id_pais": row[3],
                "price_id": row[4], "cantidad_precio": row[5], "ratio_imagen": row[6], "status": row[7], "ambiente": row[8],
                "pertenencia_id": row[9], "producto_nombre": row[10], "producto_cantidad": row[11],
                "tipo_producto_nombre": row[12], "conjunto_nombre": row[13],
                "pais_nombre": row[14], "pais_moneda": row[15], "pais_simbolo": row[16],
                "pais_side": row[17], "pais_decs": row[18]
            }
            precios.append(precio)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(precios)} precios para la pertenencia",
            data=precios,
            total=total
        )
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/precios/pais/{pais_id}", response_model=ListResponse)
async def get_precios_by_pais(pais_id: str, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), ambiente: str = Query(None)):
    """Obtener todos los precios para un país específico. Filtrar por ambiente opcional (sandbox/production)"""
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        
        count_query = "SELECT COUNT(*) FROM precio WHERE id_pais = %s"
        if ambiente:
            count_query += " AND ambiente = %s"
            cursor.execute(count_query, (pais_id, ambiente))
        else:
            cursor.execute(count_query, (pais_id,))
        total = cursor.fetchone()[0]
        
        if ambiente:
            query = """
                SELECT 
                    pr.id, pr.nombre, pr.id_pertenencia, pr.id_pais, pr.price_id,
                    pr.cantidad_precio, pr.ratio_imagen, pr.status, pr.ambiente,
                    pe.id, p.nombre, p.cantidad,
                    tp.nombre,
                    c.nombre,
                    pa.nombre, pa.moneda, pa.simbolo, pa.side, pa.decs
                FROM precio pr
                LEFT JOIN pertenencia pe ON pr.id_pertenencia = pe.id
                LEFT JOIN producto p ON pe.id_producto = p.id
                LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
                LEFT JOIN conjunto c ON pe.id_conjunto = c.id
                LEFT JOIN pais pa ON pr.id_pais = pa.id
                WHERE pr.id_pais = %s AND pr.ambiente = %s
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (pais_id, ambiente, limit, skip))
        else:
            query = """
                SELECT 
                    pr.id, pr.nombre, pr.id_pertenencia, pr.id_pais, pr.price_id,
                    pr.cantidad_precio, pr.ratio_imagen, pr.status, pr.ambiente,
                    pe.id, p.nombre, p.cantidad,
                    tp.nombre,
                    c.nombre,
                    pa.nombre, pa.moneda, pa.simbolo, pa.side, pa.decs
                FROM precio pr
                LEFT JOIN pertenencia pe ON pr.id_pertenencia = pe.id
                LEFT JOIN producto p ON pe.id_producto = p.id
                LEFT JOIN tipo_producto tp ON p.id_tipo_producto = tp.id
                LEFT JOIN conjunto c ON pe.id_conjunto = c.id
                LEFT JOIN pais pa ON pr.id_pais = pa.id
                WHERE pr.id_pais = %s
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (pais_id, limit, skip))
        
        precios = []
        for row in cursor.fetchall():
            precio = {
                "id": row[0], "nombre": row[1], "id_pertenencia": row[2], "id_pais": row[3],
                "price_id": row[4], "cantidad_precio": row[5], "ratio_imagen": row[6], "status": row[7], "ambiente": row[8],
                "pertenencia_id": row[9], "producto_nombre": row[10], "producto_cantidad": row[11],
                "tipo_producto_nombre": row[12], "conjunto_nombre": row[13],
                "pais_nombre": row[14], "pais_moneda": row[15], "pais_simbolo": row[16],
                "pais_side": row[17], "pais_decs": row[18]
            }
            precios.append(precio)
        
        cursor.close()
        conn.close()
        
        return ListResponse(
            success=True,
            message=f"Se obtuvieron {len(precios)} precios para el país",
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
