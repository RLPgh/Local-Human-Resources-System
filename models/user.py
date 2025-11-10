"""
Modelo de Usuario
"""

from models.database import Database
import bcrypt


class User:
    """Clase que representa un usuario del sistema"""
    
    def __init__(self, id_usuario, id_empleado, id_rol):
        self.id_usuario = id_usuario
        self.id_empleado = id_empleado
        self.id_rol = id_rol
    
    @staticmethod
    def crear(id_empleado, contraseña, id_rol):
        """Crea un nuevo usuario con contraseña hasheada"""
        try:
            # Hashear contraseña
            contraseña_hash = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
            
            query = """INSERT INTO usuarios (fk_id_empleado_u, contraseña_hash, fk_id_rol_u) 
                       VALUES (%s, %s, %s)"""
            return Database.execute_command(query, (id_empleado, contraseña_hash, id_rol))
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return None
    
    @staticmethod
    def autenticar(correo, contraseña):
        """Autentica un usuario con correo y contraseña"""
        try:
            # Buscar usuario por correo
            query = """SELECT e.*, u.contraseña_hash 
                       FROM empleados e
                       JOIN usuarios u ON e.id_empleado = u.fk_id_empleado_u
                       WHERE e.correo = %s"""
            resultado = Database.execute_query(query, (correo,), fetchone=True)
            
            if not resultado:
                return None
            
            # Verificar contraseña
            if bcrypt.checkpw(contraseña.encode('utf-8'), resultado['contraseña_hash'].encode('utf-8')):
                # Remover el hash de la contraseña antes de retornar
                resultado.pop('contraseña_hash', None)
                return resultado
            return None
        except Exception as e:
            print(f"Error al autenticar: {e}")
            return None
    
    @staticmethod
    def existe_por_empleado(id_empleado):
        """Verifica si existe un usuario para un empleado"""
        query = "SELECT id_usuario FROM usuarios WHERE fk_id_empleado_u = %s"
        resultado = Database.execute_query(query, (id_empleado,), fetchone=True)
        return resultado is not None
    
    @staticmethod
    def eliminar_por_empleado(id_empleado):
        """Elimina el usuario asociado a un empleado"""
        query = "DELETE FROM usuarios WHERE fk_id_empleado_u = %s"
        return Database.execute_command(query, (id_empleado,))
