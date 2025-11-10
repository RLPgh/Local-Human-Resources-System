"""
Vista de registro de usuarios
"""

import tkinter as tk
from tkinter import ttk
from datetime import date
import config
from controllers.auth_controller import AuthController
from controllers.employee_controller import EmployeeController
from models.employee import Employee
from utils.validators import Validators
from utils.ui_helpers import UIHelpers


class RegisterView:
    """Vista para el registro de nuevos usuarios"""
    
    def __init__(self, root, on_back):
        """
        Inicializa la vista de registro
        
        Args:
            root: Ventana principal
            on_back: Callback para volver atrás
        """
        self.root = root
        self.on_back = on_back
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.root.title(f"{config.APP_CONFIG['titulo_app']} - Registro")
        UIHelpers.centrar_ventana(self.root, 600, 700)
        self.root.configure(bg=config.COLORS['light'])
        
        # Frame principal con scrollbar
        canvas = tk.Canvas(self.root, bg=config.COLORS['light'])
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=config.COLORS['light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        titulo = tk.Label(
            scrollable_frame,
            text="Registro de Nuevo Usuario",
            font=('Arial', 18, 'bold'),
            bg=config.COLORS['light'],
            fg=config.COLORS['primary']
        )
        titulo.pack(pady=10)
        
        # Frame de formulario
        form_frame = UIHelpers.crear_frame_con_titulo(scrollable_frame, "Información Personal")
        form_frame.pack(pady=10, padx=20, fill=tk.BOTH)
        
        # Campos
        self.nombre_entry = UIHelpers.crear_label_entry(form_frame, "Nombre:", 0)
        self.apellido_entry = UIHelpers.crear_label_entry(form_frame, "Apellido:", 1)
        self.edad_entry = UIHelpers.crear_label_entry(form_frame, "Edad:", 2)
        self.direccion_entry = UIHelpers.crear_label_entry(form_frame, "Dirección:", 3)
        self.telefono_entry = UIHelpers.crear_label_entry(form_frame, "Teléfono:", 4)
        self.correo_entry = UIHelpers.crear_label_entry(form_frame, "Correo:", 5)
        
        # Frame de datos laborales
        labor_frame = UIHelpers.crear_frame_con_titulo(scrollable_frame, "Información Laboral")
        labor_frame.pack(pady=10, padx=20, fill=tk.BOTH)
        
        # Fecha de contrato
        ttk.Label(labor_frame, text="Fecha de Contrato:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        fecha_frame = tk.Frame(labor_frame)
        fecha_frame.grid(row=0, column=1, padx=5, pady=5)
        
        self.fecha_entry = ttk.Entry(fecha_frame, width=15)
        self.fecha_entry.pack(side=tk.LEFT)
        self.fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        
        ttk.Label(fecha_frame, text="(YYYY-MM-DD)").pack(side=tk.LEFT, padx=5)
        
        # Salario
        self.salario_entry = UIHelpers.crear_label_entry(labor_frame, "Salario:", 1)
        
        # Rol
        ttk.Label(labor_frame, text="Rol:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.rol_var = tk.StringVar(value="102")
        
        roles_frame = tk.Frame(labor_frame)
        roles_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Radiobutton(roles_frame, text="Empleado", variable=self.rol_var, value="102").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(roles_frame, text="Gerente", variable=self.rol_var, value="101").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(roles_frame, text="Admin RH", variable=self.rol_var, value="100").pack(side=tk.LEFT, padx=5)
        
        # Frame de seguridad
        security_frame = UIHelpers.crear_frame_con_titulo(scrollable_frame, "Seguridad")
        security_frame.pack(pady=10, padx=20, fill=tk.BOTH)
        
        self.password_entry = UIHelpers.crear_label_entry(security_frame, "Contraseña:", 0, is_password=True)
        self.password2_entry = UIHelpers.crear_label_entry(security_frame, "Confirmar Contraseña:", 1, is_password=True)
        
        # Botones
        btn_frame = tk.Frame(scrollable_frame, bg=config.COLORS['light'])
        btn_frame.pack(pady=20)
        
        UIHelpers.crear_boton(
            btn_frame,
            "Registrarse",
            self.registrar_usuario,
            config.COLORS['success']
        ).pack(side=tk.LEFT, padx=5)
        
        UIHelpers.crear_boton(
            btn_frame,
            "Volver",
            self.on_back,
            config.COLORS['secondary']
        ).pack(side=tk.LEFT, padx=5)
    
    def registrar_usuario(self):
        """Maneja el registro de usuario"""
        # Obtener datos
        nombre = self.nombre_entry.get().strip()
        apellido = self.apellido_entry.get().strip()
        edad = self.edad_entry.get().strip()
        direccion = self.direccion_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        correo = self.correo_entry.get().strip()
        fecha_contrato = self.fecha_entry.get().strip()
        salario = self.salario_entry.get().strip()
        id_rol = int(self.rol_var.get())
        password = self.password_entry.get()
        password2 = self.password2_entry.get()
        
        # Validaciones
        validaciones = [
            (Validators.validar_string(nombre, "Nombre"), nombre),
            (Validators.validar_string(apellido, "Apellido"), apellido),
            (Validators.validar_edad(edad), edad),
            (Validators.validar_direccion(direccion), direccion),
            (Validators.validar_telefono(telefono), telefono),
            (Validators.validar_correo(correo), correo),
            (Validators.validar_fecha(fecha_contrato), fecha_contrato),
            (Validators.validar_salario(salario), salario),
            (Validators.validar_contraseña(password), password)
        ]
        
        for validacion, valor in validaciones:
            valido, mensaje = validacion
            if not valido:
                UIHelpers.mostrar_error("Error de validación", mensaje)
                return
        
        # Verificar que las contraseñas coincidan
        if password != password2:
            UIHelpers.mostrar_error("Error", "Las contraseñas no coinciden")
            return
        
        # Verificar que el correo no esté registrado
        if Employee.correo_existe(correo):
            UIHelpers.mostrar_error("Error", "El correo ya está registrado")
            return
        
        # Crear empleado
        id_empleado = Employee.crear(
            nombre, apellido, int(edad), direccion, telefono,
            correo, fecha_contrato, float(salario), id_rol
        )
        
        if not id_empleado:
            UIHelpers.mostrar_error("Error", "No se pudo crear el empleado")
            return
        
        # Crear usuario
        id_usuario, mensaje = AuthController.registrar_usuario(id_empleado, password, id_rol)
        
        if id_usuario:
            UIHelpers.mostrar_info(
                "Éxito",
                f"Usuario registrado exitosamente\nID Empleado: {id_empleado}\nPuede iniciar sesión ahora"
            )
            self.on_back()
        else:
            UIHelpers.mostrar_error("Error", mensaje)
