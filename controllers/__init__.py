"""
Módulo de controladores para el sistema de gestión de recursos humanos
"""

from .auth_controller import AuthController
from .employee_controller import EmployeeController
from .project_controller import ProjectController
from .department_controller import DepartmentController
from .time_record_controller import TimeRecordController
from .report_controller import ReportController

__all__ = [
    'AuthController',
    'EmployeeController',
    'ProjectController',
    'DepartmentController',
    'TimeRecordController',
    'ReportController'
]
