# Changelog

Todos los cambios notables del proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/lang/es/).

## [0.2.0] - 2026-03-13

### Añadido
- Interfaz moderna con **CustomTkinter** (modo oscuro/claro).
- Soporte de internacionalización (**i18n**): Español e Inglés.
- Dashboard de **analíticas** con gráficos Matplotlib (distribución salarial, ocupación departamental).
- Generación de **datos sintéticos** de prueba (50+ empleados, 6 departamentos).
- Registro de **tiempos** con validación legal (máx. 12h/día).
- Vista de **Analytics** integrada con el tema de CustomTkinter.
- Archivo `VERSION` centralizado como fuente de verdad.
- Archivo `CHANGELOG.md` para seguimiento de versiones.

### Cambiado
- Migración de MySQL a **SQLite** para portabilidad total (zero-config).
- Refactorización completa de la arquitectura a **MVC**.
- Actualización a 3 roles del sistema (Admin RH, Gerente, Empleado) con flujos de autorización estrictos.
- Seguridad mejorada con hash de contraseñas **bcrypt**.
- Estandarización del versionado del proyecto a **Semantic Versioning**.

### Eliminado
- Dependencia de XAMPP/MySQL.
- Archivos y módulos obsoletos sin uso.

## [0.1.0] - 2026-02-24

### Añadido
- Commit inicial: Sistema empresarial local v2.0 (versión interna legacy).
- Estructura base del proyecto con modelos, vistas y controladores.
- Launcher automático (`iniciar_sistema.py`).
- Base de datos SQLite local.
- Autenticación básica con bcrypt.
