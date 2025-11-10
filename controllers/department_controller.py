"""
Controlador de departamentos
"""

from models.department import Department


class DepartmentController:
    """Controlador para gestión de departamentos"""
    
    def __init__(self, usuario_actual):
        """
        Inicializa el controlador
        
        Args:
            usuario_actual: Diccionario con datos del usuario actual
        """
        self.usuario = usuario_actual
    
    def puede_gestionar_departamentos(self):
        """Verifica si el usuario puede gestionar departamentos (Gerente)"""
        return self.usuario.get('fk_id_rol_e') == 101
    
    def crear_departamento(self, nombre_dep):
        """
        Crea un nuevo departamento
        
        Returns:
            Tupla (id_departamento, mensaje)
        """
        if not self.puede_gestionar_departamentos():
            return None, "No tiene permisos para crear departamentos"
        
        id_departamento = Department.crear(nombre_dep)
        if id_departamento:
            return id_departamento, f"Departamento creado exitosamente con ID: {id_departamento}"
        return None, "Error al crear departamento"
    
    def obtener_todos_departamentos(self):
        """
        Obtiene todos los departamentos
        
        Returns:
            Tupla (lista_departamentos, mensaje)
        """
        if not self.puede_gestionar_departamentos():
            return None, "No tiene permisos"
        
        departamentos = Department.obtener_todos()
        if departamentos:
            return departamentos, "Departamentos obtenidos exitosamente"
        return [], "No hay departamentos registrados"
    
    def obtener_departamento(self, id_departamento):
        """
        Obtiene un departamento específico
        
        Returns:
            Tupla (departamento, mensaje)
        """
        if not self.puede_gestionar_departamentos():
            return None, "No tiene permisos"
        
        departamento = Department.obtener_por_id(id_departamento)
        if departamento:
            return departamento, "Departamento encontrado"
        return None, "Departamento no encontrado"
    
    def actualizar_departamento(self, id_departamento, nombre_dep):
        """
        Actualiza un departamento
        
        Returns:
            Tupla (exito, mensaje)
        """
        if not self.puede_gestionar_departamentos():
            return False, "No tiene permisos para modificar departamentos"
        
        filas = Department.actualizar(id_departamento, nombre_dep)
        if filas and filas > 0:
            return True, f"Departamento {id_departamento} modificado exitosamente"
        return False, "Departamento no encontrado"
    
    def eliminar_departamento(self, id_departamento):
        """
        Elimina un departamento
        
        Returns:
            Tupla (exito, mensaje)
        """
        if not self.puede_gestionar_departamentos():
            return False, "No tiene permisos para eliminar departamentos"
        
        # Verificar si tiene gerente
        departamento = Department.obtener_por_id(id_departamento)
        if not departamento:
            return False, "Departamento no encontrado"
        
        # Permitir eliminar si no tiene gerente o si el gerente es el usuario actual
        gerente_id = departamento.get('fk_id_e_gerente')
        if gerente_id is not None and gerente_id != self.usuario.get('id_empleado'):
            return False, "No puede eliminar un departamento con otro gerente asignado"
        
        filas = Department.eliminar(id_departamento)
        if filas and filas > 0:
            return True, f"Departamento {id_departamento} eliminado exitosamente"
        return False, "Error al eliminar departamento"
    
    def asignar_empleado(self, id_empleado, id_departamento):
        """
        Asigna un empleado a un departamento
        
        Returns:
            Tupla (exito, mensaje)
        """
        if not self.puede_gestionar_departamentos():
            return False, "No tiene permisos para asignar empleados"
        
        resultado = Department.asignar_empleado(id_empleado, id_departamento)
        
        if resultado is None:
            return False, "Empleado no encontrado"
        elif resultado is False:
            return False, "El empleado ya tiene un departamento asignado"
        elif resultado > 0:
            return True, "Empleado asignado exitosamente"
        return False, "Error al asignar empleado"
    
    def desasignar_empleado(self, id_empleado):
        """
        Desasigna un empleado de su departamento
        
        Returns:
            Tupla (exito, mensaje)
        """
        if not self.puede_gestionar_departamentos():
            return False, "No tiene permisos para desasignar empleados"
        
        filas = Department.desasignar_empleado(id_empleado)
        if filas and filas > 0:
            return True, "Empleado desasignado exitosamente"
        return False, "Empleado no encontrado"
    
    def obtener_empleados_departamento(self, id_departamento):
        """
        Obtiene los empleados de un departamento
        
        Returns:
            Tupla (lista_empleados, mensaje)
        """
        if not self.puede_gestionar_departamentos():
            return None, "No tiene permisos"
        
        empleados = Department.obtener_empleados_departamento(id_departamento)
        if empleados:
            return empleados, "Empleados obtenidos exitosamente"
        return [], "No hay empleados en este departamento"
    
    def obtener_empleados_sin_departamento(self):
        """
        Obtiene empleados sin departamento asignado
        
        Returns:
            Tupla (lista_empleados, mensaje)
        """
        if not self.puede_gestionar_departamentos():
            return None, "No tiene permisos"
        
        empleados = Department.obtener_empleados_sin_departamento()
        if empleados:
            return empleados, "Empleados obtenidos exitosamente"
        return [], "No hay empleados sin departamento"
