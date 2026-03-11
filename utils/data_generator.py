import random
import datetime
from models.database import Database
from utils.i18n import I18n

class DataGenerator:
    """Generador de datos sintéticos de prueba para el sistema"""
    
    @staticmethod
    def generar_datos_prueba():
        """Genera departamentos y empleados de prueba basados en el idioma actual"""
        
        # 0. Determinar arrays según idioma actual
        idioma = I18n._current_lang
        
        if idioma == 'en':
            deptos = ['Human Resources', 'Technology', 'Marketing', 'Sales', 'Operations', 'Finance']
            nombres = ['Alice', 'John', 'Michael', 'Emma', 'David', 'Sarah', 'James', 'Olivia', 'William', 'Emily', 'Robert', 'Jessica']
            apellidos = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
            dir_falsa = '123 Fake Street'
        else:
            deptos = ['Recursos Humanos', 'Tecnología', 'Marketing', 'Ventas', 'Operaciones', 'Finanzas']
            nombres = ['Ana', 'Juan', 'Carlos', 'Elena', 'Diego', 'Lucia', 'Mateo', 'Sofia', 'Luis', 'Maria', 'Pedro', 'Rosa']
            apellidos = ['Garcia', 'Martinez', 'Rodriguez', 'Lopez', 'Hernandez', 'Gonzalez', 'Perez', 'Sanchez', 'Romero', 'Suarez']
            dir_falsa = 'Dir Ficticia 123'

        # 1. Crear departamentos
        db = Database.connect()
        cursor = db.cursor()
        
        ids_deptos = []
        for d in deptos:
            cursor.execute("INSERT INTO departamentos (nombre_dep) VALUES (?)", (d,))
            ids_deptos.append(cursor.lastrowid)
            
        # 2. Crear empleados
        roles = [101, 102] # Gerentes (101) y Empleados (102)
        
        for i in range(50):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            edad = random.randint(22, 60)
            telefono = f"555-{random.randint(1000,9999)}"
            
            # Garantizar unicidad usando el índice de iteración (i)
            correo = f"{nombre.lower()}.{apellido.lower()}_{i}@empresa.com"
            
            id_rol = random.choice([101, 102, 102, 102, 102]) # Más empleados que gerentes
            id_dep = random.choice(ids_deptos)
            
            # Salario base
            salario = random.randint(1500, 3000) if id_rol == 102 else random.randint(3500, 6000)
            
            # Fecha de hace 1 a 5 años
            fecha_contrato = (datetime.date.today() - datetime.timedelta(days=random.randint(30, 1800))).strftime('%Y-%m-%d')
            
            query = """INSERT INTO empleados (nombre_empleado, apellido_empleado, edad, 
                       direccion, telefono, correo, fecha_contrato, salario, fk_id_rol_e, fk_id_departamento) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, (nombre, apellido, edad, dir_falsa, telefono, correo, fecha_contrato, salario, id_rol, id_dep))
            
        db.commit()
        db.close()
        return True
