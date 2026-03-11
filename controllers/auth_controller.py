"""
Controlador de autenticación
"""

from models.user import User
from models.employee import Employee
import config


class AuthController:
    """Controlador para manejo de autenticación y registro"""
    
    @staticmethod
    def iniciar_sesion(correo, contraseña):
        """
        Autentica un usuario
        
        Args:
            correo: Correo electrónico del usuario
            contraseña: Contraseña del usuario
            
        Returns:
            Diccionario con datos del empleado si es exitoso, None si falla
        """
        if not correo or not contraseña:
            return None, "Correo y contraseña son requeridos"
        
        resultado = User.autenticar(correo, contraseña)
        if resultado:
            return resultado, "Inicio de sesión exitoso"
        return None, "Correo o contraseña incorrectos"
    
    @staticmethod
    def registrar_usuario(id_empleado, contraseña, id_rol):
        """
        Registra un nuevo usuario
        
        Args:
            id_empleado: ID del empleado
            contraseña: Contraseña del usuario
            id_rol: Rol del usuario (100, 101, 102)
            
        Returns:
            ID del usuario creado o None si falla
        """
        # Verificar si ya existe un usuario para este empleado
        if User.existe_por_empleado(id_empleado):
            return None, "Ya existe un usuario para este empleado"
        
        id_usuario = User.crear(id_empleado, contraseña, id_rol)
        if id_usuario:
            return id_usuario, "Usuario registrado exitosamente"
        return None, "Error al registrar usuario"
    
    @staticmethod
    def determinar_rol_inicial():
        """
        Si la base de datos está vacía, devuelve el código 100 de Admin.
        Si ya hay alguien, devuelve None.
        """
        from models.database import Database
        result = Database.execute_query("SELECT COUNT(*) as total FROM usuarios", fetchone=True)
        if result and result.get('total', 0) == 0:
            return 100  # Administrador RH (obligatorio para el primero)
        return None
    
    @staticmethod
    def verificar_registro_habilitado():
        """
        Verifica si el registro público está habilitado
        
        Returns:
            True si está habilitado, False si no
        """
        return config.APP_CONFIG.get('registro_publico_habilitado', True)
    
    @staticmethod
    def cambiar_estado_registro(habilitado):
        config.APP_CONFIG['registro_publico_habilitado'] = habilitado
        return True
        
    @staticmethod
    def obtener_roles_permitidos():
        """
        Retorna la lista de roles permitidos para el registro público.
        """
        return config.APP_CONFIG.get('roles_registro_permitidos', [102])
        
    @staticmethod
    def actualizar_roles_permitidos(lista_roles_ids):
        """
        Actualiza los roles desde la configuración del Administrador
        """
        config.APP_CONFIG['roles_registro_permitidos'] = lista_roles_ids
        return True
