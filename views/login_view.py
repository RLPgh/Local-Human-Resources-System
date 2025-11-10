"""
Vista de inicio de sesión
"""

import tkinter as tk
from tkinter import ttk
import config
from controllers.auth_controller import AuthController
from utils.validators import Validators
from utils.ui_helpers import UIHelpers


class LoginView:
    """Vista para el inicio de sesión"""
    
    def __init__(self, root, on_login_success):
        """
        Inicializa la vista de login
        
        Args:
            root: Ventana principal
            on_login_success: Callback cuando el login es exitoso
        """
        self.root = root
        self.on_login_success = on_login_success
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.root.title(f"{config.APP_CONFIG['titulo_app']} - Inicio de Sesión")
        UIHelpers.centrar_ventana(self.root, 500, 400)
        self.root.configure(bg=config.COLORS['light'])
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=config.COLORS['light'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text=config.APP_CONFIG['nombre_empresa'].upper(),
            font=('Arial', 24, 'bold'),
            bg=config.COLORS['light'],
            fg=config.COLORS['primary']
        )
        titulo.pack(pady=10)
        
        subtitulo = tk.Label(
            main_frame,
            text="Sistema de Gestión Empresarial",
            font=('Arial', 12),
            bg=config.COLORS['light'],
            fg=config.COLORS['text']
        )
        subtitulo.pack(pady=5)
        
        # Frame de formulario
        form_frame = UIHelpers.crear_frame_con_titulo(main_frame, "Iniciar Sesión")
        form_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Campos
        self.correo_entry = UIHelpers.crear_label_entry(form_frame, "Correo:", 0)
        self.password_entry = UIHelpers.crear_label_entry(form_frame, "Contraseña:", 1, is_password=True)
        
        # Botones
        btn_frame = tk.Frame(form_frame, bg=config.COLORS['white'])
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        UIHelpers.crear_boton(
            btn_frame,
            "Iniciar Sesión",
            self.iniciar_sesion,
            config.COLORS['success']
        ).pack(side=tk.LEFT, padx=5)
        
        # Verificar si el registro está habilitado
        if AuthController.verificar_registro_habilitado():
            UIHelpers.crear_boton(
                btn_frame,
                "Registrarse",
                self.ir_a_registro,
                config.COLORS['info']
            ).pack(side=tk.LEFT, padx=5)
        
        UIHelpers.crear_boton(
            btn_frame,
            "Salir",
            self.root.quit,
            config.COLORS['danger']
        ).pack(side=tk.LEFT, padx=5)
        
        # Versión
        version = tk.Label(
            main_frame,
            text=f"Versión {config.APP_CONFIG['version']}",
            font=('Arial', 8),
            bg=config.COLORS['light'],
            fg=config.COLORS['text']
        )
        version.pack(side=tk.BOTTOM, pady=5)
    
    def iniciar_sesion(self):
        """Maneja el inicio de sesión"""
        correo = self.correo_entry.get().strip()
        password = self.password_entry.get()
        
        # Validar campos vacíos
        if not correo or not password:
            UIHelpers.mostrar_error("Error", "Por favor complete todos los campos")
            return
        
        # Validar formato de correo
        valido, mensaje = Validators.validar_correo(correo)
        if not valido:
            UIHelpers.mostrar_error("Error", mensaje)
            return
        
        # Intentar inicio de sesión
        usuario, mensaje = AuthController.iniciar_sesion(correo, password)
        
        if usuario:
            UIHelpers.mostrar_info("Éxito", f"Bienvenido {usuario['nombre_empleado']} {usuario['apellido_empleado']}")
            self.on_login_success(usuario)
        else:
            UIHelpers.mostrar_error("Error", mensaje)
    
    def ir_a_registro(self):
        """Navega a la vista de registro"""
        from views.register_view import RegisterView
        RegisterView(self.root, lambda: self.setup_ui())
