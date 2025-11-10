"""
Vista principal para empleados
"""

import tkinter as tk
from tkinter import ttk
from datetime import date
import config
from controllers.time_record_controller import TimeRecordController
from controllers.project_controller import ProjectController
from utils.validators import Validators
from utils.ui_helpers import UIHelpers


class EmployeeView:
    """Vista principal para empleados"""
    
    def __init__(self, root, usuario, on_logout):
        """
        Inicializa la vista de empleado
        
        Args:
            root: Ventana principal
            usuario: Datos del usuario actual
            on_logout: Callback para cerrar sesión
        """
        self.root = root
        self.usuario = usuario
        self.on_logout = on_logout
        self.time_controller = TimeRecordController(usuario)
        self.project_controller = ProjectController(usuario)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.root.title(f"{config.APP_CONFIG['titulo_app']} - Empleado")
        UIHelpers.centrar_ventana(self.root, 900, 600)
        self.root.configure(bg=config.COLORS['light'])
        
        # Frame superior con información del usuario
        header_frame = tk.Frame(self.root, bg=config.COLORS['primary'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        nombre_completo = f"{self.usuario['nombre_empleado']} {self.usuario['apellido_empleado']}"
        tk.Label(
            header_frame,
            text=f"Bienvenido: {nombre_completo}",
            font=('Arial', 14, 'bold'),
            bg=config.COLORS['primary'],
            fg=config.COLORS['white']
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(
            header_frame,
            text=f"Rol: Empleado",
            font=('Arial', 10),
            bg=config.COLORS['primary'],
            fg=config.COLORS['white']
        ).pack(side=tk.LEFT, padx=10)
        
        UIHelpers.crear_boton(
            header_frame,
            "Cerrar Sesión",
            self.on_logout,
            config.COLORS['danger']
        ).pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Frame principal con tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Registrar tiempo
        self.tab_registrar = tk.Frame(notebook, bg=config.COLORS['white'])
        notebook.add(self.tab_registrar, text="Registrar Tiempo")
        self.crear_tab_registrar_tiempo()
        
        # Tab 2: Mis registros
        self.tab_registros = tk.Frame(notebook, bg=config.COLORS['white'])
        notebook.add(self.tab_registros, text="Mis Registros")
        self.crear_tab_mis_registros()
        
        # Tab 3: Mis proyectos
        self.tab_proyectos = tk.Frame(notebook, bg=config.COLORS['white'])
        notebook.add(self.tab_proyectos, text="Mis Proyectos")
        self.crear_tab_mis_proyectos()
    
    def crear_tab_registrar_tiempo(self):
        """Crea el tab para registrar tiempo"""
        form_frame = UIHelpers.crear_frame_con_titulo(self.tab_registrar, "Registrar Tiempo Trabajado")
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH)
        
        # Fecha
        ttk.Label(form_frame, text="Fecha:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        fecha_frame = tk.Frame(form_frame)
        fecha_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.fecha_entry = ttk.Entry(fecha_frame, width=15)
        self.fecha_entry.pack(side=tk.LEFT)
        self.fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        ttk.Label(fecha_frame, text="(YYYY-MM-DD)").pack(side=tk.LEFT, padx=5)
        
        # Horas
        self.horas_entry = UIHelpers.crear_label_entry(form_frame, "Horas:", 1, width=10)
        
        # Proyecto (opcional)
        ttk.Label(form_frame, text="Proyecto (opcional):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.proyecto_var = tk.StringVar(value="")
        self.proyecto_combo = ttk.Combobox(form_frame, textvariable=self.proyecto_var, state="readonly", width=27)
        self.proyecto_combo.grid(row=2, column=1, padx=5, pady=5)
        self.cargar_proyectos()
        
        # Descripción
        ttk.Label(form_frame, text="Descripción:").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        self.descripcion_text = tk.Text(form_frame, width=30, height=5)
        self.descripcion_text.grid(row=3, column=1, padx=5, pady=5)
        
        # Botón
        UIHelpers.crear_boton(
            form_frame,
            "Registrar Tiempo",
            self.registrar_tiempo,
            config.COLORS['success'],
            row=4,
            column=0,
            columnspan=2
        )
    
    def crear_tab_mis_registros(self):
        """Crea el tab de mis registros"""
        # Botón actualizar
        btn_frame = tk.Frame(self.tab_registros, bg=config.COLORS['white'])
        btn_frame.pack(pady=10)
        
        UIHelpers.crear_boton(
            btn_frame,
            "Actualizar",
            self.cargar_registros,
            config.COLORS['info']
        ).pack()
        
        # Tabla
        columnas = [
            ('fecha', 'Fecha', 100),
            ('horas', 'Horas', 80),
            ('descripcion', 'Descripción', 250),
            ('proyecto', 'Proyecto', 150),
            ('departamento', 'Departamento', 150)
        ]
        self.tabla_registros, _ = UIHelpers.crear_tabla(self.tab_registros, columnas, altura=15)
        self.cargar_registros()
    
    def crear_tab_mis_proyectos(self):
        """Crea el tab de mis proyectos"""
        # Botón actualizar
        btn_frame = tk.Frame(self.tab_proyectos, bg=config.COLORS['white'])
        btn_frame.pack(pady=10)
        
        UIHelpers.crear_boton(
            btn_frame,
            "Actualizar",
            self.cargar_mis_proyectos,
            config.COLORS['info']
        ).pack()
        
        # Tabla
        columnas = [
            ('id', 'ID', 80),
            ('nombre', 'Nombre Proyecto', 300),
            ('fecha_asignacion', 'Fecha Asignación', 150)
        ]
        self.tabla_proyectos, _ = UIHelpers.crear_tabla(self.tab_proyectos, columnas, altura=15)
        self.cargar_mis_proyectos()
    
    def cargar_proyectos(self):
        """Carga los proyectos del empleado en el combobox"""
        proyectos, _ = self.project_controller.obtener_proyectos_empleado(self.usuario['id_empleado'])
        
        opciones = ["Sin proyecto"]
        self.proyecto_map = {}
        
        if proyectos:
            for p in proyectos:
                opciones.append(p['nombre_proyecto'])
                self.proyecto_map[p['nombre_proyecto']] = p['id_proyecto']
        
        self.proyecto_combo['values'] = opciones
        self.proyecto_combo.current(0)
    
    def registrar_tiempo(self):
        """Registra el tiempo trabajado"""
        fecha = self.fecha_entry.get().strip()
        horas = self.horas_entry.get().strip()
        descripcion = self.descripcion_text.get("1.0", tk.END).strip()
        proyecto_nombre = self.proyecto_var.get()
        
        # Validaciones
        valido, mensaje = Validators.validar_fecha(fecha)
        if not valido:
            UIHelpers.mostrar_error("Error", mensaje)
            return
        
        valido, mensaje = Validators.validar_horas(horas)
        if not valido:
            UIHelpers.mostrar_error("Error", mensaje)
            return
        
        if not descripcion:
            UIHelpers.mostrar_error("Error", "Debe ingresar una descripción")
            return
        
        # Obtener ID del proyecto si se seleccionó
        id_proyecto = None
        if proyecto_nombre != "Sin proyecto":
            id_proyecto = self.proyecto_map.get(proyecto_nombre)
        
        # Registrar
        exito, mensaje = self.time_controller.registrar_tiempo(
            fecha, float(horas), descripcion, id_proyecto
        )
        
        if exito:
            UIHelpers.mostrar_info("Éxito", mensaje)
            # Limpiar formulario
            self.horas_entry.delete(0, tk.END)
            self.descripcion_text.delete("1.0", tk.END)
            self.fecha_entry.delete(0, tk.END)
            self.fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))
            self.proyecto_combo.current(0)
            self.cargar_registros()
        else:
            UIHelpers.mostrar_error("Error", mensaje)
    
    def cargar_registros(self):
        """Carga los registros de tiempo en la tabla"""
        # Limpiar tabla
        for item in self.tabla_registros.get_children():
            self.tabla_registros.delete(item)
        
        # Obtener registros
        registros, _ = self.time_controller.obtener_mis_tiempos()
        
        if registros:
            for r in registros:
                self.tabla_registros.insert('', tk.END, values=(
                    r.get('fecha_rt', ''),
                    r.get('tiempo_rt_horas', ''),
                    r.get('descripcion_tareas', '')[:50] + '...' if len(r.get('descripcion_tareas', '')) > 50 else r.get('descripcion_tareas', ''),
                    r.get('nombre_proyecto', 'Sin proyecto'),
                    r.get('nombre_dep', 'Sin departamento')
                ))
    
    def cargar_mis_proyectos(self):
        """Carga los proyectos en la tabla"""
        # Limpiar tabla
        for item in self.tabla_proyectos.get_children():
            self.tabla_proyectos.delete(item)
        
        # Obtener proyectos
        proyectos, _ = self.project_controller.obtener_proyectos_empleado(self.usuario['id_empleado'])
        
        if proyectos:
            for p in proyectos:
                self.tabla_proyectos.insert('', tk.END, values=(
                    p.get('id_proyecto', ''),
                    p.get('nombre_proyecto', ''),
                    p.get('fecha_asignacion', '')
                ))
