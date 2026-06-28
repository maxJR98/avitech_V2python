from typing import Optional
import datetime
import decimal
import enum

from sqlalchemy import CheckConstraint, DECIMAL, Date, DateTime, Enum, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Text, Time, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Importamos la instancia de tu proyecto
from app.extensions import db

Base = db.Model

class ConfiguracionSistemaTipoDato(str, enum.Enum):
    STRING = 'string'
    Integer = 'Integer'
    BOOLEAN = 'boolean'
    JSON = 'json'


class EnfermedadesContagiosidad(str, enum.Enum):
    NO_CONTAGIOSO = 'no_contagioso'
    BAJA = 'baja'
    MEDIA = 'media'
    ALTA = 'alta'


class EnfermedadesTipoEnfermedad(str, enum.Enum):
    VIRAL = 'viral'
    BACTERIANA = 'bacteriana'
    PARASITARIA = 'parasitaria'
    FUNGICA = 'fungica'
    NUTRICIONAL = 'nutricional'
    AMBIENTAL = 'ambiental'


class HorariosSucursalDiaSemana(str, enum.Enum):
    LUNES = 'lunes'
    MARTES = 'martes'
    MIERCOLES = 'miercoles'
    JUEVES = 'jueves'
    VIERNES = 'viernes'
    SABADO = 'sabado'
    DOMINGO = 'domingo'


class MovimientosInventarioTipoMovimiento(str, enum.Enum):
    ENTRADA = 'entrada'
    SALIDA = 'salida'
    AJUSTE = 'ajuste'
    TRANSFERENCIA = 'transferencia'
    DEVOLUCION = 'devolucion'


class NotificacionesTipoNotificacion(str, enum.Enum):
    PEDIDO = 'pedido'
    SISTEMA = 'sistema'
    PROMOCION = 'promocion'
    ALERTA = 'alerta'


class PedidosMetodoPago(str, enum.Enum):
    EFECTIVO = 'efectivo'
    TARJETA = 'tarjeta'
    TRANSFERENCIA = 'transferencia'
    YAPE = 'yape'
    PLIN = 'plin'


class ProductosUnidadMedida(str, enum.Enum):
    UNIDAD = 'unidad'
    KG = 'kg'
    LB = 'lb'
    DOCENA = 'docena'
    CAJA = 'caja'
    SACO = 'saco'


class RemediosEfectividadEstimada(str, enum.Enum):
    BAJA = 'baja'
    MEDIA = 'media'
    ALTA = 'alta'


class RemediosTipoRemedio(str, enum.Enum):
    CASERO = 'casero'
    HERBAL = 'herbal'
    PREVENTIVO = 'preventivo'
    PALIATIVO = 'paliativo'


class SintomasEnfermedadesFrecuencia(str, enum.Enum):
    RARO = 'raro'
    OCASIONAL = 'ocasional'
    FRECUENTE = 'frecuente'
    MUY_FRECUENTE = 'muy_frecuente'


class SintomasEnfermedadesIntensidad(str, enum.Enum):
    LEVE = 'leve'
    MODERADO = 'moderado'
    SEVERO = 'severo'


class SintomasGravedad(str, enum.Enum):
    LEVE = 'leve'
    MODERADO = 'moderado'
    GRAVE = 'grave'
    CRITICO = 'critico'


class TiposAveProposito(str, enum.Enum):
    CARNE = 'carne'
    HUEVOS = 'huevos'
    DUAL = 'dual'
    ORNAMENTAL = 'ornamental'


class TratamientosTipoTratamiento(str, enum.Enum):
    MEDICAMENTO = 'medicamento'
    VACUNA = 'vacuna'
    MANEJO = 'manejo'
    NUTRICIONAL = 'nutricional'
    QUIRURGICO = 'quirurgico'


class CategoriasAveologia(Base):
    __tablename__ = 'categorias_aveologia'
    __table_args__ = (
        Index('idx_orden', 'orden'),
    )

    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_categoria: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    icono: Mapped[Optional[str]] = mapped_column(String(50))
    orden: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    articulos_aveologia: Mapped[list['ArticulosAveologia']] = relationship('ArticulosAveologia', back_populates='categorias_aveologia')


class CategoriasProducto(Base):
    __tablename__ = 'categorias_producto'
    __table_args__ = (
        ForeignKeyConstraint(['parent_id'], ['categorias_producto.id_categoria_producto'], ondelete='SET NULL', name='categorias_producto_ibfk_1'),
        Index('idx_parent', 'parent_id'),
        Index('idx_slug', 'slug'),
        Index('nombre_categoria', 'nombre_categoria', unique=True),
        Index('slug', 'slug', unique=True)
    )

    id_categoria_producto: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_categoria: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    icono: Mapped[Optional[str]] = mapped_column(String(50))
    imagen: Mapped[Optional[str]] = mapped_column(String(255))
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, comment='Para subcategorías')
    orden: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    parent: Mapped[Optional['CategoriasProducto']] = relationship('CategoriasProducto', remote_side=[id_categoria_producto], back_populates='parent_reverse')
    parent_reverse: Mapped[list['CategoriasProducto']] = relationship('CategoriasProducto', remote_side=[parent_id], back_populates='parent')
    productos: Mapped[list['Productos']] = relationship('Productos', back_populates='categorias_producto')


