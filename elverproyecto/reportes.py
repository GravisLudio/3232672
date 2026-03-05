"""
Módulo ReportesManager
Encapsula toda la lógica de reportes y estadísticas
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from config import COLORES, FUENTES
import datetime
import pandas as pd
from tkcalendar import Calendar
import logging


class ReportesManager:
    """Gestiona toda la funcionalidad de reportes y estadísticas."""
    
    def __init__(self, app, db, servicio):
        self.app = app
        self.db = db
        self.servicio = servicio
        self.sena_green = COLORES['SENA_GREEN']
        self.sena_dark = COLORES['SENA_DARK']
        
        # Variables de estado
        self.modo_filtro = tk.StringVar(value="Ficha")
        self.items_seleccionados = []
        self.combo_vals = []
        self.last_report_items = []
        self.last_report_params = None
        
        # Componentes UI
        self.canvas_rep = None
        self.btn_exp_rep = None
        self.lbl_lista_rep = None
        self.combo_seleccion = None
        self.seg_tiempo = None
        self.selector_frame = None
    
    def crear_pestana_reportes(self, t_rep):
        """Construye la pestaña completa de reportes"""
        # Contenedor principal
        f_rep_m = ctk.CTkFrame(t_rep, corner_radius=20, fg_color="white", border_width=1, border_color="#EEE")
        f_rep_m.pack(pady=20, padx=50, fill="x")
        
        grid_rep = tk.Frame(f_rep_m, bg="white")
        grid_rep.pack(pady=20, padx=25)

        # --- FILA 0: MODO ---
        ctk.CTkLabel(grid_rep, text="Filtrar por:", text_color="gray").grid(row=0, column=0, sticky="w", padx=10)
        radio_frame = tk.Frame(grid_rep, bg="white")
        radio_frame.grid(row=1, column=0, padx=10, sticky="w")
        
        ctk.CTkRadioButton(radio_frame, text="Fichas", variable=self.modo_filtro, value="Ficha", 
                           command=self.cambiar_modo_reporte).pack(side="left", padx=5)
        ctk.CTkRadioButton(radio_frame, text="Aprendices", variable=self.modo_filtro, value="Aprendiz", 
                           command=self.cambiar_modo_reporte).pack(side="left", padx=5)

        # --- FILA 0, COL 1: COMBO DINÁMICO ---
        ctk.CTkLabel(grid_rep, text="Seleccionar elemento", text_color="gray").grid(row=0, column=1, padx=12)
        self.combo_seleccion = ttk.Combobox(grid_rep, state="normal", width=40)
        self.combo_seleccion.grid(row=1, column=1, padx=5, pady=5)
        
        btn_add = ctk.CTkButton(grid_rep, text="Añadir +", width=80, command=self.agregar_item_reporte)
        btn_add.grid(row=1, column=2, padx=5)

        # --- FILA 2: LISTA DE SELECCIONADOS ---
        self.lbl_lista_rep = ctk.CTkLabel(grid_rep, text="Seleccionados: Ninguno", text_color="black", font=("Arial", 11, "italic"))
        self.lbl_lista_rep.grid(row=2, column=0, columnspan=2, sticky="w", padx=15, pady=5)
        
        ctk.CTkButton(grid_rep, text="Limpiar", width=60, fg_color="#E74C3C", command=self.limpiar_lista_reporte).grid(row=2, column=2, padx=5)

        # --- RANGO DE TIEMPO ---
        ctk.CTkLabel(grid_rep, text="Rango", text_color="gray").grid(row=0, column=3, padx=12)
        self.seg_tiempo = ctk.CTkSegmentedButton(grid_rep, values=["Día", "Semana", "Mes"], command=self.mostrar_selector_rango)
        self.seg_tiempo.set("Día")
        self.seg_tiempo.grid(row=1, column=3, padx=12)

        # Contenedor para el selector
        self.selector_frame = tk.Frame(f_rep_m, bg="white")
        self.selector_frame.pack(fill="x", padx=50)

        # --- BOTÓN GENERAR y EXPORTAR ---
        btn_frame = tk.Frame(t_rep, bg=self.sena_dark)
        btn_frame.pack(pady=10)
        btn_gen = ctk.CTkButton(btn_frame, text="GENERAR ESTADÍSTICAS", font=("Arial", 14, "bold"),
                      command=self.lanzar_reporte)
        btn_gen.pack(side="left", padx=5)
        self.btn_exp_rep = ctk.CTkButton(btn_frame, text="EXPORTAR", font=("Arial", 14, "bold"),
                      fg_color="#888", hover_color="#666", state="disabled", command=self.exportar_reporte)
        self.btn_exp_rep.pack(side="left", padx=5)

        # --- EL CANVAS ---
        self.canvas_rep = tk.Canvas(t_rep, bg="white", height=300, highlightthickness=1, highlightbackground="#DDD")
        self.canvas_rep.pack(fill="both", expand=True, padx=50, pady=10)
        self.canvas_rep.create_text(300, 150, text="Seleccione filtros y presione Generar", fill="gray")

        # Inicializar
        self.cambiar_modo_reporte()
        self.mostrar_selector_rango()
    
    def cambiar_modo_reporte(self):
        """Cambia entre modo Ficha/Aprendiz"""
        self.limpiar_lista_reporte()
        if self.modo_filtro.get() == "Ficha":
            fichas = self.servicio.obtener_fichas()
            data = [f"{f['id_ficha']} | {f['codigo_ficha']} - {f['nombre_programa']}" for f in fichas]
        else:
            self.db.cursor.execute("SELECT documento, nombre_completo FROM estudiantes")
            data = [f"{e['documento']} | {e['nombre_completo']}" for e in self.db.cursor.fetchall()]
        
        self.combo_vals = data
        self.combo_seleccion['values'] = data
        self.combo_seleccion.set("Seleccione...")
        self.combo_seleccion.configure(state='normal')
        self.combo_seleccion.bind('<KeyRelease>', self._filtrar_combo)
    
    def _filtrar_combo(self, event=None):
        """Filtra el combo según texto escrito"""
        text = self.combo_seleccion.get().lower()
        filtered = [v for v in self.combo_vals if text in v.lower()]
        self.combo_seleccion['values'] = filtered
    
    def mostrar_selector_rango(self):
        """Muestra selector según rango (Día/Semana/Mes)"""
        for w in self.selector_frame.winfo_children():
            w.destroy()

        rango = self.seg_tiempo.get()
        self.reporte_fecha_inicio = None

        if rango == "Día":
            self.cal_rep = Calendar(self.selector_frame, selectmode='day', locale='es_ES', 
                                   background=self.sena_green, headersbackground=self.sena_dark)
            self.cal_rep.pack(padx=10, pady=8)
            try:
                self.reporte_fecha_inicio = self.cal_rep.selection_get()
            except:
                self.reporte_fecha_inicio = datetime.date.today()
            
            def on_day_sel(e=None):
                try: 
                    self.reporte_fecha_inicio = self.cal_rep.selection_get()
                except: 
                    self.reporte_fecha_inicio = datetime.date.today()
            
            self.cal_rep.bind("<<CalendarSelected>>", on_day_sel)

        elif rango == "Semana":
            hoy = datetime.date.today()
            semanas = []
            self.week_map = {}
            for i in range(0, 104):
                inicio = hoy - datetime.timedelta(days=hoy.weekday()) - datetime.timedelta(weeks=i)
                fin = inicio + datetime.timedelta(days=6)
                label = f"{inicio.isocalendar()[0]}-W{inicio.isocalendar()[1]:02d}: {inicio.strftime('%d/%m/%Y')} - {fin.strftime('%d/%m/%Y')}"
                semanas.append(label)
                self.week_map[label] = inicio

            self.combo_week = ttk.Combobox(self.selector_frame, values=semanas, state='readonly', width=50)
            self.combo_week.pack(padx=10, pady=8)
            self.combo_week.set(semanas[0])
            self.reporte_fecha_inicio = self.week_map[semanas[0]]

            def on_week_sel(e=None):
                v = self.combo_week.get()
                self.reporte_fecha_inicio = self.week_map.get(v, datetime.date.today())
            
            self.combo_week.bind('<<ComboboxSelected>>', on_week_sel)

        else:  # Mes
            hoy = datetime.date.today()
            meses = []
            self.month_map = {}
            for m in range(0, 36):
                year = (hoy.year - ((hoy.month - m - 1) // 12))
                month = ((hoy.month - m - 1) % 12) + 1
                inicio = datetime.date(year, month, 1)
                label = f"{inicio.strftime('%B %Y')}"
                meses.append(label)
                self.month_map[label] = inicio

            self.combo_month = ttk.Combobox(self.selector_frame, values=meses, state='readonly', width=40)
            self.combo_month.pack(padx=10, pady=8)
            self.combo_month.set(meses[0])
            self.reporte_fecha_inicio = self.month_map[meses[0]]

            def on_month_sel(e=None):
                v = self.combo_month.get()
                self.reporte_fecha_inicio = self.month_map.get(v, datetime.date.today())
            
            self.combo_month.bind('<<ComboboxSelected>>', on_month_sel)
    
    def agregar_item_reporte(self):
        """Agrega item a la lista de seleccionados"""
        item = self.combo_seleccion.get()
        if item and item != "Seleccione..." and item not in self.items_seleccionados:
            self.items_seleccionados.append(item)
            ids_v = [i.split(" | ")[0] for i in self.items_seleccionados]
            self.lbl_lista_rep.configure(text=f"Seleccionados: {', '.join(ids_v)}")
    
    def limpiar_lista_reporte(self):
        """Limpia lista de seleccionados"""
        self.items_seleccionados = []
        if self.lbl_lista_rep:
            self.lbl_lista_rep.configure(text="Seleccionados: Ninguno")
    
    def lanzar_reporte(self):
        """Genera y dibuja el reporte"""
        if not self.items_seleccionados:
            self.canvas_rep.delete("all")
            self.canvas_rep.create_text(400, 150, text="Debe seleccionar al menos una ficha o aprendiz", 
                                       fill="#E74C3C", font=("Arial", 12, "bold"))
            self.btn_exp_rep.configure(state="disabled", fg_color="#888")
            return
        
        self.canvas_rep.delete("all")
        ids_limpios = [item.split(" | ")[0] for item in self.items_seleccionados]
        modo = self.modo_filtro.get()
        rango_sel = self.seg_tiempo.get()

        fecha_inicio = getattr(self, 'reporte_fecha_inicio', datetime.date.today())

        items = []

        if rango_sel == "Día":
            datos = self.servicio.obtener_metricas_reporte_multiple(ids_limpios, modo, rango_sel, fecha_inicio)
            if datos['total_asistencias'] == 0 and datos['expected'] == 0:
                self.canvas_rep.create_text(300, 150, text="No hay registros para esta selección", fill="red", font=("Arial", 14))
                return
            items.append({'label': fecha_inicio.strftime('%d/%m/%Y'), 'metrics': datos})

        elif rango_sel == "Semana":
            if hasattr(self, 'week_specified') and self.week_specified:
                datos = self.servicio.obtener_metricas_reporte_multiple(ids_limpios, modo, rango_sel, fecha_inicio)
                items.append({'label': f"Semana {fecha_inicio.isocalendar()[1]} ({fecha_inicio.strftime('%d/%m')})", 'metrics': datos})
            else:
                year, month = fecha_inicio.year, fecha_inicio.month
                first = datetime.date(year, month, 1)
                first_monday = first - datetime.timedelta(days=first.weekday())
                for i in range(4):
                    start = first_monday + datetime.timedelta(weeks=i)
                    label = f"W{start.isocalendar()[1]} {start.strftime('%d/%m')}"
                    d = self.servicio.obtener_metricas_reporte_multiple(ids_limpios, modo, 'Semana', start)
                    items.append({'label': label, 'metrics': d})

        else:  # Mes
            if hasattr(self, 'month_specified') and self.month_specified:
                datos = self.servicio.obtener_metricas_reporte_multiple(ids_limpios, modo, rango_sel, fecha_inicio)
                items.append({'label': fecha_inicio.strftime('%B %Y'), 'metrics': datos})
            else:
                year = fecha_inicio.year
                today = datetime.date.today()
                last_month = today.month if year == today.year else 12
                for m in range(1, last_month + 1):
                    start = datetime.date(year, m, 1)
                    d = self.servicio.obtener_metricas_reporte_multiple(ids_limpios, modo, 'Mes', start)
                    items.append({'label': start.strftime('%b'), 'metrics': d})

        if not any(it['metrics']['total_asistencias'] or it['metrics'].get('expected', 0) for it in items):
            self.canvas_rep.create_text(300, 150, text="No hay registros para esta selección", fill="red", font=("Arial", 14))
            self.btn_exp_rep.configure(state="disabled", fg_color="#888")
            return

        self.last_report_items = items
        self.last_report_params = (ids_limpios, modo, rango_sel, fecha_inicio)

        # Dibujar gráfico
        self._dibujar_grafico(items)
        self.btn_exp_rep.configure(state="normal", fg_color="#3A7FF6")
    
    def _dibujar_grafico(self, items):
        """Dibuja el gráfico de barras en el canvas"""
        self.canvas_rep.update_idletasks()
        W = self.canvas_rep.winfo_width() or 800
        H = self.canvas_rep.winfo_height() or 300
        pad = 30
        n = len(items)
        col_w = max(100, (W - 2*pad) / max(1, n))
        base_y = int(H * 0.55)
        max_h = int(H * 0.3)
        
        # Resumen global
        total_asist = sum(it['metrics'].get('total_asistencias', 0) for it in items)
        total_faltas = sum(it['metrics'].get('faltas', 0) for it in items)
        total_retardos = sum(it['metrics'].get('retardos', 0) for it in items)
        resumen = f"RESUMEN GLOBAL: Asistencias: {total_asist} | Faltas: {total_faltas} | Retardos: {total_retardos}"
        self.canvas_rep.create_text(W//2, 20, text=resumen, font=("Arial", 11, "bold"), fill="#2D5A27")

        for i, it in enumerate(items):
            m = it['metrics']
            expected = m.get('expected', 0) or 0
            total = m.get('total_asistencias', 0) or 0
            faltas = m.get('faltas', 0) or 0
            retardos = m.get('retardos', 0) or 0
            pct = (total / expected) if expected > 0 else 0
            pct_clamped = max(0, min(1, pct))

            x_center = int(pad + i * col_w + col_w/2)
            bar_w = int(min(80, col_w * 0.6))
            bar_h = int(pct_clamped * max_h)
            x0 = x_center - bar_w//2
            y0 = base_y - bar_h
            x1 = x_center + bar_w//2
            y1 = base_y
            color = self.sena_green if pct_clamped > 0.8 else ("orange" if pct_clamped > 0.3 else "#E74C3C")

            # Barras
            self.canvas_rep.create_rectangle(x_center - bar_w//2, base_y - max_h, x_center + bar_w//2, base_y, fill="#EEE", outline="")
            self.canvas_rep.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

            # Etiquetas
            self.canvas_rep.create_text(x_center, base_y + 18, text=it['label'], font=("Arial", 10, "bold"))
            self.canvas_rep.create_text(x_center, base_y + 36, text=f"A:{total}  F:{faltas}  R:{retardos}", font=("Arial", 9))
    
    def exportar_reporte(self):
        """Exporta reporte a PDF o Excel"""
        if not self.last_report_items:
            messagebox.showwarning("Exportar", "No hay datos para exportar. Genera primero un reporte.")
            return
        
        path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                           filetypes=[("PDF", "*.pdf"), ("Excel", "*.xlsx")])
        if not path:
            return
        
        items = self.last_report_items
        
        if path.lower().endswith('.xlsx'):
            rows = []
            for it in items:
                m = it['metrics']
                rows.append({
                    'Periodo': it['label'],
                    'Esperado': m.get('expected', 0),
                    'Asistencias': m.get('total_asistencias', 0),
                    'Faltas': m.get('faltas', 0),
                    'Retardos': m.get('retardos', 0)
                })
            df = pd.DataFrame(rows)
            df.to_excel(path, index=False)
            messagebox.showinfo("Exportar", f"Reporte guardado en {path}")
            return
        
        # PDF
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
        except ImportError:
            messagebox.showerror("Exportar", "Falta el paquete reportlab. Instálalo con pip.")
            return
        
        try:
            c = canvas.Canvas(path, pagesize=letter)
            width, height = letter
            y = height - 50
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y, "Reporte de Asistencias")
            y -= 30
            c.setFont("Helvetica", 10)
            
            if self.last_report_params:
                ids, modo, rango, fecha = self.last_report_params
                c.drawString(50, y, f"Modo: {modo}  Rango: {rango}  Fecha inicio: {fecha}")
                y -= 20
            
            for it in items:
                m = it['metrics']
                text = f"{it['label']} - Esperado: {m.get('expected',0)}  A: {m.get('total_asistencias',0)}  F: {m.get('faltas',0)}  R: {m.get('retardos',0)}"
                if y < 60:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 10)
                c.drawString(50, y, text)
                y -= 15
            c.save()
            messagebox.showinfo("Exportar", f"Reporte guardado en {path}")
        except Exception as e:
            messagebox.showerror("Exportar", f"Error al generar PDF: {e}")