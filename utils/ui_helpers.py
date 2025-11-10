"""
Helpers para la interfaz de usuario
"""

import tkinter as tk
from tkinter import ttk, messagebox
import config


class UIHelpers:
    """Clase con métodos estáticos para ayudar con la interfaz"""
    
    @staticmethod
    def centrar_ventana(ventana, ancho, alto):
        """
        Centra una ventana en la pantalla
        
        Args:
            ventana: Ventana de Tkinter
            ancho: Ancho de la ventana
            alto: Alto de la ventana
        """
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    @staticmethod
    def crear_label_entry(parent, texto, row, column=0, is_password=False, width=30):
        """
        Crea un label y un entry en el grid
        
        Args:
            parent: Widget padre
            texto: Texto del label
            row: Fila del grid
            column: Columna del grid (default 0)
            is_password: Si es campo de contraseña (default False)
            width: Ancho del entry (default 30)
            
        Returns:
            Entry widget
        """
        label = ttk.Label(parent, text=texto)
        label.grid(row=row, column=column, sticky="w", padx=5, pady=5)
        
        entry = ttk.Entry(parent, width=width, show="*" if is_password else "")
        entry.grid(row=row, column=column+1, padx=5, pady=5)
        
        return entry
    
    @staticmethod
    def crear_boton(parent, texto, comando, color=None, row=None, column=None, 
                    columnspan=1, sticky="ew", padx=5, pady=5):
        """
        Crea un botón estilizado
        
        Args:
            parent: Widget padre
            texto: Texto del botón
            comando: Función a ejecutar al hacer clic
            color: Color del botón (usa config.COLORS)
            row: Fila del grid (opcional)
            column: Columna del grid (opcional)
            columnspan: Número de columnas que ocupa
            sticky: Alineación
            padx: Padding horizontal
            pady: Padding vertical
            
        Returns:
            Button widget
        """
        boton = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=color or config.COLORS['primary'],
            fg=config.COLORS['white'],
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        
        if row is not None and column is not None:
            boton.grid(row=row, column=column, columnspan=columnspan, 
                      sticky=sticky, padx=padx, pady=pady)
        
        return boton
    
    @staticmethod
    def crear_tabla(parent, columnas, altura=10):
        """
        Crea una tabla (Treeview) con scrollbar
        
        Args:
            parent: Widget padre
            columnas: Lista de tuplas (id, nombre, ancho)
            altura: Altura de la tabla en filas
            
        Returns:
            Tupla (Treeview, Scrollbar)
        """
        # Frame contenedor
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        
        # Treeview
        columna_ids = [col[0] for col in columnas]
        tabla = ttk.Treeview(
            frame,
            columns=columna_ids,
            show='headings',
            height=altura,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # Configurar columnas
        for col_id, col_nombre, col_ancho in columnas:
            tabla.heading(col_id, text=col_nombre)
            tabla.column(col_id, width=col_ancho, anchor='center')
        
        # Configurar scrollbars
        scrollbar_y.config(command=tabla.yview)
        scrollbar_x.config(command=tabla.xview)
        
        # Posicionar widgets
        tabla.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        # Configurar peso de filas y columnas
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        
        return tabla, frame
    
    @staticmethod
    def mostrar_info(titulo, mensaje):
        """Muestra un mensaje de información"""
        messagebox.showinfo(titulo, mensaje)
    
    @staticmethod
    def mostrar_error(titulo, mensaje):
        """Muestra un mensaje de error"""
        messagebox.showerror(titulo, mensaje)
    
    @staticmethod
    def mostrar_advertencia(titulo, mensaje):
        """Muestra un mensaje de advertencia"""
        messagebox.showwarning(titulo, mensaje)
    
    @staticmethod
    def confirmar(titulo, mensaje):
        """
        Muestra un diálogo de confirmación
        
        Returns:
            True si el usuario confirma, False si no
        """
        return messagebox.askyesno(titulo, mensaje)
    
    @staticmethod
    def limpiar_entries(entries):
        """
        Limpia una lista de entries
        
        Args:
            entries: Lista de Entry widgets
        """
        for entry in entries:
            entry.delete(0, tk.END)
    
    @staticmethod
    def crear_frame_con_titulo(parent, titulo):
        """
        Crea un LabelFrame con título
        
        Args:
            parent: Widget padre
            titulo: Título del frame
            
        Returns:
            LabelFrame widget
        """
        frame = ttk.LabelFrame(parent, text=titulo, padding=10)
        return frame