class ConfiguracionSistema(Base):
    __tablename__ = 'configuracion_sistema'
    __table_args__ = (
        Index('clave', 'clave', unique=True),
        Index('idx_clave', 'clave'),
        Index('idx_grupo', 'grupo')
    )

    id_config: Mapped[int] = mapped_column(Integer, primary_key=True)
    clave: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    valor: Mapped[Optional[str]] = mapped_column(Text)
    tipo_dato: Mapped[Optional[ConfiguracionSistemaTipoDato]] = mapped_column(Enum(ConfiguracionSistemaTipoDato, values_callable=lambda cls: [member.value for member in cls]), server_default=text("'string'"))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    grupo: Mapped[Optional[str]] = mapped_column(String(50))


class Enfermedades(Base):
    __tablename__ = 'enfermedades'
    __table_args__ = (
        Index('ft_enfermedades', 'nombre_enfermedad', 'nombre_cientifico', 'descripcion'),
        Index('idx_tipo', 'tipo_enfermedad')
    )

    id_enfermedad: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_enfermedad: Mapped[str] = mapped_column(String(200), nullable=False)
    tipo_enfermedad: Mapped[EnfermedadesTipoEnfermedad] = mapped_column(Enum(EnfermedadesTipoEnfermedad, values_callable=lambda cls: [member.value for member in cls]), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    nombre_cientifico: Mapped[Optional[str]] = mapped_column(String(200))
    causas: Mapped[Optional[str]] = mapped_column(Text)
    prevencion: Mapped[Optional[str]] = mapped_column(Text)
    contagiosidad: Mapped[Optional[EnfermedadesContagiosidad]] = mapped_column(Enum(EnfermedadesContagiosidad, values_callable=lambda cls: [member.value for member in cls]), server_default=text("'media'"))
    mortalidad_estimada: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(5, 2), comment='Porcentaje de mortalidad')
    edad_susceptible: Mapped[Optional[str]] = mapped_column(String(100))
    imagen: Mapped[Optional[str]] = mapped_column(String(255))
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    remedios: Mapped[list['Remedios']] = relationship('Remedios', back_populates='enfermedades')
    sintomas_enfermedades: Mapped[list['SintomasEnfermedades']] = relationship('SintomasEnfermedades', back_populates='enfermedades')
    tratamientos: Mapped[list['Tratamientos']] = relationship('Tratamientos', back_populates='enfermedades')


class EstadosPedido(Base):
    __tablename__ = 'estados_pedido'
    __table_args__ = (
        Index('idx_orden', 'orden'),
        Index('nombre_estado', 'nombre_estado', unique=True)
    )

    id_estado: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_estado: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    color_hex: Mapped[Optional[str]] = mapped_column(String(7), server_default=text("'#6c757d'"))
    orden: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    es_final: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'), comment='Estado terminal (entregado, cancelado)')
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    pedidos: Mapped[list['Pedidos']] = relationship('Pedidos', back_populates='estados_pedido')
    historial_pedido: Mapped[list['HistorialPedido']] = relationship('HistorialPedido', back_populates='estados_pedido')


class EtapasVida(Base):
    __tablename__ = 'etapas_vida'
    __table_args__ = (
        CheckConstraint('edad_fin_dias > edad_inicio_dias', name='CONSTRAINT_1'),
        Index('idx_orden', 'orden')
    )

    id_etapa: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_etapa: Mapped[str] = mapped_column(String(100), nullable=False)
    edad_inicio_dias: Mapped[int] = mapped_column(Integer, nullable=False)
    edad_fin_dias: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    orden: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))

    parametros_nutricionales: Mapped[list['ParametrosNutricionales']] = relationship('ParametrosNutricionales', back_populates='etapas_vida')
    historial_calculos: Mapped[list['HistorialCalculos']] = relationship('HistorialCalculos', back_populates='etapas_vida')


class MetodosEntrega(Base):
    __tablename__ = 'metodos_entrega'
    __table_args__ = (
        Index('nombre_metodo', 'nombre_metodo', unique=True),
    )

    id_metodo_entrega: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_metodo: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    costo_base: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2), server_default=text('0.00'))
    costo_por_km: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2), server_default=text('0.00'))
    tiempo_estimado_horas: Mapped[Optional[int]] = mapped_column(Integer)
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    pedidos: Mapped[list['Pedidos']] = relationship('Pedidos', back_populates='metodos_entrega')


class Permisos(Base):
    __tablename__ = 'permisos'
    __table_args__ = (
        Index('idx_modulo', 'modulo'),
        Index('nombre_permiso', 'nombre_permiso', unique=True)
    )

    id_permiso: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_permiso: Mapped[str] = mapped_column(String(100), nullable=False)
    modulo: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    roles_permisos: Mapped[list['RolesPermisos']] = relationship('RolesPermisos', back_populates='permisos')


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        Index('nombre_rol', 'nombre_rol', unique=True),
        Index('uk_nombre_rol', 'nombre_rol', unique=True)
    )

    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_rol: Mapped[str] = mapped_column(String(50), nullable=False)
    nivel_acceso: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('1'))
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    roles_permisos: Mapped[list['RolesPermisos']] = relationship('RolesPermisos', back_populates='roles')
    usuarios: Mapped[list['Usuarios']] = relationship('Usuarios', back_populates='roles')


