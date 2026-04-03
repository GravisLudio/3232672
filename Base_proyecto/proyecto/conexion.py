import mysql.connector
from mysql.connector import Error
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class InventarioDB:
    def __init__(self):
        try:
            host = os.getenv('DB_HOST', 'localhost')
            user = os.getenv('DB_USER', 'root')
            password = os.getenv('DB_PASSWORD', '')
            database = os.getenv('DB_NAME', 'TechSenaHSGS')

            self.conexion = mysql.connector.connect(host=host, user=user, password=password, database=database)
            if self.conexion.is_connected():
                self.cursor = self.conexion.cursor(dictionary=True, buffered=True)
                logging.info("Conexión exitosa a la base de datos TechSenaHSGS.")
        except Error as e:
            logging.error(f"Error crítico de conexión HSGS: {e}", exc_info=True)
            self.conexion = None

    def insertar(self, documento, id_competencia, observaciones=""):
        if not self.conexion: return False
        try:
            query = """INSERT INTO asistencias (documento_estudiante, id_competencia, observaciones) 
                       VALUES (%s, %s, %s)"""
            self.cursor.execute(query, (documento, id_competencia, observaciones))
            self.conexion.commit()
            return True
        except Error as e:
            print(f"Error al registrar asistencia: {e}")
            return False

    # ===== CONSULTAS GENERALES =====
    def consultar_todos(self):
        if not self.conexion: return []
        try:
            self.cursor.execute("SELECT * FROM asistencias ORDER BY fecha_registro DESC")
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al consultar historial: {e}")
            return []

    def buscar_por_referencia(self, documento):
        if not self.conexion: return []
        try:
            query = "SELECT * FROM asistencias WHERE documento_estudiante = %s"
            self.cursor.execute(query, (documento,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error en búsqueda individual: {e}")
            return []

    def eliminar(self, id_asistencia):
        if not self.conexion: return False
        try:
            query = "DELETE FROM asistencias WHERE id_asistencia = %s"
            self.cursor.execute(query, (id_asistencia,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar registro: {e}")
            return False

    def cerrar_conexion(self):
        if self.conexion and self.conexion.is_connected():
            self.cursor.close()
            self.conexion.close()
            print("Sesión HSGS finalizada correctamente.")

    # ===== AUDITORÍA =====
    def registrar_auditoria(self, usuario, accion, objeto="", detalles=""):
        if not self.conexion or not self.conexion.is_connected():
            return False
        try:
            query = ("INSERT INTO auditoria (usuario, accion, objeto, detalles) "
                     "VALUES (%s, %s, %s, %s)")
            self.cursor.execute(query, (usuario, accion, objeto, detalles))
            self.conexion.commit()
            return True
        except Error as e:
            print(f"Error al registrar auditoría: {e}")
            return False

    # ===== REPORTES =====
    def obtener_reporte_horas(self, documento):
        if not self.conexion: return []
        try:
            query = """
                SELECT 
                    DATE(fecha_registro) as fecha,
                    fecha_registro as entrada,
                    fecha_salida as salida,
                    ROUND(TIMESTAMPDIFF(MINUTE, fecha_registro, fecha_salida) / 60, 2) as horas
                FROM asistencias 
                WHERE documento_estudiante = %s AND fecha_salida IS NOT NULL
                ORDER BY fecha_registro DESC
            """
            self.cursor.execute(query, (documento,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al obtener reporte: {e}")
            return []
