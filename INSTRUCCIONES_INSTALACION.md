# 🚀 Guía de Instalación - Sistema de Gestión RRHH

## ⚡ Inicio Rápido (3 pasos)

### 1️⃣ Instalar Python
- Descarga Python 3.8+ desde: https://www.python.org/downloads/
- ✅ Durante la instalación, marca "Add Python to PATH"

### 2️⃣ Instalar MySQL
Elige UNA de estas opciones:

**Opción A - XAMPP (Recomendada para principiantes):**
- Descarga desde: https://www.apachefriends.org/
- Instala y ejecuta MySQL desde el panel de control de XAMPP

**Opción B - MySQL Community Server:**
- Descarga desde: https://dev.mysql.com/downloads/installer/
- Durante instalación, configura contraseña root (o déjala vacía)

### 3️⃣ Ejecutar el Sistema
**Cualquier Sistema Operativo (Windows/Linux/Mac):**
```bash
python iniciar_sistema.py
```

## ✨ ¿Qué hace el launcher automáticamente?

El archivo `iniciar_sistema.py` realiza TODO automáticamente:

✅ Verifica que Python esté instalado (3.8+)
✅ Instala dependencias Python automáticamente:
   - mysql-connector-python
   - bcrypt
✅ Detecta MySQL en tu sistema
✅ Crea la base de datos `dbEmpresa` automáticamente
✅ Carga todas las tablas y datos iniciales
✅ Inicia la aplicación gráfica

## 🔧 Configuración de MySQL

El sistema usa esta configuración por defecto (archivo `config.py`):

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Vacío por defecto
    'database': 'dbEmpresa'
}
```

### Si tu MySQL tiene contraseña:
1. Abre `config.py`
2. Modifica la línea: `'password': 'tu_contraseña_aqui'`
3. Guarda el archivo

## 🎯 Primera Ejecución

Cuando ejecutes por primera vez:

1. El sistema verificará todo automáticamente
2. Creará la base de datos si no existe
3. Abrirá la ventana de login
4. **Usuario inicial (Administrador):**
   - Usa el botón "Registrar nuevo usuario"
   - El primer usuario registrado será Administrador RH

## 📋 Roles del Sistema

| Rol | ID | Permisos |
|-----|----|----|
| **Administrador RH** | 100 | Gestión completa: empleados, proyectos, informes |
| **Gerente** | 101 | Gestión de departamentos |
| **Empleado** | 102 | Registro de tiempos |

## 🐛 Solución de Problemas

### ❌ Error: "Python no está instalado"
- Instala Python 3.8+ desde python.org
- Asegúrate de marcar "Add Python to PATH"

### ❌ Error: "MySQL no detectado"
- Instala XAMPP o MySQL Community Server
- Asegúrate de que el servicio MySQL esté ejecutándose

### ❌ Error: "No se pudo conectar a MySQL"
- Verifica que MySQL esté ejecutándose
- Si tienes contraseña en MySQL, actualiza `config.py`
- Verifica host (debe ser 'localhost')
- Verifica usuario (por defecto es 'root')

### ❌ Error: "Access denied for user"
- Tu MySQL tiene contraseña configurada
- Edita `config.py` y añade tu contraseña en el campo `password`

## 📁 Archivos del Sistema

```
iniciar_sistema.py     ← ⭐ ÚNICO ARCHIVO EJECUTABLE
config.py              ← Configuración MySQL
dbEmpresa.sql          ← Script de base de datos (auto-cargado)
test_sistema.py        ← Tests automatizados
```

## 🆘 Soporte

Si encuentras problemas:

1. Verifica que MySQL esté ejecutándose
2. Revisa la configuración en `config.py`
3. Los mensajes de error son descriptivos y te guiarán

## 🎉 ¡Listo!

Una vez instalado, solo ejecuta:
```bash
python iniciar_sistema.py
```

El sistema verificará todo automáticamente en cada ejecución.
