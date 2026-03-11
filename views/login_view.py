"""
Vista de inicio de sesión
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import config
from controllers.auth_controller import AuthController
from utils.validators import Validators
from utils.ui_helpers import UIHelpers
from utils.i18n import I18n


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
        self.root.configure()
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame,
            text=config.APP_CONFIG['nombre_empresa'].upper(),
            font=('Arial', 28, 'bold'),
            text_color=config.COLORS['primary']
        )
        titulo.pack(pady=(10, 2))
        
        subtitulo = ctk.CTkLabel(
            main_frame,
            text=I18n.get('login_subtitle'),
            font=('Arial', 14))
        subtitulo.pack(pady=(0, 15))
        
        # Opciones Superiores (Tema e Idioma)
        top_opts_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_opts_frame.pack(fill=tk.X, padx=10)
        
        # Selector de Tema
        tema_label = ctk.CTkLabel(top_opts_frame, text=I18n.get('theme'))
        tema_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.tema_var = ctk.StringVar(value="Dark")
        tema_combo = ctk.CTkComboBox(
            top_opts_frame, 
            values=["Light", "Dark", "System"],
            variable=self.tema_var,
            command=self.cambiar_tema,
            width=90, height=28
        )
        tema_combo.pack(side=tk.LEFT, padx=(0, 15))
        ctk.set_appearance_mode(self.tema_var.get())
        
        # Selector de Idioma
        lang_label = ctk.CTkLabel(top_opts_frame, text=I18n.get('lang'))
        lang_label.pack(side=tk.LEFT, padx=(0, 5))
        self.lang_var = ctk.StringVar(value=I18n._current_lang.upper())
        lang_combo = ctk.CTkComboBox(
            top_opts_frame, 
            values=["ES", "EN"],
            variable=self.lang_var,
            command=self.cambiar_idioma,
            width=70, height=28
        )
        lang_combo.pack(side=tk.LEFT)
        
        # Frame de formulario
        form_frame = UIHelpers.crear_frame_con_titulo(main_frame, I18n.get('login_title'))
        form_frame.pack(pady=15, fill=tk.BOTH, expand=True)
        
        # Campos
        self.correo_entry = UIHelpers.crear_label_entry(form_frame, I18n.get('email'), 0)
        self.password_entry = UIHelpers.crear_label_entry(form_frame, I18n.get('password'), 1, is_password=True)
        
        # Botones
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        UIHelpers.crear_boton(
            btn_frame,
            I18n.get('login_btn'),
            self.iniciar_sesion,
            config.COLORS['success']
        ).pack(side=tk.LEFT, padx=5)
        
        # Verificar si el registro está habilitado
        if AuthController.verificar_registro_habilitado():
            UIHelpers.crear_boton(
                btn_frame,
                I18n.get('register_btn'),
                self.ir_a_registro,
                config.COLORS['info']
            ).pack(side=tk.LEFT, padx=5)
        
        UIHelpers.crear_boton(
            btn_frame,
            I18n.get('exit_btn'),
            self.root.quit,
            config.COLORS['danger']
        ).pack(side=tk.LEFT, padx=5)
        
        # Versión
        version = ctk.CTkLabel(
            main_frame,
            text=f"{I18n.get('version')} {config.APP_CONFIG['version']}",
            font=('Arial', 8))
        version.pack(side=tk.BOTTOM, pady=5)
    
    def iniciar_sesion(self):
        """Maneja el inicio de sesión"""
        correo = self.correo_entry.get().strip()
        password = self.password_entry.get()
        
        # Validar campos vacíos
        if not correo or not password:
            UIHelpers.mostrar_error(I18n.get('error'), I18n.get('error_empty_fields'))
            return
        
        # Validar formato de correo
        valido, mensaje = Validators.validar_correo(correo)
        if not valido:
            UIHelpers.mostrar_error(I18n.get('error'), mensaje)
            return
        
        # Intentar inicio de sesión
        usuario, mensaje = AuthController.iniciar_sesion(correo, password)
        
        if usuario:
            UIHelpers.mostrar_info(I18n.get('success'), f"{I18n.get('welcome')} {usuario['nombre_empleado']} {usuario['apellido_empleado']}")
            self.on_login_success(usuario)
        else:
            UIHelpers.mostrar_error(I18n.get('error'), mensaje)
    
    def ir_a_registro(self):
        """Navega a la vista de registro"""
        from views.register_view import RegisterView
        RegisterView(self.root, lambda: self.setup_ui())

    def cambiar_tema(self, nuevo_tema):
        """Cambia el tema de claro a oscuro o sistema"""
        ctk.set_appearance_mode(nuevo_tema)
        
    def cambiar_idioma(self, nuevo_idioma):
        """Cambia el idioma de la aplicación y recarga la UI"""
        I18n.set_language(nuevo_idioma.lower())
        self.setup_ui()