class Sintomas(Base):
    __tablename__ = 'sintomas'
    __table_args__ = (
        Index('ft_sintomas', 'nombre_sintoma', 'descripcion', 'keywords'),
        Index('idx_gravedad', 'gravedad')
    )

    id_sintoma: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_sintoma: Mapped[str] = mapped_column(String(150), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    gravedad: Mapped[Optional[SintomasGravedad]] = mapped_column(Enum(SintomasGravedad, values_callable=lambda cls: [member.value for member in cls]), server_default=text("'moderado'"))
    categoria: Mapped[Optional[str]] = mapped_column(String(100))
    keywords: Mapped[Optional[str]] = mapped_column(Text, comment='Palabras clave para búsqueda semántica')
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    sintomas_enfermedades: Mapped[list['SintomasEnfermedades']] = relationship('SintomasEnfermedades', back_populates='sintomas')


class TiposAve(Base):
    __tablename__ = 'tipos_ave'
    __table_args__ = (
        Index('nombre_tipo', 'nombre_tipo', unique=True),
    )

    id_tipo_ave: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    proposito: Mapped[TiposAveProposito] = mapped_column(Enum(TiposAveProposito, values_callable=lambda cls: [member.value for member in cls]), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    imagen: Mapped[Optional[str]] = mapped_column(String(255))
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    parametros_nutricionales: Mapped[list['ParametrosNutricionales']] = relationship('ParametrosNutricionales', back_populates='tipos_ave')
    historial_calculos: Mapped[list['HistorialCalculos']] = relationship('HistorialCalculos', back_populates='tipos_ave')


class ParametrosNutricionales(Base):
    __tablename__ = 'parametros_nutricionales'
    __table_args__ = (
        ForeignKeyConstraint(['id_etapa'], ['etapas_vida.id_etapa'], ondelete='CASCADE', name='parametros_nutricionales_ibfk_2'),
        ForeignKeyConstraint(['id_tipo_ave'], ['tipos_ave.id_tipo_ave'], ondelete='CASCADE', name='parametros_nutricionales_ibfk_1'),
        Index('id_etapa', 'id_etapa'),
        Index('uk_tipo_etapa', 'id_tipo_ave', 'id_etapa', unique=True)
    )

    id_parametro: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_tipo_ave: Mapped[int] = mapped_column(Integer, nullable=False)
    id_etapa: Mapped[int] = mapped_column(Integer, nullable=False)
    consumo_alimento_gr_dia: Mapped[decimal.Decimal] = mapped_column(DECIMAL(8, 2), nullable=False, comment='Gramos por ave por día')
    consumo_agua_ml_dia: Mapped[decimal.Decimal] = mapped_column(DECIMAL(8, 2), nullable=False, comment='Mililitros por ave por día')
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    proteina_porcentaje: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(5, 2))
    energia_kcal: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(8, 2))
    notas: Mapped[Optional[str]] = mapped_column(Text)

    etapas_vida: Mapped['EtapasVida'] = relationship('EtapasVida', back_populates='parametros_nutricionales')
    tipos_ave: Mapped['TiposAve'] = relationship('TiposAve', back_populates='parametros_nutricionales')


class Productos(Base):
    __tablename__ = 'productos'
    __table_args__ = (
        ForeignKeyConstraint(['id_categoria_producto'], ['categorias_producto.id_categoria_producto'], name='productos_ibfk_1'),
        Index('codigo_producto', 'codigo_producto', unique=True),
        Index('ft_productos', 'nombre_producto', 'descripcion_corta'),
        Index('idx_activo', 'activo'),
        Index('idx_categoria', 'id_categoria_producto'),
        Index('idx_destacado', 'destacado'),
        Index('idx_slug', 'slug'),
        Index('slug', 'slug', unique=True)
    )

    id_producto: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_categoria_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre_producto: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    precio_unitario: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    codigo_producto: Mapped[Optional[str]] = mapped_column(String(50))
    descripcion_corta: Mapped[Optional[str]] = mapped_column(Text)
    descripcion_larga: Mapped[Optional[str]] = mapped_column(Text)
    precio_oferta: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    unidad_medida: Mapped[Optional[ProductosUnidadMedida]] = mapped_column(Enum(ProductosUnidadMedida, values_callable=lambda cls: [member.value for member in cls]), server_default=text("'unidad'"))
    peso_gramos: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(8, 2))
    stock_total: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'), comment='Stock total en granja central')
    stock_minimo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('5'))
    requiere_refrigeracion: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    dias_frescura: Mapped[Optional[int]] = mapped_column(Integer, comment='Días de vida útil del producto')
    destacado: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    categorias_producto: Mapped['CategoriasProducto'] = relationship('CategoriasProducto', back_populates='productos')
    atributos_producto: Mapped[list['AtributosProducto']] = relationship('AtributosProducto', back_populates='productos')
    carrito: Mapped[list['Carrito']] = relationship('Carrito', back_populates='productos')
    imagenes_producto: Mapped[list['ImagenesProducto']] = relationship('ImagenesProducto', back_populates='productos')
    inventario_sucursal: Mapped[list['InventarioSucursal']] = relationship('InventarioSucursal', back_populates='productos')
    calificaciones: Mapped[list['Calificaciones']] = relationship('Calificaciones', back_populates='productos')
    detalle_pedido: Mapped[list['DetallePedido']] = relationship('DetallePedido', back_populates='productos')


