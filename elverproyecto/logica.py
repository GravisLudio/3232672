import pandas as pd
from tkinter import messagebox, filedialog
import datetime

class AsistenciaService:
    def __init__(self, db_conexion):
        """Inicializa el servicio con la conexión a la base de datos."""
        self.db = db_conexion

    # --- LÓGICA DE ASISTENCIA (TERMINAL) ---
    def registrar_entrada(self, documento):
        """Valida y registra una entrada si no hay una activa."""
        if not documento:
            return False, "Por favor ingrese un documento."
        
        # Validar existencia en tabla activa
        self.db.cursor.execute("SELECT documento FROM estudiantes WHERE documento=%s", (documento,))
        if not self.db.cursor.fetchone():
            # Verificar si está en papelera para dar un aviso más preciso
            self.db.cursor.execute("SELECT documento FROM estudiantes_eliminados WHERE documento=%s", (documento,))
            if self.db.cursor.fetchone():
                return False, "⚠️ El aprendiz está en la PAPELERA. Contacte al administrador."
            return False, "❌ El aprendiz NO existe en el sistema."

        # Validar si ya tiene una entrada abierta (sin fecha de salida)
        self.db.cursor.execute("SELECT id_asistencia FROM asistencias WHERE documento_estudiante=%s AND fecha_salida IS NULL", (documento,))
        if self.db.cursor.fetchone():
            return False, "⚠️ Ya tienes una entrada activa. Debes registrar SALIDA primero."
        
        # Insertar registro (id_competencia 1 por defecto según BD)
        if self.db.insertar(documento, 1):
            return True, "✅ Entrada Registrada con éxito."
        return False, "❌ Error técnico al conectar con la base de datos."

    def registrar_salida(self, documento):
        """Cierra una sesión de asistencia activa."""
        if not documento:
            return False, "Por favor ingrese un documento."

        self.db.cursor.execute("SELECT id_asistencia FROM asistencias WHERE documento_estudiante=%s AND fecha_salida IS NULL", (documento,))
        res = self.db.cursor.fetchone()
        
        if res:
            try:
                self.db.cursor.execute("UPDATE asistencias SET fecha_salida=NOW() WHERE id_asistencia=%s", (res['id_asistencia'],))
                self.db.conexion.commit()
                return True, "✅ Salida Registrada correctamente."
            except Exception as e:
                return False, f"❌ Error al actualizar salida: {str(e)}"
        else:
            return False, "❌ No tienes una entrada pendiente para cerrar."

    # --- LÓGICA DE USUARIO Y SEGURIDAD ---
    def login_aprendiz(self, documento, password):
        """Verifica credenciales del aprendiz."""
        q = "SELECT * FROM estudiantes WHERE documento=%s AND password=%s"
        self.db.cursor.execute(q, (documento, password))
        return self.db.cursor.fetchone()

    def actualizar_password(self, documento, nueva_pass):
        """Actualiza la contraseña y marca el cambio como realizado."""
        if len(nueva_pass) < 4:
            return False, "La contraseña debe tener al menos 4 caracteres."
        try:
            # En la tabla estudiantes debe existir la columna cambio_pass (tinyint)
            self.db.cursor.execute("UPDATE estudiantes SET password=%s, cambio_pass=1 WHERE documento=%s", (nueva_pass, documento))
            self.db.conexion.commit()
            return True, "✅ Seguridad actualizada."
        except Exception as e:
            return False, f"Error: {str(e)}"

    # --- LÓGICA ADMINISTRATIVA ---
    def obtener_fichas(self):
        """Carga las fichas disponibles para el registro."""
        self.db.cursor.execute("SELECT id_ficha, codigo_ficha, nombre_programa FROM fichas")
        return self.db.cursor.fetchall()

    def guardar_aprendiz_manual(self, datos, id_ficha):
        """Guarda un nuevo aprendiz validando integridad de datos."""
        if not datos["Documento"] or not datos["Nombre Completo"] or not id_ficha:
            return False, "Documento, Nombre y Ficha son campos obligatorios."
        try:
            self.db.cursor.execute(
                "INSERT INTO estudiantes (documento, nombre_completo, correo, id_ficha) VALUES (%s, %s, %s, %s)", 
                (datos["Documento"], datos["Nombre Completo"], datos.get("Correo", ""), id_ficha)
            )
            self.db.conexion.commit()
            return True, "✅ Aprendiz guardado en el sistema."
        except Exception as e:
            return False, f"❌ Error al guardar: {str(e)}"

    def importar_excel(self):
        """Procesa archivos Excel/CSV para carga masiva."""
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")])
        if path:
            try:
                df = pd.read_excel(path) if path.endswith('.xlsx') else pd.read_csv(path)
                # Requiere columnas: documento, nombre_completo, correo, id_ficha
                count = 0
                for _, r in df.iterrows():
                    self.db.cursor.execute(
                        "INSERT IGNORE INTO estudiantes (documento, nombre_completo, correo, id_ficha) VALUES (%s, %s, %s, %s)", 
                        (r['documento'], r['nombre_completo'], r['correo'], r['id_ficha'])
                    )
                    count += 1
                self.db.conexion.commit()
                messagebox.showinfo("C.R.G", f"✅ Importación finalizada. Se procesaron {count} registros.")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al leer el archivo: {str(e)}")
                return False
        return False

    def mandar_a_papelera(self, documento):
        """Mueve un estudiante a eliminados preservando su información."""
        try:
            self.db.cursor.execute(
                "INSERT INTO estudiantes_eliminados (documento, nombre_completo, correo, id_ficha) "
                "SELECT documento, nombre_completo, correo, id_ficha FROM estudiantes WHERE documento=%s", 
                (documento,)
            )
            self.db.cursor.execute("DELETE FROM estudiantes WHERE documento=%s", (documento,))
            self.db.conexion.commit()
            return True
        except Exception:
            return False

    def restaurar_aprendiz(self, documento):
        """Recupera un aprendiz de la papelera."""
        try:
            self.db.cursor.execute(
                "INSERT INTO estudiantes (documento, nombre_completo, correo, id_ficha) "
                "SELECT documento, nombre_completo, correo, id_ficha FROM estudiantes_eliminados WHERE documento=%s", 
                (documento,)
            )
            self.db.cursor.execute("DELETE FROM estudiantes_eliminados WHERE documento=%s", (documento,))
            self.db.conexion.commit()
            return True
        except Exception:
            return False

    def eliminar_permanente(self, documento):
        """Borrado definitivo de la base de datos."""
        try:
            self.db.cursor.execute("DELETE FROM estudiantes_eliminados WHERE documento=%s", (documento,))
            self.db.conexion.commit()
            return True
        except Exception:
            return False

    def obtener_registros_dia(self, documento, fecha):
        """Consulta asistencias para el calendario del aprendiz."""
        query = "SELECT * FROM asistencias WHERE documento_estudiante = %s AND DATE(fecha_registro) = %s"
        self.db.cursor.execute(query, (documento, fecha))
        return self.db.cursor.fetchall()