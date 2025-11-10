"""
Módulo de vistas para la interfaz gráfica
"""

from .login_view import LoginView
from .register_view import RegisterView
from .admin_view import AdminView
from .manager_view import ManagerView
from .employee_view import EmployeeView

__all__ = ['LoginView', 'RegisterView', 'AdminView', 'ManagerView', 'EmployeeView']