class Remedios(Base):
    __tablename__ = 'remedios'
    __table_args__ = (
        ForeignKeyConstraint(['id_enfermedad'], ['enfermedades.id_enfermedad'], ondelete='CASCADE', name='remedios_ibfk_1'),
        Index('idx_enfermedad', 'id_enfermedad'),
        Index('idx_tipo', 'tipo_remedio')
    )

    id_remedio: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_remedio: Mapped[str] = mapped_column(String(200), nullable=False)
    tipo_remedio: Mapped[RemediosTipoRemedio] = mapped_column(Enum(RemediosTipoRemedio, values_callable=lambda cls: [member.value for member in cls]), nullable=False)
    ingredientes: Mapped[str] = mapped_column(Text, nullable=False)
    preparacion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id_enfermedad: Mapped[Optional[int]] = mapped_column(Integer)
    modo_uso: Mapped[Optional[str]] = mapped_column(Text)
    efectividad_estimada: Mapped[Optional[RemediosEfectividadEstimada]] = mapped_column(Enum(RemediosEfectividadEstimada, values_callable=lambda cls: [member.value for member in cls]), server_default=text("'media'"))
    contraindicaciones: Mapped[Optional[str]] = mapped_column(Text)
    nota_importante: Mapped[Optional[str]] = mapped_column(Text, comment='Advertencias de seguridad')
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    enfermedades: Mapped[Optional['Enfermedades']] = relationship('Enfermedades', back_populates='remedios')


class RolesPermisos(Base):
    __tablename__ = 'roles_permisos'
    __table_args__ = (
        ForeignKeyConstraint(['id_permiso'], ['permisos.id_permiso'], ondelete='CASCADE', name='roles_permisos_ibfk_2'),
        ForeignKeyConstraint(['id_rol'], ['roles.id_rol'], ondelete='CASCADE', name='roles_permisos_ibfk_1'),
        Index('id_permiso', 'id_permiso')
    )

    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_permiso: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_asignacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    permisos: Mapped['Permisos'] = relationship('Permisos', back_populates='roles_permisos')
    roles: Mapped['Roles'] = relationship('Roles', back_populates='roles_permisos')


class SintomasEnfermedades(Base):
    __tablename__ = 'sintomas_enfermedades'
    __table_args__ = (
        ForeignKeyConstraint(['id_enfermedad'], ['enfermedades.id_enfermedad'], ondelete='CASCADE', name='sintomas_enfermedades_ibfk_1'),
        ForeignKeyConstraint(['id_sintoma'], ['sintomas.id_sintoma'], ondelete='CASCADE', name='sintomas_enfermedades_ibfk_2'),
        Index('id_sintoma', 'id_sintoma')
    )

    id_enfermedad: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_sintoma: Mapped[int] = mapped_column(Integer, primary_key=True)
    frecuencia: Mapped[Optional[SintomasEnfermedadesFrecuencia]] = mapped_column(Enum(SintomasEnfermedadesFrecuencia, values_callable=lambda cls: [member.value for member in cls]), server_default=text("'frecuente'"))
    intensidad: Mapped[Optional[SintomasEnfermedadesIntensidad]] = mapped_column(Enum(SintomasEnfermedadesIntensidad, values_callable=lambda cls: [member.value for member in cls]), server_default=text("'moderado'"))

    enfermedades: Mapped['Enfermedades'] = relationship('Enfermedades', back_populates='sintomas_enfermedades')
    sintomas: Mapped['Sintomas'] = relationship('Sintomas', back_populates='sintomas_enfermedades')


class Tratamientos(Base):
    __tablename__ = 'tratamientos'
    __table_args__ = (
        ForeignKeyConstraint(['id_enfermedad'], ['enfermedades.id_enfermedad'], ondelete='CASCADE', name='tratamientos_ibfk_1'),
        Index('idx_enfermedad', 'id_enfermedad'),
        Index('idx_tipo', 'tipo_tratamiento')
    )

    id_tratamiento: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_enfermedad: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre_tratamiento: Mapped[str] = mapped_column(String(200), nullable=False)
    tipo_tratamiento: Mapped[TratamientosTipoTratamiento] = mapped_column(Enum(TratamientosTipoTratamiento, values_callable=lambda cls: [member.value for member in cls]), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    dosificacion: Mapped[Optional[str]] = mapped_column(Text)
    duracion: Mapped[Optional[str]] = mapped_column(String(100))
    efectividad: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(5, 2), comment='Porcentaje de efectividad')
    costo_aproximado: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    advertencias: Mapped[Optional[str]] = mapped_column(Text)
    requiere_veterinario: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    orden_recomendacion: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    enfermedades: Mapped['Enfermedades'] = relationship('Enfermedades', back_populates='tratamientos')


