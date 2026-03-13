"""
Módulo PasswordManager
Encapsula funcionalidades de cambio de contraseña y calendario personalizado
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from config import COLORES, FUENTES
import datetime
import calendar as _calendar
import bcrypt
import logging


class CalendarioPersonalizado(ctk.CTkFrame):
    """Calendario personalizado moderno con diseño CustomTkinter - Vista de mes grande con horarios"""
    
    def __init__(self, parent, sena_green, bg_light):
        super().__init__(parent, fg_color="white", corner_radius=10, border_width=2, border_color="#CCC")
        
        self.sena_green = sena_green
        self.bg_light = bg_light
        self.fecha_seleccionada = datetime.date.today()
        self.callback = None
        self.registros_mes = {}  # Dict: {datetime.date: [{'entrada': '10:20', 'salida': '12:00'}, ...]}
        self.mapeo_celdas_fechas = {}  # Mapea índice de celda a fecha para clicks
        
        # Header del calendario
        header_cal = ctk.CTkFrame(self, fg_color=self.sena_green, corner_radius=8)
        header_cal.pack(fill="x", padx=2, pady=2)
        
        # Controles de navegación
        nav_frame = ctk.CTkFrame(header_cal, fg_color="transparent")
        nav_frame.pack(fill="x", padx=10, pady=8)
        
        self.btn_prev = ctk.CTkButton(nav_frame, text="◀", width=40, height=40,
                                     fg_color="transparent", text_color="white",
                                     hover_color="#2D5A27", font=("Segoe UI", 14, "bold"),
                                     command=self._mes_anterior)
        self.btn_prev.pack(side="left")
        
        self.lbl_mes_anio = ctk.CTkLabel(nav_frame, text="", font=("Segoe UI", 14, "bold"),
                                        text_color="white")
        self.lbl_mes_anio.pack(side="left", expand=True)
        
        self.btn_next = ctk.CTkButton(nav_frame, text="▶", width=40, height=40,
                                     fg_color="transparent", text_color="white",
                                     hover_color="#2D5A27", font=("Segoe UI", 14, "bold"),
                                     command=self._mes_siguiente)
        self.btn_next.pack(side="right")
        
        # Días de la semana (usar X para miércoles)
        dias_semana = ["L", "M", "X", "J", "V", "S", "D"]
        dias_header = ctk.CTkFrame(self, fg_color="transparent", height=40)
        dias_header.pack(fill="x", padx=5, pady=5)
        
        for dia in dias_semana:
            ctk.CTkLabel(dias_header, text=dia, font=("Segoe UI", 12, "bold"),
                        text_color="#333", fg_color="transparent").pack(side="left", expand=True, fill="both")
        
        # Grid de días (celdas grandes)
        self.dias_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dias_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.celdas_dias = []  # Frames para cada día
        self._crear_grid_dias()
        self._actualizar_calendario()
    
    def _crear_grid_dias(self):
        """Crea la cuadrícula de celdas para los días (frames grandes)"""
        for widget in self.dias_frame.winfo_children():
            widget.destroy()
        
        self.celdas_dias = []
        self.mapeo_celdas_fechas = {}
        
        for idx in range(42):  # 6 semanas x 7 días
            semana = idx // 7
            dia = idx % 7
            
            # Celda grande para el día (frame)
            celda = ctk.CTkFrame(self.dias_frame, fg_color="#F9F9F9", 
                                border_width=1, border_color="#DDD",
                                corner_radius=6)
            celda.grid(row=semana, column=dia, padx=2, pady=2, sticky="nsew")
            
            # Binding SOLO click - SIN hover
            celda.bind("<Button-1>", lambda e, idx_celda=idx: self._click_celda(idx_celda))
            
            # Frame interior para organizar mejor el contenido
            interior = ctk.CTkFrame(celda, fg_color="transparent")
            interior.pack(fill="both", expand=True, padx=6, pady=6)
            
            # Label para el número del día (arriba)
            lbl_numero = ctk.CTkLabel(interior, text="", font=("Segoe UI", 18, "bold"),
                                     text_color="#333", fg_color="transparent")
            lbl_numero.pack(anchor="ne", expand=False)
            
            # Label para entrada/salida (abajo, expandible)
            lbl_horarios = ctk.CTkLabel(interior, text="", font=("Segoe UI", 10),
                                       text_color="#666", fg_color="transparent", 
                                       justify="left")
            lbl_horarios.pack(anchor="sw", expand=True, fill="y")
            
            # Enlazar click también en los labels - SIN hover
            lbl_numero.bind("<Button-1>", lambda e, idx_celda=idx: self._click_celda(idx_celda))
            lbl_horarios.bind("<Button-1>", lambda e, idx_celda=idx: self._click_celda(idx_celda))
            
            # El interior también debe ser clickeable - SIN hover
            interior.bind("<Button-1>", lambda e, idx_celda=idx: self._click_celda(idx_celda))
            
            self.celdas_dias.append({
                'frame': celda,
                'interior': interior,
                'numero': lbl_numero,
                'horarios': lbl_horarios,
                'fecha': None,
                'color_original': '#F9F9F9'
            })
        
        # Configurar grid weights para que se expanda uniformemente
        for i in range(7):
            self.dias_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.dias_frame.grid_rowconfigure(i, weight=1)
    
    def _actualizar_calendario(self):
        """Actualiza la visualización del calendario con horarios (SIN tocar bindings)"""
        anio = self.fecha_seleccionada.year
        mes = self.fecha_seleccionada.month
        
        # Actualizar título
        nombre_mes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes-1]
        self.lbl_mes_anio.configure(text=f"{nombre_mes} {anio}")
        
        # Calcular días del mes
        cal = _calendar.monthcalendar(anio, mes)
        
        # Limpiar mapeo y celdas
        self.mapeo_celdas_fechas = {}
        for celda in self.celdas_dias:
            celda['numero'].configure(text="")
            celda['horarios'].configure(text="")
            celda['frame'].configure(fg_color="#F9F9F9", border_color="#DDD")
            celda['numero'].configure(text_color="#333")
            celda['horarios'].configure(text_color="#666")
            celda['fecha'] = None
        
        # Llenar con días del mes
        idx_celda = 0
        for semana in cal:
            for dia in semana:
                if idx_celda < len(self.celdas_dias):
                    celda = self.celdas_dias[idx_celda]
                    
                    if dia != 0:
                        fecha_btn = datetime.date(anio, mes, dia)
                        celda['fecha'] = fecha_btn
                        self.mapeo_celdas_fechas[idx_celda] = fecha_btn
                        celda['numero'].configure(text=str(dia))
                        
                        # Buscar registros para este día
                        texto_horarios = ""
                        if fecha_btn in self.registros_mes:
                            registros = self.registros_mes[fecha_btn]
                            for reg in registros[:2]:  # Máximo 2 registros en la vista
                                if reg.get('entrada'):
                                    texto_horarios += f"IN: {reg['entrada']}\n"
                                if reg.get('salida'):
                                    texto_horarios += f"OUT: {reg['salida']}\n"
                        celda['horarios'].configure(text=texto_horarios.rstrip())
                        
                        # Resaltar día seleccionado
                        if fecha_btn == self.fecha_seleccionada:
                            celda['frame'].configure(fg_color=self.sena_green, border_color=self.sena_green)
                            celda['numero'].configure(text_color="white")
                            celda['horarios'].configure(text_color="white")
                        elif fecha_btn == datetime.date.today():
                            celda['frame'].configure(fg_color="#FFF3CD", border_color="#FFD700")
                        elif texto_horarios:  # Si tiene registros, color de fondo claro
                            celda['frame'].configure(fg_color="#E8F5E8", border_color="#90EE90")
                    
                    idx_celda += 1
    
    def _click_celda(self, idx_celda):
        """Maneja click en celda usando el mapeo de fechas con feedback visual"""
        fecha = self.mapeo_celdas_fechas.get(idx_celda)
        if fecha and idx_celda < len(self.celdas_dias):
            self.fecha_seleccionada = fecha
            self.after(50, self._actualizar_calendario)
            self.after(100, lambda: self.callback() if self.callback else None)
    
    def _mes_anterior(self):
        """Ir al mes anterior con transición suave"""
        if self.fecha_seleccionada.month == 1:
            self.fecha_seleccionada = self.fecha_seleccionada.replace(year=self.fecha_seleccionada.year - 1, month=12)
        else:
            self.fecha_seleccionada = self.fecha_seleccionada.replace(month=self.fecha_seleccionada.month - 1)
        
        # Pequeña pausa para sentir la transición
        self.after(30, self._actualizar_calendario)
        self.after(80, lambda: self.callback() if self.callback else None)
    
    def _mes_siguiente(self):
        """Ir al mes siguiente con transición suave"""
        if self.fecha_seleccionada.month == 12:
            self.fecha_seleccionada = self.fecha_seleccionada.replace(year=self.fecha_seleccionada.year + 1, month=1)
        else:
            self.fecha_seleccionada = self.fecha_seleccionada.replace(month=self.fecha_seleccionada.month + 1)
        
        # Pequeña pausa para sentir la transición
        self.after(30, self._actualizar_calendario)
        self.after(80, lambda: self.callback() if self.callback else None)
    
    def selection_get(self):
        """Método de compatibilidad con Calendar original"""
        return self.fecha_seleccionada
    
    def selection_set(self, fecha):
        """Método de compatibilidad con Calendar original"""
        if isinstance(fecha, str):
            fecha = datetime.datetime.fromisoformat(fecha).date()
        self.fecha_seleccionada = fecha
        self._actualizar_calendario()
    
    def establecer_registros_mes(self, dict_registros):
        """Establece los registros de asistencia del mes.
        Param: dict_registros - {datetime.date: [{'entrada': 'HH:MM', 'salida': 'HH:MM'}, ...]}
        """
        self.registros_mes = dict_registros or {}
        self._actualizar_calendario()
    
    def bind(self, evento, callback):
        """Método de compatibilidad con Calendar original"""
        if evento == "<<CalendarSelected>>":
            self.callback = callback


class PasswordManager:
    """Gestiona el cambio obligatorio de contraseña con diseño moderno"""

    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.sena_green = COLORES['SENA_GREEN']
        self.sena_orange = COLORES['SENA_ORANGE']
        self.bg_light = COLORES['BG_LIGHT']

    def actualizar_password_ventana(self, documento):
        """Muestra ventana modal para cambio obligatorio de contraseña"""
        v = ctk.CTkToplevel(self.app.root)
        v.title("🔒 Seguridad C.R.S")
        v.geometry("500x650")
        v.configure(fg_color=self.bg_light)
        v.resizable(False, False)
        v.grab_set()

        def bloquear_cierre():
            messagebox.showwarning("Obligatorio", "Debe cambiar la contraseña antes de continuar.")
        v.protocol("WM_DELETE_WINDOW", bloquear_cierre)

        # Header
        header = ctk.CTkFrame(v, height=80, corner_radius=0, 
                             fg_color=self.sena_orange, border_width=0)
        header.pack(fill="x", side="top")
        
        ctk.CTkLabel(header, text="🔒 Cambio Obligatorio de Contraseña", 
                    font=("Segoe UI", 16, "bold"),
                    text_color="white").pack(pady=(15, 10), padx=20)
        
        ctk.CTkLabel(header, text="Configura una contraseña segura para proteger tu cuenta", 
                    font=("Segoe UI", 10),
                    text_color="white").pack(padx=20, pady=(0, 15))

        # Contenedor principal
        main_frame = ctk.CTkFrame(v, fg_color=self.bg_light)
        main_frame.pack(fill="both", expand=True, padx=30, pady=25)

        # Campo de contraseña
        ctk.CTkLabel(main_frame, text="Nueva Contraseña:", 
                    font=("Segoe UI", 12, "bold"),
                    text_color="#2C3E50").pack(anchor="w", pady=(0, 8))
        
        pass_var = ctk.StringVar()
        entry_pass = ctk.CTkEntry(main_frame, textvariable=pass_var, 
                                 show="•", height=40, placeholder_text="Ingresa tu nueva contraseña",
                                 border_color=self.sena_green, border_width=2)
        entry_pass.pack(fill="x", pady=(0, 20))

        # Marcos de requisitos con diseño mejorado
        ctk.CTkLabel(main_frame, text="Requisitos de Seguridad:", 
                    font=("Segoe UI", 11, "bold"),
                    text_color="#2C3E50").pack(anchor="w", pady=(0, 12))

        req_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10, 
                                border_width=1, border_color="#E0E0E0")
        req_frame.pack(fill="x", pady=(0, 20))

        requisitos = {
            "long": ctk.CTkLabel(req_frame, text="✗ Mínimo 8 caracteres", 
                                text_color="#E74C3C", font=("Segoe UI", 11)),
            "upper": ctk.CTkLabel(req_frame, text="✗ Al menos una mayúscula", 
                                 text_color="#E74C3C", font=("Segoe UI", 11)),
            "lower": ctk.CTkLabel(req_frame, text="✗ Al menos una minúscula", 
                                 text_color="#E74C3C", font=("Segoe UI", 11)),
            "num": ctk.CTkLabel(req_frame, text="✗ Al menos un número", 
                               text_color="#E74C3C", font=("Segoe UI", 11))
        }
        
        for lbl in requisitos.values():
            lbl.pack(anchor="w", padx=15, pady=6)

        def validar(*args):
            p = pass_var.get()
            cond = {
                "long": len(p) >= 8,
                "upper": any(c.isupper() for c in p),
                "lower": any(c.islower() for c in p),
                "num": any(c.isdigit() for c in p)
            }
            
            symbols = {"long": "✓", "upper": "✓", "lower": "✓", "num": "✓"}
            texts = {
                "long": "Mínimo 8 caracteres",
                "upper": "Al menos una mayúscula",
                "lower": "Al menos una minúscula",
                "num": "Al menos un número"
            }
            
            for k, c in cond.items():
                color = self.sena_green if c else "#E74C3C"
                symbol = symbols[k] if c else "✗"
                requisitos[k].configure(text=f"{symbol} {texts[k]}", text_color=color)
            
            return all(cond.values())

        pass_var.trace_add("write", validar)

        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0))

        def guardar():
            if validar():
                try:
                    # Hashear contraseña con bcrypt
                    hash_password = bcrypt.hashpw(pass_var.get().encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    self.db.cursor.execute(
                        "UPDATE estudiantes SET password=%s, cambio_pass=1 WHERE documento=%s",
                        (hash_password, documento)
                    )
                    self.db.conexion.commit()
                    messagebox.showinfo("✅ C.R.S", "Contraseña configurada exitosamente")
                    v.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
            else:
                messagebox.showwarning("Atención", "Por favor cumple todos los requisitos de seguridad")

        ctk.CTkButton(btn_frame, text="✓ GUARDAR Y ENTRAR", height=45,
                     fg_color=self.sena_green, hover_color="#32900D",
                     font=("Segoe UI", 12, "bold"),
                     command=guardar).pack(fill="x")

