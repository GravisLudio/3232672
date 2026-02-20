import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
from tkcalendar import Calendar
import pandas as pd
from conexion import InventarioDB
from logica import AsistenciaService

# Configuración de apariencia global (Estilo similar a Tailwind)
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("green") 

class SistemaHSGS:
    def __init__(self, root):
        self.root = root
        self.root.title("SREE PRO - High Softwares From Gravis Systems")
        
        # Inicializar base de datos con cursor bufferizado
        self.db = InventarioDB()
        if self.db.conexion:
            self.db.cursor = self.db.conexion.cursor(dictionary=True, buffered=True)
        
        # Inicializar capa de lógica (Cerebro del programa)
        self.servicio = AsistenciaService(self.db)

        # Colores Corporativos
        self.sena_green = "#39A900"
        self.sena_dark = "#2D5A27"

        # Contenedor Maestro donde se intercambian las pantallas
        self.main_container = ctk.CTkFrame(self.root, fg_color="#F0F2F5", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        self.mostrar_inicio()
        
        # FIX: Forzar pantalla completa después de cargar componentes para evitar redimensionado
        self.root.after(100, lambda: self.root.state('zoomed'))

    def limpiar_pantalla(self):
        """Elimina todos los widgets del contenedor principal para cambiar de vista."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- VISTA 1: INICIO (GATEWAY) ---
    def mostrar_inicio(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=500, height=550, corner_radius=20, fg_color="white", border_width=1, border_color="#E0E0E0")
        f.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(f, text="GATEWAY HSGS", font=("Segoe UI", 32, "bold"), text_color=self.sena_dark).pack(pady=(50, 5))
        ctk.CTkLabel(f, text="High Softwares From Gravis Systems", font=("Segoe UI", 13), text_color="#888").pack(pady=(0, 40))
        
        ctk.CTkButton(f, text="💻 TERMINAL APRENDICES", font=("Segoe UI", 14, "bold"), height=55, width=350, 
                      corner_radius=10, command=self.mostrar_terminal).pack(pady=10)
        
        ctk.CTkButton(f, text="🔐 PANEL ADMINISTRATIVO", font=("Segoe UI", 14, "bold"), height=55, width=350, 
                      corner_radius=10, fg_color="#333", hover_color="#1a1a1a", command=self.mostrar_login).pack(pady=10)
        
        ctk.CTkButton(f, text="👤 MI PERFIL (APRENDIZ)", font=("Segoe UI", 14, "bold"), height=55, width=350, 
                      corner_radius=10, fg_color="transparent", text_color=self.sena_green, border_width=2, 
                      border_color=self.sena_green, hover_color="#E8F5E9", command=self.login_aprendiz_view).pack(pady=10)

    # --- VISTA 2: TERMINAL (REGISTRO RÁPIDO) ---
    def mostrar_terminal(self):
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=70, corner_radius=0, fg_color=self.sena_green)
        head.pack(fill="x")
        ctk.CTkButton(head, text="⬅ VOLVER AL INICIO", width=150, fg_color=self.sena_dark, command=self.mostrar_inicio).pack(side="left", padx=20, pady=15)
        
        f = ctk.CTkFrame(self.main_container, width=600, height=500, corner_radius=25, fg_color="white", border_width=1, border_color="#DDD")
        f.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(f, text="REGISTRO DE ASISTENCIA", font=("Segoe UI", 24, "bold")).pack(pady=30)
        ent_doc = ctk.CTkEntry(f, font=("Segoe UI", 28), width=450, height=70, placeholder_text="Documento", justify="center")
        ent_doc.pack(pady=20); ent_doc.focus()

        def procesar(tipo):
            doc = ent_doc.get()
            # Llamada a la lógica estricta para evitar duplicados
            exito, msg = self.servicio.registrar_entrada(doc) if tipo=="in" else self.servicio.registrar_salida(doc)
            if exito:
                messagebox.showinfo("HSGS", msg)
                ent_doc.delete(0, 'end')
            else:
                messagebox.showwarning("Atención", msg)

        ctk.CTkButton(f, text="📥 REGISTRAR ENTRADA", font=("bold", 15), height=60, width=400, command=lambda:procesar("in")).pack(pady=10)
        ctk.CTkButton(f, text="📤 REGISTRAR SALIDA", font=("bold", 15), height=60, width=400, fg_color="#E67E22", hover_color="#D35400", command=lambda:procesar("out")).pack(pady=10)

    # --- VISTA 3: LOGIN APRENDIZ ---
    def login_aprendiz_view(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=450, height=450, corner_radius=20, fg_color="white")
        f.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(f, text="ACCESO APRENDIZ", font=("Segoe UI", 22, "bold")).pack(pady=30)
        u_ent = ctk.CTkEntry(f, width=300, height=45, placeholder_text="Documento")
        u_ent.pack(pady=10)
        p_ent = ctk.CTkEntry(f, width=300, height=45, placeholder_text="Contraseña", show="*")
        p_ent.pack(pady=10)

        def entrar():
            user = self.servicio.login_aprendiz(u_ent.get(), p_ent.get())
            if user:
                # Forzar cambio de clave si es sena123 o primera vez
                if user.get('cambio_pass') == 0 or p_ent.get() == 'sena123':
                    self.actualizar_pass_modal(user['documento'])
                self.mostrar_panel_aprendiz(user)
            else:
                messagebox.showerror("Error", "Documento o clave incorrectos")

        ctk.CTkButton(f, text="INGRESAR AL PERFIL", width=300, height=50, command=entrar).pack(pady=30)
        ctk.CTkButton(f, text="VOLVER", fg_color="gray", width=300, command=self.mostrar_inicio).pack()

    # --- VISTA 4: PANEL APRENDIZ (CALENDARIO) ---
    def mostrar_panel_aprendiz(self, user):
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=70, corner_radius=0, fg_color="white", border_width=1, border_color="#EEE")
        head.pack(fill="x")
        ctk.CTkButton(head, text="🚪 CERRAR SESIÓN", fg_color="#FF5252", hover_color="#D32F2F", command=self.mostrar_inicio).pack(side="left", padx=20)
        ctk.CTkLabel(head, text=f"Aprendiz: {user['nombre_completo']}", font=("Segoe UI", 14, "bold")).pack(side="right", padx=30)

        body = ctk.CTkFrame(self.main_container, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=40, pady=20)

        # Lado Izquierdo: Calendario Físico
        left = ctk.CTkFrame(body, corner_radius=20, fg_color="white", border_width=1, border_color="#DDD")
        left.place(relx=0, rely=0, relwidth=0.65, relheight=1)
        cal = Calendar(left, selectmode='day', locale='es_ES', background=self.sena_green, headersbackground=self.sena_dark)
        cal.pack(fill="both", expand=True, padx=20, pady=20)

        # Lado Derecho: Reporte de Tarjetas
        right = ctk.CTkFrame(body, corner_radius=20, fg_color="white", border_width=1, border_color="#DDD")
        right.place(relx=0.67, rely=0, relwidth=0.33, relheight=1)
        lbl_info = ctk.CTkLabel(right, text="Actividad del día", font=("Segoe UI", 16, "bold"))
        lbl_info.pack(pady=15)

        container_cards = ctk.CTkScrollableFrame(right, fg_color="transparent")
        container_cards.pack(fill="both", expand=True, padx=10, pady=5)

        def actualizar(e=None):
            for w in container_cards.winfo_children(): w.destroy()
            fecha = cal.selection_get()
            regs = self.servicio.obtener_registros_dia(user['documento'], fecha)
            if not regs:
                ctk.CTkLabel(container_cards, text="Sin actividad este día", text_color="#AAA").pack(pady=50)
            else:
                for r in regs:
                    card = ctk.CTkFrame(container_cards, fg_color="#F8F9FA", corner_radius=10, border_width=1, border_color="#EEE")
                    card.pack(fill="x", pady=4, padx=5)
                    ctk.CTkLabel(card, text=f"📥 Ent: {r['fecha_registro'].strftime('%H:%M')}", font=("Segoe UI", 11)).pack(side="left", padx=10, pady=8)
                    if r['fecha_salida']:
                        ctk.CTkLabel(card, text=f"📤 Sal: {r['fecha_salida'].strftime('%H:%M')}", font=("Segoe UI", 11), text_color="#E67E22").pack(side="right", padx=10)

        cal.bind("<<CalendarSelected>>", actualizar); actualizar()

    # --- VISTA 5: LOGIN ADMIN ---
    def mostrar_login(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=400, height=450, corner_radius=20, fg_color="white")
        f.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f, text="ADMINISTRACIÓN", font=("Segoe UI", 22, "bold")).pack(pady=30)
        u = ctk.CTkEntry(f, placeholder_text="Usuario", width=280, height=45)
        u.pack(pady=10)
        p = ctk.CTkEntry(f, placeholder_text="Contraseña", show="*", width=280, height=45)
        p.pack(pady=10)
        
        def log_admin():
            self.db.cursor.execute("SELECT * FROM usuarios_admin WHERE usuario=%s AND password=%s", (u.get(), p.get()))
            if self.db.cursor.fetchone(): self.mostrar_panel_admin_ui()
            else: messagebox.showerror("Error", "Acceso Denegado")
            
        ctk.CTkButton(f, text="ACCEDER AL PANEL", width=280, height=50, command=log_admin).pack(pady=30)
        ctk.CTkButton(f, text="VOLVER", fg_color="transparent", text_color="gray", command=self.mostrar_inicio).pack()

    # --- VISTA 6: PANEL ADMIN INTEGRAL ---
    def mostrar_panel_admin_ui(self):
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=70, corner_radius=0, fg_color=self.sena_dark)
        head.pack(fill="x")
        ctk.CTkLabel(head, text="SREE PRO - GESTIÓN INTEGRAL HSGS", font=("Segoe UI", 18, "bold"), text_color="white").pack(side="left", padx=30)
        ctk.CTkButton(head, text="🔒 CERRAR SESIÓN", fg_color="#444", hover_color="#222", command=self.mostrar_inicio).pack(side="right", padx=20)

        tabview = ctk.CTkTabview(self.main_container, segmented_button_selected_color=self.sena_green)
        tabview.pack(fill="both", expand=True, padx=20, pady=10)

        t_asis = tabview.add("🕒 HISTORIAL"); t_gest = tabview.add("👥 GESTIÓN")
        t_reg  = tabview.add("📝 REGISTRO"); t_pap  = tabview.add("🗑️ PAPELERA")

        # --- HISTORIAL ---
        def refresh_asis():
            for i in tv_asis.get_children(): tv_asis.delete(i)
            query = """SELECT a.id_asistencia, a.documento_estudiante, e.nombre_completo, a.fecha_registro, a.fecha_salida 
                       FROM asistencias a JOIN estudiantes e ON a.documento_estudiante = e.documento 
                       ORDER BY a.fecha_registro DESC LIMIT 100"""
            self.db.cursor.execute(query)
            for r in self.db.cursor.fetchall():
                salida = r['fecha_salida'].strftime('%H:%M:%S') if r['fecha_salida'] else "PENDIENTE"
                tv_asis.insert("", "end", values=(r['id_asistencia'], r['documento_estudiante'], r['nombre_completo'], r['fecha_registro'].strftime('%Y-%m-%d %H:%M'), salida))

        tv_frame = tk.Frame(t_asis, bg="white")
        tv_frame.pack(fill="both", expand=True, padx=10, pady=10)
        cols = ("ID", "DOCUMENTO", "NOMBRE", "ENTRADA", "SALIDA")
        tv_asis = ttk.Treeview(tv_frame, columns=cols, show="headings")
        for c in cols: tv_asis.heading(c, text=c); tv_asis.column(c, anchor="center")
        tv_asis.pack(fill="both", expand=True)
        ctk.CTkButton(t_asis, text="🔄 REFRESCAR HISTORIAL", command=refresh_asis).pack(pady=5)
        refresh_asis()

        # --- GESTIÓN ---
        f_bus = ctk.CTkFrame(t_gest, fg_color="transparent")
        f_bus.pack(fill="x", padx=20, pady=15)
        ent_bus = ctk.CTkEntry(f_bus, placeholder_text="Buscar por nombre o documento...", width=400)
        ent_bus.pack(side="left", padx=10)

        tv_g_frame = tk.Frame(t_gest, bg="white")
        tv_g_frame.pack(fill="both", expand=True, padx=20)
        tv_gest = ttk.Treeview(tv_g_frame, columns=("DOC", "NOMBRE", "FICHA"), show="headings")
        for c in ("DOC", "NOMBRE", "FICHA"): tv_gest.heading(c, text=c); tv_gest.column(c, anchor="center")
        tv_gest.pack(fill="both", expand=True)

        def filtrar():
            for i in tv_gest.get_children(): tv_gest.delete(i)
            val = f"%{ent_bus.get()}%"
            self.db.cursor.execute("SELECT documento, nombre_completo, id_ficha FROM estudiantes WHERE documento LIKE %s OR nombre_completo LIKE %s", (val, val))
            for r in self.db.cursor.fetchall(): tv_gest.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))

        ctk.CTkButton(f_bus, text="🔍 FILTRAR", width=120, command=filtrar).pack(side="left")
        ctk.CTkButton(t_gest, text="🗑️ DESACTIVAR (PAPELERA)", fg_color="#E74C3C", command=lambda: [self.servicio.mandar_a_papelera(tv_gest.item(tv_gest.selection())['values'][0]), filtrar()] if tv_gest.selection() else None).pack(pady=10)
        filtrar()

        # --- REGISTRO ---
        f_reg_m = ctk.CTkFrame(t_reg, corner_radius=15, fg_color="white", border_width=1, border_color="#EEE")
        f_reg_m.pack(pady=20, padx=40, fill="x")
        grid_f = tk.Frame(f_reg_m, bg="white")
        grid_f.pack(pady=10, padx=20)
        fields = ["Documento", "Nombre Completo", "Correo"]
        entries = {}
        for i, label in enumerate(fields):
            ctk.CTkLabel(grid_f, text=label, text_color="gray").grid(row=0, column=i, padx=10)
            e = ctk.CTkEntry(grid_f, width=180); e.grid(row=1, column=i, padx=5, pady=5); entries[label] = e

        ctk.CTkLabel(grid_f, text="Ficha / Programa", text_color="gray").grid(row=0, column=3, padx=10)
        cb_fichas = ttk.Combobox(grid_f, state="readonly", width=40)
        cb_fichas.grid(row=1, column=3, padx=5)
        cb_fichas['values'] = [f"{f['id_ficha']} | {f['codigo_ficha']} - {f['nombre_programa']}" for f in self.servicio.obtener_fichas()]

        def guardar_m():
            id_f = cb_fichas.get().split(" | ")[0] if cb_fichas.get() else None
            res, msg = self.servicio.guardar_aprendiz_manual({k: v.get() for k, v in entries.items()}, id_f)
            messagebox.showinfo("Registro", msg)
            if res: [v.delete(0, 'end') for v in entries.values()]; cb_fichas.set('')
        
        ctk.CTkButton(f_reg_m, text="💾 GUARDAR APRENDIZ", command=guardar_m).pack(pady=15)
        ctk.CTkButton(t_reg, text="📂 CARGA MASIVA (EXCEL)", fg_color="#333", command=lambda: self.servicio.importar_excel()).pack(pady=10)

        # --- PAPELERA ---
        tv_p_frame = tk.Frame(t_pap, bg="white")
        tv_p_frame.pack(fill="both", expand=True, padx=20, pady=10)
        tv_pap = ttk.Treeview(tv_p_frame, columns=("DOC", "NOMBRE", "FICHA"), show="headings")
        for c in ("DOC", "NOMBRE", "FICHA"): tv_pap.heading(c, text=c); tv_pap.column(c, anchor="center")
        tv_pap.pack(fill="both", expand=True)

        def refresh_pap():
            for i in tv_pap.get_children(): tv_pap.delete(i)
            self.db.cursor.execute("SELECT documento, nombre_completo, id_ficha FROM estudiantes_eliminados")
            for r in self.db.cursor.fetchall(): tv_pap.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))

        btn_p_f = ctk.CTkFrame(t_pap, fg_color="transparent")
        btn_p_f.pack(pady=10)
        ctk.CTkButton(btn_p_f, text="♻️ RESTAURAR", fg_color=self.sena_green, command=lambda: [self.servicio.restaurar_aprendiz(tv_pap.item(tv_pap.selection())['values'][0]), refresh_pap()] if tv_pap.selection() else None).pack(side="left", padx=10)
        ctk.CTkButton(btn_p_f, text="🔥 BORRADO DEFINITIVO", fg_color="black", command=lambda: [self.servicio.eliminar_permanente(tv_pap.item(tv_pap.selection())['values'][0]), refresh_pap()] if tv_pap.selection() and messagebox.askyesno("HSGS", "Borrar de por vida?") else None).pack(side="left", padx=10)
        refresh_pap()

    # --- MODALES ---
    def actualizar_pass_modal(self, doc):
        v = ctk.CTkToplevel(self.root); v.title("Seguridad"); v.geometry("400x300")
        v.after(100, lambda: v.focus()); v.grab_set()
        ctk.CTkLabel(v, text="Cambio de Contraseña Obligatorio", font=("Segoe UI", 14, "bold")).pack(pady=20)
        e = ctk.CTkEntry(v, placeholder_text="Nueva contraseña", show="*", width=250); e.pack(pady=10)
        def guardar():
            res, msg = self.servicio.actualizar_password(doc, e.get())
            if res: messagebox.showinfo("OK", msg); v.destroy()
            else: messagebox.showwarning("Error", msg)
        ctk.CTkButton(v, text="ACTUALIZAR", command=guardar).pack(pady=20)

if __name__ == "__main__":
    root = ctk.CTk()
    app = SistemaHSGS(root)
    root.mainloop()