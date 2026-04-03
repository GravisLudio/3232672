# ── Bootstrap: verifica e instala dependencias con el Python que está corriendo ──
import sys
import subprocess
import importlib

def _asegurar_pip():
    """Instala pip si no está disponible"""
    try:
        import pip  # noqa
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "ensurepip", "--upgrade"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

def _instalar_si_falta(paquete, import_name=None):
    nombre = import_name or paquete
    try:
        importlib.import_module(nombre)
    except ImportError:
        print(f"[CRS] Instalando {paquete}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", paquete,
                 "--only-binary", ":all:", "-q"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", paquete, "-q"]
            )

_asegurar_pip()

_dependencias = [
    ("bcrypt",                 "bcrypt"),
    ("customtkinter",          "customtkinter"),
    ("mysql-connector-python", "mysql.connector"),
    ("tkcalendar",             "tkcalendar"),
    ("pandas",                 "pandas"),
    ("openpyxl",               "openpyxl"),
    ("reportlab",              "reportlab"),
    ("python-dotenv",          "dotenv"),
    ("Pillow",                 "PIL"),
]

for _pkg, _imp in _dependencias:
    _instalar_si_falta(_pkg, _imp)
# ── Fin bootstrap ─────────────────────────────────────────────────────────────

import tkinter as tk 
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from conexion import InventarioDB 
from tkcalendar import Calendar
import datetime
import re
import bcrypt
import customtkinter as ctk 
import logging
from logging_config import configure_logging
from PIL import Image, ImageTk
import os
from config import COLORES, FUENTES, DIMENSIONES, TEXTOS, CACHE
from admin_panel import PantallaAdministrador
from validadores import Validador
from reportes import ReportesManager
from dashboard_password import PasswordManager, CalendarioPersonalizado


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

configure_logging()


def _calcular_escala(root):
    """Calcula factor de escala según resolución real de la pantalla.
    Referencia: 1080p = factor 1.0. Pantallas menores reducen, mayores aumentan."""
    alto = root.winfo_screenheight()
    if alto >= 1440:  return 1.25
    if alto >= 1080:  return 1.0
    if alto >= 900:   return 0.88
    if alto >= 768:   return 0.78
    return 0.70       # resoluciones muy pequeñas

def _s(valor, escala):
    """Escala un valor numérico (tamaño, font, padding) según el factor."""
    return max(1, int(valor * escala))


