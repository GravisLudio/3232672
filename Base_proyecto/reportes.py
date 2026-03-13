"""
Módulo ReportesManager — CRS 2.0
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from config import COLORES
import datetime
import calendar as _cal
import logging


class ReportesManager:
    """Gestiona reportes de asistencia con diseño CRS 2.0."""

    def __init__(self, app, db, servicio):
        self.app      = app
        self.db       = db
        self.servicio = servicio
        self.GREEN  = COLORES['SENA_GREEN']
        self.ORANGE = COLORES['SENA_ORANGE']
        self.DARK   = COLORES['SENA_DARK']

        self.modo_filtro         = tk.StringVar(value="Ficha")
        self.items_seleccionados = []
        self.combo_vals          = []
        self.last_rows           = []
        self.last_params         = None
        self.reporte_fecha_inicio = None

        # refs UI
        self.combo_seleccion = None
        self.lbl_seleccionados = None
        self.seg_tiempo      = None
        self.selector_frame  = None
        self.tv_rep          = None
        self.canvas_chart    = None
        self.btn_exportar    = None
        self.lbl_c_asist = self.lbl_c_faltas = self.lbl_c_ret = self.lbl_c_pct = None

    # ─────────────────────────────────────────────────────────────────────────
    # CONSTRUCCIÓN DE PESTAÑA
    # ─────────────────────────────────────────────────────────────────────────
    def crear_pestana_reportes(self, parent):
        scroll = ctk.CTkScrollableFrame(parent, fg_color=COLORES['BG_LIGHT'])
        scroll.pack(fill="both", expand=True)

        # ── Panel de filtros ─────────────────────────────────────────────────
        f_fil = ctk.CTkFrame(scroll, fg_color="white", corner_radius=12,
                             border_width=1, border_color="#E0E0E0")
        f_fil.pack(fill="x", padx=22, pady=(14, 6))

        ctk.CTkLabel(f_fil, text="🔎  Filtros del Reporte",
                    font=("Segoe UI", 12, "bold"),
                    text_color=self.DARK).pack(anchor="w", padx=16, pady=(10, 4))

        # Fila 1: modo + combo + añadir/limpiar
        r1 = ctk.CTkFrame(f_fil, fg_color="transparent")
        r1.pack(fill="x", padx=16, pady=(0, 4))

        ctk.CTkLabel(r1, text="Filtrar por:", font=("Segoe UI", 11)).pack(side="left", padx=(0,6))
        rf = ctk.CTkFrame(r1, fg_color="transparent")
        rf.pack(side="left", padx=(0,18))
        ctk.CTkRadioButton(rf, text="Fichas",     variable=self.modo_filtro, value="Ficha",
                           command=self.cambiar_modo).pack(side="left", padx=4)
        ctk.CTkRadioButton(rf, text="Aprendices", variable=self.modo_filtro, value="Aprendiz",
                           command=self.cambiar_modo).pack(side="left", padx=4)

        ctk.CTkLabel(r1, text="Seleccionar:", font=("Segoe UI", 11)).pack(side="left", padx=(0,6))
        self.combo_seleccion = ttk.Combobox(r1, state="normal", width=34)
        self.combo_seleccion.pack(side="left", padx=(0,6))

        ctk.CTkButton(r1, text="＋ Añadir", width=90, height=32,
                     fg_color=self.GREEN, hover_color=self.DARK,
                     font=("Segoe UI", 11, "bold"),
                     command=self.agregar_item).pack(side="left", padx=(0,6))
        ctk.CTkButton(r1, text="✖ Limpiar", width=80, height=32,
                     fg_color="#E74C3C", hover_color="#C0392B",
                     font=("Segoe UI", 11),
                     command=self.limpiar_items).pack(side="left")

        self.lbl_seleccionados = ctk.CTkLabel(f_fil, text="Seleccionados: Ninguno",
                                              font=("Segoe UI", 10, "italic"),
                                              text_color="#888")
        self.lbl_seleccionados.pack(anchor="w", padx=16, pady=(0,4))

        # Fila 2: rango + selector fecha + generar/exportar
        r2 = ctk.CTkFrame(f_fil, fg_color="transparent")
        r2.pack(fill="x", padx=16, pady=(0, 12))

        ctk.CTkLabel(r2, text="Rango:", font=("Segoe UI", 11)).pack(side="left", padx=(0,6))
        self.seg_tiempo = ctk.CTkSegmentedButton(
            r2, values=["Día", "Semana", "Mes"],
            command=self._rebuild_selector,
            selected_color=self.GREEN, selected_hover_color=self.DARK,
            font=("Segoe UI", 11))
        self.seg_tiempo.set("Mes")
        self.seg_tiempo.pack(side="left", padx=(0,16))

        self.selector_frame = ctk.CTkFrame(r2, fg_color="transparent")
        self.selector_frame.pack(side="left", fill="x", expand=True)

        self.btn_exportar = ctk.CTkButton(r2, text="⬇ Exportar", height=36, width=110,
                                          fg_color="#888", hover_color="#666",
                                          font=("Segoe UI", 11), state="disabled",
                                          command=self.exportar)
        self.btn_exportar.pack(side="right")

        ctk.CTkButton(r2, text="📊  GENERAR REPORTE", height=36, width=185,
                     fg_color=self.ORANGE, hover_color="#C25A0D",
                     font=("Segoe UI", 12, "bold"),
                     command=self.generar).pack(side="right", padx=(0,8))

        # ── Tarjetas de resumen ──────────────────────────────────────────────
        f_cards = ctk.CTkFrame(scroll, fg_color="transparent")
        f_cards.pack(fill="x", padx=22, pady=(0, 6))

        self.lbl_c_asist  = self._make_card(f_cards, "✅ Asistencias",  self.GREEN)
        self.lbl_c_faltas = self._make_card(f_cards, "❌ Faltas",        "#E74C3C")
        self.lbl_c_ret    = self._make_card(f_cards, "⏰ Retardos",      "#E67E22")
        self.lbl_c_pct    = self._make_card(f_cards, "📈 % Promedio",   "#3A7FF6")

        # ── Gráfico ──────────────────────────────────────────────────────────
        f_chart = ctk.CTkFrame(scroll, fg_color="white", corner_radius=12,
                               border_width=1, border_color="#E0E0E0")
        f_chart.pack(fill="x", padx=22, pady=(0, 6))

        ctk.CTkLabel(f_chart, text="📊  Porcentaje de Asistencia por Estudiante",
                    font=("Segoe UI", 11, "bold"),
                    text_color=self.DARK).pack(anchor="w", padx=14, pady=(10,2))

        self.canvas_chart = tk.Canvas(f_chart, bg="white", height=230,
                                      highlightthickness=0)
        self.canvas_chart.pack(fill="x", padx=14, pady=(0,12))
        self._chart_placeholder()

        # ── Tabla detalle ────────────────────────────────────────────────────
        f_tabla = ctk.CTkFrame(scroll, fg_color="white", corner_radius=12,
                               border_width=1, border_color="#E0E0E0")
        f_tabla.pack(fill="both", expand=True, padx=22, pady=(0, 18))

        hdr = ctk.CTkFrame(f_tabla, fg_color="transparent")
        hdr.pack(fill="x", padx=14, pady=(10,4))
        ctk.CTkLabel(hdr, text="📋  Detalle por Estudiante",
                    font=("Segoe UI", 11, "bold"),
                    text_color=self.DARK).pack(side="left")
        self.lbl_total = ctk.CTkLabel(hdr, text="", font=("Segoe UI", 10),
                                      text_color="#888")
        self.lbl_total.pack(side="right")

        cols = ("Estudiante", "Documento", "Ficha", "Asistencias", "Faltas", "Retardos", "% Asist.")
        f_tree = tk.Frame(f_tabla, bg="white")
        f_tree.pack(fill="both", expand=True, padx=12, pady=(0,12))

        st = ttk.Style()
        st.configure("CRS.Treeview",
                     font=("Segoe UI", 10), rowheight=26,
                     background="white", foreground="#2C3E50",
                     fieldbackground="white")
        st.configure("CRS.Treeview.Heading",
                     font=("Segoe UI", 10, "bold"),
                     background=self.GREEN, foreground="white")
        st.map("CRS.Treeview",
               background=[("selected", self.GREEN)],
               foreground=[("selected", "white")])

        self.tv_rep = ttk.Treeview(f_tree, columns=cols, show="headings",
                                   height=10, style="CRS.Treeview")
        ancho = {"Estudiante":215,"Documento":115,"Ficha":90,
                 "Asistencias":100,"Faltas":75,"Retardos":85,"% Asist.":85}
        for col in cols:
            self.tv_rep.heading(col, text=col,
                               command=lambda c=col: self._sort(c))
            self.tv_rep.column(col, width=ancho[col], anchor="center")

        vsb = ttk.Scrollbar(f_tree, orient="vertical", command=self.tv_rep.yview)
        self.tv_rep.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tv_rep.pack(side="left", fill="both", expand=True)

        self.tv_rep.tag_configure("rojo",     background="#FFE8E8", foreground="#C0392B")
        self.tv_rep.tag_configure("amarillo", background="#FFF8E0", foreground="#D68910")
        self.tv_rep.tag_configure("verde",    background="#F0FFF4", foreground="#1E8449")

        # Inicializar
        self.cambiar_modo()
        self._rebuild_selector("Mes")

    def _make_card(self, parent, titulo, color):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12,
                           border_width=1, border_color="#EBEBEB")
        card.pack(side="left", fill="both", expand=True, padx=4)
        barra = ctk.CTkFrame(card, fg_color=color, height=5, corner_radius=6)
        barra.pack(fill="x", padx=5, pady=(5,0))
        ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 10),
                    text_color="#999").pack(pady=(8,2))
        lbl = ctk.CTkLabel(card, text="—", font=("Segoe UI", 28, "bold"),
                          text_color=color)
        lbl.pack(pady=(0,10))
        return lbl

    def _chart_placeholder(self):
        self.canvas_chart.delete("all")
        W = 860
        self.canvas_chart.create_text(W//2, 115,
            text="Genera un reporte para ver el gráfico",
            fill="#CCCCCC", font=("Segoe UI", 12))

    # ─────────────────────────────────────────────────────────────────────────
    # FILTROS
    # ─────────────────────────────────────────────────────────────────────────
    def cambiar_modo(self):
        self.limpiar_items()
        if self.modo_filtro.get() == "Ficha":
            fichas = self.servicio.obtener_fichas()
            data = [f"{f['id_ficha']} | {f['codigo_ficha']} - {f['nombre_programa']}"
                   for f in fichas]
        else:
            self.db.cursor.execute(
                "SELECT documento, nombre_completo FROM estudiantes ORDER BY nombre_completo")
            data = [f"{e['documento']} | {e['nombre_completo']}"
                   for e in self.db.cursor.fetchall()]
        self.combo_vals = data
        self.combo_seleccion['values'] = data
        self.combo_seleccion.set("Seleccione...")
        self.combo_seleccion.bind('<KeyRelease>', self._filtrar_combo)

    def _filtrar_combo(self, e=None):
        txt = self.combo_seleccion.get().lower()
        self.combo_seleccion['values'] = [v for v in self.combo_vals if txt in v.lower()]

    def agregar_item(self):
        item = self.combo_seleccion.get()
        if item and item != "Seleccione..." and item not in self.items_seleccionados:
            self.items_seleccionados.append(item)
            ids = [i.split(" | ")[0] for i in self.items_seleccionados]
            self.lbl_seleccionados.configure(text=f"Seleccionados: {', '.join(ids)}")

    def limpiar_items(self):
        self.items_seleccionados = []
        if self.lbl_seleccionados:
            self.lbl_seleccionados.configure(text="Seleccionados: Ninguno")

    def _rebuild_selector(self, rango=None):
        if rango is None:
            rango = self.seg_tiempo.get() if self.seg_tiempo else "Mes"
        for w in self.selector_frame.winfo_children():
            w.destroy()
        self.reporte_fecha_inicio = None

        if rango == "Día":
            try:
                from tkcalendar import Calendar
                cal = Calendar(self.selector_frame, selectmode='day', locale='es_ES',
                              background=self.GREEN, headersbackground=self.DARK,
                              font=("Segoe UI", 9))
                cal.pack(padx=4, pady=2)
                try:
                    self.reporte_fecha_inicio = cal.selection_get()
                except Exception:
                    self.reporte_fecha_inicio = datetime.date.today()
                def on_cal(e=None):
                    try:
                        self.reporte_fecha_inicio = cal.selection_get()
                    except Exception:
                        self.reporte_fecha_inicio = datetime.date.today()
                cal.bind("<<CalendarSelected>>", on_cal)
            except ImportError:
                # fallback: entry manual
                ctk.CTkLabel(self.selector_frame, text="Fecha (DD/MM/YYYY):",
                            font=("Segoe UI", 11)).pack(side="left", padx=(0,6))
                entry = ctk.CTkEntry(self.selector_frame, width=120, height=32)
                entry.insert(0, datetime.date.today().strftime('%d/%m/%Y'))
                entry.pack(side="left")
                self.reporte_fecha_inicio = datetime.date.today()
                def on_entry(e=None):
                    try:
                        self.reporte_fecha_inicio = datetime.datetime.strptime(
                            entry.get(), '%d/%m/%Y').date()
                    except Exception:
                        pass
                entry.bind("<FocusOut>", on_entry)

        elif rango == "Semana":
            hoy = datetime.date.today()
            semanas, self._week_map = [], {}
            for i in range(104):
                ini = hoy - datetime.timedelta(days=hoy.weekday()) - datetime.timedelta(weeks=i)
                fin = ini + datetime.timedelta(days=6)
                lbl = (f"{ini.isocalendar()[0]}-W{ini.isocalendar()[1]:02d}  "
                       f"{ini.strftime('%d/%m/%Y')} → {fin.strftime('%d/%m/%Y')}")
                semanas.append(lbl)
                self._week_map[lbl] = ini
            cb = ttk.Combobox(self.selector_frame, values=semanas, state="readonly", width=42)
            cb.pack(padx=4, pady=4)
            cb.set(semanas[0])
            self.reporte_fecha_inicio = self._week_map[semanas[0]]
            def on_w(e=None):
                self.reporte_fecha_inicio = self._week_map.get(cb.get(), datetime.date.today())
            cb.bind("<<ComboboxSelected>>", on_w)

        else:  # Mes
            hoy = datetime.date.today()
            meses, self._month_map = [], {}
            for m in range(36):
                total_meses = hoy.year * 12 + (hoy.month - 1) - m
                y  = total_meses // 12
                mo = total_meses % 12 + 1
                ini = datetime.date(y, mo, 1)
                lbl = ini.strftime("%B %Y").capitalize()
                meses.append(lbl)
                self._month_map[lbl] = ini
            cb = ttk.Combobox(self.selector_frame, values=meses, state="readonly", width=20)
            cb.pack(padx=4, pady=4)
            cb.set(meses[0])
            self.reporte_fecha_inicio = self._month_map[meses[0]]
            def on_m(e=None):
                self.reporte_fecha_inicio = self._month_map.get(cb.get(), datetime.date.today())
            cb.bind("<<ComboboxSelected>>", on_m)

    # ─────────────────────────────────────────────────────────────────────────
    # GENERACIÓN
    # ─────────────────────────────────────────────────────────────────────────
    def generar(self):
        if not self.items_seleccionados:
            messagebox.showwarning("Reporte", "Selecciona al menos una ficha o aprendiz.")
            return

        ids   = [i.split(" | ")[0] for i in self.items_seleccionados]
        modo  = self.modo_filtro.get()
        rango = self.seg_tiempo.get()
        fi    = self.reporte_fecha_inicio or datetime.date.today()

        if rango == "Día":
            ff = fi
        elif rango == "Semana":
            ff = fi + datetime.timedelta(days=6)
        else:
            last = _cal.monthrange(fi.year, fi.month)[1]
            ff = datetime.date(fi.year, fi.month, last)

        filas = self._calcular(ids, modo, fi, ff)
        if not filas:
            messagebox.showinfo("Reporte", "No hay datos para el período seleccionado.")
            return

        self.last_rows   = filas
        self.last_params = (ids, modo, rango, fi, ff)

        self._refresh_tarjetas(filas)
        self._refresh_tabla(filas)
        self._refresh_grafico(filas, fi, ff, rango)
        self.btn_exportar.configure(state="normal",
                                    fg_color="#3A7FF6", hover_color="#2563EB")

    def _calcular(self, ids, modo, fi, ff):
        if ids and modo == "Ficha":
            fmt = ','.join(['%s'] * len(ids))
            self.db.cursor.execute(
                f"SELECT e.documento, e.nombre_completo, e.id_ficha, f.codigo_ficha "
                f"FROM estudiantes e JOIN fichas f ON e.id_ficha=f.id_ficha "
                f"WHERE e.id_ficha IN ({fmt})", tuple(ids))
        elif ids and modo == "Aprendiz":
            fmt = ','.join(['%s'] * len(ids))
            self.db.cursor.execute(
                f"SELECT e.documento, e.nombre_completo, e.id_ficha, f.codigo_ficha "
                f"FROM estudiantes e JOIN fichas f ON e.id_ficha=f.id_ficha "
                f"WHERE e.documento IN ({fmt})", tuple(ids))
        else:
            self.db.cursor.execute(
                "SELECT e.documento, e.nombre_completo, e.id_ficha, f.codigo_ficha "
                "FROM estudiantes e JOIN fichas f ON e.id_ficha=f.id_ficha")
        estudiantes = self.db.cursor.fetchall()

        filas = []
        for est in estudiantes:
            doc  = est['documento']
            ifid = est['id_ficha']

            # ── Días con marca del INSTRUCTOR (fuente de verdad) ──────────────
            # Si el instructor marcó Inasistencia o Retardo en un día,
            # ese día se reporta según el instructor, ignorando la asistencia del aprendiz.
            self.db.cursor.execute(
                "SELECT fecha_falta, tipo_falta FROM faltas "
                "WHERE documento_estudiante=%s AND id_ficha=%s "
                "AND fecha_falta BETWEEN %s AND %s",
                (doc, ifid, fi, ff))
            marcas_instructor = {}  # fecha → tipo_falta
            for row in self.db.cursor.fetchall():
                marcas_instructor[row['fecha_falta']] = row['tipo_falta']

            # ── Días con asistencia registrada por el aprendiz ────────────────
            self.db.cursor.execute(
                "SELECT DISTINCT DATE(fecha_registro) as dia FROM asistencias "
                "WHERE documento_estudiante=%s AND DATE(fecha_registro) BETWEEN %s AND %s",
                (doc, fi, ff))
            dias_asistencia = {row['dia'] for row in self.db.cursor.fetchall()}

            # ── Días de clase del rango según horario de la ficha ────────────
            self.db.cursor.execute(
                "SELECT DISTINCT dia_semana FROM horarios WHERE id_ficha=%s", (ifid,))
            dias_horario = {r['dia_semana'] for r in self.db.cursor.fetchall()}
            _DIA = {'Lunes':0,'Martes':1,'Miércoles':2,'Jueves':3,'Viernes':4,'Sábado':5,'Domingo':6}
            dias_clase_idx = {_DIA[d] for d in dias_horario if d in _DIA} or {0,1,2,3,4}
            dias_clase_rango = [
                fi + datetime.timedelta(days=i)
                for i in range((ff - fi).days + 1)
                if (fi + datetime.timedelta(days=i)).weekday() in dias_clase_idx
            ]

            # ── Calcular estado real de cada día de clase ─────────────────────
            # Prioridad: instructor > aprendiz
            asist = faltas = retardos = 0
            for dia in dias_clase_rango:
                if dia in marcas_instructor:
                    tipo = marcas_instructor[dia]
                    if tipo == 'Retardo':
                        retardos += 1
                        asist += 1   # retardo = llegó tarde, pero asistió
                    else:  # Inasistencia o Justificada
                        faltas += 1
                elif dia in dias_asistencia:
                    asist += 1
                # Si no hay registro de nada ese día → no se cuenta (día sin datos)

            total_dias = asist + faltas  # retardos ya están dentro de asist
            # Excluir retardos del numerador de asistencia pura pero contar como asistencia
            # pct = días presentes (incluyendo retardos) / total días con registro
            if total_dias > 0:
                pct = min(100, round(asist / total_dias * 100))
            else:
                pct = 0

            filas.append({
                'nombre':    est['nombre_completo'],
                'documento': doc,
                'ficha':     est.get('codigo_ficha', '—'),
                'asist':     asist,
                'faltas':    faltas,
                'retardos':  retardos,
                'pct':       pct,
            })
        return filas

    # ─────────────────────────────────────────────────────────────────────────
    # REFRESH UI
    # ─────────────────────────────────────────────────────────────────────────
    def _refresh_tarjetas(self, filas):
        ta = sum(f['asist']    for f in filas)
        tf = sum(f['faltas']   for f in filas)
        tr = sum(f['retardos'] for f in filas)
        pa = round(sum(f['pct'] for f in filas) / len(filas)) if filas else 0
        self.lbl_c_asist.configure(text=str(ta))
        self.lbl_c_faltas.configure(text=str(tf))
        self.lbl_c_ret.configure(text=str(tr))
        self.lbl_c_pct.configure(text=f"{pa}%")

    def _refresh_tabla(self, filas):
        for item in self.tv_rep.get_children():
            self.tv_rep.delete(item)
        for f in filas:
            tag = "verde" if f['pct'] >= 85 else ("amarillo" if f['pct'] >= 70 else "rojo")
            self.tv_rep.insert("", tk.END, tags=(tag,), values=(
                f['nombre'], f['documento'], f['ficha'],
                f['asist'], f['faltas'], f['retardos'], f"{f['pct']}%"))
        n = len(filas)
        self.lbl_total.configure(text=f"{n} estudiante{'s' if n != 1 else ''}")

    def _refresh_grafico(self, filas, fi, ff, rango):
        c = self.canvas_chart
        c.delete("all")
        c.update_idletasks()
        W = c.winfo_width() or 860
        H = 230
        PL, PR, PT, PB = 48, 30, 24, 58
        aW = W - PL - PR
        aH = H - PT - PB
        BY = PT + aH   # base y

        if not filas:
            self._chart_placeholder()
            return

        # Limitar a 30 estudiantes — mostrar los de menor % primero (más en riesgo)
        MAX_BARRAS = 30
        filas_graf = sorted(filas, key=lambda f: f['pct'])[:MAX_BARRAS]
        n = len(filas_graf)
        hay_mas = len(filas) > MAX_BARRAS

        # Guías horizontales
        for g in [25, 50, 75, 100]:
            yg = BY - int(g / 100 * aH)
            c.create_line(PL, yg, W - PR, yg, fill="#F2F2F2", dash=(4,4))
            c.create_text(PL - 6, yg, text=f"{g}%",
                         font=("Segoe UI", 8), fill="#C0C0C0", anchor="e")

        # Umbral crítico 80 %
        y80 = BY - int(0.80 * aH)
        c.create_line(PL, y80, W - PR, y80, fill="#E74C3C", dash=(5,3), width=1)
        c.create_text(W - PR + 3, y80, text="80%",
                     font=("Segoe UI", 8, "bold"), fill="#E74C3C", anchor="w")

        # Ejes
        c.create_line(PL, PT, PL, BY, fill="#D0D0D0", width=1)
        c.create_line(PL, BY, W - PR, BY, fill="#D0D0D0", width=1)

        col_w = aW / n
        bw    = max(8, min(52, int(col_w * 0.60)))

        for i, f in enumerate(filas_graf):
            xc   = int(PL + i * col_w + col_w / 2)
            pct  = f['pct']
            bh   = int(pct / 100 * aH)
            x0, y0 = xc - bw // 2, BY - bh
            x1, y1 = xc + bw // 2, BY

            color = self.GREEN if pct >= 85 else ("#E67E22" if pct >= 70 else "#E74C3C")

            # Fondo de barra
            c.create_rectangle(x0, PT, x1, BY, fill="#F5F5F5", outline="")
            # Barra
            if bh > 2:
                c.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
                c.create_rectangle(x0, y0, x1, min(y0+4, y1),
                                  fill=self._lighten(color), outline="")

            # Valor encima
            if bh > 16:
                c.create_text(xc, y0 - 9, text=f"{pct}%",
                             font=("Segoe UI", 8, "bold"), fill=color)

            # Nombre abajo
            nom = (f['nombre'].split()[0] if f['nombre'] else "—")
            if len(nom) > 9:
                nom = nom[:8] + "…"
            c.create_text(xc, BY + 9, text=nom, font=("Segoe UI", 8),
                         fill="#555", anchor="n")

        # Título
        rng_txt = (fi.strftime('%d/%m/%Y') if rango == "Día"
                  else f"{fi.strftime('%d/%m/%Y')} → {ff.strftime('%d/%m/%Y')}")
        titulo = f"% Asistencia — {rng_txt}"
        if hay_mas:
            titulo += f"  (mostrando {MAX_BARRAS} con menor % de {len(filas)})"
        c.create_text(W // 2, 10, text=titulo,
                     font=("Segoe UI", 9, "bold"), fill=self.DARK)

    def _lighten(self, h):
        try:
            r = min(255, int(h[1:3], 16) + 38)
            g = min(255, int(h[3:5], 16) + 38)
            b = min(255, int(h[5:7], 16) + 38)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return h

    def _sort(self, col):
        km = {"Estudiante":"nombre","Documento":"documento","Ficha":"ficha",
              "Asistencias":"asist","Faltas":"faltas","Retardos":"retardos","% Asist.":"pct"}
        k   = km.get(col, "nombre")
        rev = getattr(self, f"_sr_{col}", False)
        self.last_rows.sort(key=lambda r: r.get(k, 0), reverse=rev)
        setattr(self, f"_sr_{col}", not rev)
        self._refresh_tabla(self.last_rows)

    # ─────────────────────────────────────────────────────────────────────────
    # EXPORTAR
    # ─────────────────────────────────────────────────────────────────────────
    def exportar(self):
        if not self.last_rows:
            messagebox.showwarning("Exportar", "Genera primero un reporte.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")])
        if not path:
            return
        try:
            import pandas as pd
            df = pd.DataFrame([{
                'Estudiante':   f['nombre'],
                'Documento':    f['documento'],
                'Ficha':        f['ficha'],
                'Asistencias':  f['asist'],
                'Faltas':       f['faltas'],
                'Retardos':     f['retardos'],
                '% Asistencia': f"{f['pct']}%"
            } for f in self.last_rows])
            if path.lower().endswith('.csv'):
                df.to_csv(path, index=False, encoding='utf-8-sig')
            else:
                df.to_excel(path, index=False)
            messagebox.showinfo("✅ Exportado", f"Guardado en:\n{path}")
        except Exception as e:
            messagebox.showerror("Error exportar", str(e))

    # ── Compatibilidad con llamadas antiguas desde main.py ───────────────────
    def lanzar_reporte(self):
        self.generar()

    def exportar_reporte(self):
        self.exportar()

    def cambiar_modo_reporte(self):
        self.cambiar_modo()

    def mostrar_selector_rango(self, v=None):
        self._rebuild_selector(v)

    def agregar_item_reporte(self):
        self.agregar_item()

    def limpiar_lista_reporte(self):
        self.limpiar_items()

