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
VERSION: 0.2.0
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
    print_step(1, 4, "Verificando versión de Python...")
    
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
    print_step(2, 4, "Verificando dependencias de Python...")
    
    required_packages = {
        'customtkinter': 'customtkinter',
        'bcrypt': 'bcrypt',
        'matplotlib': 'matplotlib'
    }
    
    missing_packages = []
    
    for module, package in required_packages.items():
        try:
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


def setup_database():
    """Crea la base de datos automáticamente si no existe"""
    print_step(3, 4, "Configurando base de datos local SQLite...")
    
    try:
        import sqlite3
        from config import DB_CONFIG
        
        db_file = DB_CONFIG.get('database', 'dbEmpresa.db')
        
        # Si el archivo ya existe, comprobamos si tiene tablas
        db_exists = os.path.exists(db_file)
        
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        
        if db_exists:
            cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table'")
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"    ✅ Base de datos '{db_file}' ya existe y está configurada")
                cursor.close()
                connection.close()
                return True
        
        print(f"    📊 Creando y configurando base de datos '{db_file}'...")
        
        # Leer y ejecutar el script SQL
        sql_file = os.path.join(os.path.dirname(__file__), 'dbEmpresa.sql')
        
        if not os.path.exists(sql_file):
            print(f"    ❌ Archivo dbEmpresa.sql no encontrado")
            cursor.close()
            connection.close()
            return False
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Ejecutar el script SQL
        cursor.executescript(sql_script)
        
        connection.commit()
        print(f"    ✅ Base de datos configurada correctamente")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"    ❌ Error al configurar base de datos: {e}")
        if 'connection' in locals() and connection:
            connection.close()
        return False


def start_application():
    """Inicia la aplicación principal"""
    print_step(4, 4, "Iniciando aplicación...\n")
    
    try:
        print("="*60)
        print("✨ ¡Sistema listo! Abriendo interfaz gráfica...")
        print("="*60 + "\n")
        
        time.sleep(1)
        
        # Importar componentes de la aplicación
        import tkinter as tk
        import customtkinter as ctk
        from tkinter import messagebox
        from views.login_view import LoginView
        from views.admin_view import AdminView
        from views.manager_view import ManagerView
        from views.employee_view import EmployeeView
        
        class AplicacionRH:
            """Clase principal de la aplicación"""
            
            def __init__(self):
                """Inicializa la aplicación"""
                ctk.set_appearance_mode('dark')
                ctk.set_default_color_theme('blue')
                self.root = ctk.CTk()
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
