"""
Vista principal para Administrador RH
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from datetime import date
import config
from controllers.employee_controller import EmployeeController
from controllers.project_controller import ProjectController
from controllers.report_controller import ReportController
from controllers.auth_controller import AuthController
from utils.validators import Validators
from utils.ui_helpers import UIHelpers
from utils.data_generator import DataGenerator
from views.analytics_view import AnalyticsView


class AdminView:
    """Vista principal para Administrador RH"""
    
    def __init__(self, root, usuario, on_logout):
        self.root = root
        self.usuario = usuario
        self.on_logout = on_logout
        self.employee_controller = EmployeeController(usuario)
        self.project_controller = ProjectController(usuario)
        self.report_controller = ReportController(usuario)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"{config.APP_CONFIG['titulo_app']} - Administrador RH")
        UIHelpers.centrar_ventana(self.root, 1100, 700)
        self.root.configure()
        
        # Header
        header_frame = ctk.CTkFrame(self.root, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        nombre_completo = f"{self.usuario['nombre_empleado']} {self.usuario['apellido_empleado']}"
        ctk.CTkLabel(
            header_frame,
            text=f"Admin RH: {nombre_completo}",
            font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Botón de Configuración de Registro
        self.btn_toggle_registro = UIHelpers.crear_boton(
            header_frame,
            "Ajustes de Registro Público",
            self.abrir_configuracion_registro,
            config.COLORS['warning']
        )
        self.btn_toggle_registro.pack(side=tk.RIGHT, padx=10, pady=10)
        
        UIHelpers.crear_boton(
            header_frame,
            "Cerrar Sesión",
            self.on_logout,
            config.COLORS['danger']
        ).pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Notebook nativo CTkTabview para correcta compatibilidad de tema oscuro/claro
        notebook = ctk.CTkTabview(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabs
        notebook.add("Gestionar Empleados")
        self.tab_empleados = notebook.tab("Gestionar Empleados")
        self.crear_tab_empleados()
        
        notebook.add("Gestionar Proyectos")
        self.tab_proyectos = notebook.tab("Gestionar Proyectos")
        self.crear_tab_proyectos()
        
        notebook.add("Asignaciones")
        self.tab_asignaciones = notebook.tab("Asignaciones")
        self.crear_tab_asignaciones()
        
        notebook.add("Informes")
        self.tab_informes = notebook.tab("Informes")
        self.crear_tab_informes()
    
    def abrir_configuracion_registro(self):
        """Abre panel para configuración granular de roles de registro publico"""
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Configuración de Registro")
        UIHelpers.centrar_ventana(ventana, 400, 350)
        ventana.transient(self.root)
        ventana.grab_set()
        
        frame = UIHelpers.crear_frame_con_titulo(ventana, "Acceso Público")
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Switch General
        self.switch_var = ctk.BooleanVar(value=AuthController.verificar_registro_habilitado())
        ctk.CTkSwitch(
            frame, text="Habilitar Portal de Registro",
            variable=self.switch_var
        ).pack(pady=10, padx=20, anchor="w")
        
        # Opciones de Roles
        ctk.CTkLabel(frame, text="Roles Permitidos para Nuevos Usuarios:", font=('Arial', 12, 'bold')).pack(pady=(10, 5), anchor="w", padx=20)
        
        roles_actuales = AuthController.obtener_roles_permitidos()
        self.check_vars = {}
        
        for id_rol, nombre_rol in config.ROLES.items():
            var = ctk.BooleanVar(value=(id_rol in roles_actuales))
            self.check_vars[id_rol] = var
            ctk.CTkCheckBox(
                frame, text=nombre_rol, variable=var
            ).pack(pady=5, padx=30, anchor="w")
            
        def guardar_configs():
            # Extraer elegidos
            roles_elegidos = [r_id for r_id, var in self.check_vars.items() if var.get()]
            
            if self.switch_var.get() and not roles_elegidos:
                UIHelpers.mostrar_error("Error", "Debe seleccionar al menos un rol si el registro está activado.")
                return
                
            AuthController.cambiar_estado_registro(self.switch_var.get())
            AuthController.actualizar_roles_permitidos(roles_elegidos)
            
            UIHelpers.mostrar_info("Éxito", "Restricciones de registro actualizadas.")
            ventana.destroy()
            
        UIHelpers.crear_boton(frame, "Guardar Cambios", guardar_configs, config.COLORS['success']).pack(pady=20)
    
    def crear_tab_empleados(self):
        """Crea el tab de gestión de empleados"""
        # Botones superiores
        btn_frame = ctk.CTkFrame(self.tab_empleados)
        btn_frame.pack(pady=10)
        
        UIHelpers.crear_boton(btn_frame, "Actualizar", self.cargar_empleados, config.COLORS['info']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Nuevo Empleado", self.nuevo_empleado, config.COLORS['success']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Editar", self.editar_empleado, config.COLORS['warning']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Eliminar", self.eliminar_empleado, config.COLORS['danger']).pack(side=tk.LEFT, padx=5)
        
        # Tabla
        columnas = [
            ('id', 'ID', 60),
            ('nombre', 'Nombre', 120),
            ('apellido', 'Apellido', 120),
            ('edad', 'Edad', 50),
            ('telefono', 'Teléfono', 100),
            ('correo', 'Correo', 180),
            ('salario', 'Salario', 100),
            ('rol', 'Rol', 120)
        ]
        self.tabla_empleados, _ = UIHelpers.crear_tabla(self.tab_empleados, columnas, altura=20)
        self.cargar_empleados()
    
    def crear_tab_proyectos(self):
        """Crea el tab de gestión de proyectos"""
        btn_frame = ctk.CTkFrame(self.tab_proyectos)
        btn_frame.pack(pady=10)
        
        UIHelpers.crear_boton(btn_frame, "Actualizar", self.cargar_proyectos, config.COLORS['info']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Nuevo Proyecto", self.nuevo_proyecto, config.COLORS['success']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Editar", self.editar_proyecto, config.COLORS['warning']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Eliminar", self.eliminar_proyecto, config.COLORS['danger']).pack(side=tk.LEFT, padx=5)
        
        columnas = [
            ('id', 'ID', 80),
            ('nombre', 'Nombre', 300),
            ('descripcion', 'Descripción', 400),
            ('fecha', 'Fecha Inicio', 120)
        ]
        self.tabla_proyectos, _ = UIHelpers.crear_tabla(self.tab_proyectos, columnas, altura=20)
        self.cargar_proyectos()
    
    def crear_tab_asignaciones(self):
        """Crea el tab de asignaciones"""
        btn_frame = ctk.CTkFrame(self.tab_asignaciones)
        btn_frame.pack(pady=10)
        
        UIHelpers.crear_boton(btn_frame, "Actualizar", self.cargar_asignaciones, config.COLORS['info']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Asignar Proyecto", self.asignar_proyecto, config.COLORS['success']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Desasignar", self.desasignar_proyecto, config.COLORS['danger']).pack(side=tk.LEFT, padx=5)
        
        columnas = [
            ('id_emp', 'ID Emp', 70),
            ('nombre_emp', 'Empleado', 200),
            ('id_proy', 'ID Proy', 70),
            ('nombre_proy', 'Proyecto', 250),
            ('fecha', 'Fecha Asignación', 120)
        ]
        self.tabla_asignaciones, _ = UIHelpers.crear_tabla(self.tab_asignaciones, columnas, altura=20)
        self.cargar_asignaciones()
    
    def crear_tab_informes(self):
        """Crea el tab de informes"""
        btn_frame = ctk.CTkFrame(self.tab_informes)
        btn_frame.pack(pady=20)
        
        UIHelpers.crear_boton(btn_frame, "Empleados por Departamento", lambda: self.generar_informe('departamento'), config.COLORS['info']).pack(pady=5)
        UIHelpers.crear_boton(btn_frame, "Empleados por Proyecto", lambda: self.generar_informe('proyecto'), config.COLORS['info']).pack(pady=5)
        UIHelpers.crear_boton(btn_frame, "Todos los Empleados", lambda: self.generar_informe('todos'), config.COLORS['info']).pack(pady=5)
        
        ctk.CTkLabel(btn_frame, text="Herramientas Avanzadas", font=('Arial', 12, 'bold')).pack(pady=(15, 5))
        UIHelpers.crear_boton(btn_frame, "Ver Analíticas (Gráficos)", self.abrir_analiticas, config.COLORS['primary']).pack(pady=5)
        
        datos_btn_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
        datos_btn_frame.pack(pady=5)
        UIHelpers.crear_boton(datos_btn_frame, "Generar Datos de Prueba Sintéticos", self.generar_datos_prueba, config.COLORS['warning']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(datos_btn_frame, "Limpiar Datos", self.limpiar_datos_prueba, config.COLORS['danger']).pack(side=tk.LEFT, padx=5)
        
    def abrir_analiticas(self):
        """Abre la ventana de analíticas"""
        AnalyticsView(self.root)
        
    def generar_datos_prueba(self):
        """Genera datos sintéticos con confirmación y salvaguarda contra duplicados"""
        # Chequeo preventivo de si ya existen departamentos gringos o latinos
        from models.database import Database
        q = "SELECT COUNT(*) as c FROM departamentos WHERE nombre_dep IN ('Tecnología', 'Technology')"
        res = Database.execute_query(q, fetchone=True)
        if res and res['c'] > 0:
            UIHelpers.mostrar_error("Bloqueo", "Los datos de prueba ya existen en la base de datos.\nSi deseas regenerarlos, debes presionar 'Limpiar Datos' primero.")
            return

        if UIHelpers.confirmar("Advertencia", "Esto insertará múltiples registros hipotéticos.\n¿Desea continuar?"):
            DataGenerator.generar_datos_prueba()
            UIHelpers.mostrar_info("Éxito", "Datos de prueba generados correctamente.")
            self.cargar_empleados()
            self.cargar_proyectos()
            self.cargar_asignaciones()
            
    def limpiar_datos_prueba(self):
        """Limpia los datos generados por el DataGenerator"""
        if UIHelpers.confirmar("Limpieza Peligrosa", "Esta acción eliminará todos los Empleados cuyos correos contengan '@empresa.com' y Departamentos de prueba.\n¿Confirmar limpieza múltiple?"):
            from models.database import Database
            # Eliminar en cascada los empleados ficticios generados
            Database.execute_command("DELETE FROM empleados WHERE correo LIKE '%@empresa.com'")
            # Eliminar los departamentos ficticios (Inglés y Español)
            deptos_test = (
                'Recursos Humanos', 'Tecnología', 'Marketing', 'Ventas', 'Operaciones', 'Finanzas',
                'Human Resources', 'Technology', 'Sales', 'Finance'
            )
            placeholders = ', '.join(['?'] * len(deptos_test))
            Database.execute_command(f"DELETE FROM departamentos WHERE nombre_dep IN ({placeholders})", deptos_test)
            
            UIHelpers.mostrar_info("Limpieza", "Se expurgaron correctamente los datos sistéticos de la sesión.")
            self.cargar_empleados()
    
    def cargar_empleados(self):
        """Carga empleados en la tabla"""
        for item in self.tabla_empleados.get_children():
            self.tabla_empleados.delete(item)
        
        empleados, _ = self.employee_controller.obtener_todos_empleados()
        if empleados:
            for e in empleados:
                self.tabla_empleados.insert('', tk.END, values=(
                    e.get('id_empleado', ''),
                    e.get('nombre_empleado', ''),
                    e.get('apellido_empleado', ''),
                    e.get('edad', ''),
                    e.get('telefono', ''),
                    e.get('correo', ''),
                    e.get('salario', ''),
                    e.get('nombre_rol', '')
                ))
    
    def nuevo_empleado(self):
        """Abre ventana para crear empleado"""
        self.ventana_empleado(None)
    
    def editar_empleado(self):
        """Abre ventana para editar empleado"""
        seleccion = self.tabla_empleados.selection()
        if not seleccion:
            UIHelpers.mostrar_advertencia("Advertencia", "Seleccione un empleado")
            return
        
        valores = self.tabla_empleados.item(seleccion[0])['values']
        self.ventana_empleado(valores[0])  # ID
    
    def eliminar_empleado(self):
        """Elimina uno o múltiples empleados seleccionados"""
        selecciones = self.tabla_empleados.selection()
        if not selecciones:
            UIHelpers.mostrar_advertencia("Advertencia", "Seleccione al menos un empleado para eliminar")
            return
            
        nombres_lista = []
        ids_lista = []
        
        for item in selecciones:
            valores = self.tabla_empleados.item(item)['values']
            ids_lista.append(valores[0])
            nombres_lista.append(f"{valores[1]} {valores[2]}")
            
        lista_txt = ", ".join(nombres_lista[:3]) + ("..." if len(nombres_lista) > 3 else "")
        mensaje = f"¿Eliminar los {len(selecciones)} empleado(s) seleccionado(s) ({lista_txt})?"
        
        if UIHelpers.confirmar("Confirmación Masiva", mensaje):
            exitos = 0
            for id_empleado in ids_lista:
                exito, _ = self.employee_controller.eliminar_empleado(id_empleado)
                if exito:
                    exitos += 1
                    
            UIHelpers.mostrar_info("Completado", f"Se eliminaron {exitos} de {len(ids_lista)} registros.")
            self.cargar_empleados()
    
    def ventana_empleado(self, id_empleado=None):
        """Ventana para crear/editar empleado"""
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Nuevo Empleado" if not id_empleado else "Editar Empleado")
        UIHelpers.centrar_ventana(ventana, 500, 650)
        ventana.transient(self.root)
        ventana.grab_set()
        
        frame = UIHelpers.crear_frame_con_titulo(ventana, "Datos del Empleado")
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Campos
        entries = {}
        entries['nombre'] = UIHelpers.crear_label_entry(frame, "Nombre:", 0)
        entries['apellido'] = UIHelpers.crear_label_entry(frame, "Apellido:", 1)
        entries['edad'] = UIHelpers.crear_label_entry(frame, "Edad:", 2)
        entries['direccion'] = UIHelpers.crear_label_entry(frame, "Dirección:", 3)
        entries['telefono'] = UIHelpers.crear_label_entry(frame, "Teléfono:", 4)
        entries['correo'] = UIHelpers.crear_label_entry(frame, "Correo:", 5)
        entries['salario'] = UIHelpers.crear_label_entry(frame, "Salario:", 6)
        
        # Rol (solo para nuevo empleado)
        ctk.CTkLabel(frame, text="Rol:").grid(row=7, column=0, sticky='e', padx=10, pady=5)
        rol_var = ctk.StringVar()
        rol_combo = ctk.CTkComboBox(frame, textvariable=rol_var, state='readonly', width=30)
        rol_combo['values'] = [f"{id_rol} - {nombre}" for id_rol, nombre in config.ROLES.items()]
        rol_combo.grid(row=7, column=1, sticky='w', padx=10, pady=5)
        
        # Contraseña (solo para nuevo empleado)
        if not id_empleado:
            entries['password'] = UIHelpers.crear_label_entry(frame, "Contraseña:", 8, show='*')
            entries['password2'] = UIHelpers.crear_label_entry(frame, "Confirmar Contraseña:", 9, show='*')
            rol_combo.set("102 - Empleado")  # Empleado por defecto nativo de CTk
        else:
            rol_combo.configure(state='disabled') # Fix de bug nativo AttributeError ctk
        
        
        # Llenar si es edición
        if id_empleado:
            empleado, _ = self.employee_controller.obtener_empleado(id_empleado)
            if empleado:
                entries['nombre'].insert(0, empleado['nombre_empleado'])
                entries['apellido'].insert(0, empleado['apellido_empleado'])
                entries['edad'].insert(0, empleado['edad'])
                entries['direccion'].insert(0, empleado['direccion'])
                entries['telefono'].insert(0, empleado['telefono'])
                entries['correo'].insert(0, empleado['correo'])
                entries['salario'].insert(0, empleado['salario'])
                # Mostrar rol actual
                rol_actual = empleado.get('fk_id_rol_e')
                for id_r, nombre in config.ROLES.items():
                    if id_r == rol_actual:
                        rol_combo.set(f"{id_r} - {nombre}")
                        break
        
        def guardar():
            datos = {k: v.get().strip() for k, v in entries.items() if k not in ['password', 'password2']}
            
            # Validar campos básicos
            if not all(datos.values()):
                UIHelpers.mostrar_error("Error", "Complete todos los campos")
                return
            
            # Validar edad
            try:
                edad = int(datos['edad'])
                if edad < 18 or edad > 100:
                    UIHelpers.mostrar_error("Error", "Edad debe estar entre 18 y 100")
                    return
            except ValueError:
                UIHelpers.mostrar_error("Error", "Edad debe ser un número")
                return
            
            # Validar salario
            try:
                salario = float(datos['salario'])
                if salario < 0:
                    UIHelpers.mostrar_error("Error", "Salario debe ser positivo")
                    return
            except ValueError:
                UIHelpers.mostrar_error("Error", "Salario debe ser un número")
                return
            
            if id_empleado:
                # Editar empleado existente
                exito, mensaje = self.employee_controller.actualizar_empleado(
                    id_empleado, datos['nombre'], datos['apellido'], edad,
                    datos['direccion'], datos['telefono'], datos['correo'], salario
                )
            else:
                # Crear nuevo empleado con usuario
                password = entries['password'].get().strip()
                password2 = entries['password2'].get().strip()
                
                if not password or not password2:
                    UIHelpers.mostrar_error("Error", "Ingrese la contraseña")
                    return
                
                if password != password2:
                    UIHelpers.mostrar_error("Error", "Las contraseñas no coinciden")
                    return
                
                if len(password) < 8:
                    UIHelpers.mostrar_error("Error", "La contraseña debe tener al menos 8 caracteres")
                    return
                
                # Obtener ID del rol seleccionado
                rol_seleccionado = rol_var.get().split(' - ')[0]
                id_rol = int(rol_seleccionado)
                
                # Crear empleado y usuario
                from datetime import date
                auth_controller = AuthController()
                exito, mensaje = auth_controller.registrar_usuario(
                    datos['nombre'], datos['apellido'], edad, datos['direccion'],
                    datos['telefono'], datos['correo'], password, id_rol,
                    date.today().isoformat(), salario
                )
            
            if exito:
                UIHelpers.mostrar_info("Éxito", mensaje)
                self.cargar_empleados()
                ventana.destroy()
            else:
                UIHelpers.mostrar_error("Error", mensaje)
        
        row_btn = 10 if not id_empleado else 8
        UIHelpers.crear_boton(frame, "Guardar", guardar, config.COLORS['success'], row=row_btn, column=0, columnspan=2)
    
    def cargar_proyectos(self):
        """Carga proyectos"""
        for item in self.tabla_proyectos.get_children():
            self.tabla_proyectos.delete(item)
        
        proyectos, _ = self.project_controller.obtener_todos_proyectos()
        if proyectos:
            for p in proyectos:
                desc = p.get('descripcion_p', '')[:50] + '...' if len(p.get('descripcion_p', '')) > 50 else p.get('descripcion_p', '')
                self.tabla_proyectos.insert('', tk.END, values=(
                    p.get('id_proyecto', ''),
                    p.get('nombre_proyecto', ''),
                    desc,
                    p.get('fecha_inicio_p', '')
                ))
    
    def nuevo_proyecto(self):
        """Crea nuevo proyecto"""
        self.ventana_proyecto(None)
    
    def editar_proyecto(self):
        """Edita proyecto"""
        seleccion = self.tabla_proyectos.selection()
        if not seleccion:
            UIHelpers.mostrar_advertencia("Advertencia", "Seleccione un proyecto")
            return
        
        valores = self.tabla_proyectos.item(seleccion[0])['values']
        self.ventana_proyecto(valores[0])
    
    def eliminar_proyecto(self):
        """Elimina proyecto"""
        seleccion = self.tabla_proyectos.selection()
        if not seleccion:
            UIHelpers.mostrar_advertencia("Advertencia", "Seleccione un proyecto")
            return
        
        valores = self.tabla_proyectos.item(seleccion[0])['values']
        if UIHelpers.confirmar("Confirmar", f"¿Eliminar proyecto {valores[1]}?"):
            exito, mensaje = self.project_controller.eliminar_proyecto(valores[0])
            if exito:
                UIHelpers.mostrar_info("Éxito", mensaje)
                self.cargar_proyectos()
            else:
                UIHelpers.mostrar_error("Error", mensaje)
    
    def ventana_proyecto(self, id_proyecto=None):
        """Ventana crear/editar proyecto"""
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Proyecto")
        UIHelpers.centrar_ventana(ventana, 500, 400)
        ventana.transient(self.root)
        ventana.grab_set()
        
        frame = UIHelpers.crear_frame_con_titulo(ventana, "Datos del Proyecto")
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        nombre_entry = UIHelpers.crear_label_entry(frame, "Nombre:", 0)
        
        ctk.CTkLabel(frame, text="Descripción:").grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        desc_text = tk.Text(frame, width=30, height=5)
        desc_text.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(frame, text="Fecha Inicio:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        fecha_entry = ctk.CTkEntry(frame, width=120, height=32)
        fecha_entry.grid(row=2, column=1, padx=5, pady=5)
        fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        
        if id_proyecto:
            proyecto, _ = self.project_controller.obtener_proyecto(id_proyecto)
            if proyecto:
                nombre_entry.insert(0, proyecto['nombre_proyecto'])
                desc_text.insert("1.0", proyecto['descripcion_p'] or '')
                fecha_entry.delete(0, tk.END)
                fecha_entry.insert(0, proyecto['fecha_inicio_p'])
        
        def guardar():
            nombre = nombre_entry.get().strip()
            descripcion = desc_text.get("1.0", tk.END).strip()
            fecha = fecha_entry.get().strip()
            
            if not nombre or not fecha:
                UIHelpers.mostrar_error("Error", "Complete los campos requeridos")
                return
            
            if id_proyecto:
                exito, mensaje = self.project_controller.actualizar_proyecto(id_proyecto, nombre, descripcion, fecha)
            else:
                id_nuevo, mensaje = self.project_controller.crear_proyecto(nombre, descripcion, fecha)
                exito = id_nuevo is not None
            
            if exito:
                UIHelpers.mostrar_info("Éxito", mensaje)
                self.cargar_proyectos()
                ventana.destroy()
            else:
                UIHelpers.mostrar_error("Error", mensaje)
        
        UIHelpers.crear_boton(frame, "Guardar", guardar, config.COLORS['success'], row=3, column=0, columnspan=2)
    
    def cargar_asignaciones(self):
        """Carga asignaciones"""
        for item in self.tabla_asignaciones.get_children():
            self.tabla_asignaciones.delete(item)
        
        asignaciones, _ = self.project_controller.obtener_asignaciones()
        if asignaciones:
            for a in asignaciones:
                self.tabla_asignaciones.insert('', tk.END, values=(
                    a.get('id_empleado', ''),
                    f"{a.get('nombre_empleado', '')} {a.get('apellido_empleado', '')}",
                    a.get('id_proyecto', ''),
                    a.get('nombre_proyecto', ''),
                    a.get('fecha_asignacion', '')
                ))
    
    def asignar_proyecto(self):
        """Asigna proyecto a empleado"""
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Asignar Proyecto")
        UIHelpers.centrar_ventana(ventana, 400, 250)
        ventana.transient(self.root)
        ventana.grab_set()
        
        frame = UIHelpers.crear_frame_con_titulo(ventana, "Asignación")
        frame.pack(pady=10, padx=10)
        
        id_emp_entry = UIHelpers.crear_label_entry(frame, "ID Empleado:", 0)
        id_proy_entry = UIHelpers.crear_label_entry(frame, "ID Proyecto:", 1)
        fecha_entry = UIHelpers.crear_label_entry(frame, "Fecha:", 2)
        fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        
        def asignar():
            id_emp = id_emp_entry.get().strip()
            id_proy = id_proy_entry.get().strip()
            fecha = fecha_entry.get().strip()
            
            if not id_emp or not id_proy:
                UIHelpers.mostrar_error("Error", "Complete los campos")
                return
            
            exito, mensaje = self.project_controller.asignar_empleado(int(id_emp), int(id_proy), fecha)
            if exito:
                UIHelpers.mostrar_info("Éxito", mensaje)
                self.cargar_asignaciones()
                ventana.destroy()
            else:
                UIHelpers.mostrar_error("Error", mensaje)
        
        UIHelpers.crear_boton(frame, "Asignar", asignar, config.COLORS['success'], row=3, column=0, columnspan=2)
    
    def desasignar_proyecto(self):
        """Desasigna proyecto"""
        seleccion = self.tabla_asignaciones.selection()
        if not seleccion:
            UIHelpers.mostrar_advertencia("Advertencia", "Seleccione una asignación")
            return
        
        valores = self.tabla_asignaciones.item(seleccion[0])['values']
        if UIHelpers.confirmar("Confirmar", "¿Desasignar proyecto?"):
            exito, mensaje = self.project_controller.desasignar_empleado(valores[0], valores[2])
            if exito:
                UIHelpers.mostrar_info("Éxito", mensaje)
                self.cargar_asignaciones()
            else:
                UIHelpers.mostrar_error("Error", mensaje)
    
    def generar_informe(self, tipo):
        """Genera informe"""
        if tipo == 'departamento':
            datos, mensaje = self.report_controller.informe_empleados_por_departamento()
            nombre = 'empleados_por_departamento'
        elif tipo == 'proyecto':
            datos, mensaje = self.report_controller.informe_empleados_por_proyecto()
            nombre = 'empleados_por_proyecto'
        else:
            datos, mensaje = self.report_controller.informe_empleados_totales()
            nombre = 'empleados_totales'
        
        if datos:
            exito, mensaje = self.report_controller.generar_archivo_txt(datos, nombre)
            if exito:
                UIHelpers.mostrar_info("Éxito", mensaje)
            else:
                UIHelpers.mostrar_error("Error", mensaje)
        else:
            UIHelpers.mostrar_advertencia("Advertencia", "No hay datos para el informe")
