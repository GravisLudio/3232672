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
        
        # 1. SOLUCIÓN: Iniciar en pantalla completa (maximizada)
        self.root.state('zoomed') 
        self.root.configure(bg="#F0F2F5")
        
        self.db = InventarioDB()
        if self.db.conexion:
            self.db.cursor = self.db.conexion.cursor(dictionary=True, buffered=True)

        self.sena_green = "#39A900"
        self.sena_dark = "#2D5A27"

        # Estilos
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Sena.TButton", font=("Segoe UI", 10, "bold"), background=self.sena_green, foreground="white")
        self.style.map("Sena.TButton", background=[('active', self.sena_dark)])

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
        tk.Label(f, text="GATEWAY HSGS", font=("Segoe UI", 24, "bold"), bg="white", fg=self.sena_dark).pack(pady=40)
        tk.Button(f, text="💻 TERMINAL APRENDICES", bg=self.sena_green, fg="white", font=("bold", 12), width=30, height=2, command=self.mostrar_terminal).pack(pady=10)
        tk.Button(f, text="🔐 PANEL ADMINISTRATIVO", bg="#333333", fg="white", font=("bold", 12), width=30, height=2, command=self.mostrar_login).pack(pady=10)
        ttk.Button(f, text="👤 MI PERFIL (APRENDIZ)", style="Sena.TButton", command=self.login_aprendiz).pack(pady=10, ipady=10, padx=60, fill="x")

    # --- VISTA 2: TERMINAL (VALIDACIONES ESTRICTAS) ---
    def mostrar_terminal(self):
        self.limpiar_pantalla()
        head = tk.Frame(self.main_container, bg=self.sena_green, height=60); head.pack(fill="x")
        tk.Button(head, text="⬅ VOLVER", bg=self.sena_dark, fg="white", command=self.mostrar_inicio, font=("bold", 10)).pack(side="left", padx=10, pady=15)
        
        f = tk.Frame(self.main_container, bg="white", padx=50, pady=50)
        f.place(relx=0.5, rely=0.5, anchor="center", width=600, height=550)
        tk.Label(f, text="REGISTRO DE ASISTENCIA", font=("bold", 18), bg="white").pack(pady=20)
        self.ent_doc = tk.Entry(f, font=("Segoe UI", 24), bd=2, relief="solid", justify="center")
        self.ent_doc.pack(pady=20, fill="x")

        def cmd_entrada():
            doc = self.ent_doc.get()
            if not doc: return
            # Validar existencia
            self.db.cursor.execute("SELECT documento FROM estudiantes WHERE documento=%s", (doc,))
            if not self.db.cursor.fetchone():
                self.db.cursor.execute("SELECT documento FROM estudiantes_eliminados WHERE documento=%s", (doc,))
                msg = "⚠️ El aprendiz está en la PAPELERA." if self.db.cursor.fetchone() else "❌ El aprendiz NO existe."
                messagebox.showerror("HSGS", msg); return

            # 2. SOLUCIÓN: Limitar a una sola entrada activa
            self.db.cursor.execute("SELECT id_asistencia FROM asistencias WHERE documento_estudiante=%s AND fecha_salida IS NULL", (doc,))
            if self.db.cursor.fetchone():
                messagebox.showwarning("HSGS", "⚠️ Ya tienes una entrada activa. Registra SALIDA primero."); return
            
            if self.db.insertar(doc, 1):
                messagebox.showinfo("HSGS", "✅ Entrada Exitosa"); self.ent_doc.delete(0, tk.END)

        def cmd_salida():
            doc = self.ent_doc.get()
            if not doc: return
            # 3. SOLUCIÓN: Validar que exista una entrada previa antes de permitir salida
            self.db.cursor.execute("SELECT id_asistencia FROM asistencias WHERE documento_estudiante=%s AND fecha_salida IS NULL", (doc,))
            res = self.db.cursor.fetchone()
            if res:
                self.db.cursor.execute("UPDATE asistencias SET fecha_salida=NOW() WHERE id_asistencia=%s", (res['id_asistencia'],))
                self.db.conexion.commit(); messagebox.showinfo("HSGS", "✅ Salida Exitosa"); self.ent_doc.delete(0, tk.END)
            else: 
                messagebox.showerror("HSGS", "❌ No tienes ninguna entrada activa para cerrar.")

        tk.Button(f, text="📥 ENTRADA", bg=self.sena_green, fg="white", font=("bold", 14), height=2, command=cmd_entrada).pack(fill="x", pady=10)
        tk.Button(f, text="📤 SALIDA", bg=self.sena_dark, fg="white", font=("bold", 14), height=2, command=cmd_salida).pack(fill="x", pady=10)

    # --- VISTA 3: LOGIN ---
    def mostrar_login(self):
        self.limpiar_pantalla()
        f = tk.Frame(self.main_container, bg="white", highlightthickness=1, highlightbackground="#CCC")
        f.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)
        tk.Label(f, text="LOGIN ADMIN", font=("bold", 16), bg="white").pack(pady=20)
        tk.Label(f, text="Usuario:", bg="white").pack(); u_ent = ttk.Entry(f); u_ent.pack(pady=5)
        tk.Label(f, text="Contraseña:", bg="white").pack(); p_ent = ttk.Entry(f, show="*"); p_ent.pack(pady=5)

        def intentar_login():
            self.db.cursor.execute("SELECT * FROM usuarios_admin WHERE usuario=%s AND password=%s", (u_ent.get(), p_ent.get()))
            if self.db.cursor.fetchone(): self.mostrar_panel_admin()
            else: messagebox.showerror("HSGS", "Usuario o clave incorrecta")

        tk.Button(f, text="INGRESAR", bg="#333", fg="white", font=("bold", 10), width=20, height=2, command=intentar_login).pack(pady=20)
        tk.Button(f, text="CANCELAR", fg="red", bg="white", bd=0, command=self.mostrar_inicio).pack()

    # --- VISTA 4: PANEL ADMIN (CON COMBOBOX DE FICHAS) ---
    def mostrar_panel_admin(self):
        self.limpiar_pantalla()
        head = tk.Frame(self.main_container, bg=self.sena_dark, height=60); head.pack(fill="x")
        tk.Label(head, text="PANEL ADMINISTRATIVO HSGS", fg="white", bg=self.sena_dark, font=("bold", 12)).pack(side="left", padx=20)
        tk.Button(head, text="🔒 SALIR", bg="#444", fg="white", command=self.mostrar_inicio).pack(side="right", padx=10, pady=15)

        nb = ttk.Notebook(self.main_container)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        t_asis = tk.Frame(nb, bg="white"); nb.add(t_asis, text=" 🕒 HISTORIAL ")
        t_gest = tk.Frame(nb, bg="white"); nb.add(t_gest, text=" 👥 GESTIÓN ")
        t_reg  = tk.Frame(nb, bg="white"); nb.add(t_reg,  text=" 📝 REGISTRO ")
        t_pap  = tk.Frame(nb, bg="white"); nb.add(t_pap,  text=" 🗑️ PAPELERA ")

        # --- LÓGICA HISTORIAL ---
        tv_asis = ttk.Treeview(t_asis, columns=("ID_E", "ID_S", "DOC", "FICHA", "FECHA"), show="headings")
        for c in ("ID_E", "ID_S", "DOC", "FICHA", "FECHA"): tv_asis.heading(c, text=c); tv_asis.column(c, anchor="center")
        tv_asis.pack(fill="both", expand=True, padx=10, pady=10)
        
        def refresh_asis():
            for i in tv_asis.get_children(): tv_asis.delete(i)
            q = "SELECT a.id_asistencia, a.documento_estudiante, e.id_ficha, a.fecha_registro, a.fecha_salida FROM asistencias a JOIN estudiantes e ON a.documento_estudiante = e.documento ORDER BY a.fecha_registro DESC"
            self.db.cursor.execute(q)
            for r in self.db.cursor.fetchall():
                tv_asis.insert("", "end", values=(f"E-{r['id_asistencia']}", f"S-{r['id_asistencia']}" if r['fecha_salida'] else "---", r['documento_estudiante'], r['id_ficha'], r['fecha_registro']))
        tk.Button(t_asis, text="🔄 ACTUALIZAR", command=refresh_asis).pack(pady=5); refresh_asis()

        # --- LÓGICA GESTIÓN ---
        f_bus = tk.Frame(t_gest, bg="white", pady=10); f_bus.pack(fill="x", padx=20)
        ent_bus = ttk.Entry(f_bus, width=30); ent_bus.pack(side="left", padx=10)
        tv_gest = ttk.Treeview(t_gest, columns=("DOC", "NOM", "FICHA"), show="headings")
        for c in ("DOC", "NOM", "FICHA"): tv_gest.heading(c, text=c); tv_gest.column(c, anchor="center")
        tv_gest.pack(fill="both", expand=True, padx=20)

        def filtrar():
            for i in tv_gest.get_children(): tv_gest.delete(i)
            val = f"%{ent_bus.get()}%"
            self.db.cursor.execute("SELECT documento, nombre_completo, id_ficha FROM estudiantes WHERE documento LIKE %s OR nombre_completo LIKE %s", (val, val))
            for r in self.db.cursor.fetchall(): tv_gest.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))

        def mandar_papelera():
            sel = tv_gest.selection()
            if not sel: return
            doc = tv_gest.item(sel)['values'][0]
            if messagebox.askyesno("HSGS", f"¿Mover a {doc} a la papelera?"):
                self.db.cursor.execute("INSERT INTO estudiantes_eliminados (documento, nombre_completo, correo, id_ficha) SELECT documento, nombre_completo, correo, id_ficha FROM estudiantes WHERE documento=%s", (doc,))
                self.db.cursor.execute("DELETE FROM estudiantes WHERE documento=%s", (doc,))
                self.db.conexion.commit(); filtrar(); refresh_pap()

        tk.Button(f_bus, text="🔍 BUSCAR", command=filtrar).pack(side="left")
        tk.Button(t_gest, text="🗑️ MOVER A PAPELERA", bg="#dc3545", fg="white", font=("bold", 9), command=mandar_papelera).pack(pady=10)

        # --- LÓGICA REGISTRO (CON COMBOBOX DE FICHAS) ---
        f1 = tk.LabelFrame(t_reg, text=" REGISTRO MANUAL ", bg="white", padx=20, pady=20); f1.pack(pady=20, padx=50, fill="x")
        ins = {}
        campos = ["Documento", "Nombre Completo", "Correo"]
        for i, k in enumerate(campos):
            tk.Label(f1, text=k, bg="white").grid(row=0, column=i, padx=5, sticky="w")
            e = ttk.Entry(f1); e.grid(row=1, column=i, padx=5, sticky="ew"); ins[k] = e

        # Selector de Ficha
        tk.Label(f1, text="Seleccionar Ficha", bg="white").grid(row=0, column=3, padx=5, sticky="w")
        cb_ficha = ttk.Combobox(f1, state="readonly")
        cb_ficha.grid(row=1, column=3, padx=5, sticky="ew")

        def actualizar_fichas():
            self.db.cursor.execute("SELECT id_ficha, codigo_ficha, nombre_programa FROM fichas")
            fichas = self.db.cursor.fetchall()
            cb_ficha['values'] = [f"{f['id_ficha']} | {f['codigo_ficha']} - {f['nombre_programa']}" for f in fichas]
        
        actualizar_fichas()

        def save_one():
            vals = {k: ins[k].get() for k in campos}
            ficha_sel = cb_ficha.get()
            if "" in vals.values() or not ficha_sel:
                messagebox.showwarning("HSGS", "Todos los campos son obligatorios."); return
            
            id_ficha = ficha_sel.split(" | ")[0] # Extraemos el ID numérico
            try:
                self.db.cursor.execute("INSERT INTO estudiantes (documento, nombre_completo, correo, id_ficha) VALUES (%s, %s, %s, %s)", 
                                     (vals["Documento"], vals["Nombre Completo"], vals["Correo"], id_ficha))
                self.db.conexion.commit(); messagebox.showinfo("HSGS", "✅ Guardado."); 
                for e in ins.values(): e.delete(0, tk.END)
                cb_ficha.set('')
            except Exception as e: messagebox.showerror("Error", str(e))

        tk.Button(f1, text="💾 GUARDAR", bg=self.sena_green, fg="white", command=save_one).grid(row=1, column=4, padx=10)

        def load_ex():
            path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")])
            if path:
                df = pd.read_excel(path) if path.endswith('.xlsx') else pd.read_csv(path)
                for _, r in df.iterrows():
                    self.db.cursor.execute("INSERT IGNORE INTO estudiantes (documento, nombre_completo, correo, id_ficha) VALUES (%s, %s, %s, %s)", (r['documento'], r['nombre_completo'], r['correo'], r['id_ficha']))
                self.db.conexion.commit(); messagebox.showinfo("HSGS", "✅ Importación finalizada.")

        tk.Button(t_reg, text="📂 IMPORTAR EXCEL/CSV", bg=self.sena_dark, fg="white", command=load_ex).pack(pady=10)

        # --- LÓGICA PAPELERA (RESTAURADA CON FICHA) ---
        tv_pap = ttk.Treeview(t_pap, columns=("DOC", "NOM", "FICHA"), show="headings")
        tv_pap.heading("DOC", text="DOC"); tv_pap.heading("NOM", text="NOMBRE"); tv_pap.heading("FICHA", text="FICHA")
        tv_pap.pack(fill="both", expand=True, padx=20, pady=10)
        
        def refresh_pap():
            for i in tv_pap.get_children(): tv_pap.delete(i)
            self.db.cursor.execute("SELECT documento, nombre_completo, id_ficha FROM estudiantes_eliminados")
            for r in self.db.cursor.fetchall(): tv_pap.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))
        
        def restaurar():
            sel = tv_pap.selection()
            if sel:
                d = tv_pap.item(sel)['values'][0]
                self.db.cursor.execute("INSERT INTO estudiantes (documento, nombre_completo, correo, id_ficha) SELECT documento, nombre_completo, correo, id_ficha FROM estudiantes_eliminados WHERE documento=%s", (d,))
                self.db.cursor.execute("DELETE FROM estudiantes_eliminados WHERE documento=%s", (d,))
                self.db.conexion.commit(); refresh_pap(); filtrar()

        def hard_delete():
            sel = tv_pap.selection()
            if not sel: return
            doc = tv_pap.item(sel)['values'][0]
            if messagebox.askyesno("HSGS CRÍTICO", f"¿Borrar PERMANENTEMENTE a {doc}?\nEsta acción es irreversible."):
                self.db.cursor.execute("DELETE FROM estudiantes_eliminados WHERE documento=%s", (doc,))
                self.db.conexion.commit(); refresh_pap()

        f_btn_p = tk.Frame(t_pap, bg="white"); f_btn_p.pack(pady=5)
        tk.Button(f_btn_p, text="♻️ RESTAURAR", bg=self.sena_green, fg="white", command=restaurar).pack(side="left", padx=10)
        tk.Button(f_btn_p, text="🔥 ELIMINAR PERMANENTE", bg="black", fg="white", command=hard_delete).pack(side="left", padx=10)
        refresh_pap()


    # --- PANEL APRENDIZ (CALENDARIO + TARJETAS) ---
    def login_aprendiz(self):
        self.limpiar_pantalla()
        f = tk.Frame(self.main_container, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
        f.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)
        tk.Label(f, text="ACCESO APRENDIZ", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=30)
        tk.Label(f, text="Documento", bg="white").pack(anchor="w", padx=50); doc_ent = ttk.Entry(f); doc_ent.pack(pady=5, padx=50, fill="x")
        tk.Label(f, text="Contraseña", bg="white").pack(anchor="w", padx=50, pady=(10,0)); pass_ent = ttk.Entry(f, show="*"); pass_ent.pack(pady=5, padx=50, fill="x")

        def intentar_login():
            doc = doc_ent.get(); pas = pass_ent.get()
            q = "SELECT * FROM estudiantes WHERE documento=%s AND password=%s"
            self.db.cursor.execute(q, (doc, pas))
            user = self.db.cursor.fetchone()
            if user:
                if user.get('cambio_pass') == 0 or pas == 'sena123':
                    self.actualizar_password_ventana(user['documento'])
                self.mostrar_panel_aprendiz(user)
            else: messagebox.showerror("Error", "Documento o clave incorrectos")
        ttk.Button(f, text="ENTRAR", style="Sena.TButton", command=intentar_login).pack(pady=20, padx=50, fill="x")
        ttk.Button(f, text="VOLVER", command=self.mostrar_inicio).pack()

    def mostrar_panel_aprendiz(self, datos_user):
        self.limpiar_pantalla()
        doc_usuario = datos_user['documento']
        head = tk.Frame(self.main_container, bg=self.sena_green, height=60); head.pack(fill="x")
        tk.Button(head, text="⬅ CERRAR SESIÓN", bg=self.sena_dark, fg="white", command=self.mostrar_inicio, font=("bold", 10)).pack(side="left", padx=10, pady=15)
        tk.Label(head, text=f"BIENVENIDO: {datos_user['nombre_completo']}", bg=self.sena_green, fg="white", font=("bold", 12)).pack(side="right", padx=20)

        main_frame = tk.Frame(self.main_container, bg="#F4F7F6"); main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        left_side = tk.Frame(main_frame, bg="white", highlightthickness=1, highlightbackground="#DDD")
        left_side.place(relx=0, rely=0, relwidth=0.65, relheight=1)
        cal = Calendar(left_side, selectmode='day', locale='es_ES', background=self.sena_green, headersbackground=self.sena_dark)
        cal.pack(fill="both", expand=True, padx=20, pady=20)

        right_side = tk.Frame(main_frame, bg="white", highlightthickness=1, highlightbackground="#DDD")
        right_side.place(relx=0.67, rely=0, relwidth=0.33, relheight=1)
        lbl_date = tk.Label(right_side, text="Día Seleccionado", font=("bold", 12), bg="white"); lbl_date.pack(pady=15)
        lbl_h = tk.Label(right_side, text="⏱️ 0h 0m", font=("Segoe UI", 10), bg="white", fg="#007bff"); lbl_h.pack()

        canvas_asis = tk.Canvas(right_side, bg="white", highlightthickness=0); canvas_asis.pack(side="left", fill="both", expand=True)
        scroll_y = ttk.Scrollbar(right_side, orient="vertical", command=canvas_asis.yview); scroll_y.pack(side="right", fill="y")
        frame_tarjetas = tk.Frame(canvas_asis, bg="white")
        canvas_asis.create_window((0, 0), window=frame_tarjetas, anchor="nw", width=350)
        canvas_asis.configure(yscrollcommand=scroll_y.set)

        def cargar_datos_dia(event=None):
            for widget in frame_tarjetas.winfo_children(): widget.destroy()
            fecha_sel = cal.selection_get(); lbl_date.config(text=fecha_sel.strftime("%A, %d de %B"))
            query = "SELECT fecha_registro, fecha_salida FROM asistencias WHERE documento_estudiante = %s AND DATE(fecha_registro) = %s"
            self.db.cursor.execute(query, (doc_usuario, fecha_sel))
            registros = self.db.cursor.fetchall()
            minutos_totales = 0
            if not registros:
                tk.Label(frame_tarjetas, text="Sin registros.", bg="white", fg="#BBB", pady=40).pack()
                lbl_h.config(text="⏱️ 0h 0m")
            else:
                for r in registros:
                    f = tk.Frame(frame_tarjetas, bg="#EBF7F3", pady=8, highlightbackground="#39A900", highlightthickness=1)
                    f.pack(fill="x", pady=4, padx=10)
                    tk.Label(f, text=f"📥 Ent: {r['fecha_registro'].strftime('%H:%M:%S')}", bg="#EBF7F3").pack(side="left", padx=10)
                    if r['fecha_salida']:
                        tk.Label(f, text=f"📤 Sal: {r['fecha_salida'].strftime('%H:%M:%S')}", bg="#EBF7F3").pack(side="right", padx=10)
                        minutos_totales += (r['fecha_salida'] - r['fecha_registro']).total_seconds() / 60
                lbl_h.config(text=f"⏱️ Total: {int(minutos_totales//60)}h {int(minutos_totales%60)}m")
            frame_tarjetas.update_idletasks(); canvas_asis.config(scrollregion=canvas_asis.bbox("all"))

        cal.bind("<<CalendarSelected>>", cargar_datos_dia); cargar_datos_dia()

    def actualizar_password_ventana(self, documento):
        v = tk.Toplevel(self.root); v.title("Seguridad"); v.geometry("350x250"); v.configure(bg="white")
        tk.Label(v, text="🔒 ACTUALIZAR CONTRASEÑA", font=("bold", 11), bg="white").pack(pady=20)
        e = ttk.Entry(v, show="*"); e.pack(pady=10, padx=40, fill="x"); e.focus()
        def save():
            if len(e.get()) < 4: return messagebox.showwarning("HSGS", "Mínimo 4 caracteres")
            self.db.cursor.execute("UPDATE estudiantes SET password=%s, cambio_pass=1 WHERE documento=%s", (e.get(), documento))
            self.db.conexion.commit(); messagebox.showinfo("HSGS", "✅ Éxito"); v.destroy()
        ttk.Button(v, text="GUARDAR", command=save).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaHSGS(root)
    root.mainloop()