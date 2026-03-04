# Presentación centrada en `main.py`

A continuación se presenta el contenido completo de `main.py` dividido en
bloques lógicos. Cada bloque se acompaña de una explicación clara.

## 1. Importaciones iniciales

```python
import tkinter as tk 
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from conexion import InventarioDB 
from tkcalendar import Calendar
import datetime
import re
import customtkinter as ctk 
import logging
from logging_config import configure_logging
```

Se importan:

- **tkinter/ttk**: biblioteca GUI.
- **pandas**: para operaciones sobre tablas cuando se exportan o importan hojas de cálculo.
- **InventarioDB** (de `conexion.py`): acceso a la base de datos.
- **Calendar** de `tkcalendar`: calendario visual.
- Módulos estándar `datetime` y `re`.
- **customtkinter (ctk)**: versión estilizada de tkinter utilizada en toda la interfaz.
- **logging** y la función `configure_logging` para inicializar los logs.

_Esta sección establece las dependencias del archivo y ya contiene una
nota histórica: usamos `ctk` porque queríamos un aspecto más moderno que el de
`tkinter` puro._

---

## 2. Clase `ToolTip`

```python
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
```

**Descripción bloque - Desglose detallado:**

#### Constructor (`__init__`)

El constructor recibe dos parámetros:

- **`widget`**: el componente de interfaz sobre el cual se asignará el tooltip (por ejemplo, un botón). Se almacena en `self.widget` para poder referenciarlo después.
- **`text`**: el mensaje de ayuda que aparecerá en el globo. Se almacena en `self.text`.

¿Por qué pasar ambos parámetros? Porque esta clase es **reutilizable**: cuando creamos un botón en cualquier parte del código, queremos asignarle un tooltip específico sin tener que reescribir toda la lógica. De este modo:
```python
btn_dash = ctk.CTkButton(..., command=self.mostrar_dashboard)
ToolTip(btn_dash, "Ver indicadores clave (KPIs)")  # Se pasa el botón y el texto
```

Finalmente, se inicializa `self.tipwindow = None` (no hay ventana aún) y se enlazan los eventos `<Enter>` y `<Leave>` del widget a los métodos `show_tip` e `hide_tip`.

#### Método `show_tip` – el guardián del tooltip

```python
if self.tipwindow or not self.text:
    return
```

Esta línea es **crítica** y merece explicación:

- **`self.tipwindow`**: si ya existe una ventana de tooltip abierta, no queremos abrir otra encima. Esto evita duplicados.
- **`not self.text`**: si el texto está vacío, no hay nada que mostrar, así que salimos sin hacer nada.

En otras palabras, esta línea dice: *"Si ya hay una ventana abierta O si no hay texto, detente aquí y no hagas nada más"*. Es un **mecanismo de protección** contra creaciones múltiples o innecesarias.

El resto del método calcula la posición relativa al cursor (sumando 10 píxeles a las coordenadas absolutas para que no tape el cursor) y crea un `Toplevel` sin bordes con una etiqueta amarilla.

#### Método `hide_tip` – cerrar limpiamente

Cuando el cursor sale del widget:
1. Se guarda una referencia a la ventana actual.
2. Se establece `self.tipwindow = None` (la marcamos como inexistente).
3. Si la referencia es válida, se destruye.

_Se utiliza en muchos botones administrativos (como el botón "📈 DASHBOARD") para dar pistas al usuario._

---

## 3. Configuración global de `ctk` y logging

```python
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("green")

# Configurar logging centralizado
configure_logging()
```

_Módulo `customtkinter` requiere establecer un modo de apariencia y un tema de
colores_; aquí elegimos modo claro y verde. A continuación llamamos a
`configure_logging()` para que cualquier mensaje de `logging` se dirija a
consola/archivo según lo definido en `logging_config.py`.

---

## 4. Clase principal `SistemaHSGSCRS`

La mayor parte del archivo está dentro de esta clase. A continuación desglosamos
sus sub-bloques.

