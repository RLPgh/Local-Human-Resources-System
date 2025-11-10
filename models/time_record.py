"""
Modelo de Registro de Tiempos
"""

from models.database import Database


class TimeRecord:
    """Clase que representa un registro de tiempo trabajado"""
    
    def __init__(self, id_rt, fecha, horas, descripcion, id_empleado, id_proyecto=None):
        self.id_rt = id_rt
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto
    
    @staticmethod
    def crear(fecha, horas, descripcion, id_empleado, id_proyecto=None):
        """Crea un nuevo registro de tiempo"""
        query = """INSERT INTO registro_tiempos (fecha_rt, tiempo_rt_horas, descripcion_tareas, 
                   fk_id_empleado_rt, fk_id_proyecto_rt) VALUES (%s, %s, %s, %s, %s)"""
        return Database.execute_command(query, (fecha, horas, descripcion, id_empleado, id_proyecto))
    
    @staticmethod
    def obtener_por_empleado(id_empleado):
        """Obtiene los registros de tiempo de un empleado"""
        query = """SELECT rt.id_rt, rt.fecha_rt, rt.tiempo_rt_horas, rt.descripcion_tareas, 
                   p.nombre_proyecto, d.nombre_dep
                   FROM registro_tiempos rt
                   LEFT JOIN proyectos p ON rt.fk_id_proyecto_rt = p.id_proyecto
                   LEFT JOIN empleados e ON rt.fk_id_empleado_rt = e.id_empleado
                   LEFT JOIN departamentos d ON e.fk_id_departamento = d.id_departamento
                   WHERE rt.fk_id_empleado_rt = %s
                   ORDER BY rt.fecha_rt DESC"""
        return Database.execute_query(query, (id_empleado,))
    
    @staticmethod
    def obtener_horas_diarias(id_empleado, fecha):
        """Obtiene las horas totales registradas por un empleado en una fecha"""
        query = """SELECT SUM(tiempo_rt_horas) as total_horas 
                   FROM registro_tiempos 
                   WHERE fk_id_empleado_rt = %s AND fecha_rt = %s"""
        resultado = Database.execute_query(query, (id_empleado, fecha), fetchone=True)
        
        if resultado and resultado['total_horas']:
            return float(resultado['total_horas'])
        return 0.0
    
    @staticmethod
    def validar_horas_diarias(id_empleado, fecha, horas_nuevas):
        """Valida que no se excedan las 12 horas diarias (ley chilena)"""
        horas_existentes = TimeRecord.obtener_horas_diarias(id_empleado, fecha)
        horas_totales = horas_existentes + float(horas_nuevas)
        
        if horas_totales > 12:
            return False, horas_existentes, horas_totales
        
        return True, horas_existentes, horas_totales
