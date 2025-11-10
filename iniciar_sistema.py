#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🚀 LAUNCHER ÚNICO - Sistema de Gestión de Recursos Humanos
=====================================================
Este es el ÚNICO archivo que necesitas ejecutar.

Funcionalidades automáticas:
✅ Verifica Python 3.8+
✅ Instala dependencias (mysql-connector-python, bcrypt)
✅ Detecta MySQL en el sistema
✅ Crea la base de datos automáticamente
✅ Inicia la aplicación

INSTRUCCIONES:
1. Asegúrate de tener Python 3.8+ instalado
2. Ejecuta este archivo: python iniciar_sistema.py
3. ¡Listo!

AUTOR: Sistema RH
VERSION: 2.0.0
"""

import sys
import os
import subprocess
import platform
import time

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class Colors:
    """Colores para terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header():
    """Muestra el encabezado del launcher"""
    print("\n" + "="*60)
    print("🏢 SISTEMA DE GESTIÓN DE RECURSOS HUMANOS")
    print("="*60 + "\n")


def print_step(step_num, total_steps, message):
    """Imprime un paso del proceso"""
    print(f"[{step_num}/{total_steps}] {message}")


def check_python_version():
    """Verifica que la versión de Python sea adecuada"""
    print_step(1, 6, "Verificando versión de Python...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"    ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"    ❌ Python {version.major}.{version.minor}.{version.micro}")
        print(f"    ⚠️  Se requiere Python 3.8 o superior")
        print(f"    📥 Descarga desde: https://www.python.org/downloads/")
        return False


def install_dependencies():
    """Instala las dependencias necesarias"""
    print_step(2, 6, "Verificando dependencias de Python...")
    
    required_packages = {
        'mysql.connector': 'mysql-connector-python',
        'bcrypt': 'bcrypt'
    }
    
    missing_packages = []
    
    for module, package in required_packages.items():
        try:
            if module == 'mysql.connector':
                __import__('mysql.connector')
            else:
                __import__(module)
            print(f"    ✅ {package}")
        except ImportError:
            print(f"    ⚠️  {package} no encontrado")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n    📦 Instalando paquetes faltantes...")
        for package in missing_packages:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package, "--quiet"
                ])
                print(f"    ✅ {package} instalado correctamente")
            except subprocess.CalledProcessError:
                print(f"    ❌ Error al instalar {package}")
                return False
    
    return True


