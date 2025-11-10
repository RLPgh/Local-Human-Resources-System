"""
Modelo de Empleado
"""

from models.database import Database
import config


class Employee:
    """Clase que representa un empleado en el sistema"""
    
    def __init__(self, id_empleado, nombre, apellido, edad, direccion, telefono, 
                 email, fecha_contrato, salario, id_rol, id_departamento=None):
        self.__id_empleado = id_empleado
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.fecha_contrato = fecha_contrato
        self.salario = salario
        self.id_rol = id_rol
        self.id_departamento = id_departamento
    
    @property
    def id_empleado(self):
        """ID de empleado - Solo lectura"""
        return self.__id_empleado
    
    def obtener_nombre_completo(self):
        """Retorna el nombre completo del empleado"""
        return f"{self.nombre} {self.apellido}"
    
    def es_admin_rh(self):
        """Verifica si el empleado es Administrador RH"""
        return self.id_rol == 100
    
    def es_gerente(self):
        """Verifica si el empleado es Gerente"""
        return self.id_rol == 101
    
    def es_empleado_regular(self):
        """Verifica si el empleado es Empleado regular"""
        return self.id_rol == 102
    
    def obtener_nombre_rol(self):
        """Retorna el nombre del rol"""
        return config.ROLES.get(self.id_rol, 'Desconocido')
    
    def __str__(self):
        """Representación en string del empleado"""
        return f"{self.obtener_nombre_completo()} - {self.obtener_nombre_rol()}"
    
    # Métodos estáticos para interactuar con la base de datos
    
    @staticmethod
    def crear(nombre, apellido, edad, direccion, telefono, correo, fecha_contrato, salario, id_rol):
        """Crea un nuevo empleado en la base de datos"""
        query = """INSERT INTO empleados (nombre_empleado, apellido_empleado, edad, 
                   direccion, telefono, correo, fecha_contrato, salario, fk_id_rol_e) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        return Database.execute_command(query, (nombre, apellido, edad, direccion, 
                                                telefono, correo, fecha_contrato, salario, id_rol))
    
    @staticmethod
    def obtener_por_id(id_empleado):
        """Obtiene un empleado por su ID"""
        query = """SELECT e.*, r.nombre_rol, d.nombre_dep
                   FROM empleados e
                   LEFT JOIN roles r ON e.fk_id_rol_e = r.id_rol
                   LEFT JOIN departamentos d ON e.fk_id_departamento = d.id_departamento
                   WHERE e.id_empleado = %s"""
        return Database.execute_query(query, (id_empleado,), fetchone=True)
    
    @staticmethod
    def obtener_por_correo(correo):
        """Obtiene un empleado por su correo"""
        query = """SELECT e.* FROM empleados e WHERE e.correo = %s"""
        return Database.execute_query(query, (correo,), fetchone=True)
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los empleados"""
        query = """SELECT e.id_empleado, e.nombre_empleado, e.apellido_empleado, 
                   e.edad, e.telefono, e.correo, e.salario, r.nombre_rol, d.nombre_dep
                   FROM empleados e
                   LEFT JOIN roles r ON e.fk_id_rol_e = r.id_rol
                   LEFT JOIN departamentos d ON e.fk_id_departamento = d.id_departamento
                   ORDER BY e.id_empleado"""
        return Database.execute_query(query)
    
    @staticmethod
    def actualizar(id_empleado, nombre, apellido, edad, direccion, telefono, correo, salario):
        """Actualiza los datos de un empleado"""
        query = """UPDATE empleados SET nombre_empleado=%s, apellido_empleado=%s, 
                   edad=%s, direccion=%s, telefono=%s, correo=%s, salario=%s 
                   WHERE id_empleado=%s"""
        return Database.execute_command(query, (nombre, apellido, edad, direccion, 
                                               telefono, correo, salario, id_empleado))
    
    @staticmethod
    def eliminar(id_empleado):
        """Elimina un empleado"""
        query = "DELETE FROM empleados WHERE id_empleado=%s"
        return Database.execute_command(query, (id_empleado,))
    
    @staticmethod
    def existe(id_empleado):
        """Verifica si un empleado existe"""
        query = "SELECT id_empleado FROM empleados WHERE id_empleado = %s"
        resultado = Database.execute_query(query, (id_empleado,), fetchone=True)
        return resultado is not None
    
    @staticmethod
    def correo_existe(correo, id_empleado_actual=None):
        """Verifica si un correo ya está registrado"""
        if id_empleado_actual:
            query = "SELECT id_empleado FROM empleados WHERE correo = %s AND id_empleado != %s"
            resultado = Database.execute_query(query, (correo, id_empleado_actual), fetchone=True)
        else:
            query = "SELECT id_empleado FROM empleados WHERE correo = %s"
            resultado = Database.execute_query(query, (correo,), fetchone=True)
        return resultado is not None
    
    @staticmethod
    def obtener_por_departamento():
        """Obtiene empleados agrupados por departamento"""
        query = """SELECT d.nombre_dep, e.id_empleado, e.nombre_empleado, 
                   e.apellido_empleado, r.nombre_rol
                   FROM empleados e
                   LEFT JOIN departamentos d ON e.fk_id_departamento = d.id_departamento
                   LEFT JOIN roles r ON e.fk_id_rol_e = r.id_rol
                   ORDER BY d.nombre_dep, e.apellido_empleado"""
        return Database.execute_query(query)
