import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from conexion import InventarioDB # Asegúrate de que apunte a TechSenaHSGS

class SREE_HSGS:
    def __init__(self, root):
        self.root = root
        self.root.title("HSGS - SREE | Sistema de Registro Estudiantil")
        self.root.geometry("1100x700")
        self.root.configure(bg="#F0F2F5")

        # Paleta Institucional SENA (HSGS Edition)
        self.sena_green = "#39A900"
        self.sena_dark = "#2D5A27"
        self.sena_orange = "#FF6B00"
        self.white = "#FFFFFF"

        self.db = InventarioDB()

        # --- HEADER CON CANVAS (Efecto Moderno) ---
        self.header_canvas = tk.Canvas(self.root, height=100, bg=self.sena_green, highlightthickness=0)
        self.header_canvas.pack(fill="x")
        
        # Dibujamos un diseño decorativo en el canvas
        self.header_canvas.create_rectangle(0, 0, 2000, 100, fill=self.sena_green, outline="")
        self.header_canvas.create_polygon(800, 0, 1100, 0, 1100, 100, 950, 100, fill="#329200", outline="")
        
        self.header_canvas.create_text(50, 50, text="SREE", font=("Segoe UI", 32, "bold"), fill="white", anchor="w")
        self.header_canvas.create_text(170, 55, text="High Softwares From Gravis Systems", 
                                      font=("Segoe UI", 10, "italic"), fill="#E0E0E0", anchor="w")

        # --- CONTENEDOR PRINCIPAL ---
        self.container = tk.Frame(self.root, bg="#F0F2F5", padx=20, pady=20)
        self.container.pack(fill="both", expand=True)

        # --- PANEL IZQUIERDO: REGISTRO RÁPIDO ---
        self.left_panel = tk.Frame(self.container, bg=self.white, bd=0, padx=20, pady=20)
        self.left_panel.place(x=0, y=0, width=350, height=540)
        
        # Sombra simulada (Canvas pequeño)
        tk.Label(self.left_panel, text="REGISTRO DE ENTRADA", font=("Segoe UI", 14, "bold"), 
                 bg=self.white, fg=self.sena_dark).pack(pady=(0, 20))

        # Campos
        self.fields = {}
        for label_text in ["Documento Aprendiz:", "ID Competencia:"]:
            tk.Label(self.left_panel, text=label_text, bg=self.white, font=("Segoe UI", 10)).pack(anchor="w")
            entry = tk.Entry(self.left_panel, font=("Segoe UI", 12), bd=1, relief="solid")
            entry.pack(fill="x", pady=(5, 15))
            self.fields[label_text] = entry

        # Botón de Registro con Canvas (Estilo botón moderno)
        self.btn_reg_canvas = tk.Canvas(self.left_panel, width=280, height=50, bg=self.white, highlightthickness=0, cursor="hand2")
        self.btn_reg_canvas.pack(pady=10)
        self.draw_button(self.btn_reg_canvas, self.sena_green, "REGISTRAR ENTRADA")
        self.btn_reg_canvas.bind("<Button-1>", lambda e: self.registrar_asistencia())

        # Separador decorativo
        tk.Frame(self.left_panel, height=2, bg="#EEEEEE").pack(fill="x", pady=20)

        # Botón de Limpiar
        tk.Button(self.left_panel, text="Limpiar Campos", font=("Segoe UI", 9), bg="#F5F5F5", 
                  relief="flat", command=self.limpiar).pack(fill="x")

        # --- PANEL DERECHO: VISUALIZACIÓN ---
        self.right_panel = tk.Frame(self.container, bg="#F0F2F5")
        self.right_panel.place(x=370, y=0, width=690, height=540)

        # Tabla con estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", rowheight=30, font=("Segoe UI", 9), borderwidth=0)
        self.style.configure("Treeview.Heading", background="#EFEFEF", font=("Segoe UI", 10, "bold"), relief="flat")

        self.tree_frame = tk.Frame(self.right_panel, bg=self.white, bd=1, relief="solid")
        self.tree_frame.pack(fill="both", expand=True)

        cols = ("ID", "DOCUMENTO", "COMPETENCIA", "FECHA/HORA")
        self.tabla = ttk.Treeview(self.tree_frame, columns=cols, show="headings")
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, anchor="center")
        
        self.tabla.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        sc = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=sc.set)
        sc.pack(side="right", fill="y")

        # --- PANEL INFERIOR: ACCIONES DE MARCA ---
        self.footer = tk.Frame(self.root, bg=self.white, height=60)
        self.footer.pack(fill="x", side="bottom")
        
        tk.Label(self.footer, text=f"© 2026 High Softwares From Gravis Systems | Desarrollado por: {self.get_user_name()}", 
                 bg=self.white, fg="#999999", font=("Segoe UI", 9)).pack(pady=10)

    def draw_button(self, canvas, color, text):
        canvas.create_rectangle(0, 0, 280, 50, fill=color, outline="", tags="rect")
        canvas.create_text(140, 25, text=text, fill="white", font=("Segoe UI", 11, "bold"), tags="text")

    def get_user_name(self):
        return "GRAVIS LUDIO"

    def limpiar(self):
        for e in self.fields.values(): e.delete(0, tk.END)

    def registrar_asistencia(self):
        doc = self.fields["Documento Aprendiz:"].get()
        comp = self.fields["ID Competencia:"].get()
        
        if not doc or not comp:
            messagebox.showwarning("HSGS", "Por favor complete los campos.")
            return

        # Lógica de inserción en SQL
        query = "INSERT INTO asistencias (documento_estudiante, id_competencia) VALUES (%s, %s)"
        try:
            self.db.cursor.execute(query, (doc, comp))
            self.db.conexion.commit()
            messagebox.showinfo("HSGS", f"Entrada registrada para: {doc}")
            self.cargar_datos()
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error HSGS", f"No se pudo registrar: {e}")

    def cargar_datos(self):
        for i in self.tabla.get_children(): self.tabla.delete(i)
        self.db.cursor.execute("SELECT id_asistencia, documento_estudiante, id_competencia, fecha_registro FROM asistencias ORDER BY fecha_registro DESC")
        for r in self.db.cursor.fetchall():
            self.tabla.insert("", "end", values=r)

if __name__ == "__main__":
    root = tk.Tk()
    app = SREE_HSGS(root)
    root.mainloop()