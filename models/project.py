"""
Modelo de Proyecto
"""

from models.database import Database
from datetime import date


class Project:
    """Clase que representa un proyecto"""
    
    def __init__(self, id_proyecto, nombre, descripcion, fecha_inicio):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
    
    @staticmethod
    def crear(nombre, descripcion, fecha_inicio):
        """Crea un nuevo proyecto"""
        query = """INSERT INTO proyectos (nombre_proyecto, descripcion_p, fecha_inicio_p) 
                   VALUES (%s, %s, %s)"""
        return Database.execute_command(query, (nombre, descripcion, fecha_inicio))
    
    @staticmethod
    def obtener_por_id(id_proyecto):
        """Obtiene un proyecto por su ID"""
        query = """SELECT * FROM proyectos WHERE id_proyecto = %s"""
        return Database.execute_query(query, (id_proyecto,), fetchone=True)
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los proyectos"""
        query = """SELECT id_proyecto, nombre_proyecto, descripcion_p, fecha_inicio_p 
                   FROM proyectos ORDER BY id_proyecto"""
        return Database.execute_query(query)
    
    @staticmethod
    def actualizar(id_proyecto, nombre, descripcion, fecha_inicio):
        """Actualiza un proyecto"""
        query = """UPDATE proyectos SET nombre_proyecto=%s, descripcion_p=%s, 
                   fecha_inicio_p=%s WHERE id_proyecto=%s"""
        return Database.execute_command(query, (nombre, descripcion, fecha_inicio, id_proyecto))
    
    @staticmethod
    def eliminar(id_proyecto):
        """Elimina un proyecto"""
        query = "DELETE FROM proyectos WHERE id_proyecto=%s"
        return Database.execute_command(query, (id_proyecto,))
    
    @staticmethod
    def existe_alguno():
        """Verifica si existe al menos un proyecto"""
        query = "SELECT COUNT(*) as total FROM proyectos"
        resultado = Database.execute_query(query, fetchone=True)
        return resultado and resultado['total'] > 0
    
    @staticmethod
    def asignar_empleado(id_empleado, id_proyecto, fecha_asignacion=None):
        """Asigna un proyecto a un empleado"""
        if fecha_asignacion is None:
            fecha_asignacion = date.today()
        
        query = """INSERT INTO asignacion_proyectos (fecha_asignacion, fk_id_empleado_ap, fk_id_proyecto_ap) 
                   VALUES (%s, %s, %s)"""
        return Database.execute_command(query, (fecha_asignacion, id_empleado, id_proyecto))
    
    @staticmethod
    def desasignar_empleado(id_empleado, id_proyecto):
        """Desasigna un proyecto de un empleado"""
        query = """DELETE FROM asignacion_proyectos 
                   WHERE fk_id_empleado_ap=%s AND fk_id_proyecto_ap=%s"""
        return Database.execute_command(query, (id_empleado, id_proyecto))
    
    @staticmethod
    def obtener_asignaciones():
        """Obtiene todas las asignaciones de proyectos"""
        query = """SELECT ap.id_asig_proyecto, ap.fecha_asignacion, 
                   e.id_empleado, e.nombre_empleado, e.apellido_empleado,
                   p.id_proyecto, p.nombre_proyecto
                   FROM asignacion_proyectos ap
                   JOIN empleados e ON ap.fk_id_empleado_ap = e.id_empleado
                   JOIN proyectos p ON ap.fk_id_proyecto_ap = p.id_proyecto
                   ORDER BY p.nombre_proyecto, e.apellido_empleado"""
        return Database.execute_query(query)
    
    @staticmethod
    def obtener_proyectos_empleado(id_empleado):
        """Obtiene los proyectos asignados a un empleado"""
        query = """SELECT p.id_proyecto, p.nombre_proyecto, ap.fecha_asignacion
                   FROM asignacion_proyectos ap
                   JOIN proyectos p ON ap.fk_id_proyecto_ap = p.id_proyecto
                   WHERE ap.fk_id_empleado_ap = %s
                   ORDER BY p.nombre_proyecto"""
        return Database.execute_query(query, (id_empleado,))
    
    @staticmethod
    def obtener_empleados_por_proyecto():
        """Obtiene empleados agrupados por proyecto"""
        query = """SELECT p.nombre_proyecto, e.id_empleado, e.nombre_empleado, 
                   e.apellido_empleado, ap.fecha_asignacion
                   FROM asignacion_proyectos ap
                   JOIN empleados e ON ap.fk_id_empleado_ap = e.id_empleado
                   JOIN proyectos p ON ap.fk_id_proyecto_ap = p.id_proyecto
                   ORDER BY p.nombre_proyecto, e.apellido_empleado"""
        return Database.execute_query(query)
