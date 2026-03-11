# Configuración de conexión a la base de datos
DB_CONFIG = {
    'database': 'dbEmpresa.db'
}

# Configuración de la aplicación
APP_CONFIG = {
    'nombre_empresa': 'NexusHR',
    'version': '3.0.0',
    'titulo_app': 'Gestión de RRHH - NexusHR',
    'registro_publico_habilitado': True,  # Controla si el registro público (el botón) está visible
    'roles_registro_permitidos': [102]    # Por defecto, solo permite registrar Empleado
}

# Roles del sistema
ROLES = {
    100: 'Administrador RH',
    101: 'Gerente',
    102: 'Empleado'
}

# Colores para la interfaz
COLORS = {
    'primary': '#2c3e50',      # Azul oscuro
    'secondary': '#3498db',    # Azul claro
    'success': '#27ae60',      # Verde
    'danger': '#e74c3c',       # Rojo
    'warning': '#f39c12',      # Naranja
    'info': '#16a085',         # Turquesa
    'light': '#ecf0f1',        # Gris claro
    'dark': '#34495e',         # Gris oscuro
    'white': '#ffffff',        # Blanco
    'text': '#2c3e50'          # Texto
}
