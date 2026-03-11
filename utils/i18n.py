"""
Manejo de Internacionalización (i18n)
"""

TRANSLATIONS = {
    'es': {
        'login_title': 'Iniciar Sesión',
        'login_subtitle': 'Sistema Integral de Gestión de RRHH',
        'email': 'Correo:',
        'password': 'Contraseña:',
        'login_btn': 'Iniciar Sesión',
        'register_btn': 'Registrarse',
        'exit_btn': 'Salir',
        'theme': 'Tema:',
        'lang': 'Idioma:',
        'error_empty_fields': 'Por favor complete todos los campos',
        'success': 'Éxito',
        'error': 'Error',
        'welcome': 'Bienvenido',
        'version': 'Versión'
    },
    'en': {
        'login_title': 'Login',
        'login_subtitle': 'Comprehensive HR Management System',
        'email': 'Email:',
        'password': 'Password:',
        'login_btn': 'Log In',
        'register_btn': 'Register',
        'exit_btn': 'Exit',
        'theme': 'Theme:',
        'lang': 'Language:',
        'error_empty_fields': 'Please fill all fields',
        'success': 'Success',
        'error': 'Error',
        'welcome': 'Welcome',
        'version': 'Version'
    }
}

class I18n:
    _current_lang = 'es'

    @classmethod
    def set_language(cls, lang_code):
        if lang_code in TRANSLATIONS:
            cls._current_lang = lang_code
            
    @classmethod
    def get(cls, key):
        return TRANSLATIONS.get(cls._current_lang, {}).get(key, key)
