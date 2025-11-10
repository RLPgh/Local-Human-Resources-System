"""
Validadores de datos para la interfaz gráfica
"""

import re
from datetime import datetime


class Validators:
    """Clase con métodos estáticos para validar datos de entrada"""
    
    @staticmethod
    def validar_string(texto, campo_nombre="Campo"):
        """
        Valida que el texto no esté vacío
        
        Returns:
            Tupla (valido, mensaje)
        """
        if not texto or not texto.strip():
            return False, f"{campo_nombre} no puede estar vacío"
        return True, ""
    
    @staticmethod
    def validar_edad(edad_str):
        """
        Valida que la edad esté entre 18 y 100
        
        Returns:
            Tupla (valido, mensaje)
        """
        try:
            edad = int(edad_str)
            if 18 <= edad <= 100:
                return True, ""
            return False, "La edad debe estar entre 18 y 100 años"
        except ValueError:
            return False, "La edad debe ser un número válido"
    
    @staticmethod
    def validar_telefono(telefono):
        """
        Valida que el teléfono tenga 9 dígitos
        
        Returns:
            Tupla (valido, mensaje)
        """
        telefono = telefono.strip()
        if not telefono.isdigit():
            return False, "El teléfono debe contener solo números"
        if len(telefono) != 9:
            return False, "El teléfono debe tener 9 dígitos"
        return True, ""
    
    @staticmethod
    def validar_correo(correo):
        """
        Valida el formato del correo electrónico
        
        Returns:
            Tupla (valido, mensaje)
        """
        correo = correo.strip()
        
        if not correo:
            return False, "El correo no puede estar vacío"
        
        # Verificar que tenga exactamente un @
        if correo.count("@") != 1:
            return False, "El correo debe tener exactamente un @"
        
        # Verificar formato básico
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            return False, "Formato de correo inválido"
        
        return True, ""
    
    @staticmethod
    def validar_direccion(direccion):
        """
        Valida que la dirección no contenga @
        
        Returns:
            Tupla (valido, mensaje)
        """
        direccion = direccion.strip()
        
        if not direccion:
            return False, "La dirección no puede estar vacía"
        
        if "@" in direccion:
            return False, "La dirección no puede contener el símbolo @"
        
        return True, ""
    
    @staticmethod
    def validar_salario(salario_str):
        """
        Valida que el salario sea un número positivo
        
        Returns:
            Tupla (valido, mensaje)
        """
        try:
            salario = float(salario_str)
            if salario > 0:
                return True, ""
            return False, "El salario debe ser mayor a 0"
        except ValueError:
            return False, "El salario debe ser un número válido"
    
    @staticmethod
    def validar_fecha(fecha_str):
        """
        Valida que la fecha tenga el formato YYYY-MM-DD
        
        Returns:
            Tupla (valido, mensaje)
        """
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            return True, ""
        except ValueError:
            return False, "Formato de fecha inválido. Use YYYY-MM-DD"
    
    @staticmethod
    def validar_contraseña(contraseña):
        """
        Valida que la contraseña tenga al menos 8 caracteres
        
        Returns:
            Tupla (valido, mensaje)
        """
        if not contraseña:
            return False, "La contraseña no puede estar vacía"
        
        if len(contraseña) < 8:
            return False, "La contraseña debe tener mínimo 8 caracteres"
        
        return True, ""
    
    @staticmethod
    def validar_horas(horas_str):
        """
        Valida que las horas sean un número entre 0 y 12
        
        Returns:
            Tupla (valido, mensaje)
        """
        try:
            horas = float(horas_str)
            if horas > 0 and horas <= 12:
                return True, ""
            elif horas > 12:
                return False, "Máximo 12 horas por día (ley chilena)"
            else:
                return False, "Las horas deben ser mayores a 0"
        except ValueError:
            return False, "Las horas deben ser un número válido"
    
    @staticmethod
    def validar_id(id_str):
        """
        Valida que el ID sea un número positivo
        
        Returns:
            Tupla (valido, mensaje)
        """
        try:
            id_num = int(id_str)
            if id_num > 0:
                return True, ""
            return False, "El ID debe ser mayor a 0"
        except ValueError:
            return False, "El ID debe ser un número válido"