### 4.1. Inicialización (`__init__`)

```python
class SistemaHSGSCRS:
    def __init__(self, root):
        self.root = root
        self.root.title("C.R.S - Chronos Registry System")
        
        self.db = InventarioDB()
        if self.db.conexion:
            self.db.cursor = self.db.conexion.cursor(dictionary=True, buffered=True)

        self.servicio = AsistenciaService(self.db)
        self.admin_actual = None
        self.aprendiz_actual = None 
        self.sena_green = "#39A900"
        self.sena_dark = "#2D5A27"
        self.bg_light = "#E2E2E2"

        self.main_container = ctk.CTkFrame(self.root, fg_color=self.bg_light, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        self.root.withdraw()
        self.root.after(100, self.lanzar_sistema)
```

**Qué hace:**

- Guarda `root` y configura título de la ventana principal.
- Crea objeto `InventarioDB`; si la conexión fue exitosa se prepara el cursor.
- Instancia el servicio de lógica `AsistenciaService`.
- Inicializa variables de estado para el administrador y el aprendiz actual,
  así como colores reutilizados.
- Construye el `main_container` (frame raíz donde se montarán todas las vistas).
- Oculta la ventana inicialmente y programa la llamada a `lanzar_sistema` unos
  milisegundos después para iniciar la animación de bienvenida.

### 4.2. Helpers de navegación y animación

Métodos cortos que limpian la pantalla y generan la animación inicial:

- `limpiar_pantalla`: destruye todos los widgets hijos del contenedor.
- `animacion_entrada`, `animar_ciclo`, `efecto_pop`: dibujan el texto "C.R.S"
  que crece de tamaño con colores animados y luego muestran el nombre completo.
  Esta pantalla aparece al iniciar y luego llama a `mostrar_inicio`.

_La animación es puramente estética; sirve para demostrar habilidades con
`t kinter` y temporizadores._

### 4.3. Primera vista: pantalla de inicio

```python
    def mostrar_inicio(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=500, height=550, corner_radius=20,
                         fg_color=self.bg_light, border_width=2, border_color="#E0E0E0")
        f.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(f, text="GATEWAY C.R.S", font=("Segoe UI", 32, "bold"), text_color=self.sena_dark).pack(pady=(50, 5))
        ctk.CTkLabel(f, text="Chronos Registry System | High Softwares", font=("Segoe UI", 13), text_color="#888").pack(pady=(0, 40))

        ctk.CTkButton(f, text="TERMINAL APRENDICES", height=55, width=350, corner_radius=10,
                       command=self.mostrar_terminal).pack(pady=10, padx=20)
        ctk.CTkButton(f, text="PANEL ADMINISTRATIVO", height=55, width=350, corner_radius=10,
                       fg_color="#333", hover_color="#1a1a1a", command=self.mostrar_login).pack(pady=10, padx=20)
        ctk.CTkButton(f, text="MI PERFIL (APRENDIZ)", height=55, width=350, corner_radius=10,
                       fg_color="transparent", text_color=self.sena_green, border_width=2,
                       border_color=self.sena_green, hover_color="#E8F5E9", command=self.login_aprendiz_view).pack(pady=10, padx=20)
```

**Descripción:** crea un panel central con tres botones principales: terminal
para marcación, acceso administrativo y perfil de aprendiz. Se usa un `CTkFrame`
con estilo, etiquetas y botones con comandos ligados a métodos de la clase.

### 4.4. Terminal de asistencia (para aprendices)

Método `mostrar_terminal` construye la vista donde se introduce el documento
en una entrada grande; botones de "MARCAR ENTRADA" y "MARCAR SALIDA" llaman
al servicio correspondiente. Usa `messagebox` para mostrar éxito o advertencias.

