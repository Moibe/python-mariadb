from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ============ MODELOS CONJUNTO ============
class ConjuntoBase(BaseModel):
    sitio: str
    nombre: str

class ConjuntoCreate(ConjuntoBase):
    pass

class Conjunto(ConjuntoBase):
    id: int
    
    class Config:
        from_attributes = True

# ============ MODELOS PAIS ============
class PaisBase(BaseModel):
    nombre: str
    unidad: str
    unidades: str
    moneda: str
    moneda_tic: str
    simbolo: str

class PaisCreate(PaisBase):
    pass

class Pais(PaisBase):
    id: int
    
    class Config:
        from_attributes = True

# ============ MODELOS PRODUCTO ============
class ProductoBase(BaseModel):
    nombre: str
    cantidad: int
    unidad_general: str
    precio_base: str

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    
    class Config:
        from_attributes = True

# ============ MODELOS LINEA ============
class LineaBase(BaseModel):
    id_conjunto: int
    id_producto: int

class LineaCreate(LineaBase):
    pass

class Linea(LineaBase):
    id: int
    
    class Config:
        from_attributes = True

class LineaDetallada(BaseModel):
    id: int
    id_conjunto: int
    id_producto: int
    conjunto_nombre: str
    conjunto_sitio: str
    producto_nombre: str
    producto_cantidad: int
    
    class Config:
        from_attributes = True

# ============ MODELOS PRECIO ============
class PrecioBase(BaseModel):
    nombre: str
    id_linea: int
    id_pais: int
    price_id: str
    cantidad_precio: int
    ratio_imagen: int
    status: str

class PrecioCreate(PrecioBase):
    pass

class Precio(PrecioBase):
    id: int
    
    class Config:
        from_attributes = True

class PrecioDetallado(BaseModel):
    id: int
    nombre: str
    id_linea: int
    id_pais: int
    price_id: str
    cantidad_precio: int
    ratio_imagen: int
    status: str
    linea_id: int
    producto_nombre: str
    producto_cantidad: int
    conjunto_nombre: str
    pais_nombre: str
    pais_moneda: str
    pais_simbolo: str
    
    class Config:
        from_attributes = True

# ============ RESPUESTAS GENÉRICAS ============
class GenericResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class ListResponse(BaseModel):
    success: bool
    message: str
    data: List[dict] = []
    total: int = 0
