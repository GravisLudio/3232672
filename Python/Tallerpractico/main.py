import tkinter as tk
from tkinter import ttk, messagebox
from conexion import InventarioDB 

class AppInventario:
    def __init__(self, root):
        self.root = root
        self.root.title("HSGS - High Softwares From Gravis Systems | Gestión TechSENA")
        self.root.geometry("1000x680")
        
        self.bg_principal = "#F5F5F5"
        self.color_hsgs_v = "#2D5A27"
        self.color_oscuro = "#333333"
        self.color_celeste = "#E3F2FD"
        
        self.root.configure(bg=self.bg_principal)
        self.db = InventarioDB()

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="white", fieldbackground="white", rowheight=28, font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading", background="#E0E0E0", font=("Segoe UI", 10, "bold"))

        self.header = tk.Frame(self.root, bg=self.color_hsgs_v, height=70)
        self.header.pack(fill="x")
        tk.Label(self.header, text="SISTEMA DE GESTIÓN HSGS - TECHSENA", 
                 fg="white", bg=self.color_hsgs_v, font=("Segoe UI", 18, "bold")).pack(pady=15)

        self.main_container = tk.Frame(self.root, bg=self.bg_principal, padx=20, pady=20)
        self.main_container.pack(fill="both", expand=True)

        self.frame_form = tk.LabelFrame(self.main_container, text=" DATOS DEL COMPONENTE ", 
                                        bg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=15, fg=self.color_hsgs_v)
        self.frame_form.place(x=0, y=0, width=320, height=420)

        labels = ["Referencia:", "Descripción:", "Marca:", "Stock:", "Costo Unitario:"]
        self.entries = {}
        for i, text in enumerate(labels):
            tk.Label(self.frame_form, text=text, bg="white", font=("Segoe UI", 9), fg=self.color_oscuro).grid(row=i*2, column=0, sticky="w", pady=(5, 2))
            entry = tk.Entry(self.frame_form, font=("Segoe UI", 10), bd=1, relief="solid")
            entry.grid(row=i*2+1, column=0, sticky="ew", pady=(0, 10))
            self.entries[text] = entry
        
        self.frame_form.columnconfigure(0, weight=1)

        tk.Button(self.frame_form, text="💾 GUARDAR PRODUCTO", bg=self.color_hsgs_v, fg="white", 
              font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", command=self.guardar_producto).grid(row=10, column=0, sticky="ew", pady=(10, 5))
        tk.Button(self.frame_form, text="🧹 LIMPIAR CAMPOS", bg="#6c757d", fg="white", 
              relief="flat", cursor="hand2", command=self.limpiar_campos).grid(row=11, column=0, sticky="ew")

        self.frame_ops = tk.Frame(self.main_container, bg="white", bd=1, relief="solid", padx=10, pady=10)
        self.frame_ops.place(x=0, y=435, width=320, height=135)

        tk.Label(self.frame_ops, text="BUSCAR / ELIMINAR (REF):", bg="white", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.entry_busqueda = tk.Entry(self.frame_ops, font=("Segoe UI", 11), bd=1, relief="solid")
        self.entry_busqueda.pack(fill="x", pady=5)

        btn_c = tk.Frame(self.frame_ops, bg="white")
        btn_c.pack(fill="x")
        tk.Button(btn_c, text="🔍 BUSCAR", bg="#007bff", fg="white", relief="flat", command=self.buscar_producto).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(btn_c, text="🗑️ ELIMINAR", bg="#dc3545", fg="white", relief="flat", command=self.eliminar_producto).pack(side="left", fill="x", expand=True, padx=2)
        
        tk.Button(self.frame_ops, text="⚠️ ELIMINADO PERMANENTE", bg="#000000", fg="white", font=("Segoe UI", 8, "bold"),
              relief="flat", command=self.borrado_total_principal).pack(fill="x", pady=(5,0))

        self.frame_tabla_master = tk.Frame(self.main_container, bg=self.bg_principal)
        self.frame_tabla_master.place(x=345, y=10, width=610, height=550)

        self.frame_tabla = tk.Frame(self.frame_tabla_master, bg="white", bd=1, relief="solid")
        self.frame_tabla.pack(fill="both", expand=True)

        columnas = ("ID", "Referencia", "Descripción", "Marca", "Stock", "Costo")
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col.upper())
            self.tabla.column(col, width=90, anchor="center")

        self.tabla.tag_configure('oddrow', background="white")
        self.tabla.tag_configure('evenrow', background=self.color_celeste)
        self.tabla.pack(side="left", fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar_item)

        self.frame_botones_tabla = tk.Frame(self.frame_tabla_master, bg=self.bg_principal, pady=10)
        self.frame_botones_tabla.pack(fill="x")

        self.btn_listar = tk.Button(self.frame_botones_tabla, text="📋 LISTAR INVENTARIO", 
                                    bg=self.color_oscuro, fg="white", relief="flat",
                                    padx=15, font=("Segoe UI", 9, "bold"), command=self.cargar_datos)
        self.btn_listar.pack(side="left", padx=5)

        self.btn_historial = tk.Button(self.frame_botones_tabla, text="📜 HISTORIAL ELIMINADOS", 
                                       bg="#6c757d", fg="white", relief="flat",
                                       padx=15, font=("Segoe UI", 9, "bold"), command=self.abrir_ventana_historial)
        self.btn_historial.pack(side="left", padx=5)

        self.cargar_datos()

    def limpiar_campos(self):
        for entry in self.entries.values(): entry.delete(0, tk.END)
        self.entry_busqueda.delete(0, tk.END)

    def al_seleccionar_item(self, event):
        sel = self.tabla.selection()
        if sel:
            item_data = self.tabla.item(sel)['values']
            self.entry_busqueda.delete(0, tk.END)
            self.entry_busqueda.insert(0, item_data[1])
            fields = ["Referencia:", "Descripción:", "Marca:", "Stock:", "Costo Unitario:"]
            for i, field in enumerate(fields):
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, item_data[i+1])

    def cargar_datos(self):
        for item in self.tabla.get_children(): self.tabla.delete(item)
        productos = self.db.consultar_todos()
        for i, p in enumerate(productos):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tabla.insert("", "end", values=(p['id_item'], p['referencia'], p['descripcion'], p['marca'], p['stock'], p['costo_unitario']), tags=(tag,))

    def guardar_producto(self):
        ref = self.entries["Referencia:"].get()
        desc = self.entries["Descripción:"].get()
        marca = self.entries["Marca:"].get()
        stock = self.entries["Stock:"].get()
        costo = self.entries["Costo Unitario:"].get()
        if all([ref, desc, marca, stock, costo]) and self.db.insertar(ref, desc, marca, stock, costo):
            messagebox.showinfo("HSGS", "✅ Producto registrado.")
            self.limpiar_campos(); self.cargar_datos()
        else: messagebox.showwarning("HSGS", "Complete todos los campos correctamente.")

    def buscar_producto(self):
        ref = self.entry_busqueda.get()
        res = self.db.buscar_por_referencia(ref)
        for item in self.tabla.get_children(): self.tabla.delete(item)
        if res:
            for p in res: self.tabla.insert("", "end", values=(p['id_item'], p['referencia'], p['descripcion'], p['marca'], p['stock'], p['costo_unitario']), tags=('evenrow',))
        else: messagebox.showinfo("HSGS", "No se encontraron resultados.")

    def eliminar_producto(self):
        ref = self.entry_busqueda.get()
        if ref and messagebox.askyesno("HSGS", f"¿Mover {ref} al historial?"):
            if self.db.mover_a_historial(ref) and self.db.eliminar(ref):
                messagebox.showinfo("HSGS", "Movido al historial."); self.cargar_datos(); self.limpiar_campos()

    def borrado_total_principal(self):
        ref = self.entry_busqueda.get()
        
        if ref and messagebox.showwarning("HSGS", f"⚠️ ¿BORRADO PERMANENTE de {ref}?\nEsta acción no se puede deshacer."):
            if self.db.eliminar(ref):
                messagebox.showinfo("HSGS", f"Producto {ref} eliminado permanentemente."); self.cargar_datos(); self.limpiar_campos()

    def abrir_ventana_historial(self):
        v_h = tk.Toplevel(self.root)
        v_h.title("Historial HSGS")
        v_h.geometry("700x500")
        v_h.configure(bg="white")

        tk.Label(v_h, text="HISTORIAL DE PRODUCTOS ELIMINADOS", bg="white", font=("Segoe UI", 12, "bold"), fg="#dc3545").pack(pady=10)

        t_h = ttk.Treeview(v_h, columns=("REF", "DESC", "FECHA"), show="headings")
        for c in ("REF", "DESC", "FECHA"): t_h.heading(c, text=c)
        t_h.pack(fill="both", expand=True, padx=20)

        for i in self.db.consultar_historial():
            t_h.insert("", "end", values=(i['referencia'], i['descripcion'], i['fecha_eliminado']))

        def restaurar():
            s = t_h.selection()
            if s and self.db.restaurar_producto(t_h.item(s)['values'][0]):
                v_h.destroy(); self.cargar_datos()

        def borrar_definitivo():
            s = t_h.selection()
            if s:
                ref = t_h.item(s)['values'][0]
                if messagebox.askyesno("HSGS CRÍTICO", f"¿Borrar permanentemente {ref}?"):
                    try:
                        self.db.cursor.execute("DELETE FROM historial_eliminados WHERE referencia = %s", (ref,))
                        self.db.conexion.commit(); v_h.destroy(); messagebox.showinfo("HSGS", "Borrado definitivo.")
                    except: messagebox.showerror("Error", "No se pudo completar la operación.")

        btn_f = tk.Frame(v_h, bg="white")
        btn_f.pack(pady=20)
        tk.Button(btn_f, text="✅ RESTAURAR", bg=self.color_hsgs_v, fg="white", command=restaurar, width=15, relief="flat").pack(side="left", padx=5)
        tk.Button(btn_f, text="🔥 BORRADO TOTAL", bg="black", fg="white", command=borrar_definitivo, width=15, relief="flat").pack(side="left", padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppInventario(root)
    root.mainloop()