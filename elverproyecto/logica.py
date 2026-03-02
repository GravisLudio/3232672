
import pandas as pd
from tkinter import messagebox, filedialog
import datetime

class AsistenciaService:
    def __init__(self, db_conexion):
        
       
        self.db = db_conexion

  
    def registrar_entrada(self, documento):
        
        if not documento:
            return False, "Por favor ingrese un documento."
        
        self.db.cursor.execute("SELECT documento FROM estudiantes WHERE documento=%s", (documento,))
        if not self.db.cursor.fetchone():
            
            self.db.cursor.execute("SELECT documento FROM estudiantes_eliminados WHERE documento=%s", (documento,))
            if self.db.cursor.fetchone():
                return False, "⚠️ El aprendiz está en la PAPELERA. Contacte al administrador."
            return False, "❌ El aprendiz NO existe en el sistema."

        
        self.db.cursor.execute("SELECT id_asistencia FROM asistencias WHERE documento_estudiante=%s AND fecha_salida IS NULL", (documento,))
        if self.db.cursor.fetchone():
            return False, "⚠️ Ya tienes una entrada activa. Debes registrar SALIDA primero."
        
        if self.db.insertar(documento, 1):
            return True, "✅ Entrada Registrada con éxito."
        return False, "❌ Error técnico al conectar con la base de datos."

    def registrar_salida(self, documento):
       
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


    
    def login_aprendiz(self, documento, password):
       
        q = "SELECT * FROM estudiantes WHERE documento=%s AND password=%s"
        self.db.cursor.execute(q, (documento, password))
        return self.db.cursor.fetchone()

    def actualizar_password(self, documento, nueva_pass):
        
        if len(nueva_pass) < 4:
            return False, "La contraseña debe tener al menos 4 caracteres."
        try:
            self.db.cursor.execute("UPDATE estudiantes SET password=%s, cambio_pass=1 WHERE documento=%s", (nueva_pass, documento))
            self.db.conexion.commit()
            return True, "✅ Seguridad actualizada."
        except Exception as e:
            return False, f"Error: {str(e)}"


    
    def obtener_fichas(self):
        
        self.db.cursor.execute("SELECT id_ficha, codigo_ficha, nombre_programa FROM fichas")
        return self.db.cursor.fetchall()

    def guardar_aprendiz_manual(self, datos, id_ficha):

        documento = datos.get("Documento", "").strip()
        
        if not documento or not datos["Nombre Completo"] or not id_ficha:
            return False, "Documento, Nombre y Ficha son campos obligatorios."
        
        if len(documento) > 10:
            return False, "❌ El documento no puede tener más de 10 dígitos."
        
        if not documento.isdigit():
            return False, "❌ El documento debe contener solo números."

        try:
            self.db.cursor.execute(
                "INSERT INTO estudiantes (documento, nombre_completo, correo, id_ficha) VALUES (%s, %s, %s, %s)", 
                (datos["Documento"], datos["Nombre Completo"], datos.get("Correo", ""), id_ficha)
            )
            self.db.conexion.commit()
            return True, "✅ Aprendiz guardado en el sistema."
        
        except Exception as e:
            if "Duplicate entry" in str(e) or "1062" in str(e):
                return False, f"❌ El documento {datos['Documento']} ya se encuentra registrado."
            return False, f"❌ Error al guardar: {str(e)}"

    def importar_excel(self):
       
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")])
        if path:
            try:
                df = pd.read_excel(path) if path.endswith('.xlsx') else pd.read_csv(path)
                
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
        
        try:
            self.db.cursor.execute("DELETE FROM estudiantes_eliminados WHERE documento=%s", (documento,))
            self.db.conexion.commit()
            return True
        except Exception:
            return False

    def obtener_registros_dia(self, documento, fecha):
        
        query = "SELECT * FROM asistencias WHERE documento_estudiante = %s AND DATE(fecha_registro) = %s"
        self.db.cursor.execute(query, (documento, fecha))
        return self.db.cursor.fetchall()