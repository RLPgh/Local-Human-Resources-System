"""
Controlador de proyectos
"""

from models.project import Project


class ProjectController:
    """Controlador para gestión de proyectos"""
    
    def __init__(self, usuario_actual):
        """
        Inicializa el controlador
        
        Args:
            usuario_actual: Diccionario con datos del usuario actual
        """
        self.usuario = usuario_actual
    
    def puede_gestionar_proyectos(self):
        """Verifica si el usuario puede gestionar proyectos (Admin RH)"""
        return self.usuario.get('fk_id_rol_e') == 100
    
    def crear_proyecto(self, nombre, descripcion, fecha_inicio):
        """
        Crea un nuevo proyecto
        
        Returns:
            Tupla (id_proyecto, mensaje)
        """
        if not self.puede_gestionar_proyectos():
            return None, "No tiene permisos para crear proyectos"
        
        id_proyecto = Project.crear(nombre, descripcion, fecha_inicio)
        if id_proyecto:
            return id_proyecto, f"Proyecto creado exitosamente con ID: {id_proyecto}"
        return None, "Error al crear proyecto"
    
    def obtener_todos_proyectos(self):
        """
        Obtiene todos los proyectos
        
        Returns:
            Tupla (lista_proyectos, mensaje)
        """
        if not self.puede_gestionar_proyectos():
            return None, "No tiene permisos"
        
        proyectos = Project.obtener_todos()
        if proyectos:
            return proyectos, "Proyectos obtenidos exitosamente"
        return [], "No hay proyectos registrados"
    
    def obtener_proyecto(self, id_proyecto):
        """
        Obtiene un proyecto específico
        
        Returns:
            Tupla (proyecto, mensaje)
        """
        if not self.puede_gestionar_proyectos():
            return None, "No tiene permisos"
        
        proyecto = Project.obtener_por_id(id_proyecto)
        if proyecto:
            return proyecto, "Proyecto encontrado"
        return None, "Proyecto no encontrado"
    
    def actualizar_proyecto(self, id_proyecto, nombre, descripcion, fecha_inicio):
        """
        Actualiza un proyecto
        
        Returns:
            Tupla (exito, mensaje)
        """
        if not self.puede_gestionar_proyectos():
            return False, "No tiene permisos para modificar proyectos"
        
        filas = Project.actualizar(id_proyecto, nombre, descripcion, fecha_inicio)
        if filas and filas > 0:
            return True, f"Proyecto {id_proyecto} modificado exitosamente"
        return False, "Proyecto no encontrado"
    
    def eliminar_proyecto(self, id_proyecto):
        """
        Elimina un proyecto
        
        Returns:
            Tupla (exito, mensaje)
        """
        if not self.puede_gestionar_proyectos():
            return False, "No tiene permisos para eliminar proyectos"
        
        filas = Project.eliminar(id_proyecto)
        if filas and filas > 0:
            return True, f"Proyecto {id_proyecto} eliminado exitosamente"
        return False, "Proyecto no encontrado"
    
    def asignar_empleado(self, id_empleado, id_proyecto, fecha_asignacion=None):
        """
        Asigna un proyecto a un empleado
        
        Returns:
            Tupla (exito, mensaje)
        """
        if not self.puede_gestionar_proyectos():
            return False, "No tiene permisos para asignar proyectos"
        
        id_asignacion = Project.asignar_empleado(id_empleado, id_proyecto, fecha_asignacion)
        if id_asignacion:
            return True, "Proyecto asignado exitosamente"
        return False, "Error al asignar proyecto"
    
    def desasignar_empleado(self, id_empleado, id_proyecto):
        """
        Desasigna un proyecto de un empleado
        
        Returns:
            Tupla (exito, mensaje)
        """
        if not self.puede_gestionar_proyectos():
            return False, "No tiene permisos para desasignar proyectos"
        
        filas = Project.desasignar_empleado(id_empleado, id_proyecto)
        if filas and filas > 0:
            return True, "Proyecto desasignado exitosamente"
        return False, "Asignación no encontrada"
    
    def obtener_asignaciones(self):
        """
        Obtiene todas las asignaciones de proyectos
        
        Returns:
            Tupla (lista_asignaciones, mensaje)
        """
        if not self.puede_gestionar_proyectos():
            return None, "No tiene permisos"
        
        asignaciones = Project.obtener_asignaciones()
        if asignaciones:
            return asignaciones, "Asignaciones obtenidas exitosamente"
        return [], "No hay asignaciones registradas"
    
    def obtener_proyectos_empleado(self, id_empleado):
        """
        Obtiene los proyectos asignados a un empleado
        
        Returns:
            Tupla (lista_proyectos, mensaje)
        """
        proyectos = Project.obtener_proyectos_empleado(id_empleado)
        if proyectos:
            return proyectos, "Proyectos obtenidos exitosamente"
        return [], "No tiene proyectos asignados"