```python
    def mostrar_terminal(self):
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=70, corner_radius=0, fg_color=self.sena_green); head.pack(fill="x")
        ctk.CTkButton(head, text="⬅ VOLVER", width=140, fg_color=self.sena_dark, command=self.mostrar_inicio).pack(side="left", padx=25, pady=15)
        f = ctk.CTkFrame(self.main_container, width=650, height=550, corner_radius=25, fg_color=self.bg_light, border_width=1, border_color="#DDD"); f.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f, text="REGISTRO DE ASISTENCIA", font=("Segoe UI", 26, "bold")).pack(pady=35)
        ent_doc = ctk.CTkEntry(f, font=("Segoe UI", 30), width=480, height=80, placeholder_text="N° Documento", justify="center"); ent_doc.pack(pady=25); ent_doc.focus()

        def procesar(tipo):
            exito, msg = self.servicio.registrar_entrada(ent_doc.get()) if tipo=="in" else self.servicio.registrar_salida(ent_doc.get())
            if exito: messagebox.showinfo("C.R.S", msg); ent_doc.delete(0, tk.END)
            else: messagebox.showwarning("Atención", msg)

        ctk.CTkButton(f, text=" MARCAR ENTRADA", font=("bold", 16), height=65, width=450, command=lambda:procesar("in")).pack(pady=10)
        ctk.CTkButton(f, text=" MARCAR SALIDA", font=("bold", 16), height=65, width=450, fg_color="#E67E22", hover_color="#D35400", command=lambda:procesar("out")).pack(pady=10)
```

### 4.5. Login y panel de aprendiz

`login_aprendiz_view` muestra campos de documento y contraseña. Si el login es
correcto, guarda `self.aprendiz_actual`, registra auditoría, fuerza cambio de
contraseña si es necesario y abre `mostrar_panel_aprendiz`.

```python
    def login_aprendiz_view(self):
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=450, height=480, corner_radius=25,
                         fg_color=self.bg_light, border_width=2, border_color="#DDD")
        f.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(f, text="ACCESO APRENDIZ", font=("Segoe UI", 24, "bold")).pack(pady=35)
        u_ent = ctk.CTkEntry(f, width=320, height=50, placeholder_text="Documento"); u_ent.pack(pady=12, padx=20)
        p_ent = ctk.CTkEntry(f, width=320, height=50, placeholder_text="Contraseña", show="*"); p_ent.pack(pady=12, padx=20)
        
        ctk.CTkButton(f, text="INGRESAR", width=320, height=55, command=lambda:self.entrar(u_ent, p_ent)).pack(pady=35, padx=20)
        ctk.CTkButton(f, text="VOLVER", fg_color="transparent", text_color="gray", command=self.mostrar_inicio).pack(padx=20)
        
        def entrar(u_ent, p_ent):
            user = self.servicio.login_aprendiz(u_ent.get(), p_ent.get())
            if user:
                self.aprendiz_actual = u_ent.get()
                if not self.db.registrar_auditoria(self.aprendiz_actual, "login aprendiz"):
                    logging.warning("Advertencia: No se pudo registrar la auditoría de login.")
                if user.get('cambio_pass') == 0 or p_ent.get() == 'sena123': self.actualizar_password_ventana(user['documento'])
                self.mostrar_panel_aprendiz(user)
            else: messagebox.showerror("Error", "Credenciales Incorrectas")
```

`mostrar_panel_aprendiz` muestra calendario a la izquierda y tarjetas de
actividades del día a la derecha. Incluye botón de cerrar sesión con auditoría.

### 4.6. Interfaz de administración

`mostrar_login` para administradores y `mostrar_panel_admin_ui` contienen la
mayor parte de la lógica administrativa. Dentro de `mostrar_panel_admin_ui` se
configuran pestañas para:

- **Historial**: tabla con últimos 100 registros.
- **Gestión**: búsqueda y envío de aprendices a papelera.
- **Registro**: formulario para crear un aprendiz con ficha, importar Excel.
- **Papelera**: restaurar o eliminar definitivamente.
- **Reportes**: filtros, generación y exportación de estadísticas.

