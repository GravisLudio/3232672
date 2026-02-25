import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
from tkcalendar import Calendar
import pandas as pd
from conexion import InventarioDB
from logica import AsistenciaService

# Configuración Visual
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("green") 

class SistemaHSGS:
    def __init__(self, root):
        self.root = root
        self.root.title("C.R.G - Chronos Registry System")
        
        # Conexión Base de Datos
        self.db = InventarioDB()
        if self.db.conexion:
            self.db.cursor = self.db.conexion.cursor(dictionary=True, buffered=True)
        
        # Capa de Lógica
        self.servicio = AsistenciaService(self.db)

        # Colores Corporativos (SENA Style)
        self.sena_green = "#39A900"
        self.sena_dark = "#2D5A27"

        # Contenedor Principal
        self.main_container = ctk.CTkFrame(self.root, fg_color="#F0F2F5", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        # Iniciar con Animación C.R.G
        self.animacion_entrada()
        
        # Ajuste de ventana maximizada
        self.root.after(100, lambda: self.root.state('zoomed'))

    def limpiar_pantalla(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- ANIMACIÓN DE INICIO ---
    def animacion_entrada(self):
        self.limpiar_pantalla()
        self.f_intro = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.f_intro.place(relx=0.5, rely=0.5, anchor="center")
        
        self.lbl_siglas = ctk.CTkLabel(self.f_intro, text="C.R.G", font=("Segoe UI", 10, "bold"), text_color=self.sena_dark)
        self.lbl_siglas.pack()
        
        self.lbl_nombre = ctk.CTkLabel(self.f_intro, text="CHRONOS REGISTRY SYSTEM", font=("Segoe UI", 20, "italic"), text_color="#555")
        
        self.size_actual = 10
        self.crecer_siglas()

    def crecer_siglas(self):
        if self.size_actual < 110:
            self.size_actual += 3
            self.lbl_siglas.configure(font=("Segoe UI", self.size_actual, "bold"))
            self.root.after(15, self.crecer_siglas)
        else:
            self.lbl_nombre.pack(pady=25)
            self.root.after(2000, self.mostrar_inicio)

    # --- GATEWAY PRINCIPAL ---
    def mostrar_inicio(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=500, height=580, corner_radius=20, fg_color="white", border_width=1, border_color="#E0E0E0")
        f.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(f, text="GATEWAY C.R.G", font=("Segoe UI", 32, "bold"), text_color=self.sena_dark).pack(pady=(50, 5))
        ctk.CTkLabel(f, text="Chronos Registry System | High Softwares", font=("Segoe UI", 13), text_color="#888").pack(pady=(0, 40))
        
        ctk.CTkButton(f, text="💻 TERMINAL APRENDICES", font=("Segoe UI", 14, "bold"), height=60, width=380, 
                      corner_radius=12, command=self.mostrar_terminal).pack(pady=12)
        
        ctk.CTkButton(f, text="🔐 PANEL ADMINISTRATIVO", font=("Segoe UI", 14, "bold"), height=60, width=380, 
                      corner_radius=12, fg_color="#333", hover_color="#1a1a1a", command=self.mostrar_login).pack(pady=12)
        
        ctk.CTkButton(f, text="👤 MI PERFIL (APRENDIZ)", font=("Segoe UI", 14, "bold"), height=60, width=380, 
                      corner_radius=12, fg_color="transparent", text_color=self.sena_green, border_width=2, 
                      border_color=self.sena_green, hover_color="#E8F5E9", command=self.login_aprendiz_view).pack(pady=12)

    # --- TERMINAL DE ASISTENCIA ---
    def mostrar_terminal(self):
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=70, corner_radius=0, fg_color=self.sena_green)
        head.pack(fill="x")
        ctk.CTkButton(head, text="⬅ VOLVER", width=140, fg_color=self.sena_dark, command=self.mostrar_inicio).pack(side="left", padx=25, pady=15)
        
        f = ctk.CTkFrame(self.main_container, width=650, height=550, corner_radius=25, fg_color="white", border_width=1, border_color="#DDD")
        f.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(f, text="REGISTRO DE ASISTENCIA", font=("Segoe UI", 26, "bold")).pack(pady=35)
        ent_doc = ctk.CTkEntry(f, font=("Segoe UI", 30), width=480, height=80, placeholder_text="Documento de Identidad", justify="center")
        ent_doc.pack(pady=25); ent_doc.focus()

        def procesar(tipo):
            exito, msg = self.servicio.registrar_entrada(ent_doc.get()) if tipo=="in" else self.servicio.registrar_salida(ent_doc.get())
            if exito:
                messagebox.showinfo("C.R.G", msg)
                ent_doc.delete(0, 'end')
            else:
                messagebox.showwarning("Atención", msg)

        ctk.CTkButton(f, text="📥 MARCAR ENTRADA", font=("bold", 16), height=65, width=450, command=lambda:procesar("in")).pack(pady=10)
        ctk.CTkButton(f, text="📤 MARCAR SALIDA", font=("bold", 16), height=65, width=450, fg_color="#E67E22", hover_color="#D35400", command=lambda:procesar("out")).pack(pady=10)

    # --- VISTAS DE APRENDIZ ---
    def login_aprendiz_view(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=450, height=480, corner_radius=25, fg_color="white")
        f.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f, text="ACCESO APRENDIZ", font=("Segoe UI", 24, "bold")).pack(pady=35)
        u_ent = ctk.CTkEntry(f, width=320, height=50, placeholder_text="N° Documento"); u_ent.pack(pady=12)
        p_ent = ctk.CTkEntry(f, width=320, height=50, placeholder_text="Contraseña", show="*"); p_ent.pack(pady=12)

        def entrar():
            user = self.servicio.login_aprendiz(u_ent.get(), p_ent.get())
            if user:
                if user.get('password') == 'sena123': self.actualizar_pass_modal(user['documento'])
                self.mostrar_panel_aprendiz(user)
            else: messagebox.showerror("Error", "Credenciales Incorrectas")

        ctk.CTkButton(f, text="INGRESAR", width=320, height=55, command=entrar).pack(pady=35)
        ctk.CTkButton(f, text="CANCELAR", fg_color="transparent", text_color="gray", command=self.mostrar_inicio).pack()

    def mostrar_panel_aprendiz(self, user):
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=75, corner_radius=0, fg_color="white", border_width=1, border_color="#EEE")
        head.pack(fill="x")
        ctk.CTkButton(head, text="🚪 SALIR", fg_color="#FF5252", hover_color="#D32F2F", command=self.mostrar_inicio).pack(side="left", padx=25)
        ctk.CTkLabel(head, text=f"Aprendiz: {user['nombre_completo']}", font=("Segoe UI", 15, "bold")).pack(side="right", padx=35)

        body = ctk.CTkFrame(self.main_container, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=45, pady=25)

        left = ctk.CTkFrame(body, corner_radius=20, fg_color="white", border_width=1, border_color="#DDD")
        left.place(relx=0, rely=0, relwidth=0.64, relheight=1)
        cal = Calendar(left, selectmode='day', locale='es_ES', background=self.sena_green, headersbackground=self.sena_dark)
        cal.pack(fill="both", expand=True, padx=25, pady=25)

        right = ctk.CTkFrame(body, corner_radius=20, fg_color="white", border_width=1, border_color="#DDD")
        right.place(relx=0.66, rely=0, relwidth=0.34, relheight=1)
        lbl_info = ctk.CTkLabel(right, text="Actividad Diaria", font=("Segoe UI", 18, "bold")); lbl_info.pack(pady=20)

        container_cards = ctk.CTkScrollableFrame(right, fg_color="transparent")
        container_cards.pack(fill="both", expand=True, padx=12, pady=8)

        def actualizar(e=None):
            for w in container_cards.winfo_children(): w.destroy()
            regs = self.servicio.obtener_registros_dia(user['documento'], cal.selection_get())
            if not regs: ctk.CTkLabel(container_cards, text="Sin registros", text_color="#AAA").pack(pady=60)
            else:
                for r in regs:
                    card = ctk.CTkFrame(container_cards, fg_color="#F9F9F9", corner_radius=12, border_width=1, border_color="#EEE")
                    card.pack(fill="x", pady=6, padx=8)
                    ctk.CTkLabel(card, text=f"📥 In: {r['fecha_registro'].strftime('%H:%M')}", font=("Segoe UI", 12)).pack(side="left", padx=15, pady=12)
                    if r['fecha_salida']:
                        ctk.CTkLabel(card, text=f"📤 Out: {r['fecha_salida'].strftime('%H:%M')}", font=("Segoe UI", 12), text_color="#E67E22").pack(side="right", padx=15)
        cal.bind("<<CalendarSelected>>", actualizar); actualizar()

    # --- PANEL ADMINISTRATIVO ---
    def mostrar_login(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=420, height=480, corner_radius=25, fg_color="white")
        f.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f, text="ADMINISTRACIÓN", font=("Segoe UI", 24, "bold")).pack(pady=35)
        u = ctk.CTkEntry(f, placeholder_text="Usuario Admin", width=300, height=50); u.pack(pady=12)
        p = ctk.CTkEntry(f, placeholder_text="Contraseña", show="*", width=300, height=50); p.pack(pady=12)
        
        def log_admin():
            self.db.cursor.execute("SELECT * FROM usuarios_admin WHERE usuario=%s AND password=%s", (u.get(), p.get()))
            if self.db.cursor.fetchone(): self.mostrar_panel_admin_ui()
            else: messagebox.showerror("Denegado", "Usuario o clave incorrecta")
            
        ctk.CTkButton(f, text="ACCEDER AL PANEL", width=300, height=55, command=log_admin).pack(pady=35)
        ctk.CTkButton(f, text="VOLVER", fg_color="transparent", text_color="gray", command=self.mostrar_inicio).pack()

    def mostrar_panel_admin_ui(self):
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=75, corner_radius=0, fg_color=self.sena_dark)
        head.pack(fill="x")
        ctk.CTkLabel(head, text="C.R.G - PANEL DE GESTIÓN ADMINISTRATIVA", font=("Segoe UI", 18, "bold"), text_color="white").pack(side="left", padx=30)
        ctk.CTkButton(head, text="🔒 CERRAR PANEL", fg_color="#444", hover_color="#222", command=self.mostrar_inicio).pack(side="right", padx=25)

        tabview = ctk.CTkTabview(self.main_container, segmented_button_selected_color=self.sena_green)
        tabview.pack(fill="both", expand=True, padx=25, pady=15)

        t_asis = tabview.add("🕒 HISTORIAL"); t_gest = tabview.add("👥 GESTIÓN")
        t_reg  = tabview.add("📝 REGISTRO"); t_pap  = tabview.add("🗑️ PAPELERA")

        # Pestaña Historial
        def refresh_asis():
            for i in tv_asis.get_children(): tv_asis.delete(i)
            self.db.cursor.execute("SELECT a.id_asistencia, a.documento_estudiante, e.nombre_completo, a.fecha_registro, a.fecha_salida FROM asistencias a JOIN estudiantes e ON a.documento_estudiante = e.documento ORDER BY a.fecha_registro DESC LIMIT 100")
            for r in self.db.cursor.fetchall():
                sal = r['fecha_salida'].strftime('%H:%M:%S') if r['fecha_salida'] else "PENDIENTE"
                tv_asis.insert("", "end", values=(r['id_asistencia'], r['documento_estudiante'], r['nombre_completo'], r['fecha_registro'].strftime('%d/%m %H:%M'), sal))

        tv_f1 = tk.Frame(t_asis, bg="white"); tv_f1.pack(fill="both", expand=True, padx=12, pady=12)
        tv_asis = ttk.Treeview(tv_f1, columns=("ID", "DOC", "NOMBRE", "IN", "OUT"), show="headings")
        for c in ("ID", "DOC", "NOMBRE", "IN", "OUT"): tv_asis.heading(c, text=c); tv_asis.column(c, anchor="center")
        tv_asis.pack(fill="both", expand=True); refresh_asis()

        # Pestaña Gestión
        f_bus = ctk.CTkFrame(t_gest, fg_color="transparent"); f_bus.pack(fill="x", padx=20, pady=15)
        ent_bus = ctk.CTkEntry(f_bus, placeholder_text="Buscar por nombre o documento...", width=420); ent_bus.pack(side="left", padx=10)
        tv_f2 = tk.Frame(t_gest, bg="white"); tv_f2.pack(fill="both", expand=True, padx=20)
        tv_gest = ttk.Treeview(tv_f2, columns=("DOC", "NOMBRE", "FICHA"), show="headings")
        for c in ("DOC", "NOMBRE", "FICHA"): tv_gest.heading(c, text=c); tv_gest.column(c, anchor="center")
        tv_gest.pack(fill="both", expand=True)

        def filtrar():
            for i in tv_gest.get_children(): tv_gest.delete(i)
            val = f"%{ent_bus.get()}%"
            self.db.cursor.execute("SELECT documento, nombre_completo, id_ficha FROM estudiantes WHERE documento LIKE %s OR nombre_completo LIKE %s", (val, val))
            for r in self.db.cursor.fetchall(): tv_gest.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))
        
        ctk.CTkButton(f_bus, text="🔍 FILTRAR", width=130, command=filtrar).pack(side="left")
        ctk.CTkButton(t_gest, text="🗑️ MOVER A PAPELERA", fg_color="#E74C3C", command=lambda: [self.servicio.mandar_a_papelera(tv_gest.item(tv_gest.selection())['values'][0]), filtrar()] if tv_gest.selection() else None).pack(pady=12)
        filtrar()

        # Pestaña Registro
        f_reg_m = ctk.CTkFrame(t_reg, corner_radius=20, fg_color="white", border_width=1, border_color="#EEE"); f_reg_m.pack(pady=20, padx=50, fill="x")
        grid_f = tk.Frame(f_reg_m, bg="white"); grid_f.pack(pady=20, padx=25)
        fields = ["Documento", "Nombre Completo", "Correo"]; entries = {}
        for i, l in enumerate(fields):
            ctk.CTkLabel(grid_f, text=l, text_color="gray").grid(row=0, column=i, padx=12)
            e = ctk.CTkEntry(grid_f, width=190); e.grid(row=1, column=i, padx=12, pady=8); entries[l] = e
        
        ctk.CTkLabel(grid_f, text="Ficha / Programa", text_color="gray").grid(row=0, column=3, padx=12)
        cb_f = ttk.Combobox(grid_f, state="readonly", width=42)
        cb_f.grid(row=1, column=3, padx=12); cb_f['values'] = [f"{f['id_ficha']} | {f['codigo_ficha']} - {f['nombre_programa']}" for f in self.servicio.obtener_fichas()]

        def save_m():
            res, msg = self.servicio.guardar_aprendiz_manual({k: v.get() for k, v in entries.items()}, cb_f.get().split(" | ")[0] if cb_f.get() else None)
            messagebox.showinfo("C.R.G", msg)
            if res: [v.delete(0, 'end') for v in entries.values()]; cb_f.set(''); filtrar()
        
        ctk.CTkButton(f_reg_m, text="💾 GUARDAR APRENDIZ", command=save_m).pack(pady=20)
        ctk.CTkButton(t_reg, text="📂 CARGA MASIVA (EXCEL)", fg_color="#333", command=self.servicio.importar_excel).pack(pady=15)

        # Pestaña Papelera
        tv_f3 = tk.Frame(t_pap, bg="white"); tv_f3.pack(fill="both", expand=True, padx=20, pady=12)
        tv_pap = ttk.Treeview(tv_f3, columns=("DOC", "NOMBRE", "FICHA"), show="headings")
        for c in ("DOC", "NOMBRE", "FICHA"): tv_pap.heading(c, text=c); tv_pap.column(c, anchor="center")
        tv_pap.pack(fill="both", expand=True)

        def refresh_pap():
            for i in tv_pap.get_children(): tv_pap.delete(i)
            self.db.cursor.execute("SELECT documento, nombre_completo, id_ficha FROM estudiantes_eliminados")
            for r in self.db.cursor.fetchall(): tv_pap.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))

        btn_p = ctk.CTkFrame(t_pap, fg_color="transparent"); btn_p.pack(pady=12)
        ctk.CTkButton(btn_p, text="♻️ RESTAURAR", fg_color=self.sena_green, command=lambda: [self.servicio.restaurar_aprendiz(tv_pap.item(tv_pap.selection())['values'][0]), refresh_pap(), filtrar()] if tv_pap.selection() else None).pack(side="left", padx=12)
        ctk.CTkButton(btn_p, text="🔥 ELIMINAR PERMANENTE", fg_color="black", command=lambda: [self.servicio.eliminar_permanente(tv_pap.item(tv_pap.selection())['values'][0]), refresh_pap()] if tv_pap.selection() and messagebox.askyesno("C.R.G", "¿Borrar de por vida?") else None).pack(side="left", padx=12)
        refresh_pap()

    # --- MODALES ---
    def actualizar_pass_modal(self, doc):
        v = ctk.CTkToplevel(self.root); v.title("C.R.G Seguridad"); v.geometry("420x320"); v.grab_set()
        ctk.CTkLabel(v, text="Cambio de Clave Obligatorio", font=("Segoe UI", 16, "bold")).pack(pady=25)
        e = ctk.CTkEntry(v, placeholder_text="Nueva contraseña", show="*", width=280); e.pack(pady=15)
        def guardar():
            res, msg = self.servicio.actualizar_password(doc, e.get())
            if res: messagebox.showinfo("OK", msg); v.destroy()
            else: messagebox.showwarning("Error", msg)
        ctk.CTkButton(v, text="ACTUALIZAR SEGURIDAD", command=guardar).pack(pady=25)

if __name__ == "__main__":
    root = ctk.CTk()
    app = SistemaHSGS(root)
    root.mainloop()