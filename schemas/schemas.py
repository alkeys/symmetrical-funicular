from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema para Gasolinera
class GasolineraBase(BaseModel):
    nombre: str
    direccion: str

class GasolineraCreate(GasolineraBase):
    pass

class Gasolinera(GasolineraBase):
    id_gasolinera: int
    created_at: datetime

    class Config:
        orm_mode = True


# Schema para Proyecto
class ProyectoBase(BaseModel):
    nombre: str
    direccion: str
    activo: bool

class ProyectoCreate(ProyectoBase):
    pass

class Proyecto(ProyectoBase):
    id_proyecto: int
    created_at: datetime

    class Config:
        orm_mode = True


# Schema para Rol
class RolBase(BaseModel):
    descripcion: str

class RolCreate(RolBase):
    pass

class Rol(RolBase):
    id_rol: int

    class Config:
        orm_mode = True


# Schema para Usuario
class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    password: str
    username: str
    activo: bool
    id_rol: Optional[int] = 1

class UsuarioLogin(BaseModel):
    username: str
    password: str

class Usuarioname(BaseModel):
    username: str

class UsuarioUsername(UsuarioBase):
    username: str


class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id_usr: int
    created_at: datetime
    id_rol: int

    class Config:
        orm_mode = True


# Schema para Log
class LogBase(BaseModel):
    descripcion: str

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id_log: int
    created_at: datetime
    id_usr: int

    class Config:
        orm_mode = True


# Schema para Vehiculo
class VehiculoBase(BaseModel):
    modelo: str
    marca: str
    placa: str
    rendimiento: float
    galonaje: float
    tipo_combustible: str

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    id_vehiculo: int
    created_at: datetime

    class Config:
        orm_mode = True


# Schema para Bitacora
class BitacoraBase(BaseModel):
    comentario: str
    km_inicial: int
    km_final: int
    num_galones: float
    costo: float
    tipo_gasolina: str
    id_usr: int
    id_vehiculo: int
    id_gasolinera: int
    id_proyecto: int

class BitacoraCreate(BitacoraBase):
    pass

class Bitacora(BitacoraBase):
    id_bitacora: int
    created_at: datetime

    class Config:
        orm_mode = True