El código crea frames, treeviews, botones, y define numerosas funciones
internas (`refresh_hist`, `filtrar`, `mover_seleccion`, `save`, `restaurar`,
`eliminar`) que realizan consultas SQL y llaman a `self.servicio`. En cada caso se
intenta registrar auditoría y se captura cualquier excepción con `logging.error`.

_Un fragmento clave de periodo de reportes se muestra más adelante en la sección
del reporte._

### 4.7. Reportes y exportaciones

- `crear_pestana_reportes` construye los controles: radios para modo, combobox
  dinámico, segmento de tiempo (Día/Semana/Mes), calendario/selección de
  semanas/meses, botones generar y exportar, plus el canvas donde se dibuja el
  gráfico.
- `exportar_reporte` genera un archivo PDF o Excel con las métricas del último
  reporte. Usa `pandas` para `.xlsx` y `reportlab` para PDF.

El código también guarda `last_report_items` y `last_report_params` para
permanecer disponible para exportación.

### 4.8. Dashboard KPI

```python
    def mostrar_dashboard(self):
        """Ventana con KPIs en 3 columnas: Hoy, Semana, Mes.
        
        Detecta automáticamente:
        - Hoy: solo la fecha seleccionada
        - Semana: lunes a viernes (detecta la semana laboral que contiene la fecha)
        - Mes: primer a último día del mes
        """
        v = tk.Toplevel(self.root)
        v.title("Dashboard CRS")
        v.geometry("1000x550")
        v.config(bg=self.bg_light)

        # contenedor principal
        main_frame = tk.Frame(v, bg=self.bg_light)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # selector de fecha
        lbl_sel = tk.Label(main_frame, text="Fecha de referencia:", font=("Segoe UI", 11), bg=self.bg_light)
        lbl_sel.pack(pady=(0, 5))
        cal = Calendar(main_frame, selectmode='day', locale='es_ES',
                       background=self.sena_green, headersbackground=self.sena_dark)
        cal.pack()

        def actualizar_dashboard(e=None):
            # borrar KPIs previos (mantener selector)
            for w in main_frame.winfo_children():
                if w not in (lbl_sel, cal):
                    w.destroy()
            try:
                hoy = cal.selection_get()
                
                # Calcular rangos
                # HOY: solo esa fecha
                fecha_hoy = hoy
                
                # SEMANA: lunes a viernes de esa semana
                dias_desde_lunes = hoy.weekday()  # 0=lunes, 4=viernes, 5=sábado, 6=domingo
                lunes = hoy - datetime.timedelta(days=dias_desde_lunes)
                viernes = lunes + datetime.timedelta(days=4)
                
                # MES: primer día a último día
                mes_ini = hoy.replace(day=1)
                import calendar as _cal
                ultimo_dia = _cal.monthrange(hoy.year, hoy.month)[1]
                mes_fin = hoy.replace(day=ultimo_dia)
                
                # Obtener datos
                datos_dia = self.servicio.obtener_metricas_reporte_multiple([], "Ficha", "Día", fecha_hoy)
                datos_sem = self.servicio.obtener_metricas_reporte_multiple([], "Ficha", "Semana", lunes)
                datos_mes = self.servicio.obtener_metricas_reporte_multiple([], "Ficha", "Mes", mes_ini)

                # Contenedor de columnas
                cols_frame = tk.Frame(main_frame, bg=self.bg_light)
                cols_frame.pack(fill="both", expand=True, padx=10, pady=10)

                # Helper para crear una columna
                def crear_columna(parent, titulo, fecha_inicio, fecha_fin, datos, emoji):
                    col = tk.Frame(parent, bg="white", relief="solid", borderwidth=2)
                    col.pack(side="left", fill="both", expand=True, padx=5)
                    
                    # Encabezado
                    header = tk.Frame(col, bg=self.sena_green)
                    header.pack(fill="x")
                    
                    lbl_titulo = tk.Label(header, text=f"{emoji} {titulo}", 
                                         font=("Segoe UI", 13, "bold"), 
                                         bg=self.sena_green, fg="white")
                    lbl_titulo.pack(pady=8)
                    
                    # Rango de fechas
                    if fecha_inicio == fecha_fin:
                        rango_txt = fecha_inicio.strftime("%d/%m/%Y")
                    else:
                        rango_txt = f"{fecha_inicio.strftime('%d/%m')} - {fecha_fin.strftime('%d/%m/%Y')}"
                    
                    lbl_rango = tk.Label(col, text=rango_txt, 
                                        font=("Segoe UI", 10), 
                                        bg="white", fg="#666")
                    lbl_rango.pack(pady=5)
                    
                    # Separador
                    sep = tk.Frame(col, bg="#E0E0E0", height=1)
                    sep.pack(fill="x", padx=10)
                    
                    # Datos
                    content = tk.Frame(col, bg="white")
                    content.pack(fill="both", expand=True, padx=12, pady=12)
                    
                    def dato_linea(label, valor, color="black"):
                        f = tk.Frame(content, bg="white")
                        f.pack(fill="x", pady=6)
                        
                        lbl_l = tk.Label(f, text=label, font=("Segoe UI", 10), 
                                        bg="white", fg="#555")
                        lbl_l.pack(side="left")
                        
                        lbl_v = tk.Label(f, text=str(valor), font=("Segoe UI", 11, "bold"), 
                                        bg="white", fg=color)
                        lbl_v.pack(side="right")
                    
                    asist = datos.get('total_asistencias', 0)
                    faltas = datos.get('faltas', 0)
                    retardos = datos.get('retardos', 0)
                    
                    # Color según asistencia (rojo si poca, verde si buena)
                    color_asist = "#39A900" if asist >= 10 else "#E74C3C"
                    
                    dato_linea("Asistencias:", asist, color_asist)
                    dato_linea("Faltas:", faltas, "#FF9800" if faltas > 2 else "#555")
                    dato_linea("Retardos:", retardos, "#E67E22" if retardos > 0 else "#555")
                
                # Crear 3 columnas
                crear_columna(cols_frame, "HOY", fecha_hoy, fecha_hoy, datos_dia, "📅")
                crear_columna(cols_frame, "SEMANA", lunes, viernes, datos_sem, "📊")
                crear_columna(cols_frame, "MES", mes_ini, mes_fin, datos_mes, "📈")
                
                # Botón cerrar
                btn_frame = tk.Frame(main_frame, bg=self.bg_light)
                btn_frame.pack(pady=10)
                ctk.CTkButton(btn_frame, text="Cerrar", command=v.destroy).pack()
                
            except Exception as ex:
                tk.Label(main_frame, text=f"Error: {ex}",
                         fg="red", bg=self.bg_light, font=("Segoe UI", 10)).pack(pady=20)

        cal.bind("<<CalendarSelected>>", actualizar_dashboard)
        # inicializar con fecha de hoy
        cal.selection_set(datetime.date.today())
        actualizar_dashboard()
```

**Explicación:** la ventana emergente muestra tres columnas con KPIs.
Se calcula el rango de fechas en base a la fecha seleccionada y se llama al
servicio para obtener métricas. Un helper local `crear_columna` construye la
sección visual de cada columna con colores y texto adaptativo. Se incluye un
`try` para mostrar un mensaje de error en caso de excepción.

### 4.9. Selección y generación de reportes detallados

Los métodos `cambiar_modo_reporte`, `_filtrar_combo`, `mostrar_selector_rango`,
`agregar_item_reporte`, `limpiar_lista_reporte` y `lanzar_reporte` constituyen la
lógica de la pestaña de reportes.

- `cambiar_modo_reporte`: alterna entre filtrar por fichas o aprendices, carga
  los datos en el combobox y habilita la escritura para búsqueda.
- `_filtrar_combo`: filtra las opciones mientras el usuario escribe.
- `mostrar_selector_rango`: según 