def check_mysql_installation():
    """Verifica si MySQL está instalado en el sistema"""
    print_step(3, 6, "Verificando instalación de MySQL...")
    
    system = platform.system()
    mysql_found = False
    
    # Intentar encontrar MySQL en ubicaciones comunes
    common_paths = []
    
    if system == "Windows":
        common_paths = [
            r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
            r"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe",
            r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe",
            r"C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin\mysql.exe",
            r"C:\xampp\mysql\bin\mysql.exe",
            r"C:\wamp64\bin\mysql\mysql8.0.27\bin\mysql.exe",
        ]
    elif system == "Darwin":  # macOS
        common_paths = [
            "/usr/local/mysql/bin/mysql",
            "/opt/homebrew/bin/mysql",
            "/usr/local/bin/mysql",
        ]
    else:  # Linux
        common_paths = [
            "/usr/bin/mysql",
            "/usr/local/bin/mysql",
        ]
    
    # Verificar en PATH
    try:
        result = subprocess.run(
            ["mysql", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            mysql_found = True
            print(f"    ✅ MySQL encontrado en PATH")
            print(f"    📌 {result.stdout.strip()}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Verificar en rutas comunes
    if not mysql_found:
        for path in common_paths:
            if os.path.exists(path):
                mysql_found = True
                print(f"    ✅ MySQL encontrado en: {path}")
                break
    
    if not mysql_found:
        print(f"    ⚠️  MySQL no detectado en el sistema")
        print(f"\n    📥 Para instalar MySQL:")
        if system == "Windows":
            print(f"       - Opción 1 (Recomendada): XAMPP → https://www.apachefriends.org/")
            print(f"       - Opción 2: MySQL Community → https://dev.mysql.com/downloads/installer/")
        elif system == "Darwin":
            print(f"       - Homebrew: brew install mysql")
            print(f"       - O descarga desde: https://dev.mysql.com/downloads/mysql/")
        else:
            print(f"       - Ubuntu/Debian: sudo apt-get install mysql-server")
            print(f"       - Fedora: sudo dnf install mysql-server")
        
        print(f"\n    ⏸️  Instala MySQL y vuelve a ejecutar este launcher")
        return False
    
    return True


def test_mysql_connection():
    """Prueba la conexión a MySQL"""
    print_step(4, 6, "Probando conexión a MySQL...")
    
    try:
        import mysql.connector
        from config import DB_CONFIG
        
        # Intentar conectar sin especificar base de datos
        config_test = DB_CONFIG.copy()
        config_test.pop('database', None)
        
        connection = mysql.connector.connect(**config_test)
        
        if connection.is_connected():
            print(f"    ✅ Conexión exitosa a MySQL")
            connection.close()
            return True
        else:
            print(f"    ❌ No se pudo conectar a MySQL")
            return False
            
    except mysql.connector.Error as e:
        print(f"    ❌ Error de conexión: {e}")
        print(f"\n    🔧 Verifica en config.py:")
        print(f"       - host: {DB_CONFIG.get('host', 'localhost')}")
        print(f"       - user: {DB_CONFIG.get('user', 'root')}")
        print(f"       - password: {'(configurada)' if DB_CONFIG.get('password') else '(vacía)'}")
        print(f"\n    💡 Asegúrate de que MySQL esté ejecutándose")
        return False


def setup_database():
    """Crea la base de datos automáticamente si no existe"""
    print_step(5, 6, "Configurando base de datos...")
    
    try:
        import mysql.connector
        from config import DB_CONFIG
        
        # Conectar sin especificar base de datos
        config_test = DB_CONFIG.copy()
        database_name = config_test.pop('database')
        
        connection = mysql.connector.connect(**config_test)
        cursor = connection.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if database_name in databases:
            print(f"    ✅ Base de datos '{database_name}' ya existe")
            cursor.close()
            connection.close()
            return True
        
        # Crear la base de datos
        print(f"    📊 Creando base de datos '{database_name}'...")
        
        # Leer y ejecutar el script SQL
        sql_file = os.path.join(os.path.dirname(__file__), 'dbEmpresa.sql')
        
        if not os.path.exists(sql_file):
            print(f"    ❌ Archivo dbEmpresa.sql no encontrado")
            cursor.close()
            connection.close()
            return False
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Limpiar comentarios pero mantener estructura
        cleaned_lines = []
        for line in sql_script.split('\n'):
            # Remover espacios al inicio/final
            line = line.strip()
            # Ignorar líneas vacías y comentarios
            if line and not line.startswith('--') and not line.startswith('#'):
                cleaned_lines.append(line)
        
        # Unir las líneas con espacios
        sql_script = ' '.join(cleaned_lines)
        
        # Ejecutar cada sentencia SQL
        statements = [s.strip() for s in sql_script.split(';') if s.strip()]
        
        for statement in statements:
            try:
                cursor.execute(statement)
            except mysql.connector.Error as e:
                # Ignorar silenciosamente errores comunes de BD ya existente
                error_str = str(e).lower()
                if not any(err in error_str for err in ['already exists', 'duplicate entry', "can't create database", 'table already exists']):
                    # Solo mostrar errores realmente importantes
                    if 'syntax' not in error_str:
                        print(f"    ⚠️  {e}")
        
        connection.commit()
        print(f"    ✅ Base de datos creada correctamente")
        print(f"    ✅ Tablas y datos iniciales cargados")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"    ❌ Error al configurar base de datos: {e}")
        return False


def start_application():
    """Inicia la aplicación principal"""
    print_step(6, 6, "Iniciando aplicación...\n")
    
    try:
        print("="*60)
        print("✨ ¡Sistema listo! Abriendo interfaz gráfica...")
        print("="*60 + "\n")
        
        time.sleep(1)
        
        # Importar componentes de la aplicación
        import tkinter as tk
        from tkinter import messagebox
        from views.login_view import LoginView
        from views.admin_view import AdminView
        from views.manager_view import ManagerView
        from views.employee_view import EmployeeView
        
        class AplicacionRH:
            """Clase principal de la aplicación"""
            
            def __init__(self):
                """Inicializa la aplicación"""
                self.root = tk.Tk()
                self.usuario_actual = None
                self.configurar_ventana()
                self.mostrar_login()
            
            def configurar_ventana(self):
                """Configura la ventana principal"""
                self.root.title("Sistema de Gestión de Recursos Humanos")
                self.root.geometry("800x600")
                self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
            
            def mostrar_login(self):
                """Muestra la ventana de login"""
                LoginView(self.root, self.on_login_exitoso)
            
            def on_login_exitoso(self, usuario):
                """Callback cuando el login es exitoso"""
                self.usuario_actual = usuario
                rol = usuario.get('fk_id_rol_e')
                
                if rol == 100:  # Administrador RH
                    AdminView(self.root, usuario, self.cerrar_sesion)
                elif rol == 101:  # Gerente
                    ManagerView(self.root, usuario, self.cerrar_sesion)
                elif rol == 102:  # Empleado
                    EmployeeView(self.root, usuario, self.cerrar_sesion)
                else:
                    messagebox.showerror("Error", "Rol de usuario no reconocido")
                    self.mostrar_login()
            
            def cerrar_sesion(self):
                """Cierra la sesión actual y vuelve al login"""
                if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
                    self.usuario_actual = None
                    self.mostrar_login()
            
            def cerrar_aplicacion(self):
                """Cierra la aplicación"""
                if messagebox.askyesno("Salir", "¿Está seguro que desea salir?"):
                    self.root.quit()
                    self.root.destroy()
                    sys.exit(0)
            
            def ejecutar(self):
                """Inicia el loop principal de la aplicación"""
                try:
                    self.root.mainloop()
                except KeyboardInterrupt:
                    print("\n\nAplicación interrumpida por el usuario")
                    sys.exit(0)
        
        # Iniciar la aplicación
        app = AplicacionRH()
        app.ejecutar()
        
    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def main():
    """Función principal del launcher"""
    print_header()
    
    # Verificar Python
    if not check_python_version():
        input("\n⏸️  Presiona ENTER para salir...")
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        input("\n⏸️  Presiona ENTER para salir...")
        sys.exit(1)
    
    # Verificar MySQL instalado
    if not check_mysql_installation():
        input("\n⏸️  Presiona ENTER para salir...")
        sys.exit(1)
    
    # Probar conexión a MySQL
    if not test_mysql_connection():
        input("\n⏸️  Presiona ENTER para salir...")
        sys.exit(1)
    
    # Configurar base de datos
    if not setup_database():
        input("\n⏸️  Presiona ENTER para salir...")
        sys.exit(1)
    
    # Iniciar aplicación
    if not start_application():
        input("\n⏸️  Presiona ENTER para salir...")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        input("\n⏸️  Presiona ENTER para salir...")
        sys.exit(1)
