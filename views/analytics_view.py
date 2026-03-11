import tkinter as tk
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models.database import Database
from utils.ui_helpers import UIHelpers
from utils.i18n import I18n
import config

class AnalyticsView:
    """Dashboard de estadísticas y analítica"""
    
    def __init__(self, parent_window):
        self.window = ctk.CTkToplevel(parent_window)
        self.window.title(f"{config.APP_CONFIG['nombre_empresa']} - Analíticas")
        UIHelpers.centrar_ventana(self.window, 800, 600)
        self.window.transient(parent_window)
        self.window.grab_set()  # Modal
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self.window)
        header.pack(fill=tk.X, padx=10, pady=10)
        
        titulo = ctk.CTkLabel(header, text="Panel de Estadísticas y Analítica", font=('Arial', 20, 'bold'))
        titulo.pack(pady=10)
        
        # Area de contenido (Gráficos)
        content_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Recuperar datos
        datos_empleados = self._obtener_empleados_por_departamento()
        datos_salarios = self._obtener_salarios_por_departamento()
        
        if not datos_empleados:
            msg = ctk.CTkLabel(content_frame, text="No hay suficientes datos para graficar.\nGenera datos de prueba primero.")
            msg.grid(row=0, column=0, columnspan=2)
            return

        # Graficar Pie
        self._dibujar_pie_chart(content_frame, datos_empleados, row=0, col=0)
        # Graficar Barras
        self._dibujar_bar_chart(content_frame, datos_salarios, row=0, col=1)
        
        # Botón de cierre
        btn_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        btn_frame.pack(fill=tk.X, pady=10)
        UIHelpers.crear_boton(btn_frame, I18n.get("exit_btn"), self.window.destroy, color=config.COLORS['danger']).pack(pady=10)
        
    def _obtener_empleados_por_departamento(self):
        query = """
            SELECT d.nombre_dep, COUNT(e.id_empleado) as total
            FROM departamentos d
            LEFT JOIN empleados e ON d.id_departamento = e.fk_id_departamento
            GROUP BY d.id_departamento
            HAVING total > 0
        """
        return Database.execute_query(query)
        
    def _obtener_salarios_por_departamento(self):
        query = """
            SELECT d.nombre_dep, AVG(e.salario) as promsal
            FROM departamentos d
            INNER JOIN empleados e ON d.id_departamento = e.fk_id_departamento
            GROUP BY d.id_departamento
            HAVING promsal > 0
        """
        return Database.execute_query(query)

    def _dibujar_pie_chart(self, parent, datos, row, col):
        labels = [d['nombre_dep'] for d in datos]
        sizes = [d['total'] for d in datos]
        
        # Detectar color hexadecimal exacto del frame de CTK actual
        bg_colors = parent.cget("fg_color")
        is_dark = ctk.get_appearance_mode() == "Dark"
        exact_bg = bg_colors[1] if is_dark and isinstance(bg_colors, (list, tuple)) else (bg_colors[0] if isinstance(bg_colors, (list, tuple)) else bg_colors)
        if exact_bg == "transparent":
            # Si el frame padre es transparente, heredar del abuelo (la ventana principal)
            abuelo_bg = self.window.cget("fg_color")
            exact_bg = abuelo_bg[1] if is_dark and isinstance(abuelo_bg, (list, tuple)) else (abuelo_bg[0] if isinstance(abuelo_bg, (list, tuple)) else abuelo_bg)

        # Convertir colores de CustomTkinter (ej. 'gray14') a HEX para Matplotlib
        try:
            rgb = self.window.winfo_rgb(exact_bg)
            exact_bg = f"#{int(rgb[0]/256):02x}{int(rgb[1]/256):02x}{int(rgb[2]/256):02x}"
        except Exception:
            pass # Si falla, dejarlo tal cual

        fig = Figure(figsize=(4, 4), dpi=100)
        fig.patch.set_facecolor(exact_bg)
        
        ax = fig.add_subplot(111)
        ax.set_facecolor(exact_bg)
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90, textprops={'color': 'white' if is_dark else "black"})
        ax.set_title("Headcount por Depto", color='white' if is_dark else "black")
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        
        widget = canvas.get_tk_widget()
        # Eliminar bordes nativos de TK y fijar el fondo exacto
        widget.configure(bg=exact_bg, highlightthickness=0, bd=0)
        widget.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
    def _dibujar_bar_chart(self, parent, datos, row, col):
        labels = [d['nombre_dep'] for d in datos]
        salarios = [d['promsal'] for d in datos]
        
        # Detectar color CTK
        bg_colors = parent.cget("fg_color")
        is_dark = ctk.get_appearance_mode() == "Dark"
        exact_bg = bg_colors[1] if is_dark and isinstance(bg_colors, (list, tuple)) else (bg_colors[0] if isinstance(bg_colors, (list, tuple)) else bg_colors)
        if exact_bg == "transparent":
            abuelo_bg = self.window.cget("fg_color")
            exact_bg = abuelo_bg[1] if is_dark and isinstance(abuelo_bg, (list, tuple)) else (abuelo_bg[0] if isinstance(abuelo_bg, (list, tuple)) else abuelo_bg)
            
        # Convertir colores de CustomTkinter (ej. 'gray14') a HEX
        try:
            rgb = self.window.winfo_rgb(exact_bg)
            exact_bg = f"#{int(rgb[0]/256):02x}{int(rgb[1]/256):02x}{int(rgb[2]/256):02x}"
        except Exception:
            pass
            
        fig = Figure(figsize=(4, 4), dpi=100)
        fig.patch.set_facecolor(exact_bg)
        
        ax = fig.add_subplot(111)
        ax.set_facecolor(exact_bg)
        
        # Color del texto dinámico
        text_color = 'white' if is_dark else "black"
        ax.tick_params(axis='x', colors=text_color, rotation=45)
        ax.tick_params(axis='y', colors=text_color)
        ax.spines['bottom'].set_color(text_color)
        ax.spines['left'].set_color(text_color)
        
        # Ocultar espinas innecesarias
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)

        ax.bar(labels, salarios, color='#1f77b4')
        ax.set_title("Salario Promedio", color=text_color)
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        
        widget = canvas.get_tk_widget()
        widget.configure(bg=exact_bg, highlightthickness=0, bd=0)
        widget.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
