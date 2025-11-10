"""
Módulo para manejo de conexión a la base de datos
"""

import mysql.connector
from mysql.connector import Error
import config


class Database:
    """Clase para gestionar la conexión y operaciones de base de datos"""
    
    @staticmethod
    def connect():
        """Establece conexión con la base de datos"""
        try:
            connection = mysql.connector.connect(**config.DB_CONFIG)
            return connection
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
    
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
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchone() if fetchone else cursor.fetchall()
            return result
        except Error as e:
            print(f"Error en consulta: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
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
        
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            
            # Si es INSERT, devolver el ID insertado
            if query.strip().upper().startswith('INSERT'):
                return cursor.lastrowid
            # Para UPDATE/DELETE, devolver número de filas afectadas
            return cursor.rowcount
        except Error as e:
            print(f"Error en comando: {e}")
            if connection:
                connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
