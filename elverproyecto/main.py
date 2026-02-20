import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from conexion import InventarioDB 
from tkcalendar import Calendar
import datetime

class SistemaHSGS:
    def __init__(self, root):
        self.root = root
        self.root.title("SREE PRO - High Softwares From Gravis Systems")
        self.root.geometry("1200x850")
        self.root.configure(bg="#F0F2F5")
        
        # Conexión con cursor bufferizado para evitar errores de sincronía con la DB
        self.db = InventarioDB()
        if self.db.conexion:
            self.db.cursor = self.db.conexion.cursor(dictionary=True, buffered=True)

        self.sena_green = "#39A900"
        self.sena_dark = "#2D5A27"

        # Configuración de estilos globales
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Sena.TButton", font=("Segoe UI", 10, "bold"), background=self.sena_green, foreground="white")
        self.style.map("Sena.TButton", background=[('active', self.sena_dark)])

        # CONTENEDOR MAESTRO
        self.main_container = tk.Frame(self.root, bg="#F0F2F5")
        self.main_container.pack(fill="both", expand=True)

        self.mostrar_inicio()

    def limpiar_pantalla(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- VISTA 1: INICIO ---
    def mostrar_inicio(self):
        self.limpiar_pantalla()
        f = tk.Frame(self.main_container, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
        f.place(relx=0.5, rely=0.5, anchor="center", width=500, height=450)
        
        tk.Label(f, text="GATEWAY HSGS", font=("Segoe UI", 24, "bold"), bg="white", fg=self.sena_dark).pack(pady=(40, 10))
        tk.Label(f, text="SREE PRO System", font=("Segoe UI", 9), bg="white", fg="#888").pack()
        
        tk.Button(f, text="💻 TERMINAL APRENDICES", bg=self.sena_green, fg="white", font=("bold", 12), width=30, height=2, command=self.mostrar_terminal).pack(pady=10)
        tk.Button(f, text="🔐 PANEL ADMINISTRATIVO", bg="#333333", fg="white", font=("bold", 12), width=30, height=2, command=self.mostrar_login).pack(pady=10)
        
        ttk.Button(f, text="👤 MI PERFIL (APRENDIZ)", style="Sena.TButton", command=self.login_aprendiz).pack(pady=10, ipady=10, padx=60, fill="x")

    # --- VISTA LOGIN APRENDIZ ---
    def login_aprendiz(self):
        self.limpiar_pantalla()
        f = tk.Frame(self.main_container, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
        f.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)
        
        tk.Label(f, text="ACCESO APRENDIZ", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=30)
        
        tk.Label(f, text="Documento", bg="white").pack(anchor="w", padx=50)
        doc_ent = ttk.Entry(f); doc_ent.pack(pady=5, padx=50, fill="x")
        
        tk.Label(f, text="Contraseña", bg="white").pack(anchor="w", padx=50, pady=(10,0))
        pass_ent = ttk.Entry(f, show="*") ; pass_ent.pack(pady=5, padx=50, fill="x")

        def intentar_login():
            doc = doc_ent.get()
            pas = pass_ent.get()
            q = "SELECT * FROM estudiantes WHERE documento=%s AND password=%s"
            self.db.cursor.execute(q, (doc, pas))
            user = self.db.cursor.fetchone()
            
            if user:
                # Si el campo cambio_pass es 0, forzar actualización
                if user.get('cambio_pass') == 0 or pas == 'sena123':
                    self.actualizar_password_ventana(user['documento'])
                self.mostrar_panel_aprendiz(user)
            else:
                messagebox.showerror("Error", "Documento o clave incorrectos")

        ttk.Button(f, text="ENTRAR", style="Sena.TButton", command=intentar_login).pack(pady=20, padx=50, fill="x")
        ttk.Button(f, text="VOLVER", command=self.mostrar_inicio).pack(padx=50)

    # --- VENTANA ACTUALIZAR PASSWORD ---
    def actualizar_password_ventana(self, documento):
        ventana_pass = tk.Toplevel(self.root)
        ventana_pass.title("Seguridad HSGS")
        ventana_pass.geometry("350x300")
        ventana_pass.configure(bg="white")
        ventana_pass.transient(self.root)
        ventana_pass.grab_set()

        tk.Label(ventana_pass, text="🔒 ACTUALIZAR CONTRASEÑA", font=("Segoe UI", 12, "bold"), bg="white").pack(pady=20)
        tk.Label(ventana_pass, text="Por seguridad, cree una nueva contraseña:", bg="white", font=("Segoe UI", 9)).pack(pady=5)
        
        nueva_pass = ttk.Entry(ventana_pass, show="*")
        nueva_pass.pack(pady=10, padx=40, fill="x")
        nueva_pass.focus()

        def guardar_nueva_pass():
            pass_val = nueva_pass.get()
            if len(pass_val) < 4:
                messagebox.showwarning("HSGS", "Mínimo 4 caracteres.")
                return
            
            try:
                query = "UPDATE estudiantes SET password=%s, cambio_pass=1 WHERE documento=%s"
                self.db.cursor.execute(query, (pass_val, documento))
                self.db.conexion.commit()
                messagebox.showinfo("HSGS", "✅ Contraseña actualizada correctamente.")
                ventana_pass.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(ventana_pass, text="GUARDAR CAMBIOS", command=guardar_nueva_pass).pack(pady=20)

    # --- PANEL APRENDIZ (CALENDARIO + TARJETAS DE REGISTRO) ---
    def mostrar_panel_aprendiz(self, datos_user):
        self.limpiar_pantalla()
        doc_usuario = datos_user['documento']
        
        color_fondo = "#F4F7F6"
        color_entrada_bg = "#EBF7F3"
        color_entrada_border = "#39A900"
        color_salida_bg = "#FFF5F2"
        color_salida_border = "#FF7043"

        main_frame = tk.Frame(self.main_container, bg=color_fondo)
        main_frame.pack(fill="both", expand=True)

        # LADO IZQUIERDO: CALENDARIO FÍSICO
        left_side = tk.Frame(main_frame, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
        left_side.place(relx=0.03, rely=0.05, relwidth=0.62, relheight=0.9)

        cal = Calendar(left_side, selectmode='day', locale='es_ES',
                       background=self.sena_green, foreground='white',
                       selectbackground=self.sena_dark,
                       headersbackground='#FFFFFF', borderwidth=0)
        cal.pack(fill="both", expand=True, padx=20, pady=20)

        # LADO DERECHO: DETALLES Y BOTÓN SALIR
        right_side = tk.Frame(main_frame, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
        right_side.place(relx=0.67, rely=0.05, relwidth=0.3, relheight=0.9)

        head_detail = tk.Frame(right_side, bg="white")
        head_detail.pack(fill="x", padx=20, pady=20)
        
        lbl_dia_nombre = tk.Label(head_detail, text="Día Seleccionado", font=("Segoe UI", 12, "bold"), bg="white")
        lbl_dia_nombre.pack(anchor="w")
        lbl_horas_totales = tk.Label(head_detail, text="⏱️ 0h 0m", font=("Segoe UI", 10), bg="white", fg="#007bff")
        lbl_horas_totales.pack(anchor="w")

        # Área de tarjetas con Scroll
        canvas_asis = tk.Canvas(right_side, bg="white", highlightthickness=0)
        scroll_y = ttk.Scrollbar(right_side, orient="vertical", command=canvas_asis.yview)
        frame_tarjetas = tk.Frame(canvas_asis, bg="white")

        canvas_asis.create_window((0, 0), window=frame_tarjetas, anchor="nw", width=320)
        canvas_asis.configure(yscrollcommand=scroll_y.set)
        canvas_asis.pack(side="left", fill="both", expand=True, padx=5)
        scroll_y.pack(side="right", fill="y")

        def crear_tarjeta(tipo, hora):
            bg = color_entrada_bg if tipo == "Entrada" else color_salida_bg
            border = color_entrada_border if tipo == "Entrada" else color_salida_border
            card = tk.Frame(frame_tarjetas, bg=bg, highlightbackground=border, highlightthickness=1, pady=8)
            card.pack(fill="x", pady=4, padx=10)
            tk.Label(card, text=f"{'📥' if tipo=='Entrada' else '📤'} {tipo}", font=("bold", 9), bg=bg).pack(side="left", padx=10)
            tk.Label(card, text=hora, font=("Consolas", 9), bg=bg).pack(side="right", padx=10)

        def cargar_datos_dia(event=None):
            for widget in frame_tarjetas.winfo_children(): widget.destroy()
            fecha_sel = cal.selection_get()
            lbl_dia_nombre.config(text=fecha_sel.strftime("%A, %d de %B"))
            
            q = "SELECT fecha_registro, fecha_salida FROM asistencias WHERE documento_estudiante = %s AND DATE(fecha_registro) = %s"
            self.db.cursor.execute(q, (doc_usuario, fecha_sel))
            registros = self.db.cursor.fetchall()
            
            minutos = 0
            if not registros:
                tk.Label(frame_tarjetas, text="No hay actividad registrada.", bg="white", fg="#BBB", pady=30).pack()
                lbl_horas_totales.config(text="⏱️ 0h 0m")
            else:
                for r in registros:
                    crear_tarjeta("Entrada", r['fecha_registro'].strftime("%H:%M:%S"))
                    if r['fecha_salida']:
                        crear_tarjeta("Salida", r['fecha_salida'].strftime("%H:%M:%S"))
                        minutos += (r['fecha_salida'] - r['fecha_registro']).total_seconds() / 60
                lbl_horas_totales.config(text=f"⏱️ Total del día: {int(minutos//60)}h {int(minutos%60)}m")
            
            frame_tarjetas.update_idletasks()
            canvas_asis.config(scrollregion=canvas_asis.bbox("all"))

        # BOTÓN DE SALIDA DEL PERFIL
        tk.Button(right_side, text="🚪 CERRAR SESIÓN", command=self.mostrar_inicio, 
                  bg="#CC0000", fg="white", font=("Segoe UI", 10, "bold"), 
                  cursor="hand2", bd=0, pady=10).pack(side="bottom", fill="x", padx=20, pady=20)

        cal.bind("<<CalendarSelected>>", cargar_datos_dia)
        cargar_datos_dia()

    # --- VISTA TERMINAL (PARA REGISTRO RÁPIDO) ---
    def mostrar_terminal(self):
        self.limpiar_pantalla()
        head = tk.Frame(self.main_container, bg=self.sena_green, height=60); head.pack(fill="x")
        tk.Button(head, text="⬅ VOLVER", bg=self.sena_dark, fg="white", command=self.mostrar_inicio).pack(side="left", padx=10, pady=15)
        
        f = tk.Frame(self.main_container, bg="white", padx=50, pady=50)
        f.place(relx=0.5, rely=0.5, anchor="center", width=600, height=550)
        tk.Label(f, text="REGISTRO DE ASISTENCIA", font=("bold", 18), bg="white").pack(pady=20)
        self.ent_doc = tk.Entry(f, font=("Segoe UI", 24), bd=2, relief="solid", justify="center")
        self.ent_doc.pack(pady=20, fill="x")

        def cmd_entrada():
            doc = self.ent_doc.get()
            if not doc: return
            self.db.cursor.execute("SELECT documento FROM estudiantes WHERE documento=%s", (doc,))
            if not self.db.cursor.fetchone():
                messagebox.showerror("HSGS", "❌ El aprendiz NO existe.")
                return
            if self.db.insertar(doc, 1): # Competencia por defecto
                messagebox.showinfo("HSGS", "✅ Entrada Exitosa"); self.ent_doc.delete(0, tk.END)

        def cmd_salida():
            doc = self.ent_doc.get()
            self.db.cursor.execute("SELECT id_asistencia FROM asistencias WHERE documento_estudiante=%s AND fecha_salida IS NULL", (doc,))
            res = self.db.cursor.fetchone()
            if res:
                self.db.cursor.execute("UPDATE asistencias SET fecha_salida=NOW() WHERE id_asistencia=%s", (res['id_asistencia'],))
                self.db.conexion.commit(); messagebox.showinfo("HSGS", "✅ Salida Exitosa"); self.ent_doc.delete(0, tk.END)
            else: messagebox.showerror("HSGS", "No hay entradas pendientes para este documento.")

        tk.Button(f, text="📥 ENTRADA", bg=self.sena_green, fg="white", font=("bold", 14), height=2, command=cmd_entrada).pack(fill="x", pady=10)
        tk.Button(f, text="📤 SALIDA", bg=self.sena_dark, fg="white", font=("bold", 14), height=2, command=cmd_salida).pack(fill="x", pady=10)

    # --- PANEL ADMINISTRATIVO ---
    def mostrar_login(self):
        self.limpiar_pantalla()
        f = tk.Frame(self.main_container, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
        f.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)
        
        tk.Label(f, text="LOGIN ADMIN", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=20)
        tk.Label(f, text="Usuario:", bg="white").pack(); u_ent = tk.Entry(f); u_ent.pack(pady=5)
        tk.Label(f, text="Contraseña:", bg="white").pack(); p_ent = tk.Entry(f, show="*"); p_ent.pack(pady=5)

        def intentar_login():
            self.db.cursor.execute("SELECT * FROM usuarios_admin WHERE usuario=%s AND password=%s", (u_ent.get(), p_ent.get()))
            if self.db.cursor.fetchone(): self.mostrar_panel_admin()
            else: messagebox.showerror("HSGS", "Usuario o clave incorrecta")
        
        tk.Button(f, text="INGRESAR", bg="#333333", fg="white", width=20, height=2, command=intentar_login).pack(pady=30)
        tk.Button(f, text="VOLVER", command=self.mostrar_inicio, bd=0, bg="white", fg="blue").pack()

    def mostrar_panel_admin(self):
        self.limpiar_pantalla()
        head = tk.Frame(self.main_container, bg=self.sena_dark, height=60); head.pack(fill="x")
        tk.Label(head, text="SREE PRO - PANEL ADMINISTRATIVO", fg="white", bg=self.sena_dark, font=("bold", 12)).pack(side="left", padx=20)
        tk.Button(head, text="🔒 CERRAR PANEL", bg="#444", fg="white", command=self.mostrar_inicio).pack(side="right", padx=10, pady=15)

        nb = ttk.Notebook(self.main_container)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        t_asis = tk.Frame(nb, bg="white"); nb.add(t_asis, text=" 🕒 HISTORIAL ")
        t_gest = tk.Frame(nb, bg="white"); nb.add(t_gest, text=" 👥 GESTIÓN ")
        t_reg  = tk.Frame(nb, bg="white"); nb.add(t_reg,  text=" 📝 REGISTRO ")

        # Historial de asistencias
        def refresh_asis():
            for i in tv_asis.get_children(): tv_asis.delete(i)
            q = "SELECT a.id_asistencia, a.documento_estudiante, e.id_ficha, a.fecha_registro FROM asistencias a JOIN estudiantes e ON a.documento_estudiante = e.documento ORDER BY a.fecha_registro DESC"
            self.db.cursor.execute(q)
            for r in self.db.cursor.fetchall():
                tv_asis.insert("", "end", values=(r['id_asistencia'], r['documento_estudiante'], r['id_ficha'], r['fecha_registro']))

        tv_asis = ttk.Treeview(t_asis, columns=("ID", "DOC", "FICHA", "FECHA"), show="headings")
        for c in ("ID", "DOC", "FICHA", "FECHA"): tv_asis.heading(c, text=c); tv_asis.column(c, anchor="center")
        tv_asis.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Button(t_asis, text="🔄 ACTUALIZAR", command=refresh_asis).pack(pady=5); refresh_asis()

        # Indicadores de secciones pendientes
        tk.Label(t_gest, text="Módulo de Gestión de Aprendices\n(Filtros y Edición)", font=("italic", 12), pady=100, bg="white").pack()
        tk.Label(t_reg, text="Módulo de Registro Masivo\n(Importación Excel/CSV)", font=("italic", 12), pady=100, bg="white").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaHSGS(root)
    root.mainloop()