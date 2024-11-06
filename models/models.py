from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from config.db import Base, engine


class Gasolinera(Base):
    __tablename__ = 'gasolineras'

    id_gasolinera = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)

    # Relación con bitácora
    bitacoras = relationship('Bitacora', back_populates='gasolinera')

class Proyecto(Base):
    __tablename__ = 'proyecto'

    id_proyecto = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    activo = Column(Boolean, default=True)

    # Relación con bitácora
    bitacoras = relationship('Bitacora', back_populates='proyecto')

class Rol(Base):
    __tablename__ = 'rol'

    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String, nullable=False)

    # Relación con usuarios
    usuarios = relationship('Usuario', back_populates='rol')

class Usuario(Base):
    __tablename__ = 'usuarios'

    id_usr = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    password = Column(String, nullable=False)
    id_rol = Column(Integer, ForeignKey('rol.id_rol'))
    activo = Column(Boolean, default=True)
    username = Column(String, nullable=False)

    # Relación con rol
    rol = relationship('Rol', back_populates='usuarios')

    # Relación con bitácora y log
    bitacoras = relationship('Bitacora', back_populates='usuario')
    logs = relationship('Log', back_populates='usuario')

class Log(Base):
    __tablename__ = 'log'

    id_log = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    descripcion = Column(String, nullable=False)
    id_usr = Column(Integer, ForeignKey('usuarios.id_usr'))

    # Relación con usuario
    usuario = relationship('Usuario', back_populates='logs')

class Vehiculo(Base):
    __tablename__ = 'vehiculos'

    id_vehiculo = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    modelo = Column(String, nullable=False)
    marca = Column(String, nullable=False)
    placa = Column(String, nullable=False)
    rendimiento = Column(Float, nullable=False)
    galonaje = Column(Float, nullable=False)
    tipo_combustible = Column(String, nullable=False)

    # Relación con bitácora
    bitacoras = relationship('Bitacora', back_populates='vehiculo')

class Bitacora(Base):
    __tablename__ = 'bitacora'

    id_bitacora = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    comentario = Column(String, nullable=False)
    km_inicial = Column(Integer, nullable=False)
    km_final = Column(Integer, nullable=False)
    num_galones = Column(Float, nullable=False)
    costo = Column(Float, nullable=False)
    tipo_gasolina = Column(String, nullable=False)
    id_usr = Column(Integer, ForeignKey('usuarios.id_usr'))
    id_vehiculo = Column(Integer, ForeignKey('vehiculos.id_vehiculo'))
    id_gasolinera = Column(Integer, ForeignKey('gasolineras.id_gasolinera'))
    id_proyecto = Column(Integer, ForeignKey('proyecto.id_proyecto'))

    # Relaciones con otras tablas
    usuario = relationship('Usuario', back_populates='bitacoras')
    vehiculo = relationship('Vehiculo', back_populates='bitacoras')
    gasolinera = relationship('Gasolinera', back_populates='bitacoras')
    proyecto = relationship('Proyecto', back_populates='bitacoras')


#crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)