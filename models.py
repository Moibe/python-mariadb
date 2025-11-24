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

# ============ MODELOS TIPO_PRODUCTO ============
class TipoProductoBase(BaseModel):
    nombre: str
    unidad_base: str

class TipoProductoCreate(TipoProductoBase):
    pass

class TipoProducto(TipoProductoBase):
    id: int
    
    class Config:
        from_attributes = True

# ============ MODELOS PAIS ============
class PaisBase(BaseModel):
    nombre: str
    moneda: str
    moneda_tic: str
    simbolo: str
    side: bool
    decs: int

class PaisCreate(PaisBase):
    pass

class Pais(PaisBase):
    id: str
    
    class Config:
        from_attributes = True

# ============ MODELOS PRODUCTO ============
class ProductoBase(BaseModel):
    nombre: str
    cantidad: int
    id_tipo_producto: int
    id_conjunto: int
    precio_base: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    
    class Config:
        from_attributes = True

class ProductoDetallado(BaseModel):
    id: int
    nombre: str
    cantidad: int
    precio_base: int
    id_tipo_producto: int
    id_conjunto: int
    tipo_producto_nombre: str
    tipo_producto_unidad_base: str
    conjunto_nombre: str
    
    class Config:
        from_attributes = True

# ============ MODELOS PERTENENCIA ============
class PertenenciaBase(BaseModel):
    id_conjunto: int
    id_producto: int

class PertenenciaCreate(PertenenciaBase):
    pass

class Pertenencia(PertenenciaBase):
    id: int
    
    class Config:
        from_attributes = True

class PertenenciaDetallada(BaseModel):
    id: int
    id_conjunto: int
    id_producto: int
    conjunto_nombre: str
    conjunto_sitio: str
    producto_nombre: str
    producto_cantidad: int
    tipo_producto_nombre: str
    
    class Config:
        from_attributes = True

# ============ MODELOS TEXTOS ============
class TextosBase(BaseModel):
    id_tipo_producto: int
    id_pais: str
    unidad: str
    unidades: str

class TextosCreate(TextosBase):
    pass

class Textos(TextosBase):
    id: int
    
    class Config:
        from_attributes = True

class TextosDetallado(BaseModel):
    id: int
    id_tipo_producto: int
    id_pais: str
    unidad: str
    unidades: str
    tipo_producto_nombre: str
    pais_nombre: str
    
    class Config:
        from_attributes = True

# ============ MODELOS PRECIO ============
class PrecioBase(BaseModel):
    nombre: str
    id_pertenencia: int
    id_pais: str
    price_id: str
    cantidad_precio: int
    ratio_imagen: int
    status: str
    ambiente: Optional[str] = None

class PrecioCreate(PrecioBase):
    pass

class Precio(PrecioBase):
    id: int
    
    class Config:
        from_attributes = True

class PrecioDetallado(BaseModel):
    id: int
    nombre: str
    id_pertenencia: int
    id_pais: str
    price_id: str
    cantidad_precio: int
    ratio_imagen: int
    status: str
    ambiente: Optional[str] = None
    pertenencia_id: int
    producto_nombre: str
    producto_cantidad: int
    tipo_producto_nombre: str
    conjunto_nombre: str
    pais_nombre: str
    pais_moneda: str
    pais_simbolo: str
    pais_side: bool
    pais_decs: int
    
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