class SistemaHSGSCRS:
    def __init__(self, root):
        self.root = root
        self.root.title("C.R.S - Chronos Registry System")

        # ── Escala adaptativa según resolución ────────────────────────────────
        # Maximizar PRIMERO para que winfo_screenheight sea el real
        self.root.state('zoomed')
        self.root.update()
        self.escala = _calcular_escala(self.root)
        ctk.set_widget_scaling(self.escala)
        # NO usar set_window_scaling — interfiere con zoomed
        # ──────────────────────────────────────────────────────────────────────

        # Ruta base del script para recursos
        self.ruta_base = os.path.dirname(os.path.abspath(__file__))
        
        self.db = InventarioDB()
        if self.db.conexion:
            self.db.cursor = self.db.conexion.cursor(dictionary=True, buffered=True)

        self.servicio = AsistenciaService(self.db)
        self.admin_actual = None
        self.aprendiz_actual = None
        self.instructor_actual = None 
        
        # Instancia del gestor de reportes
        self.reportes_manager = ReportesManager(self, self.db, self.servicio)
        # Instancia para cambio de password
        self.password_manager = PasswordManager(self, self.db)
        
        # Usar colores desde config
        self.sena_green = COLORES['SENA_GREEN']
        self.sena_dark = COLORES['SENA_DARK']
        self.bg_light = COLORES['BG_LIGHT']
        self.sena_orange = COLORES['SENA_ORANGE']
        
        # CACHÉ para mejorar rendimiento
        self._cache_fichas = None
        self._cache_fichas_timestamp = 0
        self._cache_aprendices = None
        self._cache_aprendices_timestamp = 0

        # Contenedor principal
        self.main_container = ctk.CTkFrame(self.root, fg_color=self.bg_light, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)
        
        # Crear frames independientes (sin pack aún)
        self.frames = {}
        for nombre in ['intro', 'terminal', 'login', 'inicio', 'aprendiz', 'admin']:
            self.frames[nombre] = ctk.CTkFrame(self.main_container, fg_color=self.bg_light, corner_radius=0)
        
        self.frames['intro'].configure(fg_color="transparent")  # La intro es transparente
        self.current_frame = None
        
        # Construir todas las pantallas
        self._construir_pantalla_intro()
        self._construir_pantalla_inicio()
        self._construir_pantalla_terminal()
        self._construir_pantalla_login()

        self.root.withdraw()
        self.root.after(150, self.lanzar_sistema)
        

    def lanzar_sistema(self):
        self.root.deiconify()
        self.root.state('zoomed')  # re-aplicar zoomed porque deiconify lo puede resetear
        self.root.resizable(True, True)
        self.animacion_entrada()

    def _ajustar_ventana_maximizada(self):
        pass
    

    def _construir_pantalla_intro(self):
        """Construye la pantalla de intro con animación"""
        frame = self.frames['intro']
        self.f_intro = ctk.CTkFrame(frame, fg_color="transparent")
        self.f_intro.place(relx=0.5, rely=0.4, anchor="center")
        self.lbl_siglas = ctk.CTkLabel(self.f_intro, text="C.R.S", font=("Segoe UI", 10, "bold"), text_color="#D1D1D1")
        self.lbl_siglas.pack()
        self.lbl_nombre = None  # Se creará dinámicamente
        self.size_actual = 10
    

    def _construir_pantalla_inicio(self):
        """Construye la pantalla de inicio con botones"""
        frame = self.frames['inicio']
        
        # Frame principal con gradiente visual
        f_main = ctk.CTkFrame(frame, fg_color=self.bg_light)
        f_main.pack(fill="both", expand=True)
        
        # Header superior con título principal
        f_header = ctk.CTkFrame(f_main, fg_color=self.sena_green, height=150)
        f_header.pack(fill="x")
        
        ctk.CTkLabel(f_header, text="C.R.S", font=("Segoe UI", 28, "bold"), 
                    text_color="white").pack(pady=(20, 5))
        ctk.CTkLabel(f_header, text="CHRONOS REGISTRY SYSTEM", font=("Segoe UI", 16, "bold"), 
                    text_color="white").pack(pady=(0, 10))
        ctk.CTkLabel(f_header, text="Sistema Integrado de Registro de Asistencia | High Softwares", 
                    font=("Segoe UI", 11), text_color="#E8F5E9").pack(pady=(0, 20))
        
        # Contenedor central
        f_center = ctk.CTkFrame(f_main, fg_color="transparent")
        f_center.pack(fill="both", expand=True, padx=50, pady=40)
        
        # Frame para opciones
        f_options = ctk.CTkFrame(f_center, fg_color=self.bg_light, corner_radius=25, 
                                border_width=2, border_color="#E0E0E0")
        f_options.pack(fill="both", expand=True, padx=50, pady=30)
        
        # Titulo de opciones
        ctk.CTkLabel(f_options, text="ACCESO AL SISTEMA", font=("Segoe UI", 24, "bold"), 
                    text_color=self.sena_dark).pack(pady=(40, 10))
        ctk.CTkLabel(f_options, text="Selecciona tu rol para continuar", font=("Segoe UI", 12), 
                    text_color="#888").pack(pady=(0, 40))
        
        # Contenedor de botones
        f_btns = ctk.CTkFrame(f_options, fg_color="transparent")
        f_btns.pack(pady=20)
        
        # Botón Terminal (Registro de Asistencia)
        btn_terminal = ctk.CTkButton(f_btns, text="REGISTRO DE ASISTENCIA", height=65, width=450, 
                                    font=("Segoe UI", 14, "bold"), fg_color=self.sena_green, 
                                    hover_color=self.sena_dark, command=self.mostrar_terminal)
        btn_terminal.pack(pady=15)
        ToolTip(btn_terminal, "Registra tu entrada y salida")
        
        # Botón Login Unificado
        btn_login = ctk.CTkButton(f_btns, text="LOGIN", height=65, width=450, 
                                 font=("Segoe UI", 14, "bold"), fg_color="#333", 
                                 hover_color="#111", command=self.mostrar_login_unificado)
        btn_login.pack(pady=15)
        ToolTip(btn_login, "Acceso al panel de administración o tu perfil")
        
        # Botón Salir
        btn_salir = ctk.CTkButton(f_btns, text="SALIR", height=65, width=450, 
                                 font=("Segoe UI", 14, "bold"), fg_color="#E74C3C", 
                                 hover_color="#C0392B", command=self.root.quit)
        btn_salir.pack(pady=15)
        ToolTip(btn_salir, "Cerrar la aplicación")
    

    def _construir_pantalla_terminal(self):
        """Construye la pantalla de registro de asistencia"""
        frame = self.frames['terminal']

        # Header superior
        head = ctk.CTkFrame(frame, height=_s(60, self.escala), corner_radius=0, fg_color=self.sena_green)
        head.pack(fill="x")
        head.pack_propagate(False)
        ctk.CTkButton(head, text="INICIO", width=_s(120, self.escala),
                     fg_color=self.sena_dark,
                     command=self.mostrar_inicio).pack(side="left", padx=20, pady=10)

        # Footer con logo — se define ANTES del body para que pack side=bottom funcione
        logo_size = _s(55, self.escala)
        f_footer = ctk.CTkFrame(frame, fg_color=self.bg_light, height=logo_size + 16)
        f_footer.pack(fill="x", side="bottom")
        f_footer.pack_propagate(False)
        try:
            ruta_logo = os.path.join(self.ruta_base, "images", "logosena.png")
            sena_logo_pil = Image.open(ruta_logo)
            sena_logo_pil = sena_logo_pil.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            sena_logo = ImageTk.PhotoImage(sena_logo_pil)
            lbl_logo = tk.Label(f_footer, image=sena_logo, bg=self.bg_light)
            lbl_logo.image = sena_logo
            lbl_logo.pack(side="right", padx=12, pady=8)
        except Exception as e:
            logging.warning(f"No se pudo cargar logo SENA: {e}")
            ctk.CTkLabel(f_footer, text="SENA", font=("Segoe UI", 11, "bold"),
                        text_color=self.sena_green).pack(side="right", padx=15)

        # Body principal — entre header y footer
        body = ctk.CTkFrame(frame, fg_color=self.bg_light)
        body.pack(fill="both", expand=True)

        # Centrador vertical
        f_center = ctk.CTkFrame(body, fg_color="transparent")
        f_center.pack(expand=True)

        # Tarjeta central
        f = ctk.CTkFrame(f_center, corner_radius=20, width=_s(620, self.escala),
                        fg_color=self.bg_light, border_width=2, border_color=self.sena_green)
        f.pack(padx=20, pady=_s(20, self.escala))
        f.pack_propagate(False) if False else None

        # Título
        f_title = ctk.CTkFrame(f, fg_color=self.sena_green, corner_radius=15)
        f_title.pack(fill="x", pady=_s(15, self.escala), padx=_s(15, self.escala))
        ctk.CTkLabel(f_title, text="REGISTRO DE ASISTENCIA",
                    font=("Segoe UI", _s(22, self.escala), "bold"),
                    text_color="white").pack(pady=_s(15, self.escala))
        ctk.CTkLabel(f_title, text="Chronos Registry System",
                    font=("Segoe UI", _s(10, self.escala)),
                    text_color="#E8F5E9").pack(pady=(0, _s(10, self.escala)))

        # Entrada de documento
        self.ent_doc_terminal = ctk.CTkEntry(
            f, font=("Segoe UI", _s(28, self.escala)),
            height=_s(70, self.escala), width=_s(520, self.escala),
            placeholder_text="N° Documento", justify="center",
            border_width=2, border_color=self.sena_green)
        self.ent_doc_terminal.pack(pady=_s(20, self.escala),
                                   padx=_s(25, self.escala))

        # Botones
        f_btns = ctk.CTkFrame(f, fg_color="transparent")
        f_btns.pack(padx=_s(25, self.escala), pady=_s(5, self.escala))

        ctk.CTkButton(f_btns, text="MARCAR ENTRADA",
                     font=("Segoe UI", _s(13, self.escala), "bold"),
                     height=_s(58, self.escala), width=_s(520, self.escala),
                     fg_color=self.sena_green,
                     hover_color=self.sena_dark,
                     command=lambda: self._procesar_asistencia("in")).pack(
                     pady=_s(8, self.escala))

        ctk.CTkButton(f_btns, text="MARCAR SALIDA",
                     font=("Segoe UI", _s(13, self.escala), "bold"),
                     height=_s(58, self.escala), width=_s(520, self.escala),
                     fg_color="#E67E22",
                     hover_color="#D35400",
                     command=lambda: self._procesar_asistencia("out")).pack(
                     pady=_s(8, self.escala))
    
    def _procesar_asistencia(self, tipo):
        """Procesa entrada o salida de asistencia"""
        exito, msg = self.servicio.registrar_entrada(self.ent_doc_terminal.get()) if tipo=="in" else self.servicio.registrar_salida(self.ent_doc_terminal.get())
        if exito: 
            messagebox.showinfo("C.R.S", msg)
            self.ent_doc_terminal.delete(0, tk.END)
            self.ent_doc_terminal.focus()
        else: 
            messagebox.showwarning("Atención", msg)
            self.ent_doc_terminal.delete(0, tk.END)
            self.ent_doc_terminal.focus()
    

    def _construir_pantalla_login(self):
        """Construye pantalla de login con diseño moderno dos columnas"""
        frame = self.frames['login']
        
        # Contenedor central
        f_main = ctk.CTkFrame(frame, fg_color="transparent")
        f_main.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Frame principal con dos columnas
        f_login = ctk.CTkFrame(f_main, fg_color="white", corner_radius=20)
        f_login.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ===== COLUMNA IZQUIERDA (Decorativa) - SENA ORANGE =====
        f_left = ctk.CTkFrame(f_login, fg_color=self.sena_orange, corner_radius=20)
        f_left.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        
        # Logo SENA
        f_icon = ctk.CTkFrame(f_left, fg_color="transparent")
        f_icon.pack(pady=(60, 40))
        
        try:
            ruta_logo = os.path.join(self.ruta_base, "images", "logosena.png")
            logo_pil = Image.open(ruta_logo)
            logo_pil = logo_pil.resize((140, 140), Image.Resampling.LANCZOS)
            logo_tk = ImageTk.PhotoImage(logo_pil)
            lbl_logo = tk.Label(f_icon, image=logo_tk, bg=self.sena_orange)
            lbl_logo.image = logo_tk
            lbl_logo.pack()
        except Exception as e:
            logging.warning(f"No se pudo cargar logo: {e}")
            ctk.CTkLabel(f_icon, text="SENA", font=("Segoe UI", 24, "bold"),
                        text_color="white").pack()
        
        # Texto
        ctk.CTkLabel(f_left, text="Login", font=("Segoe UI", 48, "bold"),
                    text_color="white").pack(padx=20)
        
        ctk.CTkLabel(f_left, 
                    text="Chronos Registry System\nC.R.S", 
                    font=("Segoe UI", 11),
                    text_color="#F0F0F0", justify="center").pack(pady=(30, 0))
        
        # ===== COLUMNA DERECHA (Formulario) =====
        f_right = ctk.CTkFrame(f_login, fg_color="white", corner_radius=0)
        f_right.pack(side="right", fill="both", expand=True, padx=40, pady=40)
        
        # Título
        ctk.CTkLabel(f_right, text="Inicio de sesión", 
                    font=("Segoe UI", 28, "bold"),
                    text_color=self.sena_dark).pack(anchor="w", pady=(0, 5))
        
        # Subtítulo
        ctk.CTkLabel(f_right, text="Inicia sesión con tu cuenta para continuar",
                    font=("Segoe UI", 11),
                    text_color="#888888").pack(anchor="w", pady=(0, 30))
        
        # Usuario
        ctk.CTkLabel(f_right, text="Usuario", font=("Segoe UI", 12, "bold"),
                    text_color=self.sena_orange).pack(anchor="w")
        self.ent_usuario = ctk.CTkEntry(f_right, placeholder_text="tu usuario",
                                       height=45, border_width=2,
                                       border_color=self.sena_orange,
                                       placeholder_text_color=self.sena_orange,
                                       fg_color="#F5F5F5")
        self.ent_usuario.pack(fill="x", pady=(5, 20))
        
        # Contraseña
        ctk.CTkLabel(f_right, text="Contraseña", font=("Segoe UI", 12, "bold"),
                    text_color=self.sena_orange).pack(anchor="w")
        self.ent_pass = ctk.CTkEntry(f_right, placeholder_text="Introduce tu contraseña",
                                    height=45, border_width=2,
                                    border_color=self.sena_orange, show="*",
                                    placeholder_text_color=self.sena_orange,
                                    fg_color=self.bg_light)
        self.ent_pass.pack(fill="x", pady=(5, 30))
        
        # Botón Entrar
        ctk.CTkButton(f_right, text="INICIAR SESIÓN", height=50,
                     font=("Segoe UI", 14, "bold"),
                     fg_color=self.sena_orange,
                     hover_color="#C25A0D",
                     text_color="white",
                     command=self._procesar_login).pack(fill="x", pady=(0, 15))
        
        # Botón Volver
        ctk.CTkButton(f_right, text="← Volver al Inicio", height=40,
                     font=("Segoe UI", 11),
                     fg_color="#E8E8E8",
                     text_color=self.sena_dark,
                     hover_color="#D0D0D0",
                     command=self.mostrar_inicio).pack(fill="x")
    

    def _procesar_login(self):
        """Procesa el login unificado (Admin, Instructor o Aprendiz)"""
        usuario = self.ent_usuario.get().strip()
        password = self.ent_pass.get()
        
        if not usuario or not password:
            messagebox.showwarning("Validación", "Usuario y contraseña son requeridos")
            return
        
        # Intentar como ADMINISTRADOR/INSTRUCTOR en usuarios_admin
        self.db.cursor.execute("SELECT * FROM usuarios_admin WHERE usuario=%s AND password=%s", 
                              (usuario, password))
        admin = self.db.cursor.fetchone()
        
        if admin:
            tipo_usuario = admin.get('tipo_usuario', 'admin')
            self.admin_actual = usuario
            try:
                self.db.registrar_auditoria(self.admin_actual, f"login {tipo_usuario}")
            except Exception as ex:
                logging.error(f"Error registrando auditoría (login {tipo_usuario})", exc_info=True)
            
            if tipo_usuario == 'instructor':
                self.mostrar_panel_instructor(admin)
            else:
                self.mostrar_panel_admin_ui()
            return
        
        # Intentar como INSTRUCTOR en tabla instructores
        instructor = self.servicio.login_instructor(usuario, password)
        
        if instructor:
            self.instructor_actual = usuario
            try:
                self.db.registrar_auditoria(self.instructor_actual, "login instructor")
            except Exception as ex:
                logging.error("Error registrando auditoría (login instructor)", exc_info=True)

            if instructor.get('cambio_pass') == 0 or password == 'sena123':
                # Mostrar ventana obligatoria y esperar a que se cierre
                # antes de abrir el panel del instructor
                self.actualizar_password_instructor_ventana(
                    instructor['documento'],
                    callback=lambda: self.mostrar_panel_instructor_ui(instructor)
                )
            else:
                self.mostrar_panel_instructor_ui(instructor)
            return
        
        # Intentar como APRENDIZ
        aprendiz = self.servicio.login_aprendiz(usuario, password)
        
        if aprendiz:
            self.aprendiz_actual = usuario
            if not self.db.registrar_auditoria(self.aprendiz_actual, "login aprendiz"):
                logging.warning("Advertencia: No se pudo registrar la auditoría de login.")
            if aprendiz.get('cambio_pass') == 0 or password == 'sena123': 
                self.actualizar_password_ventana(aprendiz['documento'])
            self.mostrar_panel_aprendiz(aprendiz)
            return
        
        # Si llegamos aquí, credenciales inválidas
        messagebox.showerror("Error", "Credenciales incorrectas")
        self.ent_pass.delete(0, tk.END)
        self.ent_usuario.focus()
    

    def show_frame(self, nombre_frame):
        """Muestra un frame y oculta los demás (instantáneo)"""
        for frame in self.frames.values():
            frame.pack_forget()
        if nombre_frame in self.frames:
            self.frames[nombre_frame].pack(fill="both", expand=True)
            self.current_frame = nombre_frame
        self.root.update_idletasks()
    
    def limpiar_pantalla(self):
        """Destruye todos los widgets de los frames admin y aprendiz para evitar superposición entre sesiones"""
        for nombre_frame in ['admin', 'aprendiz']:
            frame = self.frames.get(nombre_frame)
            if frame:
                for widget in frame.winfo_children():
                    try:
                        widget.destroy()
                    except Exception:
                        pass
    

    def animacion_entrada(self):
        """Inicia la pantalla de intro con animación"""
        self.show_frame('intro')
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
            # Destruir label anterior si existe (evita duplicados al re-entrar)
            if self.lbl_nombre is not None:
                try:
                    self.lbl_nombre.destroy()
                except Exception:
                    pass
                self.lbl_nombre = None

            # Crear el label del nombre cuando termina la animación del C.R.S
            self.lbl_nombre = ctk.CTkLabel(self.f_intro, text="CHRONOS REGISTRY SYSTEM", 
                                        font=("Segoe UI", 3, "bold"), text_color=self.sena_green)
            self.lbl_nombre.pack(pady=20)
            self.root.update()  # Forzar actualización visual
            self.efecto_pop(3)

    def efecto_pop(self, size):
        if size < 26:
            self.lbl_nombre.configure(font=("Segoe UI", size, "bold"), text_color=self.sena_orange)
            size += 2
            self.root.after(20, lambda: self.efecto_pop(size))
        else:
            self.root.after(2000, self.mostrar_terminal)


    def mostrar_inicio(self):
        """Muestra la pantalla de inicio"""
        self.show_frame('inicio')

    def mostrar_terminal(self):
        """Muestra la pantalla de registro de asistencia"""
        self.show_frame('terminal')
        self.ent_doc_terminal.focus()
        self.ent_doc_terminal.delete(0, tk.END)

    def mostrar_login_unificado(self):
        """Muestra la pantalla de login unificada"""
        self.show_frame('login')
        self.ent_usuario.delete(0, tk.END)
        self.ent_pass.delete(0, tk.END)
        self.ent_usuario.focus()


    def mostrar_panel_aprendiz(self, user):
        # ===== VISTA APRENDIZ =====
        self.show_frame('aprendiz')
        self.limpiar_pantalla()
        # header colorido para aprendiz
        head = ctk.CTkFrame(self.frames['aprendiz'], height=75, corner_radius=0, fg_color=self.sena_orange, border_width=0)
        head.pack(fill="x")
        def cerrar_aprendiz():
            if self.aprendiz_actual:
                try:
                    self.db.registrar_auditoria(self.aprendiz_actual, "logout aprendiz")
                except Exception as ex:
                    logging.error("Error registrando auditoría (logout aprendiz)", exc_info=True)
            self.aprendiz_actual = None
            self.mostrar_inicio()
        ctk.CTkButton(head, text="CERRAR SESIÓN", fg_color="#FF5252", hover_color="#D32F2F", text_color="white", font=("Segoe UI", 11, "bold"), command=cerrar_aprendiz).pack(side="left", padx=25)
        ctk.CTkLabel(head, text=f"Aprendiz: {user['nombre_completo']}", font=("Segoe UI", 15, "bold"), text_color="white").pack(side="right", padx=35)

        body = ctk.CTkFrame(self.frames['aprendiz'], fg_color="transparent")
        body.pack(fill="both", expand=True, padx=45, pady=25)

        # panel izquierdo: calendario moderno
        left = ctk.CTkFrame(body, corner_radius=20, fg_color=self.bg_light, border_width=1, border_color="#DDD")
        # reducir ancho relativo para que calendario quede más compacto
        left.place(relx=0, rely=0, relwidth=0.55, relheight=1)
        self.cal = CalendarioPersonalizado(left, self.sena_green, self.bg_light)
        # Hacer que ocupe todo el frame disponible
        self.cal.pack(fill="both", expand=True, padx=15, pady=15)

        # panel derecho: actividad del día
        right = ctk.CTkFrame(body, corner_radius=20, fg_color=self.bg_light, border_width=1, border_color="#DDD")
        right.place(relx=0.66, rely=0, relwidth=0.34, relheight=1)
        ctk.CTkLabel(right, text="Actividad del día", font=("Segoe UI", 18, "bold"), text_color=self.sena_dark).pack(pady=20)
        
        container_cards = ctk.CTkScrollableFrame(right, fg_color="transparent")
        container_cards.pack(fill="both", expand=True, padx=12, pady=8)

        def actualizar_cards(e=None):
            try:
                for w in container_cards.winfo_children():
                    w.destroy()
                fecha = self.cal.selection_get()
                regs = self.servicio.obtener_registros_dia(user['documento'], fecha)
                if not regs:
                    ctk.CTkLabel(container_cards, text="Sin actividad este día", text_color="#AAA").pack(pady=60)
                else:
                    for r in regs:
                        card = ctk.CTkFrame(container_cards, fg_color="#F8F9FA", corner_radius=12, border_width=1, border_color="#EEE")
                        card.pack(fill="x", pady=6, padx=8)
                        ctk.CTkLabel(card, text=f"Entrada: {r['fecha_registro'].strftime('%H:%M')}", font=("Segoe UI", 11)).pack(side="left", padx=15, pady=12)
                        if r['fecha_salida']:
                            ctk.CTkLabel(card, text=f"Salida: {r['fecha_salida'].strftime('%H:%M')}", font=("Segoe UI", 11), text_color="#E67E22").pack(side="right", padx=15)
                
                # Obtener todos los registros del mes para mostrar en calendario
                fecha_inicio = fecha.replace(day=1)
                # Calcular último día del mes
                if fecha.month == 12:
                    fecha_fin = fecha.replace(year=fecha.year + 1, month=1, day=1) - __import__('datetime').timedelta(days=1)
                else:
                    fecha_fin = fecha.replace(month=fecha.month + 1, day=1) - __import__('datetime').timedelta(days=1)
                
                registros_mes = self.servicio.obtener_registros_mes(user['documento'], fecha_inicio, fecha_fin)
                
                # Agrupar registros por día
                registros_por_dia = {}
                for r in registros_mes:
                    if r.get('fecha_registro'):
                        fecha_reg = r['fecha_registro'].date() if hasattr(r['fecha_registro'], 'date') else r['fecha_registro']
                        if fecha_reg not in registros_por_dia:
                            registros_por_dia[fecha_reg] = []
                        
                        horarios = {}
                        if hasattr(r['fecha_registro'], 'strftime'):
                            horarios['entrada'] = r['fecha_registro'].strftime('%H:%M')
                        if r.get('fecha_salida') and hasattr(r['fecha_salida'], 'strftime'):
                            horarios['salida'] = r['fecha_salida'].strftime('%H:%M')
                        
                        registros_por_dia[fecha_reg].append(horarios)
                
                self.cal.establecer_registros_mes(registros_por_dia)
            except Exception as ex:
                logging.error(f"Error en actualizar_cards: {ex}", exc_info=True)
                ctk.CTkLabel(container_cards, text=f"Error: {str(ex)[:50]}", text_color="red").pack(pady=60)
        
        self.cal.bind("<<CalendarSelected>>", actualizar_cards)
        actualizar_cards()


    def mostrar_panel_admin_ui(self):
        """Muestra el panel de administrador usando PantallaAdministrador"""
        self.limpiar_pantalla()
        self.show_frame('admin')
        PantallaAdministrador(self.frames['admin'], self.db, self.servicio, 
                             self.admin_actual, self)
    

    def crear_pestana_reportes(self, t_rep):
        """Delegar construcción de pestaña de reportes al gestor especializado"""
        self.reportes_manager.crear_pestana_reportes(t_rep)

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

    # ===== CAMBIO DE CONTRASEÑA =====        
    def actualizar_password_ventana(self, documento):
        """Delegar a PasswordManager"""
        self.password_manager.actualizar_password_ventana(documento)
    

    def mostrar_panel_instructor_ui(self, instructor):
        """Muestra el panel de instructor usando PantallaInstructor"""
        self.limpiar_pantalla()
        self.show_frame('admin')
        from admin_panel import PantallaInstructor
        PantallaInstructor(self.frames['admin'], self.db, self.servicio, 
                          instructor, self)
    
    def mostrar_panel_instructor(self, admin_data):
        """Muestra el panel de instructor cuando accede como admin/instructor"""
        self.limpiar_pantalla()
        self.show_frame('admin')
        from admin_panel import PantallaInstructor
        PantallaInstructor(self.frames['admin'], self.db, self.servicio, 
                          admin_data, self)
    
    def actualizar_password_instructor_ventana(self, documento, callback=None):
        """Actualizar contraseña para instructor — OBLIGATORIO, no se puede saltar"""
        ventana = tk.Toplevel(self.root)
        ventana.title("🔒 Cambio de Contraseña Obligatorio")
        ventana.geometry("420x380")
        ventana.resizable(False, False)

        # Bloquear cierre con la X: el instructor NO puede saltarse este paso
        def bloquear_cierre():
            messagebox.showwarning(
                "Obligatorio",
                "⚠️ Debes cambiar tu contraseña antes de continuar.\n"
                "No es posible omitir este paso."
            )
        ventana.protocol("WM_DELETE_WINDOW", bloquear_cierre)

        # Hacer la ventana modal (bloquea la ventana principal)
        ventana.grab_set()
        ventana.focus_force()

        # --- Encabezado ---
        f_head = ctk.CTkFrame(ventana, fg_color=COLORES['SENA_ORANGE'], corner_radius=0)
        f_head.pack(fill="x")
        ctk.CTkLabel(f_head, text="🔒 Cambio de Contraseña",
                    font=("Segoe UI", 15, "bold"),
                    text_color="white").pack(pady=14)

        # --- Aviso ---
        ctk.CTkLabel(ventana,
                    text="Por seguridad debes establecer una nueva contraseña\nantes de acceder al sistema.",
                    font=("Segoe UI", 11), text_color="#555",
                    justify="center").pack(pady=(12, 4))

        # --- Campos ---
        ctk.CTkLabel(ventana, text="Nueva Contraseña:",
                    font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=25, pady=(10, 2))
        ent_pass = ctk.CTkEntry(ventana, show="*", width=360, height=36,
                                placeholder_text="Mín. 8 chars, mayúscula, número y especial")
        ent_pass.pack(padx=25, pady=(0, 6))

        ctk.CTkLabel(ventana, text="Confirmar Contraseña:",
                    font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=25, pady=(6, 2))
        ent_pass2 = ctk.CTkEntry(ventana, show="*", width=360, height=36,
                                 placeholder_text="Repite la contraseña")
        ent_pass2.pack(padx=25, pady=(0, 6))

        lbl_error = ctk.CTkLabel(ventana, text="", font=("Segoe UI", 10),
                                 text_color="#E74C3C")
        lbl_error.pack(pady=(2, 0))

        def actualizar():
            pass1 = ent_pass.get().strip()
            pass2 = ent_pass2.get().strip()

            if not pass1 or not pass2:
                lbl_error.configure(text="⚠️ Ambos campos son obligatorios.")
                return
            if pass1 == "sena123":
                lbl_error.configure(text="⚠️ No puedes usar la contraseña por defecto.")
                return
            if pass1 != pass2:
                lbl_error.configure(text="⚠️ Las contraseñas no coinciden.")
                return

            valido, msg = Validador.validar_password(pass1)
            if not valido:
                lbl_error.configure(text=f"⚠️ {msg}")
                return

            try:
                hash_password = bcrypt.hashpw(pass1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                self.db.cursor.execute(
                    "UPDATE instructores SET password=%s, cambio_pass=1 WHERE documento=%s",
                    (hash_password, documento)
                )
                self.db.conexion.commit()
                ventana.grab_release()
                ventana.destroy()
                messagebox.showinfo("✅ Éxito", "Contraseña actualizada correctamente.\nBienvenido al sistema.")
                # Abrir el panel del instructor SOLO después de cerrar esta ventana
                if callback:
                    callback()
            except Exception as e:
                lbl_error.configure(text=f"Error: {str(e)[:80]}")

        # Permitir confirmar con Enter
        ent_pass2.bind("<Return>", lambda e: actualizar())

        ctk.CTkButton(ventana, text="✅ Confirmar y Entrar",
                     fg_color=COLORES['SENA_GREEN'], hover_color="#32900D",
                     font=("Segoe UI", 13, "bold"), height=42,
                     command=actualizar).pack(pady=16, padx=25, fill="x")
    

    def obtener_fichas_cached(self):
        """Retorna fichas con caché (TTL: 1 hora)"""
        import time
        ahora = time.time()
        if self._cache_fichas is None or (ahora - self._cache_fichas_timestamp) > CACHE['FICHAS_TTL']:
            self._cache_fichas = self.servicio.obtener_fichas()
            self._cache_fichas_timestamp = ahora
        return self._cache_fichas
    
    def obtener_aprendices_cached(self):
        """Retorna aprendices activos con caché (TTL: 30 min)"""
        import time
        ahora = time.time()
        if self._cache_aprendices is None or (ahora - self._cache_aprendices_timestamp) > CACHE['APRENDICES_TTL']:
            self.db.cursor.execute("SELECT documento, nombre_completo FROM estudiantes WHERE estado=1")
            self._cache_aprendices = self.db.cursor.fetchall()
            self._cache_aprendices_timestamp = ahora
        return self._cache_aprendices
    
    def limpiar_cache(self):
        """Limpia todos los cachés (útil después de cambios)"""
        self._cache_fichas = None
        self._cache_aprendices = None

if __name__ == "__main__":
    root = ctk.CTk() 
    app = SistemaHSGSCRS(root)
    root.mainloop()