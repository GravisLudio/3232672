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


# Configurar estilo de ttk
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
    """Gestiona toda la pantalla de administrador con diseño profesional."""
    
    def __init__(self, frame_admin, db, servicio, admin_usuario, app):
        self.frame = frame_admin
        self.db = db
        self.servicio = servicio
        self.admin_usuario = admin_usuario
        self.app = app
        
        self.sena_orange = COLORES['SENA_ORANGE']
        self.sena_green = COLORES['SENA_GREEN']
        self.bg_light = COLORES['BG_LIGHT']
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
        
        ctk.CTkButton(head_right, text="📊 DASHBOARD", width=140,
                     fg_color="white", text_color=self.sena_orange,
                     font=("Segoe UI", 11, "bold"),
                     hover_color="#F5F5F5",
                     command=self.app.mostrar_dashboard).pack(side="left", padx=8)
        
        ctk.CTkButton(head_right, text="🚪 CERRAR", width=100,
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
        self.tab_frames['historial'] = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        self.tab_frames['gestion'] = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        self.tab_frames['registro'] = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        self.tab_frames['reportes'] = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        self.tab_frames['papelera'] = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        
        # Construir contenido de cada pestaña (sin mostrar aún)
        self._construir_historial()
        self._construir_gestion()
        self._construir_registro()
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
        
        # Barra de acciones
        action_frame = ctk.CTkFrame(self.tab_frames['gestion'], fg_color="transparent")
        action_frame.pack(fill="x", padx=0, pady=10)
        
        ctk.CTkButton(action_frame, text="🗑️ MOVER A PAPELERA", 
                     fg_color="#E74C3C", hover_color="#C0392B",
                     font=("Segoe UI", 11, "bold"),
                     command=self._mover_papelera).pack(side="left", padx=5)
        
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

# ===== CLASE PANEL INSTRUCTOR =====

class PantallaInstructor:
    """Gestiona la pantalla del instructor."""
    
    def __init__(self, frame_admin, db, servicio, instructor, app):
        self.frame = frame_admin
        self.db = db
        self.servicio = servicio
        self.instructor = instructor
        self.app = app
        
        self.sena_orange = COLORES['SENA_ORANGE']
        self.sena_green = COLORES['SENA_GREEN']
        self.bg_light = COLORES['BG_LIGHT']
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
                    font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        # Frame para filtros
        f_filtros = ctk.CTkFrame(f, fg_color="#FFFFFF", corner_radius=5)
        f_filtros.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(f_filtros, text="Selecciona una ficha:", font=("Segoe UI", 11)).pack(side="left", padx=10, pady=10)
        
        id_instructor = self.instructor.get('id_instructor', 0)
        fichas = self.servicio.obtener_fichas_instructor(id_instructor)
        ficha_opciones = [f"{fc['codigo_ficha']} - {fc['nombre_programa']}" for fc in fichas]
        
        self.combo_fichas = ctk.CTkComboBox(f_filtros, values=ficha_opciones, width=300)
        self.combo_fichas.pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(f_filtros, text="Ver", width=100,
                     command=self._cargar_historial_ficha).pack(side="left", padx=5, pady=10)
        
        # Frame para tabla
        f_tabla = ctk.CTkFrame(f, fg_color="#FFFFFF", corner_radius=5)
        f_tabla.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Crear Treeview
        columns = ("Estudiante", "Documento", "Fecha", "Entrada", "Salida")
        self.tv_historial = ttk.Treeview(f_tabla, columns=columns, height=15, show="headings")
        
        for col in columns:
            self.tv_historial.heading(col, text=col)
            self.tv_historial.column(col, width=150)
        
        self.tv_historial.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _cargar_historial_ficha(self):
        """Carga el historial de una ficha seleccionada"""
        if not self.combo_fichas.get():
            messagebox.showwarning("Selección", "Selecciona una ficha")
            return
        
        # Obtener id_ficha desde la selección
        id_instructor = self.instructor.get('id_instructor', 0)
        fichas = self.servicio.obtener_fichas_instructor(id_instructor)
        ficha_selected = self.combo_fichas.get().split(" - ")[0]
        id_ficha = next((f['id_ficha'] for f in fichas if f['codigo_ficha'] == ficha_selected), None)
        
        if not id_ficha:
            return
        
        # Obtener estudiantes de la ficha
        estudiantes = self.servicio.obtener_estudiantes_ficha(id_ficha)
        
        # Limpiar tabla
        for item in self.tv_historial.get_children():
            self.tv_historial.delete(item)
        
        # Cargar registros de asistencia
        for est in estudiantes:
            # Obtener registros del mes actual
            hoy = datetime.date.today()
            fecha_inicio = hoy.replace(day=1)
            registros = self.servicio.obtener_registros_mes(est['documento'], fecha_inicio, hoy)
            
            for reg in registros:
                entrada = reg['fecha_registro'].strftime('%H:%M') if reg['fecha_registro'] else "N/A"
                salida = reg['fecha_salida'].strftime('%H:%M') if reg['fecha_salida'] else "---"
                
                self.tv_historial.insert("", tk.END, values=(
                    est['nombre_completo'],
                    est['documento'],
                    reg['fecha_registro'].date() if hasattr(reg['fecha_registro'], 'date') else reg['fecha_registro'],
                    entrada,
                    salida
                ))
    
    def _construir_reportes(self):
        """Construye la pestaña de reportes"""
        f = self.tab_frames['reportes']
        
        ctk.CTkLabel(f, text="📊 REPORTES DE ASISTENCIA", 
                    font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        ctk.CTkLabel(f, text="Módulo de reportes disponible", 
                    font=("Segoe UI", 12)).pack(pady=50)
    
    def _construir_faltas(self):
        """Construye la pestaña de registro de faltas"""
        f = self.tab_frames['faltas']
        
        ctk.CTkLabel(f, text="❌ REGISTRO DE FALTAS", 
                    font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        # Frame para formulario de registro
        f_form = ctk.CTkFrame(f, fg_color="#FFFFFF", corner_radius=5)
        f_form.pack(fill="x", padx=20, pady=10)
        
        # Seleccionar ficha
        ctk.CTkLabel(f_form, text="Ficha:", font=("Segoe UI", 11)).pack(anchor="w", padx=15, pady=(15, 5))
        id_instructor = self.instructor.get('id_instructor', 0)
        fichas = self.servicio.obtener_fichas_instructor(id_instructor)
        ficha_opciones = [f"{fc['codigo_ficha']} - {fc['nombre_programa']}" for fc in fichas]
        self.combo_faltas_ficha = ctk.CTkComboBox(f_form, values=ficha_opciones, width=400)
        self.combo_faltas_ficha.pack(padx=15, pady=5, fill="x")
        
        # Seleccionar estudiante
        ctk.CTkLabel(f_form, text="Estudiante:", font=("Segoe UI", 11)).pack(anchor="w", padx=15, pady=(15, 5))
        self.combo_faltas_est = ctk.CTkComboBox(f_form, values=[], width=400)
        self.combo_faltas_est.pack(padx=15, pady=5, fill="x")
        
        # Actualizar estudiantes cuando cambia la ficha
        self.combo_faltas_ficha.configure(command=self._actualizar_estudiantes_faltas)
        
        # Tipo de falta
        ctk.CTkLabel(f_form, text="Tipo de Falta:", font=("Segoe UI", 11)).pack(anchor="w", padx=15, pady=(15, 5))
        self.combo_tipo_falta = ctk.CTkComboBox(f_form, values=["Inasistencia", "Retardo", "Justificada"], width=400)
        self.combo_tipo_falta.pack(padx=15, pady=5, fill="x")
        self.combo_tipo_falta.set("Inasistencia")
        
        # Fecha
        ctk.CTkLabel(f_form, text="Fecha:", font=("Segoe UI", 11)).pack(anchor="w", padx=15, pady=(15, 5))
        self.entry_fecha_falta = ctk.CTkEntry(f_form, placeholder_text="DD/MM/YYYY", width=400)
        self.entry_fecha_falta.pack(padx=15, pady=5, fill="x")
        self.entry_fecha_falta.insert(0, datetime.date.today().strftime('%d/%m/%Y'))
        
        # Razón
        ctk.CTkLabel(f_form, text="Razón (opcional):", font=("Segoe UI", 11)).pack(anchor="w", padx=15, pady=(15, 5))
        self.text_razon = ctk.CTkTextbox(f_form, height=80, width=400)
        self.text_razon.pack(padx=15, pady=5, fill="x")
        
        # Botón registrar
        ctk.CTkButton(f_form, text="✅ Registrar Falta", fg_color=self.sena_green,
                     hover_color="#32900D", font=("Segoe UI", 12, "bold"),
                     command=self._registrar_falta_click).pack(pady=20, padx=15, fill="x")
        
        # Frame para lista de faltas registradas
        f_lista = ctk.CTkFrame(f, fg_color="#FFFFFF", corner_radius=5)
        f_lista.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(f_lista, text="📝 Faltas Registradas", 
                    font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        columns = ("Estudiante", "Tipo", "Fecha", "Razón")
        self.tv_faltas = ttk.Treeview(f_lista, columns=columns, height=10, show="headings")
        
        for col in columns:
            self.tv_faltas.heading(col, text=col)
            self.tv_faltas.column(col, width=150)
        
        self.tv_faltas.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _actualizar_estudiantes_faltas(self):
        """Actualiza la lista de estudiantes cuando cambia la ficha"""
        if not self.combo_faltas_ficha.get():
            return
        
        id_instructor = self.instructor.get('id_instructor', 0)
        fichas = self.servicio.obtener_fichas_instructor(id_instructor)
        ficha_selected = self.combo_faltas_ficha.get().split(" - ")[0]
        id_ficha = next((f['id_ficha'] for f in fichas if f['codigo_ficha'] == ficha_selected), None)
        
        if id_ficha:
            estudiantes = self.servicio.obtener_estudiantes_ficha(id_ficha)
            est_opciones = [f"{e['documento']} - {e['nombre_completo']}" for e in estudiantes]
            self.combo_faltas_est.configure(values=est_opciones)
            
            # Cargar faltas de la ficha
            self._cargar_faltas_ficha(id_ficha)
    
    def _cargar_faltas_ficha(self, id_ficha):
        """Carga las faltas registradas de una ficha"""
        faltas = self.servicio.obtener_faltas_ficha(id_ficha)
        
        # Limpiar tabla
        for item in self.tv_faltas.get_children():
            self.tv_faltas.delete(item)
        
        # Cargar faltas
        for falta in faltas:
            self.tv_faltas.insert("", tk.END, values=(
                falta.get('nombre_completo', 'N/A'),
                falta.get('tipo_falta', 'N/A'),
                falta.get('fecha_falta', 'N/A'),
                falta.get('razon', '')
            ))
    
    def _registrar_falta_click(self):
        """Registra una falta en el sistema"""
        if not self.combo_faltas_est.get():
            messagebox.showwarning("Validación", "Selecciona un estudiante")
            return
        if not self.combo_faltas_ficha.get():
            messagebox.showwarning("Validación", "Selecciona una ficha")
            return
        
        try:
            # Parsear fecha
            fecha_str = self.entry_fecha_falta.get()
            fecha_falta = datetime.datetime.strptime(fecha_str, '%d/%m/%Y').date()
            
            # Obtener datos del estudiante y ficha
            est_sel = self.combo_faltas_est.get().split(" - ")[0]
            id_instructor = self.instructor.get('id_instructor', 0)
            fichas = self.servicio.obtener_fichas_instructor(id_instructor)
            ficha_selected = self.combo_faltas_ficha.get().split(" - ")[0]
            id_ficha = next((f['id_ficha'] for f in fichas if f['codigo_ficha'] == ficha_selected), None)
            
            # Usar competencia 33 como default (o la primera de la ficha)
            id_competencia = 33
            
            tipo_falta = self.combo_tipo_falta.get()
            razon = self.text_razon.get("1.0", "end").strip()
            
            success, msg = self.servicio.registrar_falta(
                est_sel, id_ficha, id_competencia, fecha_falta, tipo_falta, razon, 
                self.instructor.get('usuario', 'instructor')
            )
            
            if success:
                messagebox.showinfo("Éxito", msg)
                self._actualizar_estudiantes_faltas()
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
            self.app.show_frame('intro')
            self.app.animacion_entrada()