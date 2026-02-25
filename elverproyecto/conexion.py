import mysql.connector
from mysql.connector import Error

class InventarioDB:
    """Encapsula la conexión y las operaciones básicas contra MySQL.

    Esta clase se utiliza en toda la aplicación CRS para realizar inserciones,
    consultas, eliminaciones, cálculos de horas y, ahora, auditoría de acciones
    administrativas. Al centralizar el acceso a la base de datos evitamos
    dispersión de sentencias SQL y facilitamos la prueba unitaria.

    Convenciones de la clase:
    - Cada método comprueba `self.conexion` antes de ejecutar cualquier
      sentencia. Si la conexión es `None` simplemente retorna un valor
      neutro (False o lista vacía) para evitar excepciones en cascada.
    - Los errores se imprimen en consola; la capa de lógica puede reaccionar
      según el valor de retorno (True/False o lista).
    - Los métodos actuales cubren: asistencias, búsquedas, borrado y reporte
      de horas. Se añade un método para registrar eventos de auditoría.
    """

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

    # -------------------- NUEVA FUNCIONALIDAD: AUDITORÍA --------------------
    def registrar_auditoria(self, usuario, accion, objeto="", detalles=""):
        """Guarda un registro de auditoría en la tabla `auditoria`.

        Parámetros:
            usuario (str): nombre o identificador del admin que realiza la acción.
            accion (str): descripción breve de la operación (login, eliminar, etc.).
            objeto (str): entidad sobre la que se actuó (ej. documento aprendiz).
            detalles (str): cualquier detalle adicional (por qué, condición, etc.).

        RETORNA:
            True si la inserción fue exitosa, False en caso contrario.

        NOTA:
            Asume que existe una tabla `auditoria` con la siguiente estructura:

            CREATE TABLE auditoria (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(50),
                accion VARCHAR(100),
                objeto VARCHAR(100),
                detalles TEXT,
                fecha DATETIME DEFAULT NOW()
            );
        """
        if not self.conexion:
            return False
        try:
            # asegurar que exista la tabla de auditoría (solo la primera vez)
            ddl = ("CREATE TABLE IF NOT EXISTS auditoria ("
                   "id INT AUTO_INCREMENT PRIMARY KEY,"
                   "usuario VARCHAR(50),"
                   "accion VARCHAR(100),"
                   "objeto VARCHAR(100),"
                   "detalles TEXT,"
                   "fecha DATETIME DEFAULT NOW()"
                   ")")
            self.cursor.execute(ddl)
            query = ("INSERT INTO auditoria (usuario, accion, objeto, detalles) "
                     "VALUES (%s, %s, %s, %s)")
            self.cursor.execute(query, (usuario, accion, objeto, detalles))
            self.conexion.commit()
            return True
        except Error as e:
            print(f"Error al registrar auditoría: {e}")
            return False

    def obtener_reporte_horas(self, documento):
        """Calcula el total de horas acumuladas por aprendiz."""
        if not self.conexion: return []
        try:
            # Calcula la diferencia en horas entre entrada y salida
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