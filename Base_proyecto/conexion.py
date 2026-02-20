import mysql.connector
from mysql.connector import Error

class InventarioDB:
    def __init__(self):
        """Establece la conexión con la base de datos TechSenaHSGS de HSGS."""
        try:
            self.conexion = mysql.connector.connect(
                host='localhost',
                user='root',      # Usuario por defecto en XAMPP/WAMP
                password='',      # Contraseña por defecto (vacía)
                database='TechSenaHSGS' 
            )
            if self.conexion.is_connected():
                # dictionary=True permite acceder a los datos por nombre de columna
                self.cursor = self.conexion.cursor(dictionary=True)
                print("Conexión exitosa a la red HSGS.")
        except Error as e:
            print(f"Error crítico de conexión HSGS: {e}")
            self.conexion = None

    def insertar(self, documento, id_competencia, observaciones=""):
        """Registra una nueva entrada de aprendiz en la tabla asistencias."""
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

    def consultar_todos(self):
        """Retorna el historial completo de ingresos para el panel principal."""
        if not self.conexion: return []
        try:
            # Consulta que ordena por los registros más recientes
            self.cursor.execute("SELECT * FROM asistencias ORDER BY fecha_registro DESC")
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al consultar historial: {e}")
            return []

    def buscar_por_referencia(self, documento):
        """Busca todas las entradas registradas de un aprendiz específico."""
        if not self.conexion: return []
        try:
            query = "SELECT * FROM asistencias WHERE documento_estudiante = %s"
            self.cursor.execute(query, (documento,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error en búsqueda individual: {e}")
            return []

    def eliminar(self, id_asistencia):
        """Elimina un registro de asistencia por su ID único."""
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
        """Finaliza de forma segura la sesión con el servidor."""
        if self.conexion and self.conexion.is_connected():
            self.cursor.close()
            self.conexion.close()
            print("Sesión HSGS finalizada correctamente.")