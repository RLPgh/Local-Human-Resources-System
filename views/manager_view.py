"""
Vista principal para Gerente
"""

import tkinter as tk
from tkinter import ttk
import config
from controllers.department_controller import DepartmentController
from utils.ui_helpers import UIHelpers


class ManagerView:
    """Vista principal para Gerente"""
    
    def __init__(self, root, usuario, on_logout):
        self.root = root
        self.usuario = usuario
        self.on_logout = on_logout
        self.dept_controller = DepartmentController(usuario)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"{config.APP_CONFIG['titulo_app']} - Gerente")
        UIHelpers.centrar_ventana(self.root, 1000, 600)
        self.root.configure(bg=config.COLORS['light'])
        
        # Header
        header_frame = tk.Frame(self.root, bg=config.COLORS['primary'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        nombre_completo = f"{self.usuario['nombre_empleado']} {self.usuario['apellido_empleado']}"
        tk.Label(
            header_frame,
            text=f"Gerente: {nombre_completo}",
            font=('Arial', 14, 'bold'),
            bg=config.COLORS['primary'],
            fg=config.COLORS['white']
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        UIHelpers.crear_boton(
            header_frame,
            "Cerrar Sesión",
            self.on_logout,
            config.COLORS['danger']
        ).pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_departamentos = tk.Frame(notebook, bg=config.COLORS['white'])
        notebook.add(self.tab_departamentos, text="Gestionar Departamentos")
        self.crear_tab_departamentos()
        
        self.tab_asignaciones = tk.Frame(notebook, bg=config.COLORS['white'])
        notebook.add(self.tab_asignaciones, text="Asignar Empleados")
        self.crear_tab_asignaciones()
    
    def crear_tab_departamentos(self):
        """Crea tab de departamentos"""
        btn_frame = tk.Frame(self.tab_departamentos, bg=config.COLORS['white'])
        btn_frame.pack(pady=10)
        
        UIHelpers.crear_boton(btn_frame, "Actualizar", self.cargar_departamentos, config.COLORS['info']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Nuevo", self.nuevo_departamento, config.COLORS['success']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Editar", self.editar_departamento, config.COLORS['warning']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Eliminar", self.eliminar_departamento, config.COLORS['danger']).pack(side=tk.LEFT, padx=5)
        
        columnas = [
            ('id', 'ID', 80),
            ('nombre', 'Nombre', 300),
            ('gerente', 'Gerente', 300)
        ]
        self.tabla_departamentos, _ = UIHelpers.crear_tabla(self.tab_departamentos, columnas, altura=15)
        self.cargar_departamentos()
    
    def crear_tab_asignaciones(self):
        """Crea tab de asignaciones"""
        btn_frame = tk.Frame(self.tab_asignaciones, bg=config.COLORS['white'])
        btn_frame.pack(pady=10)
        
        UIHelpers.crear_boton(btn_frame, "Actualizar", self.cargar_empleados_sin_dept, config.COLORS['info']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Asignar", self.asignar_empleado, config.COLORS['success']).pack(side=tk.LEFT, padx=5)
        UIHelpers.crear_boton(btn_frame, "Desasignar", self.desasignar_empleado, config.COLORS['danger']).pack(side=tk.LEFT, padx=5)
        
        columnas = [
            ('id', 'ID', 80),
            ('nombre', 'Nombre', 200),
            ('apellido', 'Apellido', 200)
        ]
        self.tabla_empleados, _ = UIHelpers.crear_tabla(self.tab_asignaciones, columnas, altura=15)
        self.cargar_empleados_sin_dept()
    
    def cargar_departamentos(self):
        """Carga departamentos"""
        for item in self.tabla_departamentos.get_children():
            self.tabla_departamentos.delete(item)
        
        departamentos, _ = self.dept_controller.obtener_todos_departamentos()
        if departamentos:
            for d in departamentos:
                self.tabla_departamentos.insert('', tk.END, values=(
                    d.get('id_departamento', ''),
                    d.get('nombre_dep', ''),
                    d.get('gerente', '')
                ))
    
    def nuevo_departamento(self):
        """Crea departamento"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Nuevo Departamento")
        UIHelpers.centrar_ventana(ventana, 400, 150)
        
        frame = UIHelpers.crear_frame_con_titulo(ventana, "Datos")
        frame.pack(pady=10, padx=10)
        
        nombre_entry = UIHelpers.crear_label_entry(frame, "Nombre:", 0)
        
        def guardar():
            nombre = nombre_entry.get().strip()
            if not nombre:
                UIHelpers.mostrar_error("Error", "Ingrese un nombre")
                return
            
            id_dept, mensaje = self.dept_controller.crear_departamento(nombre)
            if id_dept:
                UIHelpers.mostrar_info("Éxito", mensaje)
                self.cargar_departamentos()
                ventana.destroy()
            else:
                UIHelpers.mostrar_error("Error", mensaje)
        
        UIHelpers.crear_boton(frame, "Guardar", guardar, config.COLORS['success'], row=1, column=0, columnspan=2)
    
    def editar_departamento(self):
        """Edita departamento"""
        seleccion = self.tabla_departamentos.selection()
        if not seleccion:
            UIHelpers.mostrar_advertencia("Advertencia", "Seleccione un departamento")
            return
        
        valores = self.tabla_departamentos.item(seleccion[0])['values']
        id_dept = valores[0]
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Editar Departamento")
        UIHelpers.centrar_ventana(ventana, 400, 150)
        
        frame = UIHelpers.crear_frame_con_titulo(ventana, "Datos")
        frame.pack(pady=10, padx=10)
        
        nombre_entry = UIHelpers.crear_label_entry(frame, "Nombre:", 0)
        nombre_entry.insert(0, valores[1])
        
        def guardar():
            nombre = nombre_entry.get().strip()
            if not nombre:
                UIHelpers.mostrar_error("Error", "Ingrese un nombre")
                return
            
            exito, mensaje = self.dept_controller.actualizar_departamento(id_dept, nombre)
            if exito:
                UIHelpers.mostrar_info("Éxito", mensaje)
                self.cargar_departamentos()
                ventana.destroy()
            else:
                UIHelpers.mostrar_error("Error", mensaje)
        
        UIHelpers.crear_boton(frame, "Guardar", guardar, config.COLORS['success'], row=1, column=0, columnspan=2)
    
    def eliminar_departamento(self):
        """Elimina departamento"""
        seleccion = self.tabla_departamentos.selection()
        if not seleccion:
            UIHelpers.mostrar_advertencia("Advertencia", "Seleccione un departamento")
            return
        
        valores = self.tabla_departamentos.item(seleccion[0])['values']
        if UIHelpers.confirmar("Confirmar", f"¿Eliminar departamento {valores[1]}?"):
            exito, mensaje = self.dept_controller.eliminar_departamento(valores[0])
            if exito:
                UIHelpers.mostrar_info("Éxito", mensaje)
                self.cargar_departamentos()
            else:
                UIHelpers.mostrar_error("Error", mensaje)
    
    def cargar_empleados_sin_dept(self):
        """Carga empleados sin departamento"""
        for item in self.tabla_empleados.get_children():
            self.tabla_empleados.delete(item)
        
        empleados, _ = self.dept_controller.obtener_empleados_sin_departamento()
        if empleados:
            for e in empleados:
                self.tabla_empleados.insert('', tk.END, values=(
                    e.get('id_empleado', ''),
                    e.get('nombre_empleado', ''),
                    e.get('apellido_empleado', '')
                ))
    
    def asignar_empleado(self):
        """Asigna empleado a departamento"""
        seleccion = self.tabla_empleados.selection()
        if not seleccion:
            UIHelpers.mostrar_advertencia("Advertencia", "Seleccione un empleado")
            return
        
        valores = self.tabla_empleados.item(seleccion[0])['values']
        id_empleado = valores[0]
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Asignar a Departamento")
        UIHelpers.centrar_ventana(ventana, 350, 150)
        
        frame = UIHelpers.crear_frame_con_titulo(ventana, "Asignación")
        frame.pack(pady=10, padx=10)
        
        id_dept_entry = UIHelpers.crear_label_entry(frame, "ID Departamento:", 0)
        
        def asignar():
            id_dept = id_dept_entry.get().strip()
            if not id_dept:
                UIHelpers.mostrar_error("Error", "Ingrese ID de departamento")
                return
            
            exito, mensaje = self.dept_controller.asignar_empleado(id_empleado, int(id_dept))
            if exito:
                UIHelpers.mostrar_info("Éxito", mensaje)
                self.cargar_empleados_sin_dept()
                ventana.destroy()
            else:
                UIHelpers.mostrar_error("Error", mensaje)
        
        UIHelpers.crear_boton(frame, "Asignar", asignar, config.COLORS['success'], row=1, column=0, columnspan=2)
    
    def desasignar_empleado(self):
        """Desasigna empleado"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Desasignar Empleado")
        UIHelpers.centrar_ventana(ventana, 350, 150)
        
        frame = UIHelpers.crear_frame_con_titulo(ventana, "Desasignar")
        frame.pack(pady=10, padx=10)
        
        id_emp_entry = UIHelpers.crear_label_entry(frame, "ID Empleado:", 0)
        
        def desasignar():
            id_emp = id_emp_entry.get().strip()
            if not id_emp:
                UIHelpers.mostrar_error("Error", "Ingrese ID de empleado")
                return
            
            exito, mensaje = self.dept_controller.desasignar_empleado(int(id_emp))
            if exito:
                UIHelpers.mostrar_info("Éxito", mensaje)
                self.cargar_empleados_sin_dept()
                ventana.destroy()
            else:
                UIHelpers.mostrar_error("Error", mensaje)
        
        UIHelpers.crear_boton(frame, "Desasignar", desasignar, config.COLORS['success'], row=1, column=0, columnspan=2)
