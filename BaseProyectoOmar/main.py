import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from conexion import InventarioDB
import calendar
from datetime import datetime 


class SistemaHSGS:
    def __init__(self, root):
        self.root = root
        self.root.title("SREE PRO - High Softwares From Gravis Systems")
        self.root.geometry("1200x850")
        self.root.configure(bg="#F0F2F5")
        
        # Conexión con cursor bufferizado para evitar "Unread result found"
        self.db = InventarioDB()
        if self.db.conexion:
            self.db.cursor = self.db.conexion.cursor(dictionary=True, buffered=True)

        self.sena_green = "#39A900"
        self.sena_dark = "#2D5A27"

        # CONTENEDOR MAESTRO (Intercambio de pantallas)
        self.main_container = tk.Frame(self.root, bg="#F0F2F5")
        self.main_container.pack(fill="both", expand=True)

        self.mostrar_inicio()

    def limpiar_pantalla(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- VISTA 1: INICIO ---
    def mostrar_inicio(self):
        self.limpiar_pantalla()
        f = tk.Frame(self.main_container, bg="white")
        f.place(relx=0.5, rely=0.5, anchor="center", width=500, height=400)
        tk.Label(f, text="GATEWAY HSGS", font=("Segoe UI", 20, "bold"), bg="white", fg=self.sena_dark).pack(pady=40)
        tk.Button(f, text="💻 TERMINAL APRENDICES", bg=self.sena_green, fg="white", font=("bold", 12), width=30, height=2, command=self.mostrar_terminal).pack(pady=10)
        tk.Button(f, text="🔐 PANEL ADMINISTRATIVO", bg="#333333", fg="white", font=("bold", 12), width=30, height=2, command=self.mostrar_login).pack(pady=10)
        # Dentro de mostrar_inicio
        ttk.Button(f, text="👤 MI PERFIL (APRENDIZ)", style="Sena.TButton", 
           command=self.login_aprendiz).pack(pady=10, ipady=10, padx=60, fill="x")
    # --- VISTA 2: TERMINAL (CON VALIDACIÓN DE PAPELERA) ---
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
            # Validar existencia/papelera
            self.db.cursor.execute("SELECT documento FROM estudiantes WHERE documento=%s", (doc,))
            if not self.db.cursor.fetchone():
                self.db.cursor.execute("SELECT documento FROM estudiantes_eliminados WHERE documento=%s", (doc,))
                if self.db.cursor.fetchone():
                    messagebox.showwarning("HSGS", "⚠️ El aprendiz está en la PAPELERA. Contacte al administrador.")
                else:
                    messagebox.showerror("HSGS", "❌ El aprendiz NO existe en el sistema.")
                return

            self.db.cursor.execute("SELECT id_asistencia FROM asistencias WHERE documento_estudiante=%s AND fecha_salida IS NULL", (doc,))
            if self.db.cursor.fetchone():
                messagebox.showwarning("HSGS", "⚠️ Ya tienes una entrada activa. Registra SALIDA primero.")
                return
            if self.db.insertar(doc, 1):
                messagebox.showinfo("HSGS", "✅ Entrada Exitosa"); self.ent_doc.delete(0, tk.END)

        def cmd_salida():
            doc = self.ent_doc.get()
            self.db.cursor.execute("SELECT id_asistencia FROM asistencias WHERE documento_estudiante=%s AND fecha_salida IS NULL", (doc,))
            res = self.db.cursor.fetchone()
            if res:
                self.db.cursor.execute("UPDATE asistencias SET fecha_salida=NOW() WHERE id_asistencia=%s", (res['id_asistencia'],))
                self.db.conexion.commit(); messagebox.showinfo("HSGS", "✅ Salida Exitosa"); self.ent_doc.delete(0, tk.END)
            else: messagebox.showerror("HSGS", "No tienes entradas pendientes para este documento.")

        tk.Button(f, text="📥 ENTRADA", bg=self.sena_green, fg="white", font=("bold", 14), height=2, command=cmd_entrada).pack(fill="x", pady=10)
        tk.Button(f, text="📤 SALIDA", bg=self.sena_dark, fg="white", font=("bold", 14), height=2, command=cmd_salida).pack(fill="x", pady=10)

    # --- VISTA 3: LOGIN ---
    def mostrar_login(self):
        self.limpiar_pantalla()
        f = tk.Frame(self.main_container, bg="white")
        f.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)
        tk.Button(f, text="❌ CANCELAR", bg="#cc0000", fg="white", command=self.mostrar_inicio).pack(anchor="e", padx=10, pady=10)
        tk.Label(f, text="LOGIN ADMIN", font=("bold", 16), bg="white").pack(pady=20)
        tk.Label(f, text="Usuario:").pack(); u_ent = tk.Entry(f); u_ent.pack(pady=5)
        tk.Label(f, text="Contraseña:").pack(); p_ent = tk.Entry(f, show="*"); p_ent.pack(pady=5)

        def intentar_login():
            self.db.cursor.execute("SELECT * FROM usuarios_admin WHERE usuario=%s AND password=%s", (u_ent.get(), p_ent.get()))
            if self.db.cursor.fetchone(): self.mostrar_panel_admin()
            else: messagebox.showerror("HSGS", "Usuario o clave incorrecta")
        tk.Button(f, text="INGRESAR", bg="#333333", fg="white", width=20, height=2, command=intentar_login).pack(pady=30)

    # --- VISTA 4: PANEL ADMIN (SUITE COMPLETA) ---
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

        # --- LÓGICA ASISTENCIA ---
        def refresh_asis():
            for i in tv_asis.get_children(): tv_asis.delete(i)
            q = "SELECT a.id_asistencia, a.documento_estudiante, e.id_ficha, a.fecha_registro, a.fecha_salida FROM asistencias a JOIN estudiantes e ON a.documento_estudiante = e.documento ORDER BY a.fecha_registro DESC"
            self.db.cursor.execute(q)
            for r in self.db.cursor.fetchall():
                tv_asis.insert("", "end", values=(f"E-{r['id_asistencia']}", f"S-{r['id_asistencia']}" if r['fecha_salida'] else "---", r['documento_estudiante'], r['id_ficha'], r['fecha_registro']))

        cols = ("ID_E", "ID_S", "DOC", "FICHA", "FECHA")
        tv_asis = ttk.Treeview(t_asis, columns=cols, show="headings")
        for c in cols: tv_asis.heading(c, text=c); tv_asis.column(c, anchor="center")
        tv_asis.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Button(t_asis, text="🔄 ACTUALIZAR", command=refresh_asis).pack(pady=5); refresh_asis()

        # --- LÓGICA GESTIÓN (FILTROS COMUNICATIVOS) ---
        f_bus = tk.Frame(t_gest, bg="white", pady=10); f_bus.pack(fill="x", padx=20)
        var_f = tk.StringVar(value="aprendiz")
        tk.Radiobutton(f_bus, text="Aprendiz", variable=var_f, value="aprendiz", bg="white").pack(side="left")
        tk.Radiobutton(f_bus, text="Ficha", variable=var_f, value="ficha", bg="white").pack(side="left", padx=10)
        ent_bus = tk.Entry(f_bus, width=30, bd=1, relief="solid"); ent_bus.pack(side="left", padx=10)

        tv_gest = ttk.Treeview(t_gest, columns=("DOC", "NOM", "FICHA"), show="headings")
        for c in ("DOC", "NOM", "FICHA"): tv_gest.heading(c, text=c); tv_gest.column(c, anchor="center")
        tv_gest.pack(fill="both", expand=True, padx=20)

        def filtrar():
            for i in tv_gest.get_children(): tv_gest.delete(i)
            val = f"%{ent_bus.get()}%"
            q = "SELECT documento, nombre_completo, id_ficha FROM estudiantes WHERE " + ("id_ficha LIKE %s" if var_f.get() == "ficha" else "documento LIKE %s OR nombre_completo LIKE %s")
            self.db.cursor.execute(q, (val,) if var_f.get() == "ficha" else (val, val))
            res = self.db.cursor.fetchall()
            if not res: messagebox.showinfo("HSGS", "🔍 No se encontraron coincidencias.")
            else:
                for r in res: tv_gest.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))

        def mandar_papelera():
            sel = tv_gest.selection()
            if not sel: return
            doc = tv_gest.item(sel)['values'][0]
            if messagebox.askyesno("HSGS", f"¿Mover a {doc} a la papelera?"):
                # Se incluyen TODAS las columnas (5) para evitar el error 1136
                self.db.cursor.execute("INSERT INTO estudiantes_eliminados (documento, nombre_completo, correo, id_ficha, fecha_eliminacion) SELECT documento, nombre_completo, correo, id_ficha, NOW() FROM estudiantes WHERE documento=%s", (doc,))
                self.db.cursor.execute("DELETE FROM estudiantes WHERE documento=%s", (doc,))
                self.db.conexion.commit(); filtrar(); refresh_pap()

        tk.Button(f_bus, text="🔍 BUSCAR", command=filtrar).pack(side="left")
        tk.Button(t_gest, text="🗑️ ENVIAR A PAPELERA", bg="#dc3545", fg="white", command=mandar_papelera).pack(pady=10)

        # --- LÓGICA REGISTRO (CON CORREO Y DETALLES DE ERROR) ---
        f1 = tk.LabelFrame(t_reg, text=" REGISTRO MANUAL ", bg="white", padx=20, pady=20); f1.pack(pady=20, padx=50, fill="x")
        ins = {}
        campos = ["Documento", "Nombre Completo", "Correo", "ID Ficha"]
        for i, k in enumerate(campos):
            tk.Label(f1, text=k, bg="white").grid(row=0, column=i, padx=5)
            e = tk.Entry(f1, bd=1, relief="solid"); e.grid(row=1, column=i, padx=5); ins[k] = e
        
        def save_one():
            vals = [ins[k].get() for k in campos]
            if "" in vals: messagebox.showwarning("HSGS", "Todos los campos son obligatorios."); return
            try:
                self.db.cursor.execute("INSERT INTO estudiantes (documento, nombre_completo, correo, id_ficha) VALUES (%s, %s, %s, %s)", tuple(vals))
                self.db.conexion.commit(); messagebox.showinfo("HSGS", "✅ Guardado."); [e.delete(0, tk.END) for e in ins.values()]
            except Exception as e:
                messagebox.showerror("HSGS Error", f"❌ No se pudo guardar.\nDetalle: {str(e)}\n\n(Verifique si el documento ya existe o la ficha es válida)")
        tk.Button(f1, text="💾 GUARDAR", bg=self.sena_green, fg="white", command=save_one).grid(row=1, column=4, padx=10)

        def load_ex():
            path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")])
            if path:
                df = pd.read_excel(path) if path.endswith('.xlsx') else pd.read_csv(path)
                for _, r in df.iterrows():
                    self.db.cursor.execute("INSERT IGNORE INTO estudiantes (documento, nombre_completo, correo, id_ficha) VALUES (%s, %s, %s, %s)", (r['documento'], r['nombre_completo'], r['correo'], r['id_ficha']))
                self.db.conexion.commit(); messagebox.showinfo("HSGS", "✅ Importación finalizada.")

        tk.Button(t_reg, text="📂 IMPORTAR EXCEL/CSV", bg=self.sena_dark, fg="white", command=load_ex).pack(pady=10)

        # --- LÓGICA PAPELERA (CON BORRADO PERMANENTE) ---
        tv_pap = ttk.Treeview(t_pap, columns=("DOC", "NOM"), show="headings")
        tv_pap.heading("DOC", text="DOC"); tv_pap.heading("NOM", text="NOMBRE"); tv_pap.pack(fill="both", expand=True, padx=20, pady=10)
        
        def refresh_pap():
            for i in tv_pap.get_children(): tv_pap.delete(i)
            self.db.cursor.execute("SELECT documento, nombre_completo FROM estudiantes_eliminados")
            for r in self.db.cursor.fetchall(): tv_pap.insert("", "end", values=(r['documento'], r['nombre_completo']))
        
        def restaurar():
            sel = tv_pap.selection()
            if sel:
                d = tv_pap.item(sel)['values'][0]
                self.db.cursor.execute("INSERT INTO estudiantes (documento, nombre_completo, correo, id_ficha) SELECT documento, nombre_completo, correo, id_ficha FROM estudiantes_eliminados WHERE documento=%s", (d,))
                self.db.cursor.execute("DELETE FROM estudiantes_eliminados WHERE documento=%s", (d,))
                self.db.conexion.commit(); refresh_pap(); filtrar()

        def hard_delete():
            sel = tv_pap.selection()
            if sel:
                d = tv_pap.item(sel)['values'][0]
                if messagebox.askyesno("HSGS CRÍTICO", f"¿Borrar PERMANENTEMENTE a {d}?\nEsta acción es irreversible."):
                    self.db.cursor.execute("DELETE FROM estudiantes_eliminados WHERE documento=%s", (d,))
                    self.db.conexion.commit(); refresh_pap()

        f_btn_p = tk.Frame(t_pap, bg="white"); f_btn_p.pack(pady=5)
        tk.Button(f_btn_p, text="♻️ RESTAURAR", bg=self.sena_green, fg="white", command=restaurar).pack(side="left", padx=10)
        tk.Button(f_btn_p, text="🔥 ELIMINAR PERMANENTE", bg="black", fg="white", command=hard_delete).pack(side="left", padx=10)
        tk.Button(t_pap, text="🔄 ACTUALIZAR", command=refresh_pap).pack(pady=5); refresh_pap()
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
            q = "SELECT * FROM estudiantes WHERE documento=%s AND password=%s"
            self.db.cursor.execute(q, (doc_ent.get(), pass_ent.get()))
            user = self.db.cursor.fetchone()
            if user: self.mostrar_panel_aprendiz(user)
            else: messagebox.showerror("Error", "Documento o clave incorrectos")

        ttk.Button(f, text="ENTRAR", style="Sena.TButton", command=intentar_login).pack(pady=20, padx=50, fill="x")
        ttk.Button(f, text="VOLVER", style="Dark.TButton", command=self.mostrar_inicio).pack(padx=50, fill="x")

    def mostrar_panel_aprendiz(self, datos_user):
            self.limpiar_pantalla()
            
            # --- ENCABEZADO ---
            head = tk.Frame(self.main_container, bg=self.sena_green, height=60)
            head.pack(fill="x")
            tk.Label(head, text=f"BIENVENIDO: {datos_user['nombre_completo']}", 
                    fg="white", bg=self.sena_green, font=("Segoe UI", 12, "bold")).pack(side="left", padx=20)
            tk.Button(head, text="SALIR", bg=self.sena_dark, fg="white", bd=0, 
                    command=self.mostrar_inicio, padx=15).pack(side="right", padx=10, pady=10)

            # --- CONTENEDOR PRINCIPAL ---
            body = tk.Frame(self.main_container, bg="#F0F2F5")
            body.pack(fill="both", expand=True, padx=40, pady=20)

            # Título y Mes Actual
            ahora = datetime.now()
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            
            titulo_cal = tk.Label(body, text=f"📅 {meses[ahora.month-1]} {ahora.year}", 
                                font=("Segoe UI", 18, "bold"), bg="#F0F2F5", fg="#333")
            titulo_cal.pack(pady=10)

            # --- CONSTRUCCIÓN DEL CALENDARIO ---
            cal_frame = tk.Frame(body, bg="white", bd=1, relief="solid")
            cal_frame.pack(pady=10)

            # Días de la semana
            dias_semana = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]
            for i, dia in enumerate(dias_semana):
                tk.Label(cal_frame, text=dia, font=("Segoe UI", 10, "bold"), 
                        bg="#EEEEEE", width=12, pady=5).grid(row=0, column=i, sticky="nsew")

            # Obtener datos de asistencia
            asistencias = self.db.obtener_reporte_horas(datos_user['documento'])
            # Convertimos las asistencias a un diccionario para búsqueda rápida {día: datos}
            dict_asistencias = {a['fecha'].day: a for a in asistencias if a['fecha'].month == ahora.month}

            # Generar matriz del mes
            cal = calendar.monthcalendar(ahora.year, ahora.month)
            
            for r, semana in enumerate(cal):
                for c, dia in enumerate(semana):
                    # Celda de día
                    celda = tk.Frame(cal_frame, bg="white", highlightbackground="#E0E0E0", 
                                    highlightthickness=1, width=100, height=100)
                    celda.grid(row=r+1, column=c, sticky="nsew")
                    celda.grid_propagate(False) # Mantener tamaño fijo

                    if dia != 0:
                        # Número de día
                        color_dia = self.sena_green if dia == ahora.day else "#333"
                        tk.Label(celda, text=str(dia), font=("Arial", 10, "bold"), 
                                bg="white", fg=color_dia).pack(anchor="nw", padx=5, pady=2)

                        # Si hay asistencia este día, mostrar registros
                        if dia in dict_asistencias:
                            asis = dict_asistencias[dia]
                            # Formatear horas para visualización corta
                            h_entrada = asis['entrada'].strftime('%I:%M %p')
                            h_salida = asis['salida'].strftime('%I:%M %p') if asis['salida'] else "..."
                            
                            tk.Label(celda, text=f"Entra: {h_entrada}", font=("Segoe UI", 7), 
                                    bg="white", fg="#cc0000").pack(pady=(5,0))
                            tk.Label(celda, text=f"Sale: {h_salida}", font=("Segoe UI", 7), 
                                    bg="white", fg="#cc0000").pack()
                            tk.Label(celda, text=f"{asis['horas']} hrs", font=("Segoe UI", 8, "bold"), 
                                    bg="#E8F5E9", fg=self.sena_dark).pack(fill="x", pady=5)

            # --- RESUMEN INFERIOR ---
            total_acumulado = sum(a['horas'] for a in asistencias)
            resumen = tk.Frame(body, bg="white", bd=1, relief="solid")
            resumen.pack(fill="x", pady=20)
            tk.Label(resumen, text=f"TOTAL HORAS ACUMULADAS: {round(total_acumulado, 2)} hrs", 
                    font=("Segoe UI", 14, "bold"), bg="white", fg=self.sena_dark, pady=10).pack()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaHSGS(root)
    root.mainloop()