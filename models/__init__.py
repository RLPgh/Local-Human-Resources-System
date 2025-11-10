"""
Módulo de modelos para el sistema de gestión de recursos humanos
"""

from .database import Database
from .employee import Employee
from .user import User
from .project import Project
from .department import Department
from .time_record import TimeRecord

__all__ = ['Database', 'Employee', 'User', 'Project', 'Department', 'TimeRecord']
