
import pandas as pd
from tkinter import messagebox, filedialog
import datetime
import logging

class AsistenciaService:
    def __init__(self, db_conexion):
        
       
        self.db = db_conexion

    def _calcular_dias_habiles(self, fecha_inicio, fecha_fin):
        """Calcula número de días hábiles (lunes-viernes) entre dos fechas (inclusive)."""
        count = 0
        current = fecha_inicio
        while current <= fecha_fin:
            # 0=lunes, 4=viernes, 5=sábado, 6=domingo
            if current.weekday() < 5:
                count += 1
            current += datetime.timedelta(days=1)
        return count

    def _calcular_sesiones_esperadas(self, horas_totales, fecha_inicio_ficha, fecha_hasta):
        """
        Calcula el número de sesiones esperadas (de 6 horas).
        Toma en cuenta solo días hábiles desde fecha_inicio_ficha hasta fecha_hasta.
        """
        if not fecha_inicio_ficha or fecha_inicio_ficha > fecha_hasta:
            return 0
        dias = self._calcular_dias_habiles(fecha_inicio_ficha, fecha_hasta)
        # 1 sesión = 6 horas
        sesiones_por_horas = horas_totales / 6
        # Limitar sesiones esperadas al número de días disponibles
        return min(dias, int(sesiones_por_horas))

  
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
        except Exception as ex:
            logging.error(f"Error al mover a papelera {documento}: {ex}", exc_info=True)
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
        except Exception as ex:
            logging.error(f"Error al restaurar aprendiz {documento}: {ex}", exc_info=True)
            return False

    def eliminar_permanente(self, documento):
        
        try:
            self.db.cursor.execute("DELETE FROM estudiantes_eliminados WHERE documento=%s", (documento,))
            self.db.conexion.commit()
            return True
        except Exception as ex:
            logging.error(f"Error al eliminar permanentemente {documento}: {ex}", exc_info=True)
            return False

    def obtener_registros_dia(self, documento, fecha):
        
        query = "SELECT * FROM asistencias WHERE documento_estudiante = %s AND DATE(fecha_registro) = %s"
        self.db.cursor.execute(query, (documento, fecha))
        return self.db.cursor.fetchall()

    
    def obtener_metricas_reporte_multiple(self, lista_ids, modo, rango, fecha_inicio=None):
        """
        Calcula métricas de asistencia con base en:
        - Sesiones esperadas = días hábiles * horas_competencia / 6
        - Asistencia = estudiante registró entrada
        - Falta = sesión esperada sin entrada
        - Retardo = entrada después de hora teórica
        """
        try:
            # Normalizar fecha_inicio
            if fecha_inicio:
                if isinstance(fecha_inicio, datetime.datetime):
                    fecha_inicio = fecha_inicio.date()
                if isinstance(fecha_inicio, str):
                    try:
                        fecha_inicio = datetime.datetime.fromisoformat(fecha_inicio).date()
                    except Exception:
                        fecha_inicio = datetime.date.today()
            else:
                hoy = datetime.date.today()
                if rango == "Día":
                    fecha_inicio = hoy
                elif rango == "Semana":
                    fecha_inicio = hoy - datetime.timedelta(days=hoy.weekday())
                else:  # Mes
                    fecha_inicio = hoy.replace(day=1)

            # Calcular fecha_fin según rango
            if rango == "Día":
                fecha_fin = fecha_inicio
            elif rango == "Semana":
                fecha_fin = fecha_inicio + datetime.timedelta(days=6)
            else:  # Mes
                import calendar as _cal
                last = _cal.monthrange(fecha_inicio.year, fecha_inicio.month)[1]
                fecha_fin = datetime.date(fecha_inicio.year, fecha_inicio.month, last)

            # Obtener estudiantes a analizar
            if lista_ids and modo == "Ficha":
                fmt = ','.join(['%s'] * len(lista_ids))
                self.db.cursor.execute(
                    f"SELECT documento, id_ficha FROM estudiantes WHERE id_ficha IN ({fmt})",
                    tuple(lista_ids)
                )
                estudiantes = self.db.cursor.fetchall()
            elif lista_ids and modo == "Aprendiz":
                fmt = ','.join(['%s'] * len(lista_ids))
                self.db.cursor.execute(
                    f"SELECT documento, id_ficha FROM estudiantes WHERE documento IN ({fmt})",
                    tuple(lista_ids)
                )
                estudiantes = self.db.cursor.fetchall()
            else:
                self.db.cursor.execute("SELECT documento, id_ficha FROM estudiantes")
                estudiantes = self.db.cursor.fetchall()

            # Mapear fichas para obtener horas y fecha_inicio
            ids_ficha = set(e['id_ficha'] for e in estudiantes if e['id_ficha'])
            fichas_data = {}
            if ids_ficha:
                fmt = ','.join(['%s'] * len(ids_ficha))
                # Obtener fichas con suma de horas de sus competencias
                self.db.cursor.execute(
                    f"SELECT f.id_ficha, f.fecha_inicio, f.jornada, COALESCE(SUM(c.horas_totales), 0) as horas "
                    f"FROM fichas f "
                    f"LEFT JOIN ficha_competencias fc ON f.id_ficha = fc.id_ficha "
                    f"LEFT JOIN competencias c ON fc.id_competencia = c.id_competencia "
                    f"WHERE f.id_ficha IN ({fmt}) "
                    f"GROUP BY f.id_ficha",
                    tuple(ids_ficha)
                )
                for row in self.db.cursor.fetchall():
                    fid = row['id_ficha']
                    fichas_data[fid] = {
                        'horas': row.get('horas', 0) or 0,
                        'fecha_inicio': row.get('fecha_inicio'),
                        'jornada': row.get('jornada', 'Mañana')
                    }

            # Obtener asistencias en el rango
            query = """
                SELECT a.documento_estudiante, DATE(a.fecha_registro) as fecha_dia, 
                       HOUR(a.fecha_registro) as hora_num, MINUTE(a.fecha_registro) as minuto_num
                FROM asistencias a
                WHERE DATE(a.fecha_registro) BETWEEN %s AND %s
            """
            params = [fecha_inicio, fecha_fin]
            if lista_ids and modo == "Ficha":
                fmt = ','.join(['%s'] * len(lista_ids))
                query += f" AND a.documento_estudiante IN (SELECT documento FROM estudiantes WHERE id_ficha IN ({fmt}))"
                params.extend(lista_ids)
            elif lista_ids and modo == "Aprendiz":
                fmt = ','.join(['%s'] * len(lista_ids))
                query += f" AND a.documento_estudiante IN ({fmt})"
                params.extend(lista_ids)

            self.db.cursor.execute(query, tuple(params))
            asistencias_raw = self.db.cursor.fetchall()

            # Agrupar asistencias por documento y fecha
            presencias = {}  # {documento: set(fechas)}
            retardos = {}    # {documento: count}
            for row in asistencias_raw:
                doc = row['documento_estudiante']
                fecha = row['fecha_dia']
                hora_num = row['hora_num'] or 0
                minuto_num = row['minuto_num'] or 0
                
                if doc not in presencias:
                    presencias[doc] = set()
                    retardos[doc] = 0
                
                presencias[doc].add(fecha)
                
                # Detectar retardo según jornada
                ficha_id = next((e['id_ficha'] for e in estudiantes if e['documento'] == doc), None)
                if ficha_id and ficha_id in fichas_data:
                    jornada = fichas_data[ficha_id]['jornada']
                    # Umbrales en minutos desde medianoche para comparación segura
                    umbrales = {
                        'Mañana': (8, 15),      # 08:15
                        'Tarde': (13, 15),      # 13:15
                        'Noche': (18, 15),      # 18:15
                        'Mixta': (8, 15)        # 08:15
                    }
                    umbral_h, umbral_m = umbrales.get(jornada, (8, 15))
                    # Convertir entrada y umbral a minutos desde medianoche
                    entrada_minutos = hora_num * 60 + minuto_num
                    umbral_minutos = umbral_h * 60 + umbral_m
                    # Si entrada > umbral, es retardo
                    if entrada_minutos > umbral_minutos:
                        retardos[doc] += 1

            # Calcular sesiones esperadas y faltas
            total_sesiones_esperadas = 0
            total_presencias = 0
            total_faltas = 0
            total_retardos = sum(retardos.values())

            for est in estudiantes:
                doc = est['documento']
                fid = est['id_ficha']
                
                if fid and fid in fichas_data:
                    ficha = fichas_data[fid]
                    fecha_inicio_ficha = ficha['fecha_inicio']
                    horas = ficha['horas']
                    sesiones = self._calcular_sesiones_esperadas(horas, fecha_inicio_ficha, fecha_fin)
                else:
                    sesiones = 0
                
                total_sesiones_esperadas += sesiones
                presentes = len(presencias.get(doc, set()))
                faltas = max(0, sesiones - presentes)
                
                total_presencias += presentes
                total_faltas += faltas

            return {
                'expected': total_sesiones_esperadas,
                'total_asistencias': total_presencias,
                'faltas': total_faltas,
                'retardos': total_retardos,
                'detalles': asistencias_raw,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            }
        except Exception as e:
            logging.exception(f"Error en obtener_metricas_reporte_multiple: {e}")
            return {'expected': 0, 'total_asistencias': 0, 'faltas': 0, 'retardos': 0, 'detalles': [], 'fecha_inicio': None, 'fecha_fin': None}