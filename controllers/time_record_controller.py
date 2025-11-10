"""
Controlador de registro de tiempos
"""

from models.time_record import TimeRecord
from models.employee import Employee
from models.project import Project
from datetime import datetime


class TimeRecordController:
    """Controlador para gestión de registros de tiempo"""
    
    def __init__(self, usuario_actual):
        """
        Inicializa el controlador
        
        Args:
            usuario_actual: Diccionario con datos del usuario actual
        """
        self.usuario = usuario_actual
    
    def registrar_tiempo(self, fecha, horas, descripcion, id_proyecto=None):
        """
        Registra tiempo trabajado
        
        Returns:
            Tupla (exito, mensaje)
        """
        id_empleado = self.usuario.get('id_empleado')
        
        # Validar fecha vs fecha de contrato
        empleado = Employee.obtener_por_id(id_empleado)
        if empleado:
            fecha_contrato = empleado.get('fecha_contrato')
            if fecha < fecha_contrato:
                return False, f"No puede registrar horas antes de su fecha de contrato ({fecha_contrato})"
        
        # Validar horas diarias (máximo 12 horas)
        valido, horas_existentes, horas_totales = TimeRecord.validar_horas_diarias(
            id_empleado, fecha, horas
        )
        
        if not valido:
            mensaje = f"Ya tiene {horas_existentes:.2f} horas registradas para el {fecha}.\n"
            mensaje += f"Agregar {horas:.2f} horas resultaría en {horas_totales:.2f} horas totales.\n"
            mensaje += "La ley chilena permite un máximo de 12 horas diarias."
            return False, mensaje
        
        # Verificar si está asignado al proyecto (si se especifica)
        if id_proyecto:
            proyectos = Project.obtener_proyectos_empleado(id_empleado)
            proyecto_asignado = any(p['id_proyecto'] == id_proyecto for p in proyectos)
            
            if not proyecto_asignado:
                return False, "No está asignado a este proyecto. El tiempo se registrará sin proyecto."
        
        # Registrar el tiempo
        id_registro = TimeRecord.crear(fecha, horas, descripcion, id_empleado, id_proyecto)
        
        if id_registro:
            mensaje = "Tiempo registrado exitosamente"
            if horas_existentes > 0:
                mensaje += f"\nTotal de horas para el {fecha}: {horas_totales:.2f}/12"
            return True, mensaje
        return False, "Error al registrar tiempo"
    
    def obtener_mis_tiempos(self):
        """
        Obtiene los registros de tiempo del usuario actual
        
        Returns:
            Tupla (lista_registros, mensaje)
        """
        id_empleado = self.usuario.get('id_empleado')
        registros = TimeRecord.obtener_por_empleado(id_empleado)
        
        if registros:
            return registros, "Registros obtenidos exitosamente"
        return [], "No tiene registros de tiempo"
