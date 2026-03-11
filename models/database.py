"""
Módulo para manejo de conexión a la base de datos (SQLite)
"""

import sqlite3
import os
import re
import config


class Database:
    """Clase para gestionar la conexión y operaciones de base de datos"""
    
    @staticmethod
    def connect():
        """Establece conexión con la base de datos"""
        try:
            # Obtener directorio base para asegurar que la db se cree en el lugar correcto
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, config.DB_CONFIG.get('database', 'dbEmpresa.db'))
            
            connection = sqlite3.connect(db_path)
            # Activar foreign keys (desactivadas por defecto en sqlite)
            connection.execute("PRAGMA foreign_keys = ON;")
            # Devolver diccionarios en lugar de tuplas para simular dictionary=True de MySQL
            connection.row_factory = sqlite3.Row
            return connection
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
    
    @staticmethod
    def _convert_query(query):
        """Convierte los placeholders de MySQL (%s) a SQLite (?)"""
        return query.replace('%s', '?')

    @staticmethod
    def execute_query(query, params=None, fetchone=False):
        """
        Ejecuta una consulta SELECT
        
        Args:
            query: La consulta SQL a ejecutar
            params: Tupla de parámetros para la consulta
            fetchone: Si es True, retorna solo un resultado
            
        Returns:
            Resultado de la consulta o None si hay error
        """
        connection = Database.connect()
        if not connection:
            return None
        
        cursor = None
        try:
            cursor = connection.cursor()
            sqlite_query = Database._convert_query(query)
            cursor.execute(sqlite_query, params or ())
            
            if fetchone:
                row = cursor.fetchone()
                return dict(row) if row else None
            else:
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error en consulta: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def execute_command(query, params=None):
        """
        Ejecuta un comando INSERT, UPDATE o DELETE
        
        Args:
            query: El comando SQL a ejecutar
            params: Tupla de parámetros para el comando
            
        Returns:
            ID insertado (para INSERT) o número de filas afectadas, None si hay error
        """
        connection = Database.connect()
        if not connection:
            return None
        
        cursor = None
        try:
            cursor = connection.cursor()
            sqlite_query = Database._convert_query(query)
            cursor.execute(sqlite_query, params or ())
            connection.commit()
            
            # Si es INSERT, devolver el ID insertado
            if query.strip().upper().startswith('INSERT'):
                return cursor.lastrowid
            # Para UPDATE/DELETE, devolver número de filas afectadas
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error en comando: {e}\nQuery: {query}\nParams: {params}")
            if connection:
                connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
