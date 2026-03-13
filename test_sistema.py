"""
Script de prueba rápida del sistema
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("\n[TEST 1] Conexión a base de datos...")
    try:
        from models.database import Database
        conn = Database.connect()
        if conn:
            print("✅ Conexión exitosa")
            conn.close()
            return True
        else:
            print("❌ Error de conexión")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_auth_controller():
    """Prueba el controlador de autenticación"""
    print("\n[TEST 2] Controlador de autenticación...")
    try:
        from controllers.auth_controller import AuthController
        # Verificar que las funciones existen
        auth = AuthController()
        print("✅ AuthController cargado correctamente")
        print(f"   - Registro habilitado: {AuthController.verificar_registro_habilitado()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_employee_controller():
    """Prueba el controlador de empleados"""
    print("\n[TEST 3] Controlador de empleados...")
    try:
        from controllers.employee_controller import EmployeeController
        # Usuario de prueba (Admin RH)
        usuario_test = {'fk_id_rol_e': 100}
        emp_ctrl = EmployeeController(usuario_test)
        print(f"✅ EmployeeController cargado")
        print(f"   - Puede gestionar empleados: {emp_ctrl.puede_gestionar_empleados()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_models():
    """Prueba los modelos"""
    print("\n[TEST 4] Modelos de datos...")
    try:
        from models.employee import Employee
        from models.user import User
        from models.project import Project
        from models.department import Department
        print("✅ Todos los modelos cargados correctamente")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_views():
    """Prueba las vistas y herramientas avanzadas"""
    print("\n[TEST 5] Vistas y Extensiones...")
    try:
        from views.login_view import LoginView
        from views.admin_view import AdminView
        from views.manager_view import ManagerView
        from views.employee_view import EmployeeView
        from views.analytics_view import AnalyticsView
        from utils.i18n import I18n
        from utils.data_generator import DataGenerator
        import matplotlib
        
        # Test basic i18n toggle
        I18n.set_language('en')
        assert I18n.get('login_btn') == 'Log In'
        
        print("✅ Todas las vistas y modulos cargados correctamente (incl. Matplotlib & i18n)")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("="*60)
    print("🧪 PRUEBAS DEL SISTEMA")
    print("="*60)
    
    tests = [
        test_database_connection,
        test_auth_controller,
        test_employee_controller,
        test_models,
        test_views
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTADOS: {passed} ✅ | {failed} ❌")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 ¡Todos los tests pasaron exitosamente!")
        print("El sistema está listo para usarse.\n")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) fallaron. Revisa los errores arriba.\n")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
