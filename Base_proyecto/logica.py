import pandas as pd
from tkinter import messagebox, filedialog
import datetime
import logging

# ===== SERVICIO DE ASISTENCIA =====
class AsistenciaService:
    def __init__(self, db_conexion):
        self.db = db_conexion

    # ===== UTILIDADES INTERNAS =====
    def _calcular_dias_habiles(self, fecha_inicio, fecha_fin):
        count = 0
        current = fecha_inicio
        while current <= fecha_fin:
            if current.weekday() < 5:
                count += 1
            current += datetime.timedelta(days=1)
        return count

    def _calcular_sesiones_esperadas(self, horas_totales, fecha_inicio_ficha, fecha_hasta, fecha_desde_rango=None):
        if not fecha_inicio_ficha:
            fecha_inicio_ficha = fecha_desde_rango
        if not fecha_inicio_ficha or fecha_inicio_ficha > fecha_hasta:
            return 0
        dias = self._calcular_dias_habiles(fecha_inicio_ficha, fecha_hasta)
        sesiones_por_horas = horas_totales / 6
        return min(dias, int(sesiones_por_horas))

    # ===== REGISTRO DE ASISTENCIA =====
    def registrar_entrada(self, documento):
        
        if not documento:
            return False, "Por favor ingrese un documento."
        
        self.db.cursor.execute("SELECT documento FROM estudiantes WHERE documento=%s", (documento,))
        if not self.db.cursor.fetchone():
            self.db.cursor.execute("SELECT documento FROM estudiantes_eliminados WHERE documento=%s", (documento,))
            if self.db.cursor.fetchone():
                return False, "El aprendiz está en la PAPELERA. Contacte al administrador."
            return False, "El aprendiz NO existe en el sistema."

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

    # ===== AUTENTICACIÓN =====
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
        self.db.cursor.execute(
            "SELECT id_ficha, codigo_ficha, nombre_programa, jornada FROM fichas ORDER BY codigo_ficha")
        return self.db.cursor.fetchall()

    # ===== GESTIÓN DE APRENDICES =====
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

    # ===== GESTIÓN DE PAPELERA =====
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

    # ===== REGISTROS DE APRENDIZ =====
    def obtener_registros_dia(self, documento, fecha):
        query = "SELECT * FROM asistencias WHERE documento_estudiante = %s AND DATE(fecha_registro) = %s"
        self.db.cursor.execute(query, (documento, fecha))
        return self.db.cursor.fetchall()

    def obtener_registros_mes(self, documento, fecha_inicio, fecha_fin):
        query = """SELECT * FROM asistencias 
                   WHERE documento_estudiante = %s 
                   AND DATE(fecha_registro) >= %s 
                   AND DATE(fecha_registro) <= %s
                   ORDER BY fecha_registro"""
        self.db.cursor.execute(query, (documento, fecha_inicio, fecha_fin))
        return self.db.cursor.fetchall()

    # ===== MÉTRICAS Y REPORTES =====
    def obtener_metricas_reporte_multiple(self, lista_ids, modo, rango, fecha_inicio=None):
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
                    sesiones = self._calcular_sesiones_esperadas(horas, fecha_inicio_ficha, fecha_fin, fecha_inicio)
                else:
                    sesiones = 0
                
                total_sesiones_esperadas += sesiones
                presentes = len(presencias.get(doc, set()))
                faltas = max(0, sesiones - presentes)
                
                total_presencias += presentes
                total_faltas += faltas

            # Solo faltas realmente registradas por instructores
            query_faltas = """
                SELECT tipo_falta, COUNT(*) as total
                FROM faltas
                WHERE fecha_falta BETWEEN %s AND %s
            """
            params_faltas = [fecha_inicio, fecha_fin]
            if lista_ids and modo == "Ficha":
                fmt = ','.join(['%s'] * len(lista_ids))
                query_faltas += f" AND id_ficha IN ({fmt})"
                params_faltas.extend(lista_ids)
            elif lista_ids and modo == "Aprendiz":
                fmt = ','.join(['%s'] * len(lista_ids))
                query_faltas += f" AND documento_estudiante IN ({fmt})"
                params_faltas.extend(lista_ids)
            query_faltas += " GROUP BY tipo_falta"
            self.db.cursor.execute(query_faltas, tuple(params_faltas))

            total_faltas_instructor = 0
            total_retardos_instructor = 0
            for row in self.db.cursor.fetchall():
                if row['tipo_falta'] == 'Retardo':
                    total_retardos_instructor += row['total']
                else:
                    total_faltas_instructor += row['total']

            # Retardos detectados automáticamente (por hora de entrada tardía)
            total_retardos_auto = sum(retardos.values())

            return {
                'expected':          total_sesiones_esperadas,
                'total_asistencias': total_presencias,
                'faltas':            total_faltas_instructor,          # solo las registradas explícitamente
                'retardos':          total_retardos_auto + total_retardos_instructor,
                'detalles':          asistencias_raw,
                'fecha_inicio':      fecha_inicio,
                'fecha_fin':         fecha_fin
            }
        except Exception as e:
            logging.exception(f"Error en obtener_metricas_reporte_multiple: {e}")
            return {'expected': 0, 'total_asistencias': 0, 'faltas': 0, 'retardos': 0, 'detalles': [], 'fecha_inicio': None, 'fecha_fin': None}

    # ===== INSTRUCTORES =====
    def login_instructor(self, usuario, password):
        q = "SELECT * FROM instructores WHERE usuario=%s AND password=%s"
        self.db.cursor.execute(q, (usuario, password))
        return self.db.cursor.fetchone()

    def obtener_fichas_instructor(self, id_instructor):
        query = """SELECT f.id_ficha, f.codigo_ficha, f.nombre_programa, f.jornada
                   FROM fichas f
                   INNER JOIN fichas_asignadas fa ON f.id_ficha = fa.id_ficha
                   WHERE fa.id_instructor = %s"""
        self.db.cursor.execute(query, (id_instructor,))
        return self.db.cursor.fetchall()

    def obtener_estudiantes_ficha(self, id_ficha):
        query = """SELECT e.documento, e.nombre_completo, e.correo, e.id_ficha
                   FROM estudiantes e
                   WHERE e.id_ficha = %s
                   ORDER BY e.nombre_completo"""
        self.db.cursor.execute(query, (id_ficha,))
        return self.db.cursor.fetchall()

    # ===== FALTAS =====
    def registrar_falta(self, documento_estudiante, id_ficha, id_competencia, fecha_falta, 
                       tipo_falta="Inasistencia", razon="", registrado_por=""):
        try:
            query = """INSERT INTO faltas 
                      (documento_estudiante, id_ficha, id_competencia, fecha_falta, tipo_falta, razon, registrado_por)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)
                      ON DUPLICATE KEY UPDATE 
                      tipo_falta=%s, razon=%s, fecha_registro=NOW()"""
            
            self.db.cursor.execute(query, (
                documento_estudiante, id_ficha, id_competencia, fecha_falta, 
                tipo_falta, razon, registrado_por,
                tipo_falta, razon
            ))
            self.db.conexion.commit()
            return True, "✅ Falta registrada correctamente."
        except Exception as e:
            logging.error(f"Error registrando falta: {e}", exc_info=True)
            return False, f"❌ Error: {str(e)[:100]}"

    def eliminar_falta(self, id_falta):
        try:
            self.db.cursor.execute("DELETE FROM faltas WHERE id_falta = %s", (id_falta,))
            self.db.conexion.commit()
            return self.db.cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error eliminando falta: {e}")
            return False

    def obtener_faltas_ficha(self, id_ficha, fecha_inicio=None, fecha_fin=None):
        if fecha_inicio and fecha_fin:
            query = """SELECT f.*, e.nombre_completo, c.nombre_competencia
                       FROM faltas f
                       INNER JOIN estudiantes e ON f.documento_estudiante = e.documento
                       INNER JOIN competencias c ON f.id_competencia = c.id_competencia
                       WHERE f.id_ficha = %s
                       AND f.fecha_falta BETWEEN %s AND %s
                       ORDER BY f.fecha_falta DESC"""
            self.db.cursor.execute(query, (id_ficha, fecha_inicio, fecha_fin))
        else:
            query = """SELECT f.*, e.nombre_completo, c.nombre_competencia
                       FROM faltas f
                       INNER JOIN estudiantes e ON f.documento_estudiante = e.documento
                       INNER JOIN competencias c ON f.id_competencia = c.id_competencia
                       WHERE f.id_ficha = %s
                       ORDER BY f.fecha_falta DESC"""
            self.db.cursor.execute(query, (id_ficha,))
        return self.db.cursor.fetchall()

    def obtener_faltas_estudiante(self, documento_estudiante, id_ficha=None):
        if id_ficha:
            query = """SELECT * FROM faltas WHERE documento_estudiante = %s AND id_ficha = %s
                       ORDER BY fecha_falta DESC"""
            self.db.cursor.execute(query, (documento_estudiante, id_ficha))
        else:
            query = """SELECT * FROM faltas WHERE documento_estudiante = %s
                       ORDER BY fecha_falta DESC"""
            self.db.cursor.execute(query, (documento_estudiante,))
        return self.db.cursor.fetchall()

    def obtener_resumen_faltas(self, id_ficha, fecha_inicio=None, fecha_fin=None):
        """Obtiene un resumen de faltas por tipo para una ficha"""
        if not fecha_inicio:
            fecha_inicio = datetime.date.today().replace(day=1)
        if not fecha_fin:
            fecha_fin = datetime.date.today()
        
        query = """SELECT tipo_falta, COUNT(*) as cantidad
                   FROM faltas
                   WHERE id_ficha = %s
                   AND fecha_falta BETWEEN %s AND %s
                   GROUP BY tipo_falta"""
        self.db.cursor.execute(query, (id_ficha, fecha_inicio, fecha_fin))
        return self.db.cursor.fetchall()

    # ──────────────────────────────────────────────────────────────────────────
    # GESTIÓN DE INSTRUCTORES
    # ──────────────────────────────────────────────────────────────────────────
    def obtener_competencias_por_tipo(self, tipo=None):
        """Retorna competencias filtradas por tipo ('Técnica', 'Complementaria') o todas."""
        if tipo:
            self.db.cursor.execute(
                "SELECT id_competencia, nombre_competencia, horas_totales, Tipo "
                "FROM competencias WHERE Tipo=%s ORDER BY nombre_competencia",
                (tipo,))
        else:
            self.db.cursor.execute(
                "SELECT id_competencia, nombre_competencia, horas_totales, Tipo "
                "FROM competencias ORDER BY Tipo, nombre_competencia")
        return self.db.cursor.fetchall()

    def obtener_instructores(self):
        """Retorna todos los instructores con su competencia principal y fichas asignadas."""
        self.db.cursor.execute("""
            SELECT i.*,
                   c.nombre_competencia AS nombre_especialidad,
                   c.Tipo               AS tipo_especialidad,
                   GROUP_CONCAT(f.codigo_ficha ORDER BY f.codigo_ficha SEPARATOR ', ')
                       AS fichas_asignadas_txt
            FROM instructores i
            LEFT JOIN competencias c ON i.id_competencia_principal = c.id_competencia
            LEFT JOIN fichas_asignadas fa ON i.id_instructor = fa.id_instructor
            LEFT JOIN fichas f ON fa.id_ficha = f.id_ficha
            GROUP BY i.id_instructor
            ORDER BY i.nombre_completo
        """)
        return self.db.cursor.fetchall()

    def crear_instructor(self, datos):
        """
        Crea un nuevo instructor.
        datos: dict con claves documento, nombre_completo, correo, usuario,
               id_competencia_principal, fichas (list of id_ficha),
               comp_complementaria_por_ficha (dict {id_ficha: id_competencia|None})
        Retorna (True, msg) o (False, msg).
        """
        try:
            self.db.cursor.execute(
                """INSERT INTO instructores
                   (documento, nombre_completo, correo, usuario, password,
                    id_competencia_principal, cambio_pass)
                   VALUES (%s,%s,%s,%s,'sena123',%s,0)""",
                (datos['documento'], datos['nombre_completo'], datos.get('correo',''),
                 datos['usuario'], datos.get('id_competencia_principal') or None)
            )
            id_inst = self.db.cursor.lastrowid

            # Asignar fichas
            for id_ficha in datos.get('fichas', []):
                comp_comp = (datos.get('comp_complementaria_por_ficha') or {}).get(id_ficha)
                self.db.cursor.execute(
                    """INSERT IGNORE INTO fichas_asignadas
                       (id_instructor, id_ficha, id_competencia_complementaria)
                       VALUES (%s,%s,%s)""",
                    (id_inst, id_ficha, comp_comp or None)
                )

            self.db.conexion.commit()
            return True, f"Instructor '{datos['nombre_completo']}' creado correctamente."
        except Exception as e:
            self.db.conexion.rollback()
            logging.error(f"Error creando instructor: {e}")
            if "Duplicate entry" in str(e):
                return False, "Ya existe un instructor con ese documento o usuario."
            return False, f"Error al crear instructor: {str(e)[:120]}"

    def actualizar_instructor(self, id_instructor, datos):
        """
        Actualiza datos de un instructor existente y sus fichas asignadas.
        datos: mismas claves que crear_instructor.
        """
        try:
            self.db.cursor.execute(
                """UPDATE instructores SET
                   nombre_completo=%s, correo=%s, usuario=%s,
                   id_competencia_principal=%s
                   WHERE id_instructor=%s""",
                (datos['nombre_completo'], datos.get('correo',''), datos['usuario'],
                 datos.get('id_competencia_principal') or None, id_instructor)
            )

            # Reemplazar fichas asignadas
            self.db.cursor.execute(
                "DELETE FROM fichas_asignadas WHERE id_instructor=%s", (id_instructor,))
            for id_ficha in datos.get('fichas', []):
                comp_comp = (datos.get('comp_complementaria_por_ficha') or {}).get(id_ficha)
                self.db.cursor.execute(
                    """INSERT INTO fichas_asignadas
                       (id_instructor, id_ficha, id_competencia_complementaria)
                       VALUES (%s,%s,%s)""",
                    (id_instructor, id_ficha, comp_comp or None)
                )

            self.db.conexion.commit()
            return True, "Instructor actualizado correctamente."
        except Exception as e:
            self.db.conexion.rollback()
            logging.error(f"Error actualizando instructor: {e}")
            return False, f"Error: {str(e)[:120]}"

    def eliminar_instructor(self, id_instructor):
        """Elimina un instructor y sus asignaciones."""
        try:
            self.db.cursor.execute(
                "DELETE FROM fichas_asignadas WHERE id_instructor=%s", (id_instructor,))
            self.db.cursor.execute(
                "DELETE FROM instructores WHERE id_instructor=%s", (id_instructor,))
            self.db.conexion.commit()
            return True, "Instructor eliminado."
        except Exception as e:
            self.db.conexion.rollback()
            return False, f"Error: {str(e)[:120]}"

    def obtener_fichas_asignadas_instructor(self, id_instructor):
        """Retorna fichas con su competencia complementaria para un instructor."""
        self.db.cursor.execute("""
            SELECT fa.id_ficha, fa.id_competencia_complementaria,
                   f.codigo_ficha, f.nombre_programa, f.jornada,
                   c.nombre_competencia AS nombre_complementaria
            FROM fichas_asignadas fa
            JOIN fichas f ON fa.id_ficha = f.id_ficha
            LEFT JOIN competencias c ON fa.id_competencia_complementaria = c.id_competencia
            WHERE fa.id_instructor = %s
            ORDER BY f.codigo_ficha
        """, (id_instructor,))
        return self.db.cursor.fetchall()