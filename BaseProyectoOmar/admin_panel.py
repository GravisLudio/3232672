"""
Módulo PantallaAdministrador
Encapsula toda la lógica de la interfaz de administración
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from config import COLORES, FUENTES
import logging
import datetime
import calendar as _cal


class PantallaAdministrador:
    """Gestiona toda la pantalla de administrador con sus pestañas."""
    
    def __init__(self, frame_admin, db, servicio, admin_usuario, app):
        self.frame = frame_admin
        self.db = db
        self.servicio = servicio
        self.admin_usuario = admin_usuario
        self.app = app  # Referencia a la app principal
        
        self.sena_green = COLORES['SENA_GREEN']
        self.sena_dark = COLORES['SENA_DARK']
        self.bg_light = COLORES['BG_LIGHT']
        
        self._construir_layout()
    
    def _construir_layout(self):
        """Construye header + tabs principales"""
        # Header
        head = ctk.CTkFrame(self.frame, height=75, corner_radius=0, fg_color=self.sena_dark)
        head.pack(fill="x")
        
        ctk.CTkButton(head, text="CERRAR", fg_color="#444", 
                     command=self._cerrar_admin).pack(side="right", padx=25)
        
        btn_dash = ctk.CTkButton(head, text="DASHBOARD", fg_color=self.sena_green, 
                                hover_color=self.sena_dark, command=self.app.mostrar_dashboard)
        btn_dash.pack(side="left", padx=25)
        
        # TabView
        tabview = ctk.CTkTabview(self.frame, 
                                segmented_button_selected_color=self.sena_green, 
                                fg_color=self.bg_light)
        tabview.pack(fill="both", expand=True, padx=25, pady=15)
        
        # Crear pestañas
        self.t_hist = tabview.add("HISTORIAL")
        self.t_gest = tabview.add("GESTION")
        self.t_reg = tabview.add("REGISTRO")
        self.t_pap = tabview.add("PAPELERA")
        self.t_rep = tabview.add("REPORTES")
        
        for t in (self.t_hist, self.t_gest, self.t_reg, self.t_pap, self.t_rep):
            t.configure(fg_color=self.sena_dark, border_width=1, 
                       border_color="#DDD", corner_radius=20)
        
        # Construir cada pestaña
        self._construir_historial()
        self._construir_gestion()
        self._construir_registro()
        self._construir_papelera()
        self._construir_reportes()
    
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
        """Tab: Historial de asistencias"""
        tv_f1 = tk.Frame(self.t_hist, bg="#f7f7f7", borderwidth=1, relief="solid")
        tv_f1.pack(fill="both", expand=True, padx=12, pady=12)
        
        self.tv_hist = ttk.Treeview(tv_f1, columns=("DOC", "NOMBRE", "IN", "OUT"), 
                                    show="headings")
        for col in ("DOC", "NOMBRE", "IN", "OUT"):
            self.tv_hist.heading(col, text=col)
        self.tv_hist.pack(fill="both", expand=True)
        
        self._refrescar_historial()
    
    def _refrescar_historial(self):
        """Recarga historial de asistencias"""
        for i in self.tv_hist.get_children():
            self.tv_hist.delete(i)
        
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
        """Tab: Gestión de aprendices"""
        f_bus = ctk.CTkFrame(self.t_gest, fg_color="transparent")
        f_bus.pack(fill="x", padx=20, pady=15)
        
        ent_bus = ctk.CTkEntry(f_bus, placeholder_text="Buscar aprendiz...", width=420)
        ent_bus.pack(side="left", padx=10)
        
        tv_f2 = tk.Frame(self.t_gest, bg=self.bg_light)
        tv_f2.pack(fill="both", expand=True, padx=20)
        
        self.tv_gest = ttk.Treeview(tv_f2, columns=("DOC", "NOMBRE", "FICHA"), 
                                   show="headings", selectmode='extended')
        for col in ("DOC", "NOMBRE", "FICHA"):
            self.tv_gest.heading(col, text=col)
        self.tv_gest.pack(fill="both", expand=True)
        
        ctk.CTkButton(f_bus, text="FILTRAR", width=120, command=self._filtrar_gestion).pack(side="left")
        self._filtrar_gestion()
        
        ctk.CTkButton(self.t_gest, text="MOVER A PAPELERA", fg_color="#E74C3C", 
                     command=self._mover_papelera).pack(pady=10)
    
    def _filtrar_gestion(self):
        """Filtra aprendices en gestión"""
        for w in self.t_gest.winfo_children():
            if isinstance(w, ctk.CTkFrame):
                for child in w.winfo_children():
                    if isinstance(child, ctk.CTkEntry):
                        busqueda = child.get()
                        break
        
        for i in self.tv_gest.get_children():
            self.tv_gest.delete(i)
        
        v = f"%{busqueda if 'busqueda' in locals() else ''}%"
        self.db.cursor.execute(
            "SELECT documento, nombre_completo, id_ficha FROM estudiantes WHERE documento LIKE %s OR nombre_completo LIKE %s",
            (v, v)
        )
        for r in self.db.cursor.fetchall():
            self.tv_gest.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))
    
    def _mover_papelera(self):
        """Mueve aprendices seleccionados a papelera"""
        docs = [self.tv_gest.item(i)['values'][0] for i in self.tv_gest.selection()]
        if not docs:
            return
        if messagebox.askyesno("Confirmar", f"¿Desea mover {len(docs)} aprendices a la papelera?"):
            for doc in docs:
                self.servicio.mandar_a_papelera(doc)
                try:
                    self.db.registrar_auditoria(self.admin_usuario, "mover a papelera", objeto=doc)
                except Exception as ex:
                    logging.error(f"Error auditoría mover a papelera", exc_info=True)
            self._filtrar_gestion()
            self._refrescar_papelera()
    
    def _construir_registro(self):
        """Tab: Registro manual de aprendices"""
        f_reg_m = ctk.CTkFrame(self.t_reg, corner_radius=20, fg_color=self.bg_light, 
                              border_width=1, border_color="#EEE")
        f_reg_m.pack(pady=20, padx=50, fill="x")
        
        grid_f = tk.Frame(f_reg_m, bg=self.bg_light)
        grid_f.pack(pady=20, padx=25)
        
        fields = ["Documento", "Nombre Completo", "Correo"]
        self.entries_registro = {}
        for i, label in enumerate(fields):
            ctk.CTkLabel(grid_f, text=label, text_color="gray").grid(row=0, column=i, padx=12)
            e = ctk.CTkEntry(grid_f, width=190)
            e.grid(row=1, column=i, padx=5, pady=5)
            self.entries_registro[label] = e
        
        self.cb_ficha = ttk.Combobox(grid_f, state="readonly", width=40)
        self.cb_ficha.grid(row=1, column=3, padx=12)
        self.cb_ficha['values'] = [f"{f['id_ficha']} | {f['nombre_programa']}" 
                                   for f in self.servicio.obtener_fichas()]
        
        ctk.CTkButton(f_reg_m, text="GUARDAR", command=self._guardar_aprendiz).pack(pady=15)
        ctk.CTkButton(self.t_reg, text="CARGA EXCEL", fg_color="#333", 
                     command=self.servicio.importar_excel).pack()
        ctk.CTkButton(f_reg_m, text="LIMPIAR", fg_color="#555", 
                     command=self._limpiar_registro).pack(pady=5)
    
    def _guardar_aprendiz(self):
        """Guarda nuevo aprendiz en BD"""
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
        """Limpia formulario de registro"""
        for e in self.entries_registro.values():
            e.delete(0, 'end')
        self.cb_ficha.set('')
    
    def _construir_papelera(self):
        """Tab: Papelera (aprendices eliminados)"""
        tv_f3 = tk.Frame(self.t_pap, bg=self.bg_light)
        tv_f3.pack(fill="both", expand=True, padx=20, pady=12)
        
        self.tv_pap = ttk.Treeview(tv_f3, columns=("DOC", "NOMBRE", "FICHA"), 
                                  show="headings", selectmode='extended')
        for col in ("DOC", "NOMBRE", "FICHA"):
            self.tv_pap.heading(col, text=col)
        self.tv_pap.pack(fill="both", expand=True)
        
        self._refrescar_papelera()
        
        btn_p = ctk.CTkFrame(self.t_pap, fg_color="transparent")
        btn_p.pack(pady=10)
        
        ctk.CTkButton(btn_p, text="RESTAURAR", fg_color=self.sena_green, 
                     command=self._restaurar_aprendices).pack(side="left", padx=10)
        ctk.CTkButton(btn_p, text="ELIMINAR", fg_color="black", 
                     command=self._eliminar_permanente).pack(side="left", padx=10)
    
    def _refrescar_papelera(self):
        """Recarga papelera"""
        for i in self.tv_pap.get_children():
            self.tv_pap.delete(i)
        
        self.db.cursor.execute("SELECT documento, nombre_completo, id_ficha FROM estudiantes_eliminados")
        for r in self.db.cursor.fetchall():
            self.tv_pap.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))
    
    def _restaurar_aprendices(self):
        """Restaura aprendices desde papelera"""
        docs = [self.tv_pap.item(i)['values'][0] for i in self.tv_pap.selection()]
        for d in docs:
            self.servicio.restaurar_aprendiz(d)
            try:
                self.db.registrar_auditoria(self.admin_usuario, "restaurar aprendiz", objeto=d)
            except Exception as ex:
                logging.error(f"Error auditoría restaurar", exc_info=True)
        self._refrescar_papelera()
        self._filtrar_gestion()
    
    def _eliminar_permanente(self):
        """Elimina permanentemente aprendices"""
        docs = [self.tv_pap.item(i)['values'][0] for i in self.tv_pap.selection()]
        if messagebox.askyesno("Confirmar", "Esta acción es irreversible"):
            for d in docs:
                self.servicio.eliminar_permanente(d)
                try:
                    self.db.registrar_auditoria(self.admin_usuario, "eliminar permanente", objeto=d)
                except Exception as ex:
                    logging.error(f"Error auditoría eliminar", exc_info=True)
            self._refrescar_papelera()
    
    def _construir_reportes(self):
        """Tab: Reportes (delegado a la app principal por su complejidad)"""
        self.app.crear_pestana_reportes(self.t_rep)
