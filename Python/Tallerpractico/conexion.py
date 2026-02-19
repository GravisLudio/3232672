import mysql.connector
from mysql.connector import Error

class InventarioDB:
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='TechSenaHSGS'
            )
            if self.conexion.is_connected():
                self.cursor = self.conexion.cursor(dictionary=True)
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conexion = None

    def insertar(self, referencia, descripcion, marca, stock, costo):
        if not self.conexion: return False
        try:
            query = "INSERT INTO inventario (referencia, descripcion, marca, stock, costo_unitario) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (referencia, descripcion, marca, stock, costo))
            self.conexion.commit()
            return True
        except Error as e:
            print(f"Error al insertar: {e}")
            return False

    def consultar_todos(self):
        if not self.conexion: return []
        try:
            self.cursor.execute("SELECT * FROM inventario")
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al consultar: {e}")
            return []

    def buscar_por_referencia(self, referencia):
        if not self.conexion: return []
        try:
            query = "SELECT * FROM inventario WHERE referencia = %s"
            self.cursor.execute(query, (referencia,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al buscar: {e}")
            return []

    def eliminar(self, referencia):
        if not self.conexion: return False
        try:
            query = "DELETE FROM inventario WHERE referencia = %s"
            self.cursor.execute(query, (referencia,))
            self.conexion.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar: {e}")
            return False

    def cerrar_conexion(self):
        if self.conexion and self.conexion.is_connected():
            self.cursor.close()
            self.conexion.close()

    def mover_a_historial(self, referencia):
        if not self.conexion: return False
        try:
            producto = self.buscar_por_referencia(referencia)
            if producto:
                p = producto[0]
                query = """INSERT INTO historial_eliminados 
                           (id_item, referencia, descripcion, marca, stock, costo_unitario) 
                           VALUES (%s, %s, %s, %s, %s, %s)"""
                self.cursor.execute(query, (p['id_item'], p['referencia'], p['descripcion'], p['marca'], p['stock'], p['costo_unitario']))
                self.conexion.commit()
                return True
        except Error as e:
            print(f"Error al mover a historial: {e}")
        return False

    def consultar_historial(self):
        if not self.conexion: return []
        self.cursor.execute("SELECT * FROM historial_eliminados")
        return self.cursor.fetchall()

    def restaurar_producto(self, referencia):
        try:
            self.cursor.execute("SELECT * FROM historial_eliminados WHERE referencia = %s", (referencia,))
            p = self.cursor.fetchone()
            if p:
                self.insertar(p['referencia'], p['descripcion'], p['marca'], p['stock'], p['costo_unitario'])
                self.cursor.execute("DELETE FROM historial_eliminados WHERE referencia = %s", (referencia,))
                self.conexion.commit()
                return True
        except Error as e:
            print(f"Error al restaurar: {e}")
        return False