# 🏢 Sistema de Gestión de Recursos Humanos

Sistema integral de gestión de RRHH con interfaz gráfica desarrollado en Python con Tkinter y arquitectura MVC.

## ⚡ INICIO RÁPIDO

### � Instalación Automática (3 pasos)

```bash
# 1. Instalar Python 3.8+ (https://www.python.org/downloads/)
# 2. Instalar MySQL (XAMPP recomendado: https://www.apachefriends.org/)
# 3. Ejecutar:
python iniciar_sistema.py
```

**¡Eso es todo!** El sistema:
- ✅ Instala dependencias automáticamente
- ✅ Crea la base de datos automáticamente
- ✅ Inicia la aplicación

📖 **Ver:** [INSTRUCCIONES_INSTALACION.md](INSTRUCCIONES_INSTALACION.md) para guía detallada

---

## �📋 Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Primer Uso](#primer-uso)
- [Roles del Sistema](#roles-del-sistema)
- [Arquitectura](#arquitectura)
- [Documentación](#documentación)

## 🚀 Características

- **Interfaz Gráfica Moderna** con Tkinter
- **3 Roles** con permisos diferenciados
- **CRUD completo** de empleados, proyectos y departamentos
- **Registro de tiempos** con validación legal (máx. 12h/día)
- **Generación de informes** en TXT
- **Seguridad** con contraseñas hasheadas (bcrypt)
- **Validaciones** de datos completas en formularios
- **Control dinámico** de registro público
- **🆕 Instalación automática** con un solo comando

## 🏗️ Arquitectura MVC

```
models/            → Capa de datos (6 modelos)
views/             → Interfaces gráficas (5 vistas)
controllers/       → Lógica de negocio (6 controladores)
utils/             → Validadores y helpers
config.py          → Configuración centralizada
iniciar_sistema.py → ⭐ ÚNICO ARCHIVO EJECUTABLE
```

**Ventajas:** Separación de responsabilidades, mantenibilidad, testabilidad y escalabilidad.

## 📦 Requisitos

- **Python** 3.8+
- **MySQL** 5.7+ (o XAMPP)

**Las dependencias Python se instalan automáticamente:**
- `mysql-connector-python`
- `bcrypt`

## 🔧 Instalación

### UN SOLO COMANDO

```bash
# 1. Instala Python 3.8+ y MySQL
# 2. Ejecuta:
python iniciar_sistema.py
```

**El sistema hace TODO automáticamente:**
1. ✅ Verifica Python y dependencias
2. ✅ Instala paquetes necesarios
3. ✅ Detecta MySQL en tu sistema
4. ✅ Crea la base de datos automáticamente
5. ✅ Inicia la aplicación

## 👤 Primer Uso

1. **Registrar usuario inicial**
   - Clic en "Registrarse" en pantalla de login
   - Completar datos personales
   - Seleccionar rol: **Admin RH (100)** para acceso completo
   - Crear contraseña (mín. 8 caracteres)

2. **Iniciar sesión** con las credenciales creadas

3. **Usar el sistema** según tu rol

## 👥 Roles del Sistema

### 🔴 Administrador RH (100)
- CRUD completo de empleados
- CRUD completo de proyectos
- Asignar/desasignar proyectos
- Generar 3 tipos de informes
- Control de registro público
- Ver todas las asignaciones

### 🟠 Gerente (101)
- CRUD de departamentos
- Asignar empleados a departamentos
- Ver empleados por departamento
- Restricciones de seguridad por rol

### 🟡 Empleado (102)
- Registrar tiempo trabajado
- Asociar horas a proyectos
- Ver histórico de tiempos
- Ver proyectos asignados
- Validación: máx. 12h/día

## 🔍 Estructura del Proyecto

```
📁 Proyecto/
├── 🚀 iniciar_sistema.bat      # Iniciar con consola
├── 🚀 iniciar_sistema.pyw      # Iniciar sin consola
├── 📄 main_gui.py              # Punto de entrada
├── ⚙️ config.py                # Configuración
├── 🗄️ dbEmpresa.sql            # Base de datos
├── 📋 requirements.txt         # Dependencias
├── 📁 models/                  # Capa de datos
├── 📁 views/                   # Interfaces gráficas
├── 📁 controllers/             # Lógica de negocio
├── 📁 utils/                   # Validadores
└── 📖 README.md                # Este archivo
```

## 📚 Documentación

- **[COMO_INICIAR.md](./COMO_INICIAR.md)** - Guía rápida de inicio (empieza aquí) ⭐
- **[INSTRUCCIONES_INSTALACION.md](./INSTRUCCIONES_INSTALACION.md)** - Guía completa de instalación
- **[dbEmpresa.sql](./dbEmpresa.sql)** - Estructura de base de datos

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "Can't connect to MySQL"
- Verificar que MySQL esté ejecutándose
- Verificar credenciales en `config.py`
- Verificar que existe la BD `dbEmpresa`

### Error: "Access denied for user"
- Actualizar contraseña de MySQL en `config.py`
- Verificar permisos del usuario

### "Máximo 12 horas por día"
- Validación de ley laboral chilena
- Ya registraste horas en esa fecha

## 📝 Notas

- Todas las contraseñas se encriptan con bcrypt
- Las validaciones protegen contra inyección SQL
- El sistema genera timestamps en los informes
- Confirmación requerida para acciones críticas

---

**¿Listo?** Ejecuta:
```bash
python iniciar_sistema.py
```
