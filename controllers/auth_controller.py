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
    def verificar_registro_habilitado():
        """
        Verifica si el registro público está habilitado
        
        Returns:
            True si está habilitado, False si no
        """
        return config.APP_CONFIG.get('registro_publico_habilitado', True)
    
    @staticmethod
    def cambiar_estado_registro(habilitado):
        """
        Cambia el estado del registro público
        
        Args:
            habilitado: True para habilitar, False para deshabilitar
            
        Returns:
            True si se cambió exitosamente
        """
        config.APP_CONFIG['registro_publico_habilitado'] = habilitado
        return True