class Usuarios(Base):
    __tablename__ = 'usuarios'
    __table_args__ = (
        ForeignKeyConstraint(['id_rol'], ['roles.id_rol'], name='usuarios_ibfk_1'),
        Index('email', 'email', unique=True),
        Index('idx_activo', 'activo'),
        Index('idx_email', 'email'),
        Index('idx_rol', 'id_rol')
    )

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_rol: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre_completo: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    fecha_registro: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    avatar: Mapped[Optional[str]] = mapped_column(String(255), server_default=text("'default-avatar.png'"))
    direccion: Mapped[Optional[str]] = mapped_column(Text)
    ciudad: Mapped[Optional[str]] = mapped_column(String(100))
    departamento: Mapped[Optional[str]] = mapped_column(String(100))
    codigo_postal: Mapped[Optional[str]] = mapped_column(String(10))
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))
    verificado: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    token_verificacion: Mapped[Optional[str]] = mapped_column(String(100))
    token_recuperacion: Mapped[Optional[str]] = mapped_column(String(100))
    fecha_token_expira: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ultimo_acceso: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP)

    roles: Mapped['Roles'] = relationship('Roles', back_populates='usuarios')
    articulos_aveologia: Mapped[list['ArticulosAveologia']] = relationship('ArticulosAveologia', back_populates='autor')
    carrito: Mapped[list['Carrito']] = relationship('Carrito', back_populates='usuarios')
    historial_calculos: Mapped[list['HistorialCalculos']] = relationship('HistorialCalculos', back_populates='usuarios')
    notificaciones: Mapped[list['Notificaciones']] = relationship('Notificaciones', back_populates='usuarios')
    sesiones_usuario: Mapped[list['SesionesUsuario']] = relationship('SesionesUsuario', back_populates='usuarios')
    sucursales: Mapped[list['Sucursales']] = relationship('Sucursales', back_populates='usuarios')
    pedidos: Mapped[list['Pedidos']] = relationship('Pedidos', back_populates='usuarios')
    calificaciones: Mapped[list['Calificaciones']] = relationship('Calificaciones', back_populates='usuarios')
    historial_pedido: Mapped[list['HistorialPedido']] = relationship('HistorialPedido', back_populates='usuarios')
    movimientos_inventario: Mapped[list['MovimientosInventario']] = relationship('MovimientosInventario', back_populates='usuarios')

    def get_id(self):
        return str(self.id_usuario)
    
    @property
    def is_active(self):
        return self.activo == 1
    
    @property
    def is_authenticated(self):
        return True
        
    @property
    def is_anonymous(self):
        return False

class ArticulosAveologia(Base):
    __tablename__ = 'articulos_aveologia'
    __table_args__ = (
        ForeignKeyConstraint(['autor_id'], ['usuarios.id_usuario'], ondelete='SET NULL', name='articulos_aveologia_ibfk_2'),
        ForeignKeyConstraint(['id_categoria'], ['categorias_aveologia.id_categoria'], name='articulos_aveologia_ibfk_1'),
        Index('autor_id', 'autor_id'),
        Index('ft_busqueda', 'titulo', 'contenido', 'tags'),
        Index('idx_categoria', 'id_categoria'),
        Index('idx_destacado', 'destacado'),
        Index('idx_slug', 'slug'),
        Index('slug', 'slug', unique=True)
    )

    id_articulo: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_categoria: Mapped[int] = mapped_column(Integer, nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_publicacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    resumen: Mapped[Optional[str]] = mapped_column(Text)
    imagen_principal: Mapped[Optional[str]] = mapped_column(String(255))
    autor_id: Mapped[Optional[int]] = mapped_column(Integer)
    visitas: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    destacado: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    tags: Mapped[Optional[str]] = mapped_column(String(255))
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    autor: Mapped[Optional['Usuarios']] = relationship('Usuarios', back_populates='articulos_aveologia')
    categorias_aveologia: Mapped['CategoriasAveologia'] = relationship('CategoriasAveologia', back_populates='articulos_aveologia')


class AtributosProducto(Base):
    __tablename__ = 'atributos_producto'
    __table_args__ = (
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], ondelete='CASCADE', name='atributos_producto_ibfk_1'),
        Index('idx_nombre', 'nombre_atributo'),
        Index('idx_producto', 'id_producto')
    )

    id_atributo: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre_atributo: Mapped[str] = mapped_column(String(100), nullable=False, comment='Ej: raza, calibre, edad')
    valor_atributo: Mapped[str] = mapped_column(String(255), nullable=False, comment='Ej: Rhode Island, Jumbo, 1 día')
    grupo_atributo: Mapped[Optional[str]] = mapped_column(String(50), comment='Para agrupar atributos similares')

    productos: Mapped['Productos'] = relationship('Productos', back_populates='atributos_producto')


class Carrito(Base):
    __tablename__ = 'carrito'
    __table_args__ = (
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], ondelete='CASCADE', name='carrito_ibfk_2'),
        ForeignKeyConstraint(['id_usuario'], ['usuarios.id_usuario'], ondelete='CASCADE', name='carrito_ibfk_1'),
        Index('id_producto', 'id_producto'),
        Index('idx_session', 'session_id'),
        Index('idx_usuario', 'id_usuario')
    )

    id_carrito: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('1'))
    fecha_agregado: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id_usuario: Mapped[Optional[int]] = mapped_column(Integer)
    session_id: Mapped[Optional[str]] = mapped_column(String(100), comment='Para usuarios no logueados')

    productos: Mapped['Productos'] = relationship('Productos', back_populates='carrito')
    usuarios: Mapped[Optional['Usuarios']] = relationship('Usuarios', back_populates='carrito')


