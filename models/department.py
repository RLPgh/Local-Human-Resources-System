"""
Modelo de Departamento
"""

from models.database import Database


class Department:
    """Clase que representa un departamento"""
    
    def __init__(self, id_departamento, nombre, id_gerente=None):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.id_gerente = id_gerente
    
    @staticmethod
    def crear(nombre_dep):
        """Crea un nuevo departamento"""
        query = "INSERT INTO departamentos (nombre_dep) VALUES (%s)"
        return Database.execute_command(query, (nombre_dep,))
    
    @staticmethod
    def obtener_por_id(id_departamento):
        """Obtiene un departamento por su ID"""
        query = """SELECT d.*, 
                   CASE 
                       WHEN e.id_empleado IS NOT NULL 
                       THEN CONCAT(e.nombre_empleado, ' ', e.apellido_empleado)
                       ELSE NULL
                   END AS nombre_gerente
                   FROM departamentos d
                   LEFT JOIN empleados e ON d.fk_id_e_gerente = e.id_empleado
                   WHERE d.id_departamento = %s"""
        return Database.execute_query(query, (id_departamento,), fetchone=True)
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los departamentos con información de gerentes"""
        query = """SELECT d.id_departamento, d.nombre_dep, d.fk_id_e_gerente,
                   CASE 
                       WHEN e.id_empleado IS NOT NULL 
                       THEN CONCAT(e.nombre_empleado, ' ', e.apellido_empleado)
                       ELSE 'Sin gerente asignado'
                   END AS gerente
                   FROM departamentos d
                   LEFT JOIN empleados e ON d.fk_id_e_gerente = e.id_empleado
                   ORDER BY d.id_departamento"""
        return Database.execute_query(query)
    
    @staticmethod
    def actualizar(id_departamento, nombre_dep):
        """Actualiza un departamento"""
        query = "UPDATE departamentos SET nombre_dep=%s WHERE id_departamento=%s"
        return Database.execute_command(query, (nombre_dep, id_departamento))
    
    @staticmethod
    def eliminar(id_departamento):
        """Elimina un departamento"""
        query = "DELETE FROM departamentos WHERE id_departamento=%s"
        return Database.execute_command(query, (id_departamento,))
    
    @staticmethod
    def asignar_empleado(id_empleado, id_departamento):
        """Asigna un empleado a un departamento"""
        # Verificar que el empleado no tenga departamento
        query_check = "SELECT fk_id_departamento FROM empleados WHERE id_empleado=%s"
        resultado = Database.execute_query(query_check, (id_empleado,), fetchone=True)
        
        if not resultado:
            return None
        
        if resultado['fk_id_departamento'] is not None:
            return False  # Ya tiene departamento
        
        # Asignar departamento
        query = "UPDATE empleados SET fk_id_departamento=%s WHERE id_empleado=%s"
        return Database.execute_command(query, (id_departamento, id_empleado))
    
    @staticmethod
    def desasignar_empleado(id_empleado):
        """Desasigna un empleado de su departamento"""
        query = "UPDATE empleados SET fk_id_departamento=NULL WHERE id_empleado=%s"
        return Database.execute_command(query, (id_empleado,))
    
    @staticmethod
    def obtener_empleados_departamento(id_departamento):
        """Obtiene los empleados de un departamento"""
        query = """SELECT e.id_empleado, e.nombre_empleado, e.apellido_empleado
                   FROM empleados e
                   WHERE e.fk_id_departamento = %s
                   ORDER BY e.apellido_empleado, e.nombre_empleado"""
        return Database.execute_query(query, (id_departamento,))
    
    @staticmethod
    def obtener_empleados_sin_departamento():
        """Obtiene empleados que no tienen departamento asignado"""
        query = """SELECT e.id_empleado, e.nombre_empleado, e.apellido_empleado
                   FROM empleados e
                   WHERE e.fk_id_departamento IS NULL
                   ORDER BY e.apellido_empleado, e.nombre_empleado"""
        return Database.execute_query(query)
