"""
Módulo UIHelper
Utilidades para construcción de interfaces de usuario
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from config import COLORES, FUENTES
from tkcalendar import Calendar


class UIHelper:
    """Utilidades para reducir código repetitivo en UI"""

    @staticmethod
    def crear_frame_con_header(parent, titulo, subtitulo=None, height=75):
        """Crea un frame con header estilizado"""
        frame = ctk.CTkFrame(parent, height=height, corner_radius=0,
                           fg_color=COLORES['SENA_DARK'])
        frame.pack(fill="x")

        ctk.CTkLabel(frame, text=titulo, font=("Segoe UI", 15, "bold"),
                    text_color="white").pack(pady=(20, 5))
        if subtitulo:
            ctk.CTkLabel(frame, text=subtitulo, font=("Segoe UI", 11),
                        text_color="#E8F5E9").pack(pady=(0, 15))
        return frame

    @staticmethod
    def crear_boton_accion(parent, text, command, fg_color=None, **kwargs):
        """Crea botón con colores por defecto del sistema"""
        fg_color = fg_color or COLORES['SENA_GREEN']
        return ctk.CTkButton(parent, text=text, command=command,
                           fg_color=fg_color, **kwargs)

    @staticmethod
    def crear_calendario(parent, **kwargs):
        """Crea calendario con colores SENA por defecto"""
        return Calendar(parent, locale='es_ES',
                       background=COLORES['SENA_GREEN'],
                       headersbackground=COLORES['SENA_DARK'], **kwargs)

    @staticmethod
    def mostrar_mensaje(tipo, titulo, mensaje):
        """Wrapper para mostrar mensajes con título consistente"""
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)