class HistorialCalculos(Base):
    __tablename__ = 'historial_calculos'
    __table_args__ = (
        ForeignKeyConstraint(['id_etapa'], ['etapas_vida.id_etapa'], name='historial_calculos_ibfk_3'),
        ForeignKeyConstraint(['id_tipo_ave'], ['tipos_ave.id_tipo_ave'], name='historial_calculos_ibfk_2'),
        ForeignKeyConstraint(['id_usuario'], ['usuarios.id_usuario'], ondelete='SET NULL', name='historial_calculos_ibfk_1'),
        Index('id_etapa', 'id_etapa'),
        Index('id_tipo_ave', 'id_tipo_ave'),
        Index('idx_fecha', 'fecha_calculo'),
        Index('idx_usuario', 'id_usuario')
    )

    id_calculo: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_tipo_ave: Mapped[int] = mapped_column(Integer, nullable=False)
    id_etapa: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad_aves: Mapped[int] = mapped_column(Integer, nullable=False)
    edad_dias: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_calculo: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id_usuario: Mapped[Optional[int]] = mapped_column(Integer)
    resultado_alimento_kg: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    resultado_agua_litros: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))

    etapas_vida: Mapped['EtapasVida'] = relationship('EtapasVida', back_populates='historial_calculos')
    tipos_ave: Mapped['TiposAve'] = relationship('TiposAve', back_populates='historial_calculos')
    usuarios: Mapped[Optional['Usuarios']] = relationship('Usuarios', back_populates='historial_calculos')


class ImagenesProducto(Base):
    __tablename__ = 'imagenes_producto'
    __table_args__ = (
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], ondelete='CASCADE', name='imagenes_producto_ibfk_1'),
        Index('idx_principal', 'es_principal'),
        Index('idx_producto', 'id_producto')
    )

    id_imagen: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    url_imagen: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_subida: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    alt_text: Mapped[Optional[str]] = mapped_column(String(255))
    es_principal: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    orden: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))

    productos: Mapped['Productos'] = relationship('Productos', back_populates='imagenes_producto')


class Notificaciones(Base):
    __tablename__ = 'notificaciones'
    __table_args__ = (
        ForeignKeyConstraint(['id_usuario'], ['usuarios.id_usuario'], ondelete='CASCADE', name='notificaciones_ibfk_1'),
        Index('idx_fecha', 'fecha_creacion'),
        Index('idx_leida', 'leida'),
        Index('idx_usuario', 'id_usuario')
    )

    id_notificacion: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    mensaje: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    tipo_notificacion: Mapped[Optional[NotificacionesTipoNotificacion]] = mapped_column(Enum(NotificacionesTipoNotificacion, values_callable=lambda cls: [member.value for member in cls]), server_default=text("'sistema'"))
    enlace: Mapped[Optional[str]] = mapped_column(String(255))
    leida: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))

    usuarios: Mapped['Usuarios'] = relationship('Usuarios', back_populates='notificaciones')


class SesionesUsuario(Base):
    __tablename__ = 'sesiones_usuario'
    __table_args__ = (
        ForeignKeyConstraint(['id_usuario'], ['usuarios.id_usuario'], ondelete='CASCADE', name='sesiones_usuario_ibfk_1'),
        Index('idx_token', 'token_sesion'),
        Index('idx_usuario', 'id_usuario'),
        Index('token_sesion', 'token_sesion', unique=True)
    )

    id_sesion: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    token_sesion: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_inicio: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    fecha_expiracion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    activa: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))

    usuarios: Mapped['Usuarios'] = relationship('Usuarios', back_populates='sesiones_usuario')


class Sucursales(Base):
    __tablename__ = 'sucursales'
    __table_args__ = (
        ForeignKeyConstraint(['id_encargado'], ['usuarios.id_usuario'], ondelete='SET NULL', name='sucursales_ibfk_1'),
        Index('codigo_sucursal', 'codigo_sucursal', unique=True),
        Index('id_encargado', 'id_encargado'),
        Index('idx_activo', 'activo'),
        Index('idx_ciudad', 'ciudad'),
        Index('idx_coords', 'latitud', 'longitud')
    )

    id_sucursal: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo_sucursal: Mapped[str] = mapped_column(String(20), nullable=False)
    nombre_sucursal: Mapped[str] = mapped_column(String(200), nullable=False)
    direccion_completa: Mapped[str] = mapped_column(Text, nullable=False)
    ciudad: Mapped[str] = mapped_column(String(100), nullable=False)
    departamento: Mapped[str] = mapped_column(String(100), nullable=False)
    latitud: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 8), nullable=False, comment='Para geolocalización')
    longitud: Mapped[decimal.Decimal] = mapped_column(DECIMAL(11, 8), nullable=False, comment='Para geolocalización')
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id_encargado: Mapped[Optional[int]] = mapped_column(Integer, comment='Usuario responsable de la sucursal')
    codigo_postal: Mapped[Optional[str]] = mapped_column(String(10))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(150))
    capacidad_almacenamiento: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2), comment='En metros cúbicos o kg')
    horario_apertura: Mapped[Optional[datetime.time]] = mapped_column(Time)
    horario_cierre: Mapped[Optional[datetime.time]] = mapped_column(Time)
    dias_atencion: Mapped[Optional[str]] = mapped_column(String(100), server_default=text("'Lunes a Sábado'"))
    permite_delivery: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))
    permite_pickup: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))
    radio_cobertura_km: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(5, 2), server_default=text('10.00'), comment='Radio de delivery')
    imagen_fachada: Mapped[Optional[str]] = mapped_column(String(255))
    activo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('1'))
    fecha_apertura: Mapped[Optional[datetime.date]] = mapped_column(Date)

    usuarios: Mapped[Optional['Usuarios']] = relationship('Usuarios', back_populates='sucursales')
    horarios_sucursal: Mapped[list['HorariosSucursal']] = relationship('HorariosSucursal', back_populates='sucursales')
    inventario_sucursal: Mapped[list['InventarioSucursal']] = relationship('InventarioSucursal', back_populates='sucursales')
    pedidos: Mapped[list['Pedidos']] = relationship('Pedidos', back_populates='sucursales')


class HorariosSucursal(Base):
    __tablename__ = 'horarios_sucursal'
    __table_args__ = (
        ForeignKeyConstraint(['id_sucursal'], ['sucursales.id_sucursal'], ondelete='CASCADE', name='horarios_sucursal_ibfk_1'),
        Index('uk_sucursal_dia', 'id_sucursal', 'dia_semana', unique=True)
    )

    id_horario: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_sucursal: Mapped[int] = mapped_column(Integer, nullable=False)
    dia_semana: Mapped[HorariosSucursalDiaSemana] = mapped_column(Enum(HorariosSucursalDiaSemana, values_callable=lambda cls: [member.value for member in cls]), nullable=False)
    hora_apertura: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    hora_cierre: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    cerrado: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))

    sucursales: Mapped['Sucursales'] = relationship('Sucursales', back_populates='horarios_sucursal')


class InventarioSucursal(Base):
    __tablename__ = 'inventario_sucursal'
    __table_args__ = (
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], ondelete='CASCADE', name='inventario_sucursal_ibfk_2'),
        ForeignKeyConstraint(['id_sucursal'], ['sucursales.id_sucursal'], ondelete='CASCADE', name='inventario_sucursal_ibfk_1'),
        Index('idx_producto', 'id_producto'),
        Index('idx_sucursal', 'id_sucursal'),
        Index('uk_sucursal_producto', 'id_sucursal', 'id_producto', unique=True)
    )

    id_inventario: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_sucursal: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad_disponible: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    cantidad_reservada: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'), comment='Productos en pedidos pendientes')
    stock_minimo: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('5'))
    stock_maximo: Mapped[Optional[int]] = mapped_column(Integer)
    ultima_reposicion: Mapped[Optional[datetime.date]] = mapped_column(Date)

    productos: Mapped['Productos'] = relationship('Productos', back_populates='inventario_sucursal')
    sucursales: Mapped['Sucursales'] = relationship('Sucursales', back_populates='inventario_sucursal')
    movimientos_inventario: Mapped[list['MovimientosInventario']] = relationship('MovimientosInventario', back_populates='inventario_sucursal')


class Pedidos(Base):
    __tablename__ = 'pedidos'
    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['usuarios.id_usuario'], name='pedidos_ibfk_1'),
        ForeignKeyConstraint(['id_estado'], ['estados_pedido.id_estado'], name='pedidos_ibfk_3'),
        ForeignKeyConstraint(['id_metodo_entrega'], ['metodos_entrega.id_metodo_entrega'], name='pedidos_ibfk_4'),
        ForeignKeyConstraint(['id_sucursal'], ['sucursales.id_sucursal'], name='pedidos_ibfk_2'),
        Index('id_metodo_entrega', 'id_metodo_entrega'),
        Index('idx_cliente', 'id_cliente'),
        Index('idx_estado', 'id_estado'),
        Index('idx_fecha', 'fecha_pedido'),
        Index('idx_numero', 'numero_pedido'),
        Index('idx_sucursal', 'id_sucursal'),
        Index('numero_pedido', 'numero_pedido', unique=True)
    )

    id_pedido: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero_pedido: Mapped[str] = mapped_column(String(20), nullable=False)
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_sucursal: Mapped[int] = mapped_column(Integer, nullable=False, comment='Sucursal asignada para el pedido')
    id_estado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_metodo_entrega: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    total: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    fecha_pedido: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    direccion_entrega: Mapped[Optional[str]] = mapped_column(Text)
    ciudad_entrega: Mapped[Optional[str]] = mapped_column(String(100))
    departamento_entrega: Mapped[Optional[str]] = mapped_column(String(100))
    codigo_postal_entrega: Mapped[Optional[str]] = mapped_column(String(10))
    latitud_entrega: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 8))
    longitud_entrega: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(11, 8))
    distancia_km: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(6, 2), comment='Distancia desde sucursal a cliente')
    nombre_receptor: Mapped[Optional[str]] = mapped_column(String(150))
    telefono_receptor: Mapped[Optional[str]] = mapped_column(String(20))
    email_receptor: Mapped[Optional[str]] = mapped_column(String(150))
    notas_cliente: Mapped[Optional[str]] = mapped_column(Text)
    costo_envio: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2), server_default=text('0.00'))
    descuento: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2), server_default=text('0.00'))
    fecha_estimada_entrega: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fecha_entrega_real: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    comprobante_pago: Mapped[Optional[str]] = mapped_column(String(255))
    metodo_pago: Mapped[Optional[PedidosMetodoPago]] = mapped_column(Enum(PedidosMetodoPago, values_callable=lambda cls: [member.value for member in cls]), server_default=text("'efectivo'"))
    pagado: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))

    usuarios: Mapped['Usuarios'] = relationship('Usuarios', back_populates='pedidos')
    estados_pedido: Mapped['EstadosPedido'] = relationship('EstadosPedido', back_populates='pedidos')
    metodos_entrega: Mapped['MetodosEntrega'] = relationship('MetodosEntrega', back_populates='pedidos')
    sucursales: Mapped['Sucursales'] = relationship('Sucursales', back_populates='pedidos')
    calificaciones: Mapped[list['Calificaciones']] = relationship('Calificaciones', back_populates='pedidos')
    detalle_pedido: Mapped[list['DetallePedido']] = relationship('DetallePedido', back_populates='pedidos')
    historial_pedido: Mapped[list['HistorialPedido']] = relationship('HistorialPedido', back_populates='pedidos')


