# ⚡ CÓMO INICIAR EL SISTEMA

## 🎯 UN SOLO ARCHIVO

```
iniciar_sistema.py  ← ⭐ ÚNICO ARCHIVO EJECUTABLE
```

## 🚀 Ejecutar el Sistema

### Desde Terminal (Recomendado):
```bash
python iniciar_sistema.py
```

### Desde Editor/IDE:
```
Ejecutar: iniciar_sistema.py
```

## ✨ El launcher hace TODO automáticamente:

```
[1/6] ✅ Verificar Python 3.8+
[2/6] ✅ Instalar dependencias (mysql-connector-python, bcrypt)
[3/6] ✅ Detectar MySQL en tu sistema
[4/6] ✅ Probar conexión a MySQL
[5/6] ✅ Crear base de datos automáticamente
[6/6] ✅ Iniciar aplicación
```

## 📋 Requisitos Previos

Solo necesitas tener instalado:

1. **Python 3.8+** → https://www.python.org/downloads/
2. **MySQL** → https://www.apachefriends.org/ (XAMPP recomendado)

## ⚙️ Configuración MySQL

Si tu MySQL tiene contraseña, edita `config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'TU_CONTRASEÑA_AQUÍ',  # ← Cambiar aquí
    'database': 'dbEmpresa'
}
```

## 🎉 ¡Eso es Todo!

Una vez instalado Python y MySQL, solo ejecuta:
```
python iniciar_sistema.py
```

---

📖 **Más información:** Ver `INSTRUCCIONES_INSTALACION.md`
📝 **Cambios realizados:** Ver `CAMBIOS_v2.0.md`
