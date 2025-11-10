"""
Controlador de empleados
"""

from models.employee import Employee


class EmployeeController:
    """Controlador para gestión de empleados"""
    
    def __init__(self, usuario_actual):
        """
        Inicializa el controlador
        
        Args:
            usuario_actual: Diccionario con datos del usuario actual
        """
        self.usuario = usuario_actual
    
    def puede_gestionar_empleados(self):
        """Verifica si el usuario puede gestionar empleados (Admin RH)"""
        return self.usuario.get('fk_id_rol_e') == 100
    
    def crear_empleado(self, nombre, apellido, edad, direccion, telefono, correo, 
                      fecha_contrato, salario, id_rol):
        """
        Crea un nuevo empleado
        
        Returns:
            Tupla (id_empleado, mensaje)
        """
        if not self.puede_gestionar_empleados():
            return None, "No tiene permisos para crear empleados"
        
        # Verificar que el correo no exista
        if Employee.correo_existe(correo):
            return None, "El correo ya está registrado"
        
        id_empleado = Employee.crear(nombre, apellido, edad, direccion, telefono, 
                                     correo, fecha_contrato, salario, id_rol)
        
        if id_empleado:
            return id_empleado, f"Empleado creado exitosamente con ID: {id_empleado}"
        return None, "Error al crear empleado"
    
    def obtener_todos_empleados(self):
        """
        Obtiene todos los empleados
        
        Returns:
            Tupla (lista_empleados, mensaje)
        """
        if not self.puede_gestionar_empleados():
            return None, "No tiene permisos"
        
        empleados = Employee.obtener_todos()
        if empleados:
            return empleados, "Empleados obtenidos exitosamente"
        return [], "No hay empleados registrados"
    
    def obtener_empleado(self, id_empleado):
        """
        Obtiene un empleado específico
        
        Returns:
            Tupla (empleado, mensaje)
        """
        if not self.puede_gestionar_empleados():
            return None, "No tiene permisos"
        
        empleado = Employee.obtener_por_id(id_empleado)
        if empleado:
            return empleado, "Empleado encontrado"
        return None, "Empleado no encontrado"
    
    def actualizar_empleado(self, id_empleado, nombre, apellido, edad, direccion, 
                           telefono, correo, salario):
        """
        Actualiza un empleado
        
        Returns:
            Tupla (exito, mensaje)
        """
        if not self.puede_gestionar_empleados():
            return False, "No tiene permisos para modificar empleados"
        
        # Verificar que el correo no esté en uso por otro empleado
        if Employee.correo_existe(correo, id_empleado):
            return False, "El correo ya está registrado por otro empleado"
        
        filas = Employee.actualizar(id_empleado, nombre, apellido, edad, direccion, 
                                   telefono, correo, salario)
        
        if filas and filas > 0:
            return True, f"Empleado {id_empleado} modificado exitosamente"
        return False, "Empleado no encontrado"
    
    def eliminar_empleado(self, id_empleado):
        """
        Elimina un empleado
        
        Returns:
            Tupla (exito, mensaje)
        """
        if not self.puede_gestionar_empleados():
            return False, "No tiene permisos para eliminar empleados"
        
        # No permitir que se elimine a sí mismo
        if self.usuario.get('id_empleado') == id_empleado:
            return False, "No puede eliminarse a sí mismo"
        
        filas = Employee.eliminar(id_empleado)
        if filas and filas > 0:
            return True, f"Empleado {id_empleado} eliminado exitosamente"
        return False, "Empleado no encontrado"
