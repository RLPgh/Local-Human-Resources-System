"""
Controlador de informes
"""

from models.employee import Employee
from models.project import Project
from datetime import datetime
import os


class ReportController:
    """Controlador para generación de informes"""
    
    def __init__(self, usuario_actual):
        """
        Inicializa el controlador
        
        Args:
            usuario_actual: Diccionario con datos del usuario actual
        """
        self.usuario = usuario_actual
    
    def puede_generar_informes(self):
        """Verifica si el usuario puede generar informes (Admin RH)"""
        return self.usuario.get('fk_id_rol_e') == 100
    
    def informe_empleados_por_departamento(self):
        """
        Genera informe de empleados agrupados por departamento
        
        Returns:
            Tupla (datos, mensaje)
        """
        if not self.puede_generar_informes():
            return None, "No tiene permisos para generar informes"
        
        datos = Employee.obtener_por_departamento()
        if datos:
            return datos, "Informe generado exitosamente"
        return [], "No hay datos para el informe"
    
    def informe_empleados_por_proyecto(self):
        """
        Genera informe de empleados agrupados por proyecto
        
        Returns:
            Tupla (datos, mensaje)
        """
        if not self.puede_generar_informes():
            return None, "No tiene permisos para generar informes"
        
        datos = Project.obtener_empleados_por_proyecto()
        if datos:
            return datos, "Informe generado exitosamente"
        return [], "No hay datos para el informe"
    
    def informe_empleados_totales(self):
        """
        Genera informe de todos los empleados
        
        Returns:
            Tupla (datos, mensaje)
        """
        if not self.puede_generar_informes():
            return None, "No tiene permisos para generar informes"
        
        datos = Employee.obtener_todos()
        if datos:
            return datos, "Informe generado exitosamente"
        return [], "No hay datos para el informe"
    
    def generar_archivo_txt(self, datos, tipo_informe):
        """
        Genera un archivo de texto con el informe
        
        Args:
            datos: Lista de diccionarios con los datos
            tipo_informe: Tipo de informe (para el nombre del archivo)
            
        Returns:
            Tupla (exito, mensaje)
        """
        if not self.puede_generar_informes():
            return False, "No tiene permisos para generar informes"
        
        if not datos:
            return False, "No hay datos para generar el informe"
        
        try:
            # Crear directorio de informes si no existe
            if not os.path.exists('informes'):
                os.makedirs('informes')
            
            # Generar nombre de archivo con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f"informes/informe_{tipo_informe}_{timestamp}.txt"
            
            # Escribir archivo
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(f"{'='*80}\n")
                archivo.write(f"INFORME: {tipo_informe.upper()}\n")
                archivo.write(f"{'='*80}\n\n")
                
                if isinstance(datos, list) and len(datos) > 0 and isinstance(datos[0], dict):
                    # Obtener encabezados
                    encabezados = list(datos[0].keys())
                    
                    # Escribir encabezados
                    archivo.write(" | ".join(f"{enc[:20]:20}" for enc in encabezados) + "\n")
                    archivo.write("-" * (len(encabezados) * 23) + "\n")
                    
                    # Escribir datos
                    for fila in datos:
                        valores = [str(fila.get(enc, ""))[:20] for enc in encabezados]
                        archivo.write(" | ".join(f"{val:20}" for val in valores) + "\n")
                else:
                    archivo.write(str(datos))
                
                archivo.write(f"\n{'='*80}\n")
                archivo.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            return True, f"Informe generado: {nombre_archivo}"
        except Exception as e:
            return False, f"Error al generar informe: {str(e)}"
