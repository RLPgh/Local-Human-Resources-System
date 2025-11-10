# Configuración de conexión a la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'dbEmpresa'
}

# Configuración de la aplicación
APP_CONFIG = {
    'nombre_empresa': 'nombre_empresa',  # Nombre genérico de la empresa
    'version': '1.0.0',
    'titulo_app': 'Sistema de Gestión de Recursos Humanos',
    'registro_publico_habilitado': True  # Controla si el registro público está disponible
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
