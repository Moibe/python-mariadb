from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ============ MODELOS PAIS ============
class PaisBase(BaseModel):
    nombre: str
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
    precio_mxn: str

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    
    class Config:
        from_attributes = True

# ============ MODELOS PRECIO ============
class PrecioBase(BaseModel):
    nombre: str
    id_producto: int
    id_pais: int
    status: str
    price_id: str

class PrecioCreate(PrecioBase):
    pass

class Precio(PrecioBase):
    id: int
    
    class Config:
        from_attributes = True

class PrecioDetallado(BaseModel):
    id: int
    nombre: str
    id_producto: int
    id_pais: int
    status: str
    price_id: str
    producto_nombre: str
    pais_nombre: str
    pais_moneda: str
    
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