class Calificaciones(Base):
    __tablename__ = 'calificaciones'
    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['usuarios.id_usuario'], ondelete='CASCADE', name='calificaciones_ibfk_2'),
        ForeignKeyConstraint(['id_pedido'], ['pedidos.id_pedido'], ondelete='CASCADE', name='calificaciones_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], ondelete='SET NULL', name='calificaciones_ibfk_3'),
        Index('id_cliente', 'id_cliente'),
        Index('idx_aprobado', 'aprobado'),
        Index('idx_pedido', 'id_pedido'),
        Index('idx_producto', 'id_producto')
    )

    id_calificacion: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido: Mapped[int] = mapped_column(Integer, nullable=False)
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_calificacion: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id_producto: Mapped[Optional[int]] = mapped_column(Integer)
    calificacion_producto: Mapped[Optional[int]] = mapped_column(Integer)
    calificacion_servicio: Mapped[Optional[int]] = mapped_column(Integer)
    comentario: Mapped[Optional[str]] = mapped_column(Text)
    respuesta_vendedor: Mapped[Optional[str]] = mapped_column(Text)
    fecha_respuesta: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    aprobado: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))

    usuarios: Mapped['Usuarios'] = relationship('Usuarios', back_populates='calificaciones')
    pedidos: Mapped['Pedidos'] = relationship('Pedidos', back_populates='calificaciones')
    productos: Mapped[Optional['Productos']] = relationship('Productos', back_populates='calificaciones')


class DetallePedido(Base):
    __tablename__ = 'detalle_pedido'
    __table_args__ = (
        ForeignKeyConstraint(['id_pedido'], ['pedidos.id_pedido'], ondelete='CASCADE', name='detalle_pedido_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='detalle_pedido_ibfk_2'),
        Index('idx_pedido', 'id_pedido'),
        Index('idx_producto', 'id_producto')
    )

    id_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    notas: Mapped[Optional[str]] = mapped_column(Text)

    pedidos: Mapped['Pedidos'] = relationship('Pedidos', back_populates='detalle_pedido')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='detalle_pedido')


class HistorialPedido(Base):
    __tablename__ = 'historial_pedido'
    __table_args__ = (
        ForeignKeyConstraint(['id_estado'], ['estados_pedido.id_estado'], name='historial_pedido_ibfk_2'),
        ForeignKeyConstraint(['id_pedido'], ['pedidos.id_pedido'], ondelete='CASCADE', name='historial_pedido_ibfk_1'),
        ForeignKeyConstraint(['id_usuario'], ['usuarios.id_usuario'], ondelete='SET NULL', name='historial_pedido_ibfk_3'),
        Index('id_estado', 'id_estado'),
        Index('id_usuario', 'id_usuario'),
        Index('idx_fecha', 'fecha_cambio'),
        Index('idx_pedido', 'id_pedido')
    )

    id_historial: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido: Mapped[int] = mapped_column(Integer, nullable=False)
    id_estado: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_cambio: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    id_usuario: Mapped[Optional[int]] = mapped_column(Integer, comment='Usuario que realizó el cambio')
    comentario: Mapped[Optional[str]] = mapped_column(Text)

    estados_pedido: Mapped['EstadosPedido'] = relationship('EstadosPedido', back_populates='historial_pedido')
    pedidos: Mapped['Pedidos'] = relationship('Pedidos', back_populates='historial_pedido')
    usuarios: Mapped[Optional['Usuarios']] = relationship('Usuarios', back_populates='historial_pedido')


class MovimientosInventario(Base):
    __tablename__ = 'movimientos_inventario'
    __table_args__ = (
        ForeignKeyConstraint(['id_inventario'], ['inventario_sucursal.id_inventario'], ondelete='CASCADE', name='movimientos_inventario_ibfk_1'),
        ForeignKeyConstraint(['id_usuario'], ['usuarios.id_usuario'], ondelete='SET NULL', name='movimientos_inventario_ibfk_2'),
        Index('id_usuario', 'id_usuario'),
        Index('idx_fecha', 'fecha_movimiento'),
        Index('idx_inventario', 'id_inventario'),
        Index('idx_tipo', 'tipo_movimiento')
    )

    id_movimiento: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_inventario: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_movimiento: Mapped[MovimientosInventarioTipoMovimiento] = mapped_column(Enum(MovimientosInventarioTipoMovimiento, values_callable=lambda cls: [member.value for member in cls]), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_movimiento: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    motivo: Mapped[Optional[str]] = mapped_column(String(255))
    id_usuario: Mapped[Optional[int]] = mapped_column(Integer, comment='Usuario que realizó el movimiento')
    id_pedido: Mapped[Optional[int]] = mapped_column(Integer, comment='Si es por una venta')
    referencia: Mapped[Optional[str]] = mapped_column(String(100))

    inventario_sucursal: Mapped['InventarioSucursal'] = relationship('InventarioSucursal', back_populates='movimientos_inventario')
    usuarios: Mapped[Optional['Usuarios']] = relationship('Usuarios', back_populates='movimientos_inventario')
