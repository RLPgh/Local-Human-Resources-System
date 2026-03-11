# 🏢 NexusHR - Sistema de Gestión de Recursos Humanos

Un sistema integral de gestión de RRHH con interfaz gráfica moderna, desarrollado en Python usando `CustomTkinter` y `SQLite` bajo arquitectura MVC.

*Leer en otros idiomas: [English](README.md)*

## ⚡ INICIO RÁPIDO

### Instalación con 1 Clic

```bash
# 1. Instala Python 3.8+ (https://www.python.org/downloads/)
# 2. Ejecuta el inicializador:
python iniciar_sistema.py
```

**¡Eso es todo!** El sistema hará lo siguiente automáticamente:
- ✅ Verificar Python e instalar dependencias (`customtkinter`, `bcrypt`, `matplotlib`).
- ✅ Configurar la base de datos local `SQLite` (¡Sin depender de XAMPP o MySQL!).
- ✅ Iniciar la aplicación.

---

## 🚀 Características (v3.0.0)

- **Interfaz Moderna** con CustomTkinter (Modo Claro/Oscuro).
- **Base de Datos Zero-Config**: Portabilidad total gracias a SQLite.
- **3 Roles del Sistema** con flujos de autorización estrictos (El primer usuario es Admin).
- **Soporte i18n**: Interfaz traducida nativamente en Inglés y Español.
- **Analítica de Datos**: Gráficos visuales (Matplotlib) para personal y salarios.
- **Datos Sintéticos**: Generación de datos de prueba con un clic para facilitar la evaluación.
- **Registro de Tiempos**: Validación legal (ej. máx 12h/día).
- **Seguridad**: Hash de contraseñas con bcrypt.

## 🏗️ Arquitectura MVC

```text
models/            → Capa de datos (Operaciones SQLite)
views/             → Interfaces gráficas (CustomTkinter)
controllers/       → Lógica de negocio y validaciones
utils/             → Helpers de UI, Validadores e i18n
config.py          → Configuración central (Temas, BD, Título de la app)
iniciar_sistema.py → ⭐ ÚNICO PUNTO DE ENTRADA EJECUTABLE
```

## 👤 Primer Uso (Flujo de Registro)

1. **Registrar al usuario inicial**
   - Haz clic en "Registrarse" en la pantalla de inicio de sesión.
   - El **Primer usuario registrado** se convierte automáticamente en **Administrador RH (100)**.
2. **Usuarios subsecuentes**
   - Cualquier otro usuario que se registre públicamente será **Empleado (102)** por defecto.
   - Los administradores deben ascenderlos manualmente a Gerentes de ser necesario.
3. **Inicia sesión** con tus credenciales.

## 👥 Roles del Sistema

### 🔴 Administrador RH (100)
- CRUD completo de empleados y proyectos.
- Dashboard de analíticas y gráficos.
- Generar datos de prueba sintéticos.
- Configuración global del sistema.

### 🟠 Gerente (101)
- CRUD de departamentos.
- Asignar empleados a departamentos.
- Ver analíticas departamentales.

### 🟡 Empleado (102)
- Registrar horas trabajadas en proyectos.
- Ver historial personal.

## 📖 Tutorial de Uso

Sigue estos pasos para experimentar todo el flujo de NexusHR:

1. **Configuración Inicial (Admin)**
   - Inicia la app y presiona **Registrarse**.
   - Crea tu cuenta. **Debido a que eres el primer usuario en la base de datos**, te convertirás automáticamente en el **Administrador RH (100)**.
   - Puedes habilitar o deshabilitar el registro público usando el botón amarillo en tu cabecera principal.

2. **Generar Datos Sintéticos (Opcional pero recomendado)**
   - Como Admin, dirígete a la pestaña **"Informes"**.
   - Clica sobre "**Generar Datos de Prueba Sintéticos**" para insertar instantáneamente más de 50 empleados falsos, 6 departamentos y salarios al azar.
   - *¡Esto te permitirá probar las búsquedas y gráficos sin esfuerzo!*

3. **Gestión de la Empresa (CRUD)**
   - Dirígete a las pestañas **"Gestionar Empleados" / "Gestionar Proyectos"** para crear, leer, actualizar o eliminar registros.
   - Si usuarios reales se registran desde la pantalla pública de inicio, nacerán como **Empleados (102)**. Puedes editarlos en la tabla para subirlos a **Gerentes (101)** si lo requieres.

4. **El Rol de Gerente**
   - Cierra sesión y entra como un Gerente.
   - Los gerentes poseen una pantalla exclusiva con la pestaña **"Gestionar Departamentos"**.
   - Aquí crean áreas (Marketing, TI, etc.) y les asignan personal libre.

5. **El Rol de Empleado**
   - Inicia sesión como un Empleado raso.
   - Verás un dashboard limitado y privado.
   - Entra a **"Registrar Tiempo"**, selecciona la fecha, la cantidad de horas trabajadas y asócialas a un Proyecto. 
   - Puedes consultar todo tu histórico en **"Mis Registros"**.

6. **Analítica en Tiempo Real**
   - ¡Vuelve a entrar como Admin!
   - En la pestaña Informes haz clic en **Ver Analíticas (Gráficos)**.
   - Un Modal moderno se abrirá con gráficas de *Matplotlib* analizando directamente la masa salarial y la ocupación departamental leyendo la base de datos SQL alojada.

## 🐛 Solución de Problemas

### "ModuleNotFoundError"
Si el autoinstalador falla, instala manualmente:
```bash
pip install -r requirements.txt
```

### Otros Errores
Ejecuta `python test_sistema.py` para diagnosticar problemas con SQLite o las interfaces gráficas.
