"""
Modelos ORM de SQLAlchemy para la aplicación de librería.
"""

from sqlalchemy import Column, Integer, String, Enum, Text, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

# ---------------------------------------------------------
# ENUMS
# ---------------------------------------------------------

class TipoPuntoVenta(enum.Enum):
    tienda = "tienda"
    metro = "metro"
    online = "online"

class RolUsuario(enum.Enum):
    admin = "admin"
    vendedor = "vendedor"

class TipoMovimiento(enum.Enum):
    entrada = "entrada"
    salida = "salida"
    venta = "venta"
    ajuste = "ajuste"


# ---------------------------------------------------------
# TABLA PUNTO DE VENTA
# ---------------------------------------------------------
class PuntoVenta(Base):
    __tablename__ = "punto_venta"

    id_punto_venta = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    ubicacion = Column(String(200))
    tipo = Column(String(50))  # o Enum(TipoPuntoVenta)


# ---------------------------------------------------------
# TABLA USUARIO
# ---------------------------------------------------------
class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    contrasena = Column(String(200), nullable=False)
    rol = Column(String(20), nullable=False)
    punto_venta_id = Column(Integer, ForeignKey("punto_venta.id_punto_venta"))

    punto_venta = relationship("PuntoVenta")


# ---------------------------------------------------------
# TABLA PAPEL
# ---------------------------------------------------------
class Papel(Base):
    __tablename__ = "papel"

    paginas = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    stock_paginas = Column(Integer, nullable=False)


# ---------------------------------------------------------
# TABLA LIBRO
# ---------------------------------------------------------
class Libro(Base):
    __tablename__ = "libro"

    id_libro = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    autor = Column(String(200), nullable=False)
    precio = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, default=0)

    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)


# ---------------------------------------------------------
# TABLA INVENTARIO GLOBAL (POR LIBRO GENERAL)
# ---------------------------------------------------------
class InventarioLibro(Base):
    __tablename__ = "inventario_libro"

    id_inventario = Column(Integer, primary_key=True, autoincrement=True)
    libro_id = Column(Integer, ForeignKey("libro.id_libro"), nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    libro = relationship("Libro")


# ---------------------------------------------------------
# TABLA INVENTARIO POR PUNTO DE VENTA
# ---------------------------------------------------------
class InventarioPV(Base):
    __tablename__ = "inventario_pv"

    id_inventario = Column(Integer, primary_key=True, autoincrement=True)
    id_libro = Column(Integer, ForeignKey("libro.id_libro"), nullable=False)
    id_punto_venta = Column(Integer, ForeignKey("punto_venta.id_punto_venta"), nullable=False)

    stock = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=5)

    libro = relationship("Libro")
    punto_venta = relationship("PuntoVenta")


# ---------------------------------------------------------
# TABLA MOVIMIENTOS DE INVENTARIO
# ---------------------------------------------------------
class MovimientoLibro(Base):
    __tablename__ = "movimiento_libro"

    id_mov_libro = Column(Integer, primary_key=True, autoincrement=True)
    inventario_id = Column(Integer, ForeignKey("inventario_libro.id_inventario"), nullable=False)
    tipo = Column(Enum(TipoMovimiento), nullable=False)
    cantidad = Column(Integer, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id_usuario"))
    observaciones = Column(Text, nullable=True)

    fecha_movimiento = Column(DateTime, server_default=func.now(), nullable=False)

    inventario = relationship("InventarioLibro")
    usuario = relationship("Usuario")
