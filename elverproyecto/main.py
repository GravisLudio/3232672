import tkinter as tk 
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from conexion import InventarioDB 
from tkcalendar import Calendar
import datetime
import re
import customtkinter as ctk 
import logging
from logging_config import configure_logging

# helper tooltip class for UI hints
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)
    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = y = 0
        x = event.x_root + 10
        y = event.y_root + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left', background='#ffffe0', relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

from logica import AsistenciaService 

ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("green")

# Configurar logging centralizado
configure_logging()



class SistemaHSGSCRS:
    def __init__(self, root):
        self.root = root
        self.root.title("C.R.S - Chronos Registry System")
        
        self.db = InventarioDB()
        if self.db.conexion:
            self.db.cursor = self.db.conexion.cursor(dictionary=True, buffered=True)

        self.servicio = AsistenciaService(self.db)
        self.admin_actual = None
        self.aprendiz_actual = None 
        self.sena_green = "#39A900"
        self.sena_dark = "#2D5A27"
        self.bg_light = "#E2E2E2"

        self.main_container = ctk.CTkFrame(self.root, fg_color=self.bg_light, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        self.root.withdraw() 
        self.root.after(100, self.lanzar_sistema)
        

    def lanzar_sistema(self):
        self.root.deiconify() 
        self.root.state('zoomed') 
        self.animacion_entrada()
        
    def limpiar_pantalla(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def animacion_entrada(self):
        self.limpiar_pantalla()
        self.f_intro = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.f_intro.place(relx=0.5, rely=0.4, anchor="center")
        self.lbl_siglas = ctk.CTkLabel(self.f_intro, text="C.R.S", font=("Segoe UI", 10, "bold"), text_color="#D1D1D1")
        self.lbl_siglas.pack()
        self.size_actual = 10
        self.root.after(20, lambda: self.animar_ciclo())

    def animar_ciclo(self, paso=0):
        total_pasos = 100
        size_inicial = 10
        target = 120

        if paso <= total_pasos:
            progreso = paso / total_pasos
            factor = 1 - (1 - progreso) ** 3 
            
            self.size_actual = int(size_inicial + (target - size_inicial) * factor)
        
            color_inicio = (136, 136, 136)
            color_fin = (57, 181, 74)
            
            r = int(color_inicio[0] + (color_fin[0] - color_inicio[0]) * progreso)
            g = int(color_inicio[1] + (color_fin[1] - color_inicio[1]) * progreso)
            b = int(color_inicio[2] + (color_fin[2] - color_inicio[2]) * progreso)
            
            color_hex = f'#{r:02x}{g:02x}{b:02x}'

            self.lbl_siglas.configure(
                text_color=color_hex,
                font=("Segoe UI", self.size_actual, "bold")
            )
            
            self.root.after(10, lambda: self.animar_ciclo(paso + 1))
        
        else:
            self.lbl_nombre = ctk.CTkLabel(self.f_intro, text="CHRONOS REGISTRY SYSTEM", 
                                        font=("Segoe UI", 1, "bold"), text_color="#555")
            self.lbl_nombre.pack(pady=20)
            self.efecto_pop(1)

    def efecto_pop(self, size):
        if size < 22:
            diff = 22 - size
            step = max(1, diff // 4)
            size += step
            self.lbl_nombre.configure(font=("Segoe UI", size, "bold"))
            self.root.after(10, lambda: self.efecto_pop(size))
        else:
            self.root.after(2000, self.mostrar_inicio)


    
    def mostrar_inicio(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=500, height=550, corner_radius=20,
                         fg_color=self.bg_light, border_width=2, border_color="#E0E0E0")
        f.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(f, text="GATEWAY C.R.S", font=("Segoe UI", 32, "bold"), text_color=self.sena_dark).pack(pady=(50, 5))
        ctk.CTkLabel(f, text="Chronos Registry System | High Softwares", font=("Segoe UI", 13), text_color="#888").pack(pady=(0, 40))

        ctk.CTkButton(f, text="TERMINAL APRENDICES", height=55, width=350, corner_radius=10,
                       command=self.mostrar_terminal).pack(pady=10, padx=20)
        ctk.CTkButton(f, text="PANEL ADMINISTRATIVO", height=55, width=350, corner_radius=10,
                       fg_color="#333", hover_color="#1a1a1a", command=self.mostrar_login).pack(pady=10, padx=20)
        ctk.CTkButton(f, text="MI PERFIL (APRENDIZ)", height=55, width=350, corner_radius=10,
                       fg_color="transparent", text_color=self.sena_green, border_width=2,
                       border_color=self.sena_green, hover_color="#E8F5E9", command=self.login_aprendiz_view).pack(pady=10, padx=20)

    def mostrar_terminal(self):
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=70, corner_radius=0, fg_color=self.sena_green); head.pack(fill="x")
        ctk.CTkButton(head, text="⬅ VOLVER", width=140, fg_color=self.sena_dark, command=self.mostrar_inicio).pack(side="left", padx=25, pady=15)
        f = ctk.CTkFrame(self.main_container, width=650, height=550, corner_radius=25, fg_color=self.bg_light, border_width=1, border_color="#DDD"); f.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f, text="REGISTRO DE ASISTENCIA", font=("Segoe UI", 26, "bold")).pack(pady=35)
        ent_doc = ctk.CTkEntry(f, font=("Segoe UI", 30), width=480, height=80, placeholder_text="N° Documento", justify="center"); ent_doc.pack(pady=25); ent_doc.focus()

        def procesar(tipo):
            exito, msg = self.servicio.registrar_entrada(ent_doc.get()) if tipo=="in" else self.servicio.registrar_salida(ent_doc.get())
            if exito: messagebox.showinfo("C.R.S", msg); ent_doc.delete(0, tk.END)
            else: messagebox.showwarning("Atención", msg)

        ctk.CTkButton(f, text=" MARCAR ENTRADA", font=("bold", 16), height=65, width=450, command=lambda:procesar("in")).pack(pady=10)
        ctk.CTkButton(f, text=" MARCAR SALIDA", font=("bold", 16), height=65, width=450, fg_color="#E67E22", hover_color="#D35400", command=lambda:procesar("out")).pack(pady=10)

    def login_aprendiz_view(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=450, height=480, corner_radius=25,
                         fg_color=self.bg_light, border_width=2, border_color="#DDD")
        f.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(f, text="ACCESO APRENDIZ", font=("Segoe UI", 24, "bold")).pack(pady=35)
        u_ent = ctk.CTkEntry(f, width=320, height=50, placeholder_text="Documento"); u_ent.pack(pady=12, padx=20)
        p_ent = ctk.CTkEntry(f, width=320, height=50, placeholder_text="Contraseña", show="*"); p_ent.pack(pady=12, padx=20)
        
        ctk.CTkButton(f, text="INGRESAR", width=320, height=55, command=lambda:self.entrar(u_ent, p_ent)).pack(pady=35, padx=20)
        ctk.CTkButton(f, text="VOLVER", fg_color="transparent", text_color="gray", command=self.mostrar_inicio).pack(padx=20)
        
        def entrar(u_ent, p_ent):
            user = self.servicio.login_aprendiz(u_ent.get(), p_ent.get())
            if user:
                self.aprendiz_actual = u_ent.get()
                if not self.db.registrar_auditoria(self.aprendiz_actual, "login aprendiz"):
                    logging.warning("Advertencia: No se pudo registrar la auditoría de login.")
                if user.get('cambio_pass') == 0 or p_ent.get() == 'sena123': self.actualizar_password_ventana(user['documento'])
                self.mostrar_panel_aprendiz(user)
            else: messagebox.showerror("Error", "Credenciales Incorrectas")
            
        
        

    def mostrar_panel_aprendiz(self, user):
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=75, corner_radius=0, fg_color=self.bg_light, border_width=1, border_color="#EEE"); head.pack(fill="x")
        def cerrar_aprendiz():
            if self.aprendiz_actual:
                try:
                    self.db.registrar_auditoria(self.aprendiz_actual, "logout aprendiz")
                except Exception as ex:
                    logging.error("Error registrando auditoría (logout aprendiz)", exc_info=True)
            self.aprendiz_actual = None
            self.mostrar_inicio()
        ctk.CTkButton(head, text="🚪 CERRAR SESIÓN", fg_color="#FF5252", hover_color="#D32F2F", command=cerrar_aprendiz).pack(side="left", padx=25)
        ctk.CTkLabel(head, text=f"Aprendiz: {user['nombre_completo']}", font=("Segoe UI", 15, "bold")).pack(side="right", padx=35)

        body = ctk.CTkFrame(self.main_container, fg_color="transparent"); body.pack(fill="both", expand=True, padx=45, pady=25)
        left = ctk.CTkFrame(body, corner_radius=20, fg_color=self.bg_light, border_width=1, border_color="#DDD"); left.place(relx=0, rely=0, relwidth=0.64, relheight=1)
        cal = Calendar(left, selectmode='day', locale='es_ES', background=self.sena_green, headersbackground=self.sena_dark); cal.pack(fill="both", expand=True, padx=25, pady=25)
        right = ctk.CTkFrame(body, corner_radius=20, fg_color=self.bg_light, border_width=1, border_color="#DDD"); right.place(relx=0.66, rely=0, relwidth=0.34, relheight=1)
        lbl_info = ctk.CTkLabel(right, text="Actividad del día", font=("Segoe UI", 18, "bold")); lbl_info.pack(pady=20)
        
        container_cards = ctk.CTkScrollableFrame(right, fg_color="transparent"); container_cards.pack(fill="both", expand=True, padx=12, pady=8)

        def actualizar_cards(e=None):
            for w in container_cards.winfo_children(): w.destroy()
            fecha = cal.selection_get()
            regs = self.servicio.obtener_registros_dia(user['documento'], fecha)
            if not regs: ctk.CTkLabel(container_cards, text="Sin actividad este día", text_color="#AAA").pack(pady=60)
            else:
                for r in regs:
                    card = ctk.CTkFrame(container_cards, fg_color="#F8F9FA", corner_radius=12, border_width=1, border_color="#EEE"); card.pack(fill="x", pady=6, padx=8)
                    ctk.CTkLabel(card, text=f"📥 Ent: {r['fecha_registro'].strftime('%H:%M')}", font=("Segoe UI", 11)).pack(side="left", padx=15, pady=12)
                    if r['fecha_salida']: ctk.CTkLabel(card, text=f"📤 Sal: {r['fecha_salida'].strftime('%H:%M')}", font=("Segoe UI", 11), text_color="#E67E22").pack(side="right", padx=15)
        cal.bind("<<CalendarSelected>>", actualizar_cards); actualizar_cards()

    def mostrar_login(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=420, height=480, corner_radius=25, fg_color=self.bg_light); f.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f, text="ADMINISTRACIÓN", font=("Segoe UI", 24, "bold")).pack(pady=35)
        u_ent = ctk.CTkEntry(f, placeholder_text="Usuario", width=300, height=50); u_ent.pack(pady=12)
        p_ent = ctk.CTkEntry(f, placeholder_text="Contraseña", show="*", width=300, height=50); p_ent.pack(pady=12)
        def log_admin():
            usuario = u_ent.get()
            self.db.cursor.execute("SELECT * FROM usuarios_admin WHERE usuario=%s AND password=%s", (usuario, p_ent.get()))
            if self.db.cursor.fetchone():
                self.admin_actual = usuario
                try:
                    self.db.registrar_auditoria(self.admin_actual, "login admin")
                except Exception as ex:
                    logging.error("Error registrando auditoría (login admin)", exc_info=True)
                self.mostrar_panel_admin_ui()
            else: messagebox.showerror("Denegado", "Usuario o clave incorrecta")
        ctk.CTkButton(f, text="ACCEDER AL PANEL", width=300, height=55, command=log_admin).pack(pady=35)
        ctk.CTkButton(f, text="VOLVER", fg_color="transparent", text_color="gray", command=self.mostrar_inicio).pack()

    def mostrar_panel_admin_ui(self):
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=75, corner_radius=0, fg_color=self.sena_dark); head.pack(fill="x")
        def cerrar_admin():
            if self.admin_actual:
                try:
                    self.db.registrar_auditoria(self.admin_actual, "logout admin")
                except Exception as ex:
                    logging.error("Error registrando auditoría (logout admin)", exc_info=True)
            self.admin_actual = None
            self.mostrar_inicio()
        ctk.CTkButton(head, text="🔒 CERRAR", fg_color="#444", command=cerrar_admin).pack(side="right", padx=25)
        # botón para dashboard rápido
        btn_dash = ctk.CTkButton(head, text="📈 DASHBOARD", fg_color="#39A900", hover_color="#2D5A27", command=self.mostrar_dashboard)
        btn_dash.pack(side="left", padx=25)
        ToolTip(btn_dash, "Ver indicadores clave (KPIs)")
        tabview = ctk.CTkTabview(self.main_container, segmented_button_selected_color=self.sena_green, fg_color=self.bg_light)
        tabview.pack(fill="both", expand=True, padx=25, pady=15)
        t_hist = tabview.add("🕒 HISTORIAL"); t_gest = tabview.add("👥 GESTIÓN"); t_reg = tabview.add("📝 REGISTRO"); t_pap = tabview.add("🗑️ PAPELERA"); t_rep = tabview.add("📊 REPORTES")
        for t in (t_hist, t_gest, t_reg, t_pap, t_rep):
            t.configure(fg_color=self.sena_dark, border_width=1, border_color="#DDD", corner_radius=20)

        def refresh_hist():
            for i in tv_hist.get_children(): tv_hist.delete(i)
            self.db.cursor.execute("SELECT a.id_asistencia, a.documento_estudiante, e.nombre_completo, a.fecha_registro, a.fecha_salida FROM asistencias a JOIN estudiantes e ON a.documento_estudiante = e.documento ORDER BY a.fecha_registro DESC LIMIT 100")
            for r in self.db.cursor.fetchall():
                sal = r['fecha_salida'].strftime('%H:%M') if r['fecha_salida'] else "PENDIENTE"
                tv_hist.insert("", "end", values=(r['documento_estudiante'], r['nombre_completo'], r['fecha_registro'].strftime('%d/%m %H:%M'), sal))
        tv_f1 = tk.Frame(t_hist, bg="#f7f7f7", borderwidth=1, relief="solid"); tv_f1.pack(fill="both", expand=True, padx=12, pady=12)
        tv_hist = ttk.Treeview(tv_f1, columns=("DOC", "NOMBRE", "IN", "OUT"), show="headings"); [tv_hist.heading(c, text=c) for c in ("DOC", "NOMBRE", "IN", "OUT")]; tv_hist.pack(fill="both", expand=True); refresh_hist()

        f_bus = ctk.CTkFrame(t_gest, fg_color="transparent"); f_bus.pack(fill="x", padx=20, pady=15)
        ent_bus = ctk.CTkEntry(f_bus, placeholder_text="Buscar aprendiz...", width=420); ent_bus.pack(side="left", padx=10)
        tv_f2 = tk.Frame(t_gest, bg=self.bg_light); tv_f2.pack(fill="both", expand=True, padx=20)
        tv_gest = ttk.Treeview(tv_f2, columns=("DOC", "NOMBRE", "FICHA"), show="headings", selectmode='extended'); [tv_gest.heading(c, text=c) for c in ("DOC", "NOMBRE", "FICHA")]; tv_gest.pack(fill="both", expand=True)
        def filtrar():
            for i in tv_gest.get_children(): tv_gest.delete(i)
            v = f"%{ent_bus.get()}%"
            self.db.cursor.execute("SELECT documento, nombre_completo, id_ficha FROM estudiantes WHERE documento LIKE %s OR nombre_completo LIKE %s", (v, v))
            for r in self.db.cursor.fetchall(): tv_gest.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))
        ctk.CTkButton(f_bus, text="🔍 FILTRAR", width=120, command=filtrar).pack(side="left"); filtrar()
        def mover_seleccion():
            docs = [tv_gest.item(i)['values'][0] for i in tv_gest.selection()]
            if not docs: return
            if messagebox.askyesno("Confirmar", f"¿Desea mover {len(docs)} aprendices a la papelera?"):
                for doc in docs:
                    self.servicio.mandar_a_papelera(doc)
                    try:
                        self.db.registrar_auditoria(self.admin_actual, "mover a papelera", objeto=doc)
                    except Exception as ex:
                        logging.error(f"Error registrando auditoría mover a papelera para {doc}", exc_info=True)
                filtrar(); refresh_pap()
        ctk.CTkButton(t_gest, text="🗑️ MOVER A PAPELERA", fg_color="#E74C3C", command=mover_seleccion).pack(pady=10)

        f_reg_m = ctk.CTkFrame(t_reg, corner_radius=20, fg_color=self.bg_light, border_width=1, border_color="#EEE"); f_reg_m.pack(pady=20, padx=50, fill="x")
        grid_f = tk.Frame(f_reg_m, bg=self.bg_light); grid_f.pack(pady=20, padx=25)
        fields = ["Documento", "Nombre Completo", "Correo"]; entries = {}
        for i, l in enumerate(fields):
            ctk.CTkLabel(grid_f, text=l, text_color="gray").grid(row=0, column=i, padx=12)
            e = ctk.CTkEntry(grid_f, width=190); e.grid(row=1, column=i, padx=5, pady=5); entries[l] = e
        cb_f = ttk.Combobox(grid_f, state="readonly", width=40); cb_f.grid(row=1, column=3, padx=12); cb_f['values'] = [f"{f['id_ficha']} | {f['nombre_programa']}" for f in self.servicio.obtener_fichas()]
        def save():
            exito, mensaje = self.servicio.guardar_aprendiz_manual(
                {k: v.get() for k, v in entries.items()}, 
                cb_f.get().split(" | ")[0] if cb_f.get() else None
            )
            if exito:
                messagebox.showinfo("C.R.S", mensaje)
                [v.delete(0, 'end') for v in entries.values()] 
                filtrar() 
            else:
                
                messagebox.showwarning("Atención", mensaje)
        ctk.CTkButton(f_reg_m, text="💾 GUARDAR", command=save).pack(pady=15)
        ctk.CTkButton(t_reg, text="📂 CARGA EXCEL", fg_color="#333", command=self.servicio.importar_excel).pack()
        
        def limpiar():
            for e in entries.values(): e.delete(0, 'end')
            cb_f.set('')
        ctk.CTkButton(f_reg_m, text="🧹 LIMPIAR", fg_color="#555", command=limpiar).pack(pady=5)
        tv_f3 = tk.Frame(t_pap, bg=self.bg_light); tv_f3.pack(fill="both", expand=True, padx=20, pady=12)
        tv_pap = ttk.Treeview(tv_f3, columns=("DOC", "NOMBRE", "FICHA"), show="headings", selectmode='extended'); [tv_pap.heading(c, text=c) for c in ("DOC", "NOMBRE", "FICHA")]; tv_pap.pack(fill="both", expand=True)
        
        
        def refresh_pap():
            for i in tv_pap.get_children(): tv_pap.delete(i)
            self.db.cursor.execute("SELECT documento, nombre_completo, id_ficha FROM estudiantes_eliminados")
            for r in self.db.cursor.fetchall(): tv_pap.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))
        btn_p = ctk.CTkFrame(t_pap, fg_color="transparent"); btn_p.pack(pady=10)
        def restaurar():
            docs = [tv_pap.item(i)['values'][0] for i in tv_pap.selection()]
            for d in docs: 
                self.servicio.restaurar_aprendiz(d)
                try:
                    self.db.registrar_auditoria(self.admin_actual, "restaurar aprendiz", objeto=d)
                except Exception as ex:
                    logging.error(f"Error registrando auditoría restaurar aprendiz para {d}", exc_info=True)
            refresh_pap(); filtrar()
        def eliminar():
            docs = [tv_pap.item(i)['values'][0] for i in tv_pap.selection()]
            if messagebox.askyesno("Confirmar", "Esta acción es irreversible"):
                for d in docs: 
                    self.servicio.eliminar_permanente(d)
                    try:
                        self.db.registrar_auditoria(self.admin_actual, "eliminar permanente", objeto=d)
                    except Exception as ex:
                        logging.error(f"Error registrando auditoría eliminar permanente para {d}", exc_info=True)
                refresh_pap()
        ctk.CTkButton(btn_p, text="♻️ RESTAURAR", fg_color=self.sena_green, command=restaurar).pack(side="left", padx=10)
        ctk.CTkButton(btn_p, text="🔥 ELIMINAR", fg_color="black", command=eliminar).pack(side="left", padx=10); refresh_pap()
        
        
        # Inicializar la pestaña de reportes (se implementa en crear_pestana_reportes)
        self.crear_pestana_reportes(t_rep)

        
    def crear_pestana_reportes(self, t_rep):
        # Contenedor principal de la pestaña
        f_rep_m = ctk.CTkFrame(t_rep, corner_radius=20, fg_color="white", border_width=1, border_color="#EEE")
        f_rep_m.pack(pady=20, padx=50, fill="x")
        
        grid_rep = tk.Frame(f_rep_m, bg="white")
        grid_rep.pack(pady=20, padx=25)

        # Variables de control para el nuevo sistema de selección
        self.modo_filtro = tk.StringVar(value="Ficha")
        self.items_seleccionados = [] 

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

        # Contenedor para el selector (calendario / semanas / meses)
        self.selector_frame = tk.Frame(f_rep_m, bg="white")
        self.selector_frame.pack(fill="x", padx=50)

        # --- BOTÓN GENERAR y EXPORTAR ---
        btn_frame = tk.Frame(t_rep, bg=self.sena_dark)
        btn_frame.pack(pady=10)
        btn_gen = ctk.CTkButton(btn_frame, text="📊 GENERAR ESTADÍSTICAS", font=("Arial", 14, "bold"),
                      command=self.lanzar_reporte)
        btn_gen.pack(side="left", padx=5)
        ToolTip(btn_gen, "Generar gráfico según filtros")
        btn_exp = ctk.CTkButton(btn_frame, text="📥 EXPORTAR", font=("Arial", 14, "bold"),
                      fg_color="#3A7FF6", hover_color="#346DD1", command=self.exportar_reporte)
        btn_exp.pack(side="left", padx=5)
        ToolTip(btn_exp, "Guardar reporte en PDF o Excel")

        # --- EL CANVAS (Fuera del frame de filtros para que no se oculte) ---
        self.canvas_rep = tk.Canvas(t_rep, bg="white", height=300, highlightthickness=1, highlightbackground="#DDD")
        self.canvas_rep.pack(fill="both", expand=True, padx=50, pady=10)
        
        self.canvas_rep.create_text(300, 150, text="Seleccione filtros y presione Generar", fill="gray")

        # Cargar datos iniciales
        self.cambiar_modo_reporte()
        # Mostrar el selector por defecto (Día)
        self.mostrar_selector_rango()
        # preparar almacenamiento de último reporte
        self.last_report_items = []
        self.last_report_params = None

    def exportar_reporte(self):
        """Genera un archivo PDF o Excel con los datos del último reporte."""
        if not getattr(self, 'last_report_items', None):
            messagebox.showwarning("Exportar", "No hay datos para exportar. Genera primero un reporte.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                            filetypes=[("PDF", "*.pdf"), ("Excel", "*.xlsx")])
        if not path:
            return
        items = self.last_report_items
        # si extensión es xlsx, usar pandas
        if path.lower().endswith('.xlsx'):
            try:
                import pandas as pd
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
            except Exception as e:
                messagebox.showerror("Exportar", f"Error al exportar: {e}")
            return
        # generar PDF
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
            # incorporar filtros
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

    def mostrar_dashboard(self):
        """Ventana con KPIs en 3 columnas: Hoy, Semana, Mes.
        
        Detecta automáticamente:
        - Hoy: solo la fecha seleccionada
        - Semana: lunes a viernes (detecta la semana laboral que contiene la fecha)
        - Mes: primer a último día del mes
        """
        v = tk.Toplevel(self.root)
        v.title("Dashboard CRS")
        v.geometry("1000x550")
        v.config(bg=self.bg_light)

        # contenedor principal
        main_frame = tk.Frame(v, bg=self.bg_light)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # selector de fecha
        lbl_sel = tk.Label(main_frame, text="Fecha de referencia:", font=("Segoe UI", 11), bg=self.bg_light)
        lbl_sel.pack(pady=(0, 5))
        cal = Calendar(main_frame, selectmode='day', locale='es_ES',
                       background=self.sena_green, headersbackground=self.sena_dark)
        cal.pack()

        def actualizar_dashboard(e=None):
            # borrar KPIs previos (mantener selector)
            for w in main_frame.winfo_children():
                if w not in (lbl_sel, cal):
                    w.destroy()
            try:
                hoy = cal.selection_get()
                
                # Calcular rangos
                # HOY: solo esa fecha
                fecha_hoy = hoy
                
                # SEMANA: lunes a viernes de esa semana
                dias_desde_lunes = hoy.weekday()  # 0=lunes, 4=viernes, 5=sábado, 6=domingo
                lunes = hoy - datetime.timedelta(days=dias_desde_lunes)
                viernes = lunes + datetime.timedelta(days=4)
                
                # MES: primer día a último día
                mes_ini = hoy.replace(day=1)
                import calendar as _cal
                ultimo_dia = _cal.monthrange(hoy.year, hoy.month)[1]
                mes_fin = hoy.replace(day=ultimo_dia)
                
                # Obtener datos
                datos_dia = self.servicio.obtener_metricas_reporte_multiple([], "Ficha", "Día", fecha_hoy)
                datos_sem = self.servicio.obtener_metricas_reporte_multiple([], "Ficha", "Semana", lunes)
                datos_mes = self.servicio.obtener_metricas_reporte_multiple([], "Ficha", "Mes", mes_ini)

                # Contenedor de columnas
                cols_frame = tk.Frame(main_frame, bg=self.bg_light)
                cols_frame.pack(fill="both", expand=True, padx=10, pady=10)

                # Helper para crear una columna
                def crear_columna(parent, titulo, fecha_inicio, fecha_fin, datos, emoji):
                    col = tk.Frame(parent, bg="white", relief="solid", borderwidth=2)
                    col.pack(side="left", fill="both", expand=True, padx=5)
                    
                    # Encabezado
                    header = tk.Frame(col, bg=self.sena_green)
                    header.pack(fill="x")
                    
                    lbl_titulo = tk.Label(header, text=f"{emoji} {titulo}", 
                                         font=("Segoe UI", 13, "bold"), 
                                         bg=self.sena_green, fg="white")
                    lbl_titulo.pack(pady=8)
                    
                    # Rango de fechas
                    if fecha_inicio == fecha_fin:
                        rango_txt = fecha_inicio.strftime("%d/%m/%Y")
                    else:
                        rango_txt = f"{fecha_inicio.strftime('%d/%m')} - {fecha_fin.strftime('%d/%m/%Y')}"
                    
                    lbl_rango = tk.Label(col, text=rango_txt, 
                                        font=("Segoe UI", 10), 
                                        bg="white", fg="#666")
                    lbl_rango.pack(pady=5)
                    
                    # Separador
                    sep = tk.Frame(col, bg="#E0E0E0", height=1)
                    sep.pack(fill="x", padx=10)
                    
                    # Datos
                    content = tk.Frame(col, bg="white")
                    content.pack(fill="both", expand=True, padx=12, pady=12)
                    
                    def dato_linea(label, valor, color="black"):
                        f = tk.Frame(content, bg="white")
                        f.pack(fill="x", pady=6)
                        
                        lbl_l = tk.Label(f, text=label, font=("Segoe UI", 10), 
                                        bg="white", fg="#555")
                        lbl_l.pack(side="left")
                        
                        lbl_v = tk.Label(f, text=str(valor), font=("Segoe UI", 11, "bold"), 
                                        bg="white", fg=color)
                        lbl_v.pack(side="right")
                    
                    asist = datos.get('total_asistencias', 0)
                    faltas = datos.get('faltas', 0)
                    retardos = datos.get('retardos', 0)
                    
                    # Color según asistencia (rojo si poca, verde si buena)
                    color_asist = "#39A900" if asist >= 10 else "#E74C3C"
                    
                    dato_linea("Asistencias:", asist, color_asist)
                    dato_linea("Faltas:", faltas, "#FF9800" if faltas > 2 else "#555")
                    dato_linea("Retardos:", retardos, "#E67E22" if retardos > 0 else "#555")
                
                # Crear 3 columnas
                crear_columna(cols_frame, "HOY", fecha_hoy, fecha_hoy, datos_dia, "📅")
                crear_columna(cols_frame, "SEMANA", lunes, viernes, datos_sem, "📊")
                crear_columna(cols_frame, "MES", mes_ini, mes_fin, datos_mes, "📈")
                
                # Botón cerrar
                btn_frame = tk.Frame(main_frame, bg=self.bg_light)
                btn_frame.pack(pady=10)
                ctk.CTkButton(btn_frame, text="Cerrar", command=v.destroy).pack()
                
            except Exception as ex:
                tk.Label(main_frame, text=f"Error: {ex}",
                         fg="red", bg=self.bg_light, font=("Segoe UI", 10)).pack(pady=20)

        cal.bind("<<CalendarSelected>>", actualizar_dashboard)
        # inicializar con fecha de hoy
        cal.selection_set(datetime.date.today())
        actualizar_dashboard()


        
    def cambiar_modo_reporte(self):
        self.limpiar_lista_reporte()
        if self.modo_filtro.get() == "Ficha":
            fichas = self.servicio.obtener_fichas()
            data = [f"{f['id_ficha']} | {f['codigo_ficha']} - {f['nombre_programa']}" for f in fichas]
        else:
            self.db.cursor.execute("SELECT documento, nombre_completo FROM estudiantes")
            data = [f"{e['documento']} | {e['nombre_completo']}" for e in self.db.cursor.fetchall()]
        # guardar valores originales para poder filtrar
        self.combo_vals = data
        self.combo_seleccion['values'] = data
        self.combo_seleccion.set("Seleccione...")
        # permitir escritura para filtrar y atar evento
        self.combo_seleccion.configure(state='normal')
        self.combo_seleccion.bind('<KeyRelease>', self._filtrar_combo)


    def _filtrar_combo(self, event=None):
        text = self.combo_seleccion.get().lower()
        if not hasattr(self, 'combo_vals'):
            return
        filtered = [v for v in self.combo_vals if text in v.lower()]
        self.combo_seleccion['values'] = filtered

    def mostrar_selector_rango(self):
        # Limpia selector previo
        for w in self.selector_frame.winfo_children():
            w.destroy()

        rango = self.seg_tiempo.get()
        self.reporte_fecha_inicio = None

        if rango == "Día":
            # Mostrar calendario para elegir un día
            self.cal_rep = Calendar(self.selector_frame, selectmode='day', locale='es_ES', background=self.sena_green, headersbackground=self.sena_dark)
            self.cal_rep.pack(padx=10, pady=8)
            # Por defecto, fecha seleccionada hoy
            try:
                self.reporte_fecha_inicio = self.cal_rep.selection_get()
            except Exception:
                self.reporte_fecha_inicio = datetime.date.today()

            def on_day_sel(e=None):
                try: self.reporte_fecha_inicio = self.cal_rep.selection_get()
                except: self.reporte_fecha_inicio = datetime.date.today()

            self.cal_rep.bind("<<CalendarSelected>>", on_day_sel)
            self.day_specified = True

        elif rango == "Semana":
            # Generar lista de semanas (inicio lunes) - últimas 52 semanas
            hoy = datetime.date.today()
            semanas = []
            self.week_map = {}
            self.week_specified = False
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
                self.week_specified = True

            self.combo_week.bind('<<ComboboxSelected>>', on_week_sel)

        else: # Mes
            hoy = datetime.date.today()
            meses = []
            self.month_map = {}
            self.month_specified = False
            # últimos 36 meses
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
                self.month_specified = True

            self.combo_month.bind('<<ComboboxSelected>>', on_month_sel)

    def agregar_item_reporte(self):
        item = self.combo_seleccion.get()
        if item and item != "Seleccione..." and item not in self.items_seleccionados:
            self.items_seleccionados.append(item)
            ids_v = [i.split(" | ")[0] for i in self.items_seleccionados]
            self.lbl_lista_rep.configure(text=f"Seleccionados: {', '.join(ids_v)}")

    def limpiar_lista_reporte(self):
        self.items_seleccionados = []
        if hasattr(self, 'lbl_lista_rep'):
            self.lbl_lista_rep.configure(text="Seleccionados: Ninguno")

    def lanzar_reporte(self):
        self.canvas_rep.delete("all")
        ids_limpios = [item.split(" | ")[0] for item in self.items_seleccionados]
        modo = self.modo_filtro.get()
        rango_sel = self.seg_tiempo.get()

        # Determinar fecha de inicio según selector (si existe)
        fecha_inicio = None
        try:
            if rango_sel == "Día":
                fecha_inicio = getattr(self, 'reporte_fecha_inicio', datetime.date.today())
            elif rango_sel == "Semana":
                fecha_inicio = getattr(self, 'reporte_fecha_inicio', datetime.date.today())
            else: # Mes
                fecha_inicio = getattr(self, 'reporte_fecha_inicio', datetime.date.today())
        except Exception:
            fecha_inicio = datetime.date.today()

        # Dependiendo del rango, generamos uno o varios periodos a mostrar
        items = []  # cada item: {'label': str, 'metrics': dict}

        if rango_sel == "Día":
            datos = self.servicio.obtener_metricas_reporte_multiple(ids_limpios, modo, rango_sel, fecha_inicio)
            if datos['total_asistencias'] == 0 and datos['expected'] == 0:
                self.canvas_rep.create_text(300, 150, text="❌ No hay registros para esta selección", fill="red", font=("Arial", 14))
                return
            items.append({'label': fecha_inicio.strftime('%d/%m/%Y'), 'metrics': datos})

        elif rango_sel == "Semana":
            # Si el usuario especificó una semana, mostramos solo esa; si no, mostramos 4 semanas del mes
            if getattr(self, 'week_specified', False):
                datos = self.servicio.obtener_metricas_reporte_multiple(ids_limpios, modo, rango_sel, fecha_inicio)
                items.append({'label': f"Semana {fecha_inicio.isocalendar()[1]} ({fecha_inicio.strftime('%d/%m')})", 'metrics': datos})
            else:
                # primeras 4 semanas (lunes) del mes de fecha_inicio
                year = fecha_inicio.year
                month = fecha_inicio.month
                first = datetime.date(year, month, 1)
                # primer lunes <= first
                first_monday = first - datetime.timedelta(days=first.weekday())
                for i in range(4):
                    start = first_monday + datetime.timedelta(weeks=i)
                    fin = start + datetime.timedelta(days=6)
                    label = f"W{start.isocalendar()[1]} {start.strftime('%d/%m')}"
                    d = self.servicio.obtener_metricas_reporte_multiple(ids_limpios, modo, 'Semana', start)
                    items.append({'label': label, 'metrics': d})

        else:  # Mes
            if getattr(self, 'month_specified', False):
                datos = self.servicio.obtener_metricas_reporte_multiple(ids_limpios, modo, rango_sel, fecha_inicio)
                items.append({'label': fecha_inicio.strftime('%B %Y'), 'metrics': datos})
            else:
                year = fecha_inicio.year
                today = datetime.date.today()
                last_month = today.month if year == today.year else 12
                for m in range(1, last_month + 1):
                    start = datetime.date(year, m, 1)
                    d = self.servicio.obtener_metricas_reporte_multiple(ids_limpios, modo, 'Mes', start)
                    items.append({'label': start.strftime('%b') , 'metrics': d})

        # Si no hay datos en todos los items
        if not any(it['metrics']['total_asistencias'] or it['metrics'].get('expected', 0) for it in items):
            self.canvas_rep.create_text(300, 150, text="❌ No hay registros para esta selección", fill="red", font=("Arial", 14))
            return
        # almacenar items para permitir exportación
        self.last_report_items = items
        self.last_report_params = (ids_limpios, modo, rango_sel, fecha_inicio)

        # Dibujar en el canvas
        self.canvas_rep.update_idletasks()
        W = self.canvas_rep.winfo_width() or 800
        H = self.canvas_rep.winfo_height() or 300
        pad = 30
        n = len(items)
        col_w = max(100, (W - 2*pad) / max(1, n))
        base_y = int(H * 0.6)
        max_h = int(H * 0.35)

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

            # barra de referencia
            self.canvas_rep.create_rectangle(x_center - bar_w//2, base_y - max_h, x_center + bar_w//2, base_y, fill="#EEE", outline="")
            # barra actual
            self.canvas_rep.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

            # etiqueta y métricas
            self.canvas_rep.create_text(x_center, base_y + 18, text=it['label'], font=("Arial", 10, "bold"))
            self.canvas_rep.create_text(x_center, base_y + 36, text=f"A:{total}  F:{faltas}  R:{retardos}", font=("Arial", 9))

        # Encabezado de resumen
        self.canvas_rep.create_text(W//2, 30, text="Reporte de Asistencias", font=("Arial", 16, "bold"))
        
    def actualizar_password_ventana(self, documento):
        v = tk.Toplevel(self.root); v.title("Seguridad C.R.S"); v.geometry("450x520"); v.configure(bg=self.bg_light); v.grab_set()
        tk.Label(v, text="🔒 CAMBIO OBLIGATORIO", font=("bold", 12), bg=self.bg_light, fg="#d32f2f").pack(pady=10)
        pass_var = tk.StringVar(); e = ttk.Entry(v, show="*", textvariable=pass_var, font=("Segoe UI", 12)); e.pack(pady=10, padx=40, fill="x")
        req_frame = tk.Frame(v, bg=self.bg_light); req_frame.pack(pady=10, padx=40, fill="x")
        requisitos = {
            "long":  tk.Label(req_frame, text="• Mínimo 8 caracteres", bg=self.bg_light, fg="red", anchor="w"),
            "upper": tk.Label(req_frame, text="• Al menos una mayúscula", bg=self.bg_light, fg="red", anchor="w"),
            "lower": tk.Label(req_frame, text="• Al menos una minúscula", bg=self.bg_light, fg="red", anchor="w"),
            "num":   tk.Label(req_frame, text="• Al menos un número", bg=self.bg_light, fg="red", anchor="w")
        }
        for lbl in requisitos.values(): lbl.pack(fill="x")
        def validar(*args):
            p = pass_var.get()
            cond = {"long": len(p)>=8, "upper": any(c.isupper() for c in p), "lower": any(c.islower() for c in p), "num": any(c.isdigit() for c in p)}
            for k, c in cond.items(): requisitos[k].config(fg="#39A900" if c else "red")
            return all(cond.values())
        pass_var.trace_add("write", validar)
        def save():
            if validar():
                self.db.cursor.execute("UPDATE estudiantes SET password=%s, cambio_pass=1 WHERE documento=%s", (pass_var.get(), documento))
                self.db.conexion.commit(); messagebox.showinfo("C.R.S", "Seguridad configurada"); v.destroy()
        tk.Button(v, text="GUARDAR Y ENTRAR", bg="#39A900", fg="white", command=save).pack(pady=20)

if __name__ == "__main__":
    root = ctk.CTk() 
    app = SistemaHSGSCRS(root)
    root.mainloop()
    
