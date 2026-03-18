"""
Módulo PantallaAdministrador
Encapsula toda la lógica de la interfaz de administración con diseño moderno
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from config import COLORES, FUENTES
import logging
import datetime
import calendar as _cal


def configurar_estilo_tablas():
    """Configura el estilo de las tablas (Treeview)"""
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Treeview',
                   font=('Segoe UI', 10),
                   rowheight=28,
                   background='#F8F9FA',
                   foreground='#2C3E50')
    style.configure('Treeview.Heading',
                   font=('Segoe UI', 11, 'bold'),
                   background='#39A900',
                   foreground='white',
                   borderwidth=0)
    style.map('Treeview', background=[('selected', '#39A900')])
    style.map('Treeview.Heading', background=[('active', '#32900D')])


class PantallaAdministrador:

    
    def __init__(self, frame_admin, db, servicio, admin_usuario, app):
        self.frame = frame_admin
        self.db = db
        self.servicio = servicio
        self.admin_usuario = admin_usuario
        self.app = app
        
        self.sena_orange = COLORES['SENA_ORANGE']
        self.sena_green  = COLORES['SENA_GREEN']
        self.sena_dark   = COLORES['SENA_DARK']
        self.bg_light    = COLORES['BG_LIGHT']
        self.current_tab = None
        self.tab_frames = {}  # Diccionario para almacenar frames de pestañas
        
        configurar_estilo_tablas()
        self._construir_layout()
    
    def _construir_layout(self):
        """Construye header + navegación por botones"""
        # Header Profesional
        head = ctk.CTkFrame(self.frame, height=130, corner_radius=0, 
                           fg_color=self.sena_orange, border_width=0)
        head.pack(fill="x", side="top")
        
        # Contenedor de título+botones en header
        head_top = ctk.CTkFrame(head, fg_color="transparent")
        head_top.pack(side="top", fill="x", padx=25, pady=(15, 10))
        
        ctk.CTkLabel(head_top, text="C.R.S - ADMINISTRACIÓN", 
                    font=("Segoe UI", 18, "bold"),
                    text_color="white").pack(side="left")
        
        head_right = ctk.CTkFrame(head_top, fg_color="transparent")
        head_right.pack(side="right")
        
        ctk.CTkButton(head_right, text=" CERRAR", width=100,
                     fg_color="#E74C3C", text_color="white",
                     font=("Segoe UI", 11, "bold"),
                     hover_color="#C0392B",
                     command=self._cerrar_admin).pack(side="left", padx=8)
        
        # Navegación con botones tipo bloque en el header
        nav_frame = ctk.CTkFrame(head, fg_color="transparent")
        nav_frame.pack(side="bottom", fill="x", padx=25, pady=(0, 15))
        
        # Crear botones de navegación
        self.nav_buttons = {}
        tabs = [
            ("📋 HISTORIAL", "historial"),
            ("👥 GESTIÓN", "gestion"),
            ("➕ REGISTRO", "registro"),
            ("👨‍🏫 INSTRUCTORES", "instructores"),
            ("� REPORTES", "reportes"),
            ("�🗑️ PAPELERA", "papelera"),
        ]
        
        for label, tab_id in tabs:
            btn = ctk.CTkButton(nav_frame, text=label, height=40,
                               fg_color=self.sena_green,
                               hover_color="#32900D",
                               font=("Segoe UI", 11, "bold"),
                               border_width=2,
                               border_color="#5FC74F",
                               command=lambda t=tab_id: self._cambiar_tab(t))
            btn.pack(side="left", padx=8)
            self.nav_buttons[tab_id] = btn
        
        # Contenedor principal para tabs
        self.main_container = ctk.CTkFrame(self.frame, fg_color="#F5F5F5")
        self.main_container.pack(fill="both", expand=True)
        
        # Crear todos los frames de pestañas de una sola vez
        self.tab_frames['historial']    = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        self.tab_frames['gestion']      = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        self.tab_frames['registro']     = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        self.tab_frames['instructores'] = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        self.tab_frames['reportes']     = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        self.tab_frames['papelera']     = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        
        # Construir contenido de cada pestaña (sin mostrar aún)
        self._construir_historial()
        self._construir_gestion()
        self._construir_registro()
        self._construir_instructores()
        self._construir_reportes()
        self._construir_papelera()
        
        # Mostrar pestaña inicial
        self._cambiar_tab("historial")
    
    def _cambiar_tab(self, tab_id):
        """Cambia entre pestañas mostrando/ocultando frames"""
        # Ocultar todas las pestañas
        for tab_name, frame in self.tab_frames.items():
            frame.pack_forget()
        
        # Mostrar la pestaña seleccionada
        if tab_id in self.tab_frames:
            self.current_tab = tab_id
            self.tab_frames[tab_id].pack(fill="both", expand=True, padx=20, pady=20)
            # Refrescar datos cuando se cambia de pestaña
            if tab_id == "gestion":
                self._filtrar_gestion()
            elif tab_id == "papelera":
                self._refrescar_papelera()
            elif tab_id == "historial":
                self._refrescar_historial()
            elif tab_id == "reportes":
                pass  # Los reportes se cargan bajo demanda
            elif tab_id == "instructores":
                self._cargar_tabla_instructores()
    
    def _cerrar_admin(self):
        """Cierra sesión del admin"""
        if self.admin_usuario:
            try:
                self.db.registrar_auditoria(self.admin_usuario, "logout admin")
            except Exception as ex:
                logging.error("Error en auditoría logout", exc_info=True)
        self.app.admin_actual = None
        self.app.mostrar_inicio()
    
    def _construir_historial(self):
        """Tab: Historial de asistencias con diseño moderno"""
        # Barra de herramientas
        toolbar = ctk.CTkFrame(self.tab_frames['historial'], fg_color="white", 
                               corner_radius=10, border_width=1,
                               border_color="#E0E0E0", height=60)
        toolbar.pack(fill="x", padx=0, pady=(0, 15))
        
        # Búsqueda
        lbl_buscar = ctk.CTkLabel(toolbar, text="🔍 Buscar:", 
                                 font=("Segoe UI", 11, "bold"),
                                 text_color="#2C3E50")
        lbl_buscar.pack(side="left", padx=15, pady=12)
        
        self.ent_hist_bus = ctk.CTkEntry(toolbar, placeholder_text="Documento o nombre...",
                                        width=250, height=35)
        self.ent_hist_bus.pack(side="left", padx=5)
        
        ctk.CTkButton(toolbar, text="BUSCAR", width=100, height=35,
                     fg_color=self.sena_green,
                     command=self._refrescar_historial).pack(side="left", padx=5)
        
        ctk.CTkButton(toolbar, text="LIMPIAR", width=100, height=35,
                     fg_color="#95A5A6",
                     command=self._limpiar_busqueda_hist).pack(side="left", padx=5)
        
        # Tabla de historial con marco decorativo
        frame_tabla = ctk.CTkFrame(self.tab_frames['historial'], fg_color="white", 
                                   corner_radius=10, border_width=1, 
                                   border_color="#E0E0E0")
        frame_tabla.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")
        
        self.tv_hist = ttk.Treeview(frame_tabla, 
                                    columns=("DOC", "NOMBRE", "ENTRADA", "SALIDA"),
                                    show="headings", height=15,
                                    yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tv_hist.yview)
        
        self.tv_hist.heading("DOC", text="DOCUMENTO")
        self.tv_hist.heading("NOMBRE", text="NOMBRE COMPLETO")
        self.tv_hist.heading("ENTRADA", text="ENTRADA")
        self.tv_hist.heading("SALIDA", text="SALIDA")
        
        self.tv_hist.column("DOC", width=120)
        self.tv_hist.column("NOMBRE", width=250)
        self.tv_hist.column("ENTRADA", width=150)
        self.tv_hist.column("SALIDA", width=150)
        
        self.tv_hist.pack(fill="both", expand=True)
        
        self._refrescar_historial()
    
    def _limpiar_busqueda_hist(self):
        """Limpia búsqueda del historial"""
        if hasattr(self, 'ent_hist_bus'):
            self.ent_hist_bus.delete(0, 'end')
            self._refrescar_historial()
    
    def _refrescar_historial(self):
        """Recarga historial con filtro opcional"""
        if not hasattr(self, 'tv_hist'):
            return
            
        for i in self.tv_hist.get_children():
            self.tv_hist.delete(i)
        
        busqueda = self.ent_hist_bus.get() if hasattr(self, 'ent_hist_bus') else ""
        
        if busqueda:
            query = f"%{busqueda}%"
            self.db.cursor.execute(
                """SELECT a.id_asistencia, a.documento_estudiante, e.nombre_completo, 
                          a.fecha_registro, a.fecha_salida FROM asistencias a 
                   JOIN estudiantes e ON a.documento_estudiante = e.documento 
                   WHERE a.documento_estudiante LIKE %s OR e.nombre_completo LIKE %s
                   ORDER BY a.fecha_registro DESC LIMIT 100""",
                (query, query)
            )
        else:
            self.db.cursor.execute(
                """SELECT a.id_asistencia, a.documento_estudiante, e.nombre_completo, 
                          a.fecha_registro, a.fecha_salida FROM asistencias a 
                   JOIN estudiantes e ON a.documento_estudiante = e.documento 
                   ORDER BY a.fecha_registro DESC LIMIT 100"""
            )
        
        for r in self.db.cursor.fetchall():
            sal = r['fecha_salida'].strftime('%H:%M') if r['fecha_salida'] else "PENDIENTE"
            self.tv_hist.insert("", "end", 
                              values=(r['documento_estudiante'], r['nombre_completo'], 
                                     r['fecha_registro'].strftime('%d/%m %H:%M'), sal))
    
    def _construir_gestion(self):
        """Tab: Gestión de aprendices con interfaz mejorada"""
        # Barra de búsqueda superior
        search_frame = ctk.CTkFrame(self.tab_frames['gestion'], fg_color="white", 
                                   corner_radius=10, border_width=1,
                                   border_color="#E0E0E0")
        search_frame.pack(fill="x", padx=0, pady=(0, 10))
        
        ctk.CTkLabel(search_frame, text="🔍 Buscar aprendiz:", 
                    font=("Segoe UI", 11, "bold"),
                    text_color="#2C3E50").pack(side="left", padx=15, pady=12)
        
        self.ent_gest_bus = ctk.CTkEntry(search_frame, placeholder_text="Documento, nombre o ficha...",
                                        height=35)
        self.ent_gest_bus.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=12)
        
        ctk.CTkButton(search_frame, text="FILTRAR", width=120, height=35,
                     fg_color=self.sena_green,
                     command=self._filtrar_gestion).pack(side="left", padx=(0, 12), pady=12)
        
        # Tabla de gestión
        frame_tabla = ctk.CTkFrame(self.tab_frames['gestion'], fg_color="white",
                                   corner_radius=10, border_width=1,
                                   border_color="#E0E0E0")
        frame_tabla.pack(fill="both", expand=True, padx=0, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")
        
        self.tv_gest = ttk.Treeview(frame_tabla, 
                                   columns=("DOC", "NOMBRE", "FICHA"),
                                   show="headings", height=15,
                                   selectmode='extended',
                                   yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tv_gest.yview)
        
        self.tv_gest.heading("DOC", text="DOCUMENTO")
        self.tv_gest.heading("NOMBRE", text="NOMBRE COMPLETO")
        self.tv_gest.heading("FICHA", text="FICHA")
        
        self.tv_gest.column("DOC", width=130)
        self.tv_gest.column("NOMBRE", width=280)
        self.tv_gest.column("FICHA", width=120)
        
        self.tv_gest.pack(fill="both", expand=True)
        self.tv_gest.bind("<<TreeviewSelect>>", self._verificar_desercion)
        
        # Barra de acciones
        action_frame = ctk.CTkFrame(self.tab_frames['gestion'], fg_color="transparent")
        action_frame.pack(fill="x", padx=0, pady=10)
        
        ctk.CTkButton(action_frame, text="🗑️ MOVER A PAPELERA", 
                     fg_color="#E74C3C", hover_color="#C0392B",
                     font=("Segoe UI", 11, "bold"),
                     command=self._mover_papelera).pack(side="left", padx=5)

        self.btn_desercion = ctk.CTkButton(
            action_frame, text="⚠️ MARCAR DESERCIÓN",
            fg_color="#D97706", hover_color="#B45309",
            font=("Segoe UI", 11, "bold"),
            command=self._marcar_desercion)
        # No se hace .pack() aquí — aparece solo cuando aplica

        ctk.CTkFrame(action_frame, fg_color="transparent").pack(side="left", expand=True)
        
        ctk.CTkButton(action_frame, text="🔄 ACTUALIZAR", 
                     fg_color="#95A5A6", hover_color="#7F8C8D",
                     font=("Segoe UI", 11, "bold"),
                     command=self._filtrar_gestion).pack(side="right", padx=5)
        
        self._filtrar_gestion()
    
    def _filtrar_gestion(self):
        """Filtra aprendices con búsqueda dinámica"""
        if not hasattr(self, 'tv_gest'):
            return
            
        busqueda = self.ent_gest_bus.get() if hasattr(self, 'ent_gest_bus') else ""
        
        for i in self.tv_gest.get_children():
            self.tv_gest.delete(i)
        
        v = f"%{busqueda}%" if busqueda else "%"
        self.db.cursor.execute(
            """SELECT documento, nombre_completo, id_ficha FROM estudiantes 
               WHERE documento LIKE %s OR nombre_completo LIKE %s OR id_ficha LIKE %s
               ORDER BY nombre_completo ASC""",
            (v, v, v)
        )
        for r in self.db.cursor.fetchall():
            self.tv_gest.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))
    
    def _mover_papelera(self):
        """Mueve aprendices a papelera"""
        if not hasattr(self, 'tv_gest'):
            return
            
        docs = [self.tv_gest.item(i)['values'][0] for i in self.tv_gest.selection()]
        if not docs:
            messagebox.showwarning("Atención", "Selecciona al menos un aprendiz")
            return
        if messagebox.askyesno("Confirmar", f"¿Mover {len(docs)} aprendiz(ces) a papelera?"):
            for doc in docs:
                self.servicio.mandar_a_papelera(doc)
                try:
                    self.db.registrar_auditoria(self.admin_usuario, "mover a papelera", objeto=doc)
                except Exception as ex:
                    logging.error(f"Error auditoría", exc_info=True)
            self._filtrar_gestion()
            messagebox.showinfo("Éxito", f"{len(docs)} aprendiz(ces) movidos a papelera")
    
    def _verificar_desercion(self, event=None):
        """Muestra el botón de deserción solo si el aprendiz seleccionado
        tiene 3 o más inasistencias registradas por el instructor."""
        if not hasattr(self, 'btn_desercion'):
            return
        sel = self.tv_gest.selection()
        if len(sel) != 1:
            self.btn_desercion.pack_forget()
            return
        doc = self.tv_gest.item(sel[0])['values'][0]
        self.db.cursor.execute(
            "SELECT COUNT(*) as c FROM faltas "
            "WHERE documento_estudiante=%s AND tipo_falta='Inasistencia'",
            (doc,))
        total_inasistencias = (self.db.cursor.fetchone() or {}).get('c', 0)
        if total_inasistencias >= 3:
            self.btn_desercion.pack(side="left", padx=5)
        else:
            self.btn_desercion.pack_forget()

    def _marcar_desercion(self):
        """Mueve al aprendiz a papelera con motivo de deserción y registra auditoría."""
        if not hasattr(self, 'tv_gest'):
            return
        sel = self.tv_gest.selection()
        if not sel:
            return
        doc   = self.tv_gest.item(sel[0])['values'][0]
        nombre = self.tv_gest.item(sel[0])['values'][1]
        if not messagebox.askyesno(
                "Confirmar deserción",
                f"¿Marcar a {nombre} como desertor?\n\n"
                "Tiene 3 o más inasistencias registradas por el instructor.\n"
                "El aprendiz será movido a papelera con motivo 'Deserción'."):
            return
        try:
            self.servicio.mandar_a_papelera(doc)
            try:
                self.db.registrar_auditoria(
                    self.admin_usuario, "deserción marcada", objeto=doc,
                    detalles=f"Aprendiz {nombre} marcado como desertor por inasistencias")
            except Exception:
                pass
            self._filtrar_gestion()
            self.btn_desercion.pack_forget()
            messagebox.showinfo("Deserción registrada",
                                f"{nombre} ha sido marcado como desertor y movido a papelera.")
        except Exception as ex:
            logging.error("Error al marcar deserción", exc_info=True)
            messagebox.showerror("Error", f"No se pudo registrar la deserción:\n{ex}")

    def _construir_registro(self):
        """Tab: Registro manual con formulario estilizado"""
        # Título de sección
        titulo = ctk.CTkLabel(self.tab_frames['registro'], text="📝 Registrar Nuevo Aprendiz",
                             font=("Segoe UI", 16, "bold"),
                             text_color="#2C3E50")
        titulo.pack(pady=(0, 15), anchor="w", padx=0)
        
        # Formulario en marco
        form_frame = ctk.CTkFrame(self.tab_frames['registro'], fg_color="white",
                                 corner_radius=10, border_width=1,
                                 border_color="#E0E0E0")
        form_frame.pack(fill="x", padx=0, pady=(0, 20))
        
        # Grid de campos
        inner_frame = ctk.CTkFrame(form_frame, fg_color="white")
        inner_frame.pack(fill="x", padx=20, pady=20)
        
        fields = ["Documento", "Nombre Completo", "Correo"]
        self.entries_registro = {}
        
        for idx, label in enumerate(fields):
            lbl = ctk.CTkLabel(inner_frame, text=label, font=("Segoe UI", 11, "bold"),
                              text_color="#2C3E50")
            lbl.grid(row=idx, column=0, sticky="w", pady=(0, 8))
            
            entry = ctk.CTkEntry(inner_frame, placeholder_text=f"Ingresa {label.lower()}...",
                                height=38, border_color=self.sena_green)
            entry.grid(row=idx, column=1, sticky="ew", pady=(0, 15), padx=(20, 0))
            self.entries_registro[label] = entry
        
        # Combobox para ficha
        lbl_ficha = ctk.CTkLabel(inner_frame, text="Ficha", font=("Segoe UI", 11, "bold"),
                                text_color="#2C3E50")
        lbl_ficha.grid(row=3, column=0, sticky="w", pady=(0, 8))
        
        self.cb_ficha = ttk.Combobox(inner_frame, state="readonly", height=10,
                                    font=("Segoe UI", 10))
        self.cb_ficha.grid(row=3, column=1, sticky="ew", pady=(0, 15), padx=(20, 0))
        self.cb_ficha['values'] = [f"{f['id_ficha']} | {f['nombre_programa']}" 
                                   for f in self.servicio.obtener_fichas()]
        
        inner_frame.columnconfigure(1, weight=1)
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(form_frame, fg_color="white")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(btn_frame, text="✓ GUARDAR", 
                     fg_color=self.sena_green, hover_color="#32900D",
                     font=("Segoe UI", 11, "bold"),
                     command=self._guardar_aprendiz).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="🗑️ LIMPIAR", 
                     fg_color="#95A5A6", hover_color="#7F8C8D",
                     font=("Segoe UI", 11, "bold"),
                     command=self._limpiar_registro).pack(side="left", padx=5)
        
        # Botón de carga Excel
        excel_frame = ctk.CTkFrame(self.tab_frames['registro'], fg_color="white",
                                  corner_radius=10, border_width=1,
                                  border_color="#E0E0E0")
        excel_frame.pack(fill="x", padx=0, pady=(0, 0))
        
        ctk.CTkLabel(excel_frame, text="📊 Carga masiva",
                    font=("Segoe UI", 12, "bold"),
                    text_color="#2C3E50").pack(padx=20, pady=(15, 10), anchor="w")
        
        ctk.CTkButton(excel_frame, text="📁 IMPORTAR EXCEL",
                     fg_color="#27AE60", hover_color="#229954",
                     font=("Segoe UI", 11, "bold"),
                     width=200,
                     command=self.servicio.importar_excel).pack(padx=20, pady=(0, 15))
    
    def _guardar_aprendiz(self):
        """Guarda aprendiz en BD"""
        exito, mensaje = self.servicio.guardar_aprendiz_manual(
            {k: v.get() for k, v in self.entries_registro.items()},
            self.cb_ficha.get().split(" | ")[0] if self.cb_ficha.get() else None
        )
        if exito:
            messagebox.showinfo("C.R.S", mensaje)
            self._limpiar_registro()
            self._filtrar_gestion()
        else:
            messagebox.showwarning("Atención", mensaje)
    
    def _limpiar_registro(self):
        """Limpia formulario"""
        for e in self.entries_registro.values():
            e.delete(0, 'end')
        self.cb_ficha.set('')

    def _construir_instructores(self):
        """Tab: Gestión completa de instructores"""
        f = self.tab_frames['instructores']

        # ── Barra superior: buscar + botón nuevo ─────────────────────────────
        top = ctk.CTkFrame(f, fg_color="white", corner_radius=10,
                           border_width=1, border_color="#E0E0E0")
        top.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(top, text="🔍 Buscar:", font=("Segoe UI", 11, "bold"),
                    text_color="#2C3E50").pack(side="left", padx=15, pady=12)
        self.ent_bus_inst = ctk.CTkEntry(
            top, placeholder_text="Nombre, documento o usuario...", height=34)
        self.ent_bus_inst.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=12)
        ctk.CTkButton(top, text="FILTRAR", width=100, height=34,
                     fg_color=self.sena_green, hover_color=self.sena_dark,
                     command=self._cargar_tabla_instructores).pack(side="left", padx=(0, 8), pady=12)
        ctk.CTkButton(top, text="➕ NUEVO INSTRUCTOR", height=34,
                     fg_color=self.sena_orange, hover_color="#C25A0D",
                     font=("Segoe UI", 11, "bold"),
                     command=lambda: self._abrir_form_instructor(None)).pack(
                     side="left", padx=(0, 12), pady=12)

        # ── Tabla ────────────────────────────────────────────────────────────
        f_tabla = ctk.CTkFrame(f, fg_color="white", corner_radius=10,
                               border_width=1, border_color="#E0E0E0")
        f_tabla.pack(fill="both", expand=True, pady=(0, 10))

        cols = ("ID", "Documento", "Nombre", "Usuario", "Especialidad Principal", "Tipo", "Fichas")
        self.tv_inst = ttk.Treeview(f_tabla, columns=cols, show="headings",
                                    height=12, selectmode="browse")
        ancho = {"ID": 45, "Documento": 110, "Nombre": 200, "Usuario": 110,
                 "Especialidad Principal": 240, "Tipo": 100, "Fichas": 160}
        for col in cols:
            self.tv_inst.heading(col, text=col)
            self.tv_inst.column(col, width=ancho[col], anchor="w")
        self.tv_inst.column("ID", anchor="center")
        self.tv_inst.column("Tipo", anchor="center")

        vsb_i = ttk.Scrollbar(f_tabla, orient="vertical", command=self.tv_inst.yview)
        self.tv_inst.configure(yscrollcommand=vsb_i.set)
        vsb_i.pack(side="right", fill="y", padx=(0, 4), pady=8)
        self.tv_inst.pack(fill="both", expand=True, padx=8, pady=8)

        # ── Acciones ─────────────────────────────────────────────────────────
        act = ctk.CTkFrame(f, fg_color="transparent")
        act.pack(fill="x")
        ctk.CTkButton(act, text="✏️ EDITAR", height=36,
                     fg_color="#3A7FF6", hover_color="#2563EB",
                     font=("Segoe UI", 11, "bold"),
                     command=self._editar_instructor_sel).pack(side="left", padx=5)
        ctk.CTkButton(act, text="🗑️ ELIMINAR", height=36,
                     fg_color="#E74C3C", hover_color="#C0392B",
                     font=("Segoe UI", 11, "bold"),
                     command=self._eliminar_instructor_sel).pack(side="left", padx=5)
        ctk.CTkButton(act, text="🔄 ACTUALIZAR", height=36,
                     fg_color="#95A5A6", hover_color="#7F8C8D",
                     font=("Segoe UI", 11),
                     command=self._cargar_tabla_instructores).pack(side="right", padx=5)

    def _cargar_tabla_instructores(self):
        """Carga/filtra la tabla de instructores"""
        if not hasattr(self, 'tv_inst'):
            return
        bus = self.ent_bus_inst.get().lower() if hasattr(self, 'ent_bus_inst') else ""
        for i in self.tv_inst.get_children():
            self.tv_inst.delete(i)
        for inst in self.servicio.obtener_instructores():
            nombre = inst.get('nombre_completo', '')
            doc    = inst.get('documento', '')
            usu    = inst.get('usuario', '')
            if bus and bus not in nombre.lower() and bus not in doc and bus not in usu:
                continue
            self.tv_inst.insert("", "end",
                iid=str(inst['id_instructor']),
                values=(inst['id_instructor'], doc, nombre, usu,
                        inst.get('nombre_especialidad') or '—',
                        inst.get('tipo_especialidad') or '—',
                        inst.get('fichas_asignadas_txt') or '—'))

    def _editar_instructor_sel(self):
        sel = self.tv_inst.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un instructor para editar.")
            return
        self.db.cursor.execute(
            "SELECT * FROM instructores WHERE id_instructor=%s", (int(sel[0]),))
        inst = self.db.cursor.fetchone()
        if inst:
            self._abrir_form_instructor(inst)

    def _eliminar_instructor_sel(self):
        sel = self.tv_inst.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un instructor para eliminar.")
            return
        nombre = self.tv_inst.item(sel[0])['values'][2]
        if messagebox.askyesno("Confirmar",
                               f"¿Eliminar al instructor '{nombre}'?\n"
                               "Esto también eliminará sus asignaciones de fichas."):
            ok, msg = self.servicio.eliminar_instructor(int(sel[0]))
            if ok:
                messagebox.showinfo("✅ Éxito", msg)
                self._cargar_tabla_instructores()
            else:
                messagebox.showerror("Error", msg)

    def _abrir_form_instructor(self, instructor=None):
        """Ventana modal para crear o editar un instructor"""
        es_nuevo = instructor is None

        ven = tk.Toplevel(self.frame)
        ven.title("➕ Nuevo Instructor" if es_nuevo else "✏️ Editar Instructor")
        ven.geometry("600x700")
        ven.resizable(False, False)
        ven.grab_set()

        # Header naranja
        hdr = ctk.CTkFrame(ven, fg_color=self.sena_orange, corner_radius=0, height=50)
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr,
                    text="➕ Nuevo Instructor" if es_nuevo else "✏️ Editar Instructor",
                    font=("Segoe UI", 14, "bold"), text_color="white").pack(
                    side="left", padx=20, pady=12)

        scroll = ctk.CTkScrollableFrame(ven, fg_color="#F8F9FA")
        scroll.pack(fill="both", expand=True)

        def campo(label, placeholder="", valor="", disabled=False):
            ctk.CTkLabel(scroll, text=label, font=("Segoe UI", 11, "bold"),
                        text_color="#2C3E50").pack(anchor="w", padx=20, pady=(10, 2))
            e = ctk.CTkEntry(scroll, placeholder_text=placeholder, height=36)
            e.pack(fill="x", padx=20)
            if valor:
                e.insert(0, str(valor))
            if disabled:
                e.configure(state="disabled")
            return e

        e_doc = campo("Documento *", "Número de cédula",
                     instructor.get('documento','') if instructor else "",
                     disabled=not es_nuevo)
        e_nom = campo("Nombre Completo *", "Nombre y apellido",
                     instructor.get('nombre_completo','') if instructor else "")
        e_cor = campo("Correo", "correo@sena.edu.co",
                     instructor.get('correo','') if instructor else "")
        e_usu = campo("Usuario *", "usuario de login",
                     instructor.get('usuario','') if instructor else "")

        # Especialidad principal — solo Técnicas
        ctk.CTkLabel(scroll, text="Especialidad Principal *  (Competencia Técnica)",
                    font=("Segoe UI", 11, "bold"), text_color="#2C3E50").pack(
                    anchor="w", padx=20, pady=(12, 2))
        tecnicas    = self.servicio.obtener_competencias_por_tipo("Técnica")
        tec_ops     = ["— Sin asignar —"] + [
            f"{c['id_competencia']} | {c['nombre_competencia']}" for c in tecnicas]
        cb_esp = ttk.Combobox(scroll, values=tec_ops, state="readonly")
        cb_esp.pack(fill="x", padx=20, pady=(0, 4))
        if instructor and instructor.get('id_competencia_principal'):
            match = next((o for o in tec_ops
                         if o.startswith(f"{instructor['id_competencia_principal']} |")), None)
            cb_esp.set(match or tec_ops[0])
        else:
            cb_esp.set(tec_ops[0])

        # Fichas asignadas con complementaria por ficha
        ctk.CTkLabel(scroll, text="Fichas Asignadas  (marca las que dicta)",
                    font=("Segoe UI", 11, "bold"), text_color="#2C3E50").pack(
                    anchor="w", padx=20, pady=(14, 4))
        ctk.CTkLabel(scroll,
                    text="  Selecciona la complementaria que dicta en esa ficha (opcional)",
                    font=("Segoe UI", 10, "italic"), text_color="#888").pack(
                    anchor="w", padx=20, pady=(0, 6))

        todas_fichas = self.servicio.obtener_fichas()
        asignadas    = {}
        if not es_nuevo:
            for r in self.servicio.obtener_fichas_asignadas_instructor(
                    instructor['id_instructor']):
                asignadas[r['id_ficha']] = r['id_competencia_complementaria']

        complementarias = self.servicio.obtener_competencias_por_tipo("Complementaria")
        comp_ops = ["— Ninguna —"] + [
            f"{c['id_competencia']} | {c['nombre_competencia']}" for c in complementarias]

        fichas_vars    = {}
        fichas_comp_cb = {}

        f_fichas = ctk.CTkFrame(scroll, fg_color="white", corner_radius=8,
                               border_width=1, border_color="#E0E0E0")
        f_fichas.pack(fill="x", padx=20, pady=(0, 10))

        for fic in todas_fichas:
            fid  = fic['id_ficha']
            var  = tk.BooleanVar(value=(fid in asignadas))
            fichas_vars[fid] = var

            fila = ctk.CTkFrame(f_fichas, fg_color="transparent")
            fila.pack(fill="x", padx=10, pady=4)

            ctk.CTkCheckBox(
                fila,
                text=f"{fic['codigo_ficha']} — {fic['nombre_programa']} ({fic['jornada']})",
                variable=var, font=("Segoe UI", 10),
                fg_color=self.sena_green, hover_color=self.sena_dark).pack(side="left")

            cb_c = ttk.Combobox(fila, values=comp_ops, state="readonly", width=34)
            cb_c.pack(side="right", padx=(6, 4))
            id_cc = asignadas.get(fid)
            if id_cc:
                match_c = next((o for o in comp_ops if o.startswith(f"{id_cc} |")), None)
                cb_c.set(match_c or comp_ops[0])
            else:
                cb_c.set(comp_ops[0])
            fichas_comp_cb[fid] = cb_c

        # Nota contraseña
        ctk.CTkLabel(scroll,
                    text=("🔑 Contraseña inicial: sena123  (el instructor la cambiará al primer login)"
                          if es_nuevo else "🔑 La contraseña no se modifica desde este formulario."),
                    font=("Segoe UI", 10, "italic"), text_color="#888").pack(
                    anchor="w", padx=20, pady=(4, 2))

        lbl_err = ctk.CTkLabel(scroll, text="", font=("Segoe UI", 10),
                              text_color="#E74C3C")
        lbl_err.pack(pady=(4, 0))

        def guardar():
            doc = e_doc.get().strip()
            nom = e_nom.get().strip()
            cor = e_cor.get().strip()
            usu = e_usu.get().strip()
            if not doc or not nom or not usu:
                lbl_err.configure(text="⚠ Documento, Nombre y Usuario son obligatorios.")
                return

            id_comp_p = None
            esp_sel = cb_esp.get()
            if not esp_sel.startswith("—"):
                try:
                    id_comp_p = int(esp_sel.split(" | ")[0])
                except Exception:
                    pass

            fichas_sel   = [fid for fid, v in fichas_vars.items() if v.get()]
            comp_x_ficha = {}
            for fid in fichas_sel:
                c_sel = fichas_comp_cb[fid].get()
                if not c_sel.startswith("—"):
                    try:
                        comp_x_ficha[fid] = int(c_sel.split(" | ")[0])
                    except Exception:
                        pass

            datos = {
                'documento':                   doc,
                'nombre_completo':             nom,
                'correo':                      cor,
                'usuario':                     usu,
                'id_competencia_principal':    id_comp_p,
                'fichas':                      fichas_sel,
                'comp_complementaria_por_ficha': comp_x_ficha,
            }

            if es_nuevo:
                ok, msg = self.servicio.crear_instructor(datos)
            else:
                ok, msg = self.servicio.actualizar_instructor(
                    instructor['id_instructor'], datos)

            if ok:
                messagebox.showinfo("✅ Éxito", msg)
                ven.destroy()
                self._cargar_tabla_instructores()
            else:
                lbl_err.configure(text=f"⚠ {msg}")

        # Botones fijos al fondo
        btn_f = ctk.CTkFrame(ven, fg_color="#F0F0F0", corner_radius=0)
        btn_f.pack(fill="x", side="bottom")
        ctk.CTkButton(btn_f, text="💾 GUARDAR", height=40,
                     fg_color=self.sena_green, hover_color=self.sena_dark,
                     font=("Segoe UI", 12, "bold"),
                     command=guardar).pack(side="left", padx=15, pady=10,
                                          expand=True, fill="x")
        ctk.CTkButton(btn_f, text="Cancelar", height=40, width=100,
                     fg_color="#95A5A6", hover_color="#7F8C8D",
                     command=ven.destroy).pack(side="right", padx=15, pady=10)

    def _construir_reportes(self):
        """Tab: Reportes (genera reportes de asistencia)"""
        # Delegar a ReportesManager para construir la pestaña
        self.app.crear_pestana_reportes(self.tab_frames['reportes'])
    
    def _construir_papelera(self):
        """Tab: Papelera (aprendices eliminados)"""
        # Tabla de papelera
        frame_tabla = ctk.CTkFrame(self.tab_frames['papelera'], fg_color="white",
                                   corner_radius=10, border_width=1,
                                   border_color="#E0E0E0")
        frame_tabla.pack(fill="both", expand=True, padx=0, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")
        
        self.tv_pap = ttk.Treeview(frame_tabla, 
                                  columns=("DOC", "NOMBRE", "FICHA"),
                                  show="headings", height=15,
                                  selectmode='extended',
                                  yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tv_pap.yview)
        
        self.tv_pap.heading("DOC", text="DOCUMENTO")
        self.tv_pap.heading("NOMBRE", text="NOMBRE COMPLETO")
        self.tv_pap.heading("FICHA", text="FICHA")
        
        self.tv_pap.column("DOC", width=130)
        self.tv_pap.column("NOMBRE", width=280)
        self.tv_pap.column("FICHA", width=120)
        
        self.tv_pap.pack(fill="both", expand=True)
        
        # Barra de acciones
        action_frame = ctk.CTkFrame(self.tab_frames['papelera'], fg_color="transparent")
        action_frame.pack(fill="x", padx=0, pady=10)
        
        ctk.CTkButton(action_frame, text="↩️ RESTAURAR",
                     fg_color=self.sena_green, hover_color="#32900D",
                     font=("Segoe UI", 11, "bold"),
                     command=self._restaurar_aprendices).pack(side="left", padx=5)
        
        ctk.CTkButton(action_frame, text="⚠️ ELIMINAR PERMANENTE",
                     fg_color="#E74C3C", hover_color="#C0392B",
                     font=("Segoe UI", 11, "bold"),
                     command=self._eliminar_permanente).pack(side="left", padx=5)
        
        ctk.CTkFrame(action_frame, fg_color="transparent").pack(side="left", expand=True)
        
        self._refrescar_papelera()
    
    def _refrescar_papelera(self):
        """Recarga papelera"""
        if not hasattr(self, 'tv_pap'):
            return
            
        for i in self.tv_pap.get_children():
            self.tv_pap.delete(i)
        
        self.db.cursor.execute(
            "SELECT documento, nombre_completo, id_ficha FROM estudiantes_eliminados ORDER BY nombre_completo ASC"
        )
        for r in self.db.cursor.fetchall():
            self.tv_pap.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))
    
    def _restaurar_aprendices(self):
        """Restaura aprendices desde papelera"""
        if not hasattr(self, 'tv_pap'):
            return
            
        docs = [self.tv_pap.item(i)['values'][0] for i in self.tv_pap.selection()]
        if not docs:
            messagebox.showwarning("Atención", "Selecciona al menos un aprendiz")
            return
        if messagebox.askyesno("Confirmar", f"¿Restaurar {len(docs)} aprendiz(ces)?"):
            for d in docs:
                self.servicio.restaurar_aprendiz(d)
                try:
                    self.db.registrar_auditoria(self.admin_usuario, "restaurar aprendiz", objeto=d)
                except Exception as ex:
                    logging.error(f"Error auditoría restaurar", exc_info=True)
            self._refrescar_papelera()
            self._filtrar_gestion()
            messagebox.showinfo("Éxito", f"{len(docs)} aprendiz(ces) restaurados")
    
    def _eliminar_permanente(self):
        """Elimina permanentemente aprendices"""
        if not hasattr(self, 'tv_pap'):
            return
            
        docs = [self.tv_pap.item(i)['values'][0] for i in self.tv_pap.selection()]
        if not docs:
            messagebox.showwarning("Atención", "Selecciona al menos un aprendiz")
            return
        if messagebox.askyesno("⚠️ ADVERTENCIA", 
                              f"Esta acción es IRREVERSIBLE.\n¿Eliminar permanentemente {len(docs)} aprendiz(ces)?"):
            for d in docs:
                self.servicio.eliminar_permanente(d)
                try:
                    self.db.registrar_auditoria(self.admin_usuario, "eliminar permanente", objeto=d)
                except Exception as ex:
                    logging.error(f"Error auditoría eliminar", exc_info=True)
            self._refrescar_papelera()
            messagebox.showinfo("Éxito", f"{len(docs)} aprendiz(ces) eliminados permanentemente")



class PantallaInstructor:
    """Gestiona la pantalla del instructor."""
    
    def __init__(self, frame_admin, db, servicio, instructor, app):
        self.frame = frame_admin
        self.db = db
        self.servicio = servicio
        self.instructor = instructor
        self.app = app
        
        self.sena_orange = COLORES['SENA_ORANGE']
        self.sena_green  = COLORES['SENA_GREEN']
        self.sena_dark   = COLORES['SENA_DARK']
        self.bg_light    = COLORES['BG_LIGHT']
        self.current_tab = None
        self.tab_frames = {}
        
        self._construir_layout()
    
    def _construir_layout(self):
        """Construye el layout del panel del instructor"""
        # Header
        head = ctk.CTkFrame(self.frame, height=100, corner_radius=0, 
                           fg_color=self.sena_orange, border_width=0)
        head.pack(fill="x", side="top")
        
        head_top = ctk.CTkFrame(head, fg_color="transparent")
        head_top.pack(side="top", fill="x", padx=25, pady=(15, 10))
        
        instructor_nombre = self.instructor.get('nombre_completo') or self.instructor.get('nombre') or self.instructor.get('usuario', 'N/A')
        ctk.CTkLabel(head_top, text=f"INSTRUCTOR: {instructor_nombre}", 
                    font=("Segoe UI", 16, "bold"),
                    text_color="white").pack(side="left")
        
        head_right = ctk.CTkFrame(head_top, fg_color="transparent")
        head_right.pack(side="right")
        
        ctk.CTkButton(head_right, text="🚪 CERRAR", width=100,
                     fg_color="#E74C3C", text_color="white",
                     font=("Segoe UI", 11, "bold"),
                     hover_color="#C0392B",
                     command=self._cerrar_instructor).pack(side="left", padx=8)
        
        # Navegación con botones
        nav_frame = ctk.CTkFrame(head, fg_color="transparent")
        nav_frame.pack(side="bottom", fill="x", padx=25, pady=(0, 15))
        
        self.nav_buttons = {}
        tabs = [
            ("📋 HISTORIAL", "historial"),
            ("📊 REPORTES", "reportes"),
            ("❌ REGISTRO DE FALTAS", "faltas"),
        ]
        
        for label, tab_id in tabs:
            btn = ctk.CTkButton(nav_frame, text=label, height=40,
                               fg_color=self.sena_green,
                               hover_color="#32900D",
                               font=("Segoe UI", 11, "bold"),
                               command=lambda t=tab_id: self._cambiar_tab(t))
            btn.pack(side="left", padx=5, expand=True, fill="x")
            self.nav_buttons[tab_id] = btn
        
        # Contenedor principal de pestañas
        self.main_container = ctk.CTkFrame(self.frame, fg_color=self.bg_light, corner_radius=5)
        self.main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Crear frames para cada pestaña
        for _, tab_id in tabs:
            f = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
            self.tab_frames[tab_id] = f
        
        # Construir contenido de cada pestaña
        self._construir_historial()
        self._construir_reportes()
        self._construir_faltas()
        
        # Mostrar la primera pestaña
        self._cambiar_tab("historial")
    
    def _cambiar_tab(self, tab_id):
        """Cambia a una pestaña"""
        # Ocultar todas
        for f in self.tab_frames.values():
            f.pack_forget()
        
        # Mostrar la seleccionada
        if tab_id in self.tab_frames:
            self.tab_frames[tab_id].pack(fill="both", expand=True)
            self.current_tab = tab_id
    
    def _construir_historial(self):
        """Construye la pestaña de historial"""
        f = self.tab_frames['historial']

        ctk.CTkLabel(f, text="📋 HISTORIAL DE ASISTENCIAS",
                    font=("Segoe UI", 14, "bold")).pack(pady=(15, 5))

        # ── Filtros ──────────────────────────────────────────────────────────
        f_filtros = ctk.CTkFrame(f, fg_color="#FFFFFF", corner_radius=8,
                                 border_width=1, border_color="#E0E0E0")
        f_filtros.pack(fill="x", padx=20, pady=10)

        fila = ctk.CTkFrame(f_filtros, fg_color="transparent")
        fila.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(fila, text="Ficha:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 8))
        id_instructor = self.instructor.get('id_instructor', 0)
        fichas = self.servicio.obtener_fichas_instructor(id_instructor)
        ficha_opciones = [f"{fc['codigo_ficha']} - {fc['nombre_programa']} ({fc['jornada']})"
                         for fc in fichas]

        self.combo_fichas = ctk.CTkComboBox(fila, values=ficha_opciones, width=340, height=34)
        self.combo_fichas.pack(side="left", padx=(0, 15))

        # Selector de mes
        ctk.CTkLabel(fila, text="Mes:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 8))
        hoy = datetime.date.today()
        meses = []
        self._hist_month_map = {}
        for i in range(12):
            d = (hoy.replace(day=1) - datetime.timedelta(days=i * 28)).replace(day=1)
            label = d.strftime("%B %Y")
            meses.append(label)
            self._hist_month_map[label] = d
        self.combo_hist_mes = ctk.CTkComboBox(fila, values=meses, width=160, height=34)
        self.combo_hist_mes.pack(side="left", padx=(0, 15))
        self.combo_hist_mes.set(meses[0])

        ctk.CTkButton(fila, text="🔍 Ver", height=34, width=90,
                     fg_color=self.sena_green, hover_color="#32900D",
                     font=("Segoe UI", 11, "bold"),
                     command=self._cargar_historial_ficha).pack(side="left")

        # ── Tabla ─────────────────────────────────────────────────────────────
        f_tabla = ctk.CTkFrame(f, fg_color="#FFFFFF", corner_radius=8,
                               border_width=1, border_color="#E0E0E0")
        f_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Estudiante", "Documento", "Fecha", "Entrada", "Salida")
        self.tv_historial = ttk.Treeview(f_tabla, columns=columns, height=16, show="headings")
        widths_h = {"Estudiante": 230, "Documento": 120, "Fecha": 110, "Entrada": 100, "Salida": 100}
        for col in columns:
            self.tv_historial.heading(col, text=col)
            self.tv_historial.column(col, width=widths_h[col], anchor="center")

        vsb_h = ttk.Scrollbar(f_tabla, orient="vertical", command=self.tv_historial.yview)
        self.tv_historial.configure(yscrollcommand=vsb_h.set)
        vsb_h.pack(side="right", fill="y", padx=(0, 5), pady=10)
        self.tv_historial.pack(fill="both", expand=True, padx=(10, 0), pady=10)

        self.lbl_hist_total = ctk.CTkLabel(f, text="", font=("Segoe UI", 10), text_color="#666")
        self.lbl_hist_total.pack(pady=(0, 5))

        # Cargar primera ficha automáticamente
        if ficha_opciones:
            self.combo_fichas.set(ficha_opciones[0])
            self.frame.after(150, self._cargar_historial_ficha)

    def _cargar_historial_ficha(self):
        """Carga el historial de la ficha seleccionada"""
        sel = self.combo_fichas.get()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona una ficha")
            return

        id_instructor = self.instructor.get('id_instructor', 0)
        fichas = self.servicio.obtener_fichas_instructor(id_instructor)
        codigo_sel = sel.split(" - ")[0].strip()
        id_ficha = next((fc['id_ficha'] for fc in fichas if fc['codigo_ficha'] == codigo_sel), None)
        if not id_ficha:
            return

        # Rango del mes seleccionado
        mes_label = self.combo_hist_mes.get()
        fecha_inicio = self._hist_month_map.get(mes_label, datetime.date.today().replace(day=1))
        import calendar as _cal
        ultimo = _cal.monthrange(fecha_inicio.year, fecha_inicio.month)[1]
        fecha_fin = fecha_inicio.replace(day=ultimo)

        estudiantes = self.servicio.obtener_estudiantes_ficha(id_ficha)

        for item in self.tv_historial.get_children():
            self.tv_historial.delete(item)

        total = 0
        for est in estudiantes:
            registros = self.servicio.obtener_registros_mes(est['documento'], fecha_inicio, fecha_fin)
            for reg in registros:
                entrada = reg['fecha_registro'].strftime('%H:%M') if reg['fecha_registro'] else "N/A"
                salida = reg['fecha_salida'].strftime('%H:%M') if reg['fecha_salida'] else "---"
                fecha_dia = (reg['fecha_registro'].date()
                             if hasattr(reg['fecha_registro'], 'date')
                             else reg['fecha_registro'])
                self.tv_historial.insert("", tk.END, values=(
                    est['nombre_completo'], est['documento'], fecha_dia, entrada, salida
                ))
                total += 1

        self.lbl_hist_total.configure(text=f"{total} registro(s) encontrado(s)")
    
    def _construir_reportes(self):
        """Construye la pestaña de reportes del instructor — filtrada por sus fichas"""
        f = self.tab_frames['reportes']

        ctk.CTkLabel(f, text="📊 REPORTES DE ASISTENCIA",
                    font=("Segoe UI", 14, "bold")).pack(pady=(15, 5))

        # ── Filtros ──────────────────────────────────────────────────────────
        f_filtros = ctk.CTkFrame(f, fg_color="#FFFFFF", corner_radius=8,
                                 border_width=1, border_color="#E0E0E0")
        f_filtros.pack(fill="x", padx=20, pady=10)

        fila1 = ctk.CTkFrame(f_filtros, fg_color="transparent")
        fila1.pack(fill="x", padx=15, pady=10)

        # Ficha
        ctk.CTkLabel(fila1, text="Ficha:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 8))
        id_instructor = self.instructor.get('id_instructor', 0)
        fichas_rep = self.servicio.obtener_fichas_instructor(id_instructor)
        # "Todas" + lista de fichas
        self._fichas_rep_data = fichas_rep
        opciones_rep = ["— Todas las fichas —"] + [
            f"{fc['codigo_ficha']} - {fc['nombre_programa']}" for fc in fichas_rep]
        self.combo_rep_ficha = ctk.CTkComboBox(fila1, values=opciones_rep, width=320, height=34)
        self.combo_rep_ficha.pack(side="left", padx=(0, 20))
        self.combo_rep_ficha.set(opciones_rep[0])

        # Rango
        ctk.CTkLabel(fila1, text="Rango:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 8))
        self.combo_rep_rango = ctk.CTkComboBox(fila1,
                                                values=["Mes actual", "Mes anterior", "Últimos 3 meses"],
                                                width=180, height=34)
        self.combo_rep_rango.pack(side="left")
        self.combo_rep_rango.set("Mes actual")

        ctk.CTkButton(fila1, text="🔍 Generar", height=34, width=110,
                     fg_color=self.sena_green, hover_color="#32900D",
                     font=("Segoe UI", 11, "bold"),
                     command=self._generar_reporte_instructor).pack(side="left", padx=15)

        # ── Tabla de resultados ───────────────────────────────────────────────
        f_tabla_rep = ctk.CTkFrame(f, fg_color="#FFFFFF", corner_radius=8,
                                   border_width=1, border_color="#E0E0E0")
        f_tabla_rep.pack(fill="both", expand=True, padx=20, pady=10)

        cols_rep = ("Estudiante", "Documento", "Ficha", "Asistencias", "Faltas", "Retardos", "% Asistencia")
        self.tv_reporte = ttk.Treeview(f_tabla_rep, columns=cols_rep, show="headings", height=14)
        widths_rep = {"Estudiante": 200, "Documento": 110, "Ficha": 130,
                      "Asistencias": 100, "Faltas": 80, "Retardos": 90, "% Asistencia": 110}
        for col in cols_rep:
            self.tv_reporte.heading(col, text=col)
            self.tv_reporte.column(col, width=widths_rep[col], anchor="center")

        vsb_rep = ttk.Scrollbar(f_tabla_rep, orient="vertical", command=self.tv_reporte.yview)
        self.tv_reporte.configure(yscrollcommand=vsb_rep.set)
        vsb_rep.pack(side="right", fill="y", padx=(0, 5), pady=10)
        self.tv_reporte.pack(fill="both", expand=True, padx=(10, 0), pady=10)

        self.lbl_rep_resumen = ctk.CTkLabel(f, text="", font=("Segoe UI", 11, "bold"),
                                            text_color=self.sena_green)
        self.lbl_rep_resumen.pack(pady=(0, 8))

    def _generar_reporte_instructor(self):
        """Genera el reporte de asistencia filtrado por ficha y rango"""
        import calendar as _cal

        # Determinar rango de fechas
        hoy = datetime.date.today()
        rango_sel = self.combo_rep_rango.get()
        if rango_sel == "Mes actual":
            fecha_inicio = hoy.replace(day=1)
            fecha_fin = hoy
        elif rango_sel == "Mes anterior":
            primer_dia_mes = hoy.replace(day=1)
            fecha_fin = primer_dia_mes - datetime.timedelta(days=1)
            fecha_inicio = fecha_fin.replace(day=1)
        else:  # Últimos 3 meses
            fecha_inicio = (hoy.replace(day=1) - datetime.timedelta(days=62)).replace(day=1)
            fecha_fin = hoy

        # Determinar fichas a analizar
        sel = self.combo_rep_ficha.get()
        if sel.startswith("—"):
            fichas_sel = self._fichas_rep_data
        else:
            codigo = sel.split(" - ")[0]
            fichas_sel = [fc for fc in self._fichas_rep_data if fc['codigo_ficha'] == codigo]

        # Limpiar tabla
        for item in self.tv_reporte.get_children():
            self.tv_reporte.delete(item)

        total_asist = total_faltas = total_ret = 0

        for ficha in fichas_sel:
            id_ficha = ficha['id_ficha']
            estudiantes = self.servicio.obtener_estudiantes_ficha(id_ficha)
            for est in estudiantes:
                doc = est['documento']

                # ── Marcas del INSTRUCTOR (fuente de verdad) ──────────────────
                self.db.cursor.execute(
                    "SELECT fecha_falta, tipo_falta FROM faltas "
                    "WHERE documento_estudiante=%s AND id_ficha=%s "
                    "AND fecha_falta BETWEEN %s AND %s",
                    (doc, id_ficha, fecha_inicio, fecha_fin)
                )
                marcas_instructor = {}
                for row in self.db.cursor.fetchall():
                    marcas_instructor[row['fecha_falta']] = row['tipo_falta']

                # ── Días con asistencia del aprendiz ──────────────────────────
                self.db.cursor.execute(
                    "SELECT DISTINCT DATE(fecha_registro) as dia FROM asistencias "
                    "WHERE documento_estudiante=%s AND DATE(fecha_registro) BETWEEN %s AND %s",
                    (doc, fecha_inicio, fecha_fin)
                )
                dias_asistencia = {row['dia'] for row in self.db.cursor.fetchall()}

                # ── Días de clase del rango según horario ─────────────────────
                self.db.cursor.execute(
                    "SELECT DISTINCT dia_semana FROM horarios WHERE id_ficha=%s", (id_ficha,))
                dias_horario = {r['dia_semana'] for r in self.db.cursor.fetchall()}
                _DIA = {'Lunes':0,'Martes':1,'Miércoles':2,'Jueves':3,'Viernes':4,'Sábado':5,'Domingo':6}
                dias_clase_idx = {_DIA[d] for d in dias_horario if d in _DIA} or {0,1,2,3,4}
                dias_clase_rango = [
                    fecha_inicio + datetime.timedelta(days=i)
                    for i in range((fecha_fin - fecha_inicio).days + 1)
                    if (fecha_inicio + datetime.timedelta(days=i)).weekday() in dias_clase_idx
                ]

                # ── Estado real por día (instructor tiene prioridad) ──────────
                asist = faltas = retardos = 0
                for dia in dias_clase_rango:
                    if dia in marcas_instructor:
                        tipo = marcas_instructor[dia]
                        if tipo == 'Retardo':
                            retardos += 1
                            asist += 1  # retardo = llegó, cuenta como asistencia
                        else:
                            faltas += 1
                    elif dia in dias_asistencia:
                        asist += 1

                total_dias = asist + faltas
                if total_dias > 0:
                    pct = f"{min(100, round(asist / total_dias * 100))}%"
                else:
                    pct = "N/A"

                # Color rojo si faltas > 3
                tag = "alerta" if faltas > 3 else ""
                self.tv_reporte.insert("", tk.END, tags=(tag,), values=(
                    est['nombre_completo'], doc,
                    ficha['codigo_ficha'], asist, faltas, retardos, pct
                ))
                total_asist += asist
                total_faltas += faltas
                total_ret += retardos

        self.tv_reporte.tag_configure("alerta", foreground="#E74C3C")
        self.lbl_rep_resumen.configure(
            text=f"Total: {total_asist} asistencias  |  {total_faltas} faltas  |  {total_ret} retardos"
        )

    def _construir_faltas(self):
        """Construye la pestaña de registro de faltas"""
        f = self.tab_frames['faltas']

        # Scrollable para que nada quede oculto
        scroll = ctk.CTkScrollableFrame(f, fg_color=self.bg_light)
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll, text="❌ REGISTRO DE FALTAS",
                    font=("Segoe UI", 14, "bold")).pack(pady=(15, 5))

        # ── Formulario ───────────────────────────────────────────────────────
        f_form = ctk.CTkFrame(scroll, fg_color="#FFFFFF", corner_radius=8,
                              border_width=1, border_color="#E0E0E0")
        f_form.pack(fill="x", padx=20, pady=10)

        # Ficha
        ctk.CTkLabel(f_form, text="Ficha:", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=15, pady=(15, 3))
        id_instructor = self.instructor.get('id_instructor', 0)
        fichas = self.servicio.obtener_fichas_instructor(id_instructor)
        ficha_opciones = [f"{fc['codigo_ficha']} - {fc['nombre_programa']} ({fc['jornada']})"
                         for fc in fichas]
        self.combo_faltas_ficha = ctk.CTkComboBox(f_form, values=ficha_opciones,
                                                   width=500, height=36,
                                                   command=self._actualizar_estudiantes_faltas)
        self.combo_faltas_ficha.pack(padx=15, pady=(0, 10), fill="x")

        # Estudiante
        ctk.CTkLabel(f_form, text="Estudiante:", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=15, pady=(5, 3))
        self.combo_faltas_est = ctk.CTkComboBox(f_form, values=[], width=500, height=36)
        self.combo_faltas_est.pack(padx=15, pady=(0, 10), fill="x")

        # Tipo + Fecha en la misma fila
        f_row = ctk.CTkFrame(f_form, fg_color="transparent")
        f_row.pack(fill="x", padx=15, pady=(5, 5))

        f_tipo = ctk.CTkFrame(f_row, fg_color="transparent")
        f_tipo.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(f_tipo, text="Tipo de Falta:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.combo_tipo_falta = ctk.CTkComboBox(
            f_tipo, values=["Inasistencia", "Retardo", "Justificada"], height=36)
        self.combo_tipo_falta.pack(fill="x", pady=(3, 0))
        self.combo_tipo_falta.set("Inasistencia")

        f_fecha = ctk.CTkFrame(f_row, fg_color="transparent")
        f_fecha.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(f_fecha, text="Fecha (DD/MM/YYYY):", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.entry_fecha_falta = ctk.CTkEntry(f_fecha, placeholder_text="DD/MM/YYYY", height=36)
        self.entry_fecha_falta.pack(fill="x", pady=(3, 0))
        self.entry_fecha_falta.insert(0, datetime.date.today().strftime('%d/%m/%Y'))

        # Razón
        ctk.CTkLabel(f_form, text="Razón (opcional):",
                    font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=15, pady=(10, 3))
        self.text_razon = ctk.CTkTextbox(f_form, height=70)
        self.text_razon.pack(padx=15, pady=(0, 5), fill="x")

        # Botón registrar
        ctk.CTkButton(f_form, text="✅ Registrar Falta",
                     fg_color=self.sena_green, hover_color="#32900D",
                     font=("Segoe UI", 12, "bold"), height=44,
                     command=self._registrar_falta_click).pack(pady=(5, 15), padx=15, fill="x")

        # ── Panel de filtros para la tabla ───────────────────────────────────
        f_filtros = ctk.CTkFrame(scroll, fg_color="#F0F7FF", corner_radius=8,
                                 border_width=1, border_color="#B3D4F5")
        f_filtros.pack(fill="x", padx=20, pady=(10, 0))

        ctk.CTkLabel(f_filtros, text="🔍 Filtrar faltas registradas",
                    font=("Segoe UI", 11, "bold"), text_color="#1565C0").pack(
                    anchor="w", padx=15, pady=(10, 5))

        fila_filtros = ctk.CTkFrame(f_filtros, fg_color="transparent")
        fila_filtros.pack(fill="x", padx=15, pady=(0, 10))

        # Ficha del filtro
        ctk.CTkLabel(fila_filtros, text="Ficha:",
                    font=("Segoe UI", 11)).pack(side="left", padx=(0, 6))
        filtro_fichas_opciones = ["— Todas —"] + ficha_opciones
        self.combo_filtro_ficha = ctk.CTkComboBox(
            fila_filtros, values=filtro_fichas_opciones, width=300, height=34,
            command=self._actualizar_filtro_estudiantes)
        self.combo_filtro_ficha.pack(side="left", padx=(0, 15))
        self.combo_filtro_ficha.set("— Todas —")

        # Estudiante del filtro
        ctk.CTkLabel(fila_filtros, text="Estudiante:",
                    font=("Segoe UI", 11)).pack(side="left", padx=(0, 6))
        self.combo_filtro_est = ctk.CTkComboBox(
            fila_filtros, values=["— Todos —"], width=260, height=34,
            command=lambda v: self._aplicar_filtro_faltas())
        self.combo_filtro_est.pack(side="left", padx=(0, 15))
        self.combo_filtro_est.set("— Todos —")

        ctk.CTkButton(fila_filtros, text="🔍 Filtrar", height=34, width=90,
                     fg_color="#1565C0", hover_color="#0D47A1",
                     font=("Segoe UI", 11, "bold"),
                     command=self._aplicar_filtro_faltas).pack(side="left", padx=(0, 8))

        ctk.CTkButton(fila_filtros, text="✖ Limpiar", height=34, width=90,
                     fg_color="#888", hover_color="#666",
                     font=("Segoe UI", 11),
                     command=self._limpiar_filtro_faltas).pack(side="left")

        # ── Fila de fechas ────────────────────────────────────────────────────
        fila_fechas = ctk.CTkFrame(f_filtros, fg_color="transparent")
        fila_fechas.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkLabel(fila_fechas, text="Desde:",
                    font=("Segoe UI", 11)).pack(side="left", padx=(0, 6))
        self.entry_filtro_desde = ctk.CTkEntry(
            fila_fechas, placeholder_text="DD/MM/YYYY", width=120, height=34)
        self.entry_filtro_desde.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(fila_fechas, text="Hasta:",
                    font=("Segoe UI", 11)).pack(side="left", padx=(0, 6))
        self.entry_filtro_hasta = ctk.CTkEntry(
            fila_fechas, placeholder_text="DD/MM/YYYY", width=120, height=34)
        self.entry_filtro_hasta.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(fila_fechas, text="(dejar vacío para ver todas las fechas)",
                    font=("Segoe UI", 10), text_color="#888").pack(side="left")

        # ── Tabla de faltas registradas ───────────────────────────────────────
        f_lista = ctk.CTkFrame(scroll, fg_color="#FFFFFF", corner_radius=8,
                               border_width=1, border_color="#E0E0E0")
        f_lista.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        self.lbl_faltas_titulo = ctk.CTkLabel(f_lista, text="📝 Faltas Registradas — Todas las fichas",
                    font=("Segoe UI", 12, "bold"))
        self.lbl_faltas_titulo.pack(pady=10)

        f_tree = tk.Frame(f_lista, bg="white")
        f_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        columns = ("Estudiante", "Tipo", "Fecha", "Razón", "Competencia")
        self.tv_faltas = ttk.Treeview(f_tree, columns=columns, height=8, show="headings")
        widths = {"Estudiante": 200, "Tipo": 110, "Fecha": 100, "Razón": 260, "Competencia": 180}
        for col in columns:
            self.tv_faltas.heading(col, text=col)
            self.tv_faltas.column(col, width=widths[col], anchor="w")

        vsb = ttk.Scrollbar(f_tree, orient="vertical", command=self.tv_faltas.yview)
        self.tv_faltas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tv_faltas.pack(side="left", fill="both", expand=True)

        self.lbl_faltas_count = ctk.CTkLabel(f_lista, text="",
                    font=("Segoe UI", 10), text_color="#666")
        self.lbl_faltas_count.pack(pady=(0, 8))

        # ── Inicializar y cargar DESPUÉS de que todos los widgets existen ─────
        self._id_ficha_actual = None
        self._id_competencia_actual = 33

        if ficha_opciones:
            self.combo_faltas_ficha.set(ficha_opciones[0])
            # after(100): garantiza que el frame está renderizado antes de cargar
            self.frame.after(100, self._actualizar_estudiantes_faltas)
            self.frame.after(120, self._aplicar_filtro_faltas)

    def _actualizar_estudiantes_faltas(self, valor_combo=None):
        """Actualiza la lista de estudiantes cuando cambia la ficha"""
        sel = self.combo_faltas_ficha.get()
        if not sel:
            return

        id_instructor = self.instructor.get('id_instructor', 0)
        fichas = self.servicio.obtener_fichas_instructor(id_instructor)
        # El código de ficha es la primera parte antes del primer " - "
        codigo_sel = sel.split(" - ")[0].strip()
        id_ficha = next((fc['id_ficha'] for fc in fichas if fc['codigo_ficha'] == codigo_sel), None)

        if not id_ficha:
            return

        estudiantes = self.servicio.obtener_estudiantes_ficha(id_ficha)
        est_opciones = [f"{e['documento']} - {e['nombre_completo']}" for e in estudiantes]
        self.combo_faltas_est.configure(values=est_opciones)
        self.combo_faltas_est.set(est_opciones[0] if est_opciones else "")

        # Guardar contexto para el registro
        self._id_ficha_actual = id_ficha
        try:
            self.db.cursor.execute(
                "SELECT id_competencia FROM ficha_competencias WHERE id_ficha=%s ORDER BY orden LIMIT 1",
                (id_ficha,)
            )
            row = self.db.cursor.fetchone()
            self._id_competencia_actual = row['id_competencia'] if row else 33
        except Exception:
            self._id_competencia_actual = 33

        # Refrescar tabla de faltas
        self._cargar_faltas_ficha(id_ficha)
    
    def _actualizar_filtro_estudiantes(self, valor_combo=None):
        """Actualiza el combo de estudiantes del filtro según la ficha seleccionada"""
        sel_ficha = self.combo_filtro_ficha.get()
        if sel_ficha.startswith("—"):
            # Todas las fichas: limpiar estudiante
            self.combo_filtro_est.configure(values=["— Todos —"])
            self.combo_filtro_est.set("— Todos —")
        else:
            id_instructor = self.instructor.get('id_instructor', 0)
            fichas = self.servicio.obtener_fichas_instructor(id_instructor)
            codigo_sel = sel_ficha.split(" - ")[0].strip()
            id_ficha = next((fc['id_ficha'] for fc in fichas if fc['codigo_ficha'] == codigo_sel), None)
            if id_ficha:
                estudiantes = self.servicio.obtener_estudiantes_ficha(id_ficha)
                opciones = ["— Todos —"] + [f"{e['documento']} - {e['nombre_completo']}"
                                             for e in estudiantes]
                self.combo_filtro_est.configure(values=opciones)
                self.combo_filtro_est.set("— Todos —")
        self._aplicar_filtro_faltas()

    def _aplicar_filtro_faltas(self, valor_combo=None):
        """Aplica los filtros de ficha, estudiante y rango de fechas a la tabla de faltas"""
        id_instructor = self.instructor.get('id_instructor', 0)
        fichas = self.servicio.obtener_fichas_instructor(id_instructor)

        sel_ficha = self.combo_filtro_ficha.get()
        sel_est = self.combo_filtro_est.get()

        # ── Parsear fechas opcionales ─────────────────────────────────────────
        fecha_desde = None
        fecha_hasta = None
        try:
            txt_desde = self.entry_filtro_desde.get().strip()
            if txt_desde:
                fecha_desde = datetime.datetime.strptime(txt_desde, '%d/%m/%Y').date()
        except (ValueError, AttributeError):
            pass
        try:
            txt_hasta = self.entry_filtro_hasta.get().strip()
            if txt_hasta:
                fecha_hasta = datetime.datetime.strptime(txt_hasta, '%d/%m/%Y').date()
        except (ValueError, AttributeError):
            pass

        # Determinar qué fichas consultar
        if sel_ficha.startswith("—"):
            fichas_a_consultar = fichas
            titulo = "📝 Faltas Registradas — Todas las fichas"
        else:
            codigo_sel = sel_ficha.split(" - ")[0].strip()
            fichas_a_consultar = [fc for fc in fichas if fc['codigo_ficha'] == codigo_sel]
            titulo = f"📝 Faltas Registradas — Ficha {codigo_sel}"

        # Determinar filtro de estudiante
        doc_filtro = None
        if not sel_est.startswith("—"):
            doc_filtro = sel_est.split(" - ")[0].strip()
            nombre_est = sel_est.split(" - ")[-1] if " - " in sel_est else sel_est
            titulo += f" — {nombre_est}"

        # Agregar rango de fechas al título si aplica
        if fecha_desde or fecha_hasta:
            desde_str = fecha_desde.strftime('%d/%m/%Y') if fecha_desde else "inicio"
            hasta_str = fecha_hasta.strftime('%d/%m/%Y') if fecha_hasta else "hoy"
            titulo += f" [{desde_str} → {hasta_str}]"

        self.lbl_faltas_titulo.configure(text=titulo)

        # Limpiar tabla
        for item in self.tv_faltas.get_children():
            self.tv_faltas.delete(item)

        total = 0
        for ficha in fichas_a_consultar:
            faltas = self.servicio.obtener_faltas_ficha(ficha['id_ficha'])
            for falta in faltas:
                # Filtro de estudiante
                if doc_filtro and falta.get('documento_estudiante') != doc_filtro:
                    continue
                # Filtro de fechas
                fecha_falta = falta.get('fecha_falta')
                if fecha_falta:
                    if hasattr(fecha_falta, 'date'):
                        fecha_falta = fecha_falta.date()
                    if fecha_desde and fecha_falta < fecha_desde:
                        continue
                    if fecha_hasta and fecha_falta > fecha_hasta:
                        continue
                self.tv_faltas.insert("", tk.END, values=(
                    falta.get('nombre_completo', 'N/A'),
                    falta.get('tipo_falta', 'N/A'),
                    falta.get('fecha_falta', 'N/A'),
                    falta.get('razon', '') or '—',
                    falta.get('nombre_competencia', 'N/A'),
                ))
                total += 1

        self.lbl_faltas_count.configure(text=f"{total} falta(s) encontrada(s)")

    def _limpiar_filtro_faltas(self):
        """Restablece todos los filtros incluyendo fechas"""
        self.combo_filtro_ficha.set("— Todas —")
        self.combo_filtro_est.configure(values=["— Todos —"])
        self.combo_filtro_est.set("— Todos —")
        self.entry_filtro_desde.delete(0, tk.END)
        self.entry_filtro_hasta.delete(0, tk.END)
        self._aplicar_filtro_faltas()

    def _cargar_faltas_ficha(self, id_ficha):
        """Recarga la tabla de faltas con el filtro actual (se llama tras registrar)"""
        # Sincronizar el combo de filtro con la ficha del formulario
        # para que el instructor vea de inmediato la falta que acaba de registrar
        fichas = self.servicio.obtener_fichas_instructor(self.instructor.get('id_instructor', 0))
        ficha_obj = next((fc for fc in fichas if fc['id_ficha'] == id_ficha), None)
        if ficha_obj:
            codigo = ficha_obj['codigo_ficha']
            programa = ficha_obj['nombre_programa']
            jornada = ficha_obj['jornada']
            etiqueta = f"{codigo} - {programa} ({jornada})"
            self.combo_filtro_ficha.set(etiqueta)
            self._actualizar_filtro_estudiantes()
        else:
            self._aplicar_filtro_faltas()
    
    def _registrar_falta_click(self):
        """Registra una falta en el sistema"""
        if not self.combo_faltas_ficha.get():
            messagebox.showwarning("Validación", "Selecciona una ficha")
            return
        if not self.combo_faltas_est.get():
            messagebox.showwarning("Validación", "Selecciona un estudiante")
            return

        try:
            fecha_str = self.entry_fecha_falta.get()
            fecha_falta = datetime.datetime.strptime(fecha_str, '%d/%m/%Y').date()

            est_sel = self.combo_faltas_est.get().split(" - ")[0].strip()

            id_ficha = getattr(self, '_id_ficha_actual', None)
            id_competencia = getattr(self, '_id_competencia_actual', 33)
            id_instructor = self.instructor.get('id_instructor', 0)

            if not id_ficha:
                messagebox.showwarning("Validación", "Error al obtener la ficha. Selecciónala de nuevo.")
                return

            tipo_falta = self.combo_tipo_falta.get()
            razon = self.text_razon.get("1.0", "end").strip()

            success, msg = self.servicio.registrar_falta(
                id_instructor, est_sel, id_ficha, id_competencia, fecha_falta, tipo_falta, razon,
                self.instructor.get('usuario', 'instructor')
            )

            if success:
                messagebox.showinfo("Éxito", msg)
                self._cargar_faltas_ficha(id_ficha)
                self.text_razon.delete("1.0", "end")
            else:
                messagebox.showerror("Error", msg)

        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Usa DD/MM/YYYY")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")
    
    def _cerrar_instructor(self):
        """Cierra la sesión del instructor"""
        if messagebox.askyesno("Cerrar", "¿Cerrar sesión?"):
            try:
                self.db.registrar_auditoria(self.instructor.get('usuario', 'instructor'), "logout instructor")
            except:
                pass
            self.app.mostrar_inicio()