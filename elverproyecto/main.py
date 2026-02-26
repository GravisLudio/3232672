###Explicacion basica parte 1: Estas son las importaciones de las librerias necesarias y las conexion a los de mas archivos del proyecto.
"""Importacion de las librerias necesarias y conexion con otros archivos del proyecto."""


import tkinter as tk 
"""Tkinter controla las interfaz grafica principal del proyecto, es la base de toda la experiencia visual."""


from tkinter import ttk, messagebox, filedialog
"""ttk provee los widgets para correcta funcionalidad del proyecto, msgbox para elertar, filedialog para los archivo cvs, excel, etc."""


import pandas as pd
"""Pandas la esencial para lecturas de archivos y manejo de los archivos que se quieran cargar al programa"""


from conexion import InventarioDB 
"""Haceos la conexion de conexion, traemos la clase InventarioDB para poder usar las funciones alli anidadas
y asi poder conectar con la bace de datos para hacer consultas o manupilar la DB"""


from tkcalendar import Calendar
"""tkcalendar otra libreria de tkinter que nos permite usar un calendario dentro de la interfaz graficas
la traemos por la necesidad de mostrar el calendario en el perfil del aprendiz y ver su actividad segun lo necesitado"""


import datetime
"""Datetime es una libreria estandar de python nos ayuda usar fechas y horas, 
en el proyecto se usar para los registros de aprendices."""


import re
"""re lib de python para expresiones regulares, en el proyecto se usa para validar contraseñas
y otros campos que requieran validacion."""


import customtkinter as ctk 
"""ctk libreria de terceros, mucho mejor que tkinter para tener una interfaz mas 
comoda a la vista y lo que nos hemos venido acostumbrando."""


from logica import AsistenciaService 
"""Traemos la logica, por ende usamos asistenciaservice, para usar las funciones como
registrar entradas, salidas, login, y demas, incluso las que estan para los administradores."""
###hasta aqui la explicacion parte 1 

###Explicacion parte 2
"""Aqui definimos definimos dos cosas, color por defecto y el modo de apareincia, set appearance mode
es para definir un modo de apariencia, y colo theme define los colores del tema.
podemos hacer esto gracias a haber importado customtkinter."""
###Explicacion parte 2
# Configuración Visual Estilo Moderno
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("green") 
"""Primer uso de ctk, configuramos la apariencia general del programa
y el tema de los colores, en este caso usamos verde"""
###Fin de la explicacion parte 2


###Explicacion parte 3
"""En toda esta seccion tenemos la creacion de la clase principal de la interfaz del programa
 usamos __init__, como sabemos init es un constructor de clases,
 si quisieramos un ejemplo basico, init es lo que se ejecuta cuando creamos el objeto
 es decir cuando llamemos a sistemaHSGSCRS(), no estas ejecutando en si el programa, sino el init,
 
 usamos self para referenciar a la clase, es decir cuando queremos usar objetos de la clase, usaremos al inicio self
 
 root es la ventana principal del programa, inicia vacia y vamos poniendo todo adentro.
 luego, le asiganmos a una variable llamada root, el valor de root que es la ventana principal, si un programador se confunde
 puede usar cualquier nombre, no es obligatorio usar root en la variable, solo es necesaria en la asignacion.
 
 
 gracias a eso, luego podemos asignarle el titulo a la ventana.
 
 Luego hacemos la conexion con la base de datos gracias a la importacion de en from conexion import inventariodb
 lo que hicimos para entenderlo mejor fue decirle a python, la variable db, sera la clase inventariodb de conexion.py
 
 luego verifimos, la conexion, si funciona:
 
 creamos un cursor(un cursor es objeto que permite ejecutar consultas en la base de datos, otros usos pueden ser
 recorrer resultados, hacer transacciones, cursor es basicamente una herramienta de interaccion de python)
 le decimos que use dic para traer los datos ordenados y buffered para evitar problemas con consultas multiples o seguidas."""

"""Una vez terminada la conexion, conectamos con la logica, gracias a la importacion from logica import asistenciaservice.

le decimos a python que no hay ningun aprendiz ni admin logueado asi cada que se ejecute el programa nos aseguramos de una sesion limpia

Terminado eso, simplificamos el uso de los colores base del programa creando 3 variables
sena green
sena dark
bg_light

gracias a esto cuando necesitemos un color que se repite mucho durante el programa solo debemos usar self.variable_color

terminamos con 4 cosas

contendor maestro donde tendremos todas las pantallas del programa

es un frame ctk que metemos en root le decimos que tome todo el especio con fill both y expand true

Y por ultimo ocultamos la ventana principal root, y le decimos que espere 100 ms para empezar con la animacion
"""
###Explicacion parte 3
class SistemaHSGSCRS:
    """El plano principal de este proyecto, sencillamente aqui ira toda la logica para la interfaz del programa
    conectando con logica y conexion para que el programa funciones."""
    def __init__(self, root):
        """Definimos el constructor principal del proyecto,
        aqui se establece la ventana principal, se conecta con la base de datos, 
        se inicializan variables globales o de logica, y lanzamos la animacion de entrada del programa."""

        

        
        self.root = root
        self.root.title("C.R.S - Chronos Registry System")
        """Primer uso de root, como dijimos es la ventana principal del programa,
        lo que queremos decir es que al usar root, y luego root.title, le estamos diciendo
        "Python a esta ventana le llamadas XYX" asi saldra en la barra de tareas y asi saldra en la barra superior"""

        
        
        # Inicializar base de datos
        self.db = InventarioDB()
        """aun no conocemos a self.db, pero si a InventarioDB que esta en la zona de las librerias,
        sencillamente le estamos diciendo a python, cuando diga self.db, llama a InventarioDB, ya que lo usare."""
        if self.db.conexion:
            """Aqui le estamos diciendo a python, si conexion funcion, o esta en conexion.py, entonces haremos esto"""
            self.db.cursor = self.db.conexion.cursor(dictionary=True, buffered=True)
            """Aca le decimos a python que use un cursor para hacer consultas, usando dictionary
            para que nso traiga los datos como diccioanrio y no perdamos tiempo intetnando saber que tiene cada tupla
            buffered evitar haciendo varias consultas o seguidas."""

        self.servicio = AsistenciaService(self.db)
        """aqui vemos a logica, donde?, claro aqui le estamos diciendo a python, "Oye python, cuando use self.servicio,
        quiero que ya que te pedi importarlo, usaras asistenciaservice, traeras de alli, self.db, y lo guardas en servicio
        asi basta con usar self.servicio, o self.servicio.variable...etc, para usar lo que tenemos dentro de logica.py"""
        self.admin_actual = None
        self.aprendiz_actual = None 
        """Aqui solo le estamos diciendo que no hay ningun usuario logueado para que al entrar al programa no haya
        confuciones, inicias el programa, entonces debes logearte."""
        self.sena_green = "#39A900"
        self.sena_dark = "#2D5A27"
        """Aqui definimos colores con un nombre espeficico para no recordar los hexa
        cada que querramos usar el color base de la administracion, ya sabemos que tenemos el sena green y dark."""
        
        # color de fondo general (gris claro, menos brillante que blanco)
        self.bg_light = "#E2E2E2"  # usado por contenedores principales
        """Definimos otro color, bg_light, no debemos confundirnos pensando que es una funcion o algo por el estilo
        al igual que sena_dark, bg_light es solo el nombre que le damos al color para usar en los fondos y estan mejor organizados."""


        # Contenedor Maestro
        self.main_container = ctk.CTkFrame(self.root, fg_color=self.bg_light, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)
        """Aqui vemos el primer uso de ctk, lo nombramos main container, y llamamos a ctk, 
        de ctk usamos ctkframe, le decimos que meteremos dentro de la ventana principal, la cual llamamos mas arriba root, 
        vemos el primer uso del color de fondo, esto podriamos cambiarlo por un hexa deximal, pero ya tenemos un color para los fondos
        definido, aqui si tenemos que diferencias, como ves no estamos nombrando nada aqui nada, sencillamente
        fg_color no podemos cambiarlo, ctkframe reconoce esto como el color de fondo, igual que corner_radius
        no podrias decir algo como radio_esquinas, o color_fondo, ctkframe no sabe que es."""
        """Pack es un metodo de tkinter para organizar widgets,
        fill both hace que el frame se expanda en root en y y x, expand true toma todo el espacio dentro de root."""

        # Forzar ventana maximizada con retraso técnico
        self.root.withdraw() 
        self.root.after(100, self.lanzar_sistema)
        """Aqui usamos withdraw, withdraw es una funcion de tkinter, que oculta la ventana,
        como estamos ocultado a root, no veremos nada al iniciar
        es basicamente una forma de hacer una animacion con recursos tecnicos,  imaginalo como cuando en una escana
        de bajo presupuesto, tapan el lente y luego lo destapan, es lo mismo aqui, after es una funcion que crea un delay
        por defecto dice milisegundos, la estructura es (delay en ms, funcion a ejecutar), en este caso, la funcion aun no esta definida
        pero es lanzar_sistemas, no debemos olvidar que podemos hacer todo en cualquier orden, solo debemos respetar identacion
        mientras entemos dentro de la clase, podemos llamar una funcion que esta definida incluso 8000 lineas mas abajo."""
        ####Fin de la explicacion parte 3
        
        
        ###Explicacion parte 4
        """Definomos la parte inicial del programa,
        usamos deiconify, contrario a withdraw, """
    def lanzar_sistema(self):
        
        """Aqui definimos a lanzar_sistema, self es la referencia de la clase asi sabemos que lanzar_sistema
        es de la clase y no global."""
        """Activa la ventana y dispara la animación inicial."""
        self.root.deiconify() 
        """aqui deiconify es sencillamente lo contrario a withdraw, mostrara la ventana, nada mas que explicar."""
        self.root.state('zoomed') 
        """Otro efecto tecnico, zoomed, hace que la ventana se abra maximizada, por defecto cuando abrimos una
        ventana tenemos el efecto de que la ventana pasa de un tamaño pequeño a su tamaño maximizado, por ende zoomed
        cre una sensacion de que el programa realmente tiene animaciones."""
        self.animacion_entrada_pro()
        """Llamamos el resto de la animacion que esta definido mas abajo."""
        

    def limpiar_pantalla(self):
        """Elimina todos los widgets del contenedor maestro."""
        for widget in self.main_container.winfo_children():
            """usamos un ciclo for para dentro del main container, eliminemos todos los widgets, 
            winfo_children, funcion para obtener todos los widgets hijos de main container,
            luego usamos widget.destroy, para eliminar todos los widgets obtenidos con winfo_children."""
            widget.destroy()

    # --- ANIMACIÓN: EFECTO ENFOQUE + POP ---
    def animacion_entrada_pro(self):
        """Inicia la animación de bienvenida con el logo C.R.S."""
        self.limpiar_pantalla()
        """Llamamos a el limpiador de pantallas, ya sabemos que hace."""
        self.f_intro = ctk.CTkFrame(self.main_container, fg_color="transparent")
        """Definimos una variable dentro de animacion de eentrada pro, es un frame transparente, la estructura es
        (contendor donde ira, color de fondo), transparente para que no se vea, solo veremos las letras."""
        self.f_intro.place(relx=0.5, rely=0.5, anchor="center")
        """Aqui le decimos con place, donde va a ir, rel signifca relativo, usamos x y y, y facil de entender
        0.5=50%, como le estamos diciendo que x y y, seria la mitad de f_intro. anchor center.
        se centrara en el frame."""
        self.lbl_siglas = ctk.CTkLabel(self.f_intro, text="C.R.S", font=("Segoe UI", 10, "bold"), text_color="#D1D1D1")
        """La magia inicial, aqui es donde definimos ese texto que acomodamosa tras, en este caso CRS, 
        definimos la variable, le decimos que usaremos una funcion de ctk, ctklabel, y la estructura es
        (contenedor donde va, texto a poner, tipo de letra(familialetra,tamaño,estilo,etc),color texto),
        usamos un color gris para que tengamos ese efecto de enfoque, aunque por la velocidad final no se nota tanto."""
        self.lbl_siglas.pack()
        """Ya sabemos que pack organiza el widget en self, en este caso self para animacion d entrada pro."""
        self.size_actual = 10
        """Sabemos que queremos que el texto crezca por lo que definimos un tamaño pequeño inicial."""
        self.root.after(500, self.animar_ciclo)
        """de nuevo nuestro rey de animaciones after, ya lo conocemos
        (delay en ms, funcion a ejecutar), aca llamos la funcion que hara crecer el texto"""

    def animar_ciclo(self):
        """Bucle interno que agranda el texto de las siglas con easing suave."""
        if self.size_actual < 120:
            """Inicio de la "animacion",
            le decinmos a la definicion que si size actual es menor a 120, entonces..."""
            target = 120
            """Queremos que sea 120"""
            diff = target - self.size_actual
            """Creamos una variable para saber la diferencia,
            es una forma de ir aumentando el tamaño de forma gradual."""
            step = max(1, diff // 10)
            """Aqui indicamos como ira creciendo nuestro texto.
            la estructura de max es primero el valor minimo que que queremos que crezca, y luego un valor calculado,
            este tomaara uno de los dos, asi que si dif dividio en 10 da 0.5 entonces terminara con 1."""
            self.size_actual += step
            """hacemos crecer el texto, con size actual, y le sumamos el paso."""
            if self.size_actual > 60:
                """Aca sencillamente indicamos que si el tamaño ya llego a 60"""
                self.lbl_siglas.configure(text_color=self.sena_dark)
                """Cambiara el color de las letras a sena dark"""
            elif self.size_actual > 30:
                """de lo contrario si apenas va pasando por 30"""
                self.lbl_siglas.configure(text_color="#888888")
                """Sera un gris oscuro"""
            self.lbl_siglas.configure(font=("Segoe UI", self.size_actual, "bold"))
            self.root.after(10, self.animar_ciclo)
        else:
            self.lbl_nombre = ctk.CTkLabel(self.f_intro, text="CHRONOS REGISTRY SYSTEM", font=("Segoe UI", 1, "bold"), text_color="#555")
            self.lbl_nombre.pack(pady=20)
            self.efecto_pop(1)

    def efecto_pop(self, size):
        """Agrega un efecto de crecimiento rápido al subtítulo."""
        if size < 22:
            """Este size es del label llamado nombre que es el que usamos para el subtitulo, 
            que creamos en el ultimo else."""
            diff = 22 - size
            """usamos de nuevo diff con el mismo fin anterior."""
            step = max(1, diff // 4)
            "Aqui el step es mucho mas agresivo, asi nos da ese efecto de pop"
            size += step
            """Mismo metodo para hacer crecer el texto"""
            self.lbl_nombre.configure(font=("Segoe UI", size, "bold"))
            """Creamos la configuracion del label nombre."""
            self.root.after(10, lambda: self.efecto_pop(size))
            """Y aqui nuevamente usamos after, en este caso
            lambda crea una funcion anonima. y de esta traemos
            el efecto pop, con el tamaño refrescado."""
        else:
            self.root.after(2000, self.mostrar_inicio)
            """Y terminamos nuestra animacion con un delay de 2 segundos para que el usuario 
            tenga tiempo de ver el logo y el nombre, y asi, pasamos a la parte tecnica del programa
            mostrando la pantalla de inicio."""
    ###Fin Efectos principales de animacion###        
            

    # --- VISTA 1: GATEWAY ---
    def mostrar_inicio(self):
        """Renderiza la pantalla de entrada con las tres opciones principales."""
        self.limpiar_pantalla()
        # outer frame with a slightly thicker border for better visibility
        f = ctk.CTkFrame(self.main_container, width=500, height=550, corner_radius=20,
                         fg_color=self.bg_light, border_width=2, border_color="#E0E0E0")
        f.place(relx=0.5, rely=0.5, anchor="center")

        # titles
        ctk.CTkLabel(f, text="GATEWAY C.R.S", font=("Segoe UI", 32, "bold"), text_color=self.sena_dark).pack(pady=(50, 5))
        ctk.CTkLabel(f, text="Chronos Registry System | High Softwares", font=("Segoe UI", 13), text_color="#888").pack(pady=(0, 40))

        # add horizontal padding so buttons don't sit right against the border
        ctk.CTkButton(f, text="TERMINAL APRENDICES", height=55, width=350, corner_radius=10,
                       command=self.mostrar_terminal).pack(pady=10, padx=20)
        ctk.CTkButton(f, text="PANEL ADMINISTRATIVO", height=55, width=350, corner_radius=10,
                       fg_color="#333", hover_color="#1a1a1a", command=self.mostrar_login).pack(pady=10, padx=20)
        ctk.CTkButton(f, text="MI PERFIL (APRENDIZ)", height=55, width=350, corner_radius=10,
                       fg_color="transparent", text_color=self.sena_green, border_width=2,
                       border_color=self.sena_green, hover_color="#E8F5E9", command=self.login_aprendiz_view).pack(pady=10, padx=20)

    # --- VISTA 2: TERMINAL ---
    def mostrar_terminal(self):
        """Pantalla de terminal para registrar asistencias."""
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

    # --- VISTA 3: PERFIL APRENDIZ ---
    def login_aprendiz_view(self):
        """Pantalla de inicio de sesión para aprendices."""
        self.limpiar_pantalla()
        # login frame with mild grey background and visible border
        f = ctk.CTkFrame(self.main_container, width=450, height=480, corner_radius=25,
                         fg_color=self.bg_light, border_width=2, border_color="#DDD")
        f.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(f, text="ACCESO APRENDIZ", font=("Segoe UI", 24, "bold")).pack(pady=35)
        u_ent = ctk.CTkEntry(f, width=320, height=50, placeholder_text="Documento"); u_ent.pack(pady=12, padx=20)
        p_ent = ctk.CTkEntry(f, width=320, height=50, placeholder_text="Contraseña", show="*"); p_ent.pack(pady=12, padx=20)

        def entrar():
            user = self.servicio.login_aprendiz(u_ent.get(), p_ent.get())
            if user:
                self.aprendiz_actual = u_ent.get()
                try: self.db.registrar_auditoria(self.aprendiz_actual, "login aprendiz")
                except: pass
                if user.get('cambio_pass') == 0 or p_ent.get() == 'sena123': self.actualizar_password_ventana(user['documento'])
                self.mostrar_panel_aprendiz(user)
            else: messagebox.showerror("Error", "Credenciales Incorrectas")

        ctk.CTkButton(f, text="INGRESAR", width=320, height=55, command=entrar).pack(pady=35, padx=20)
        ctk.CTkButton(f, text="VOLVER", fg_color="transparent", text_color="gray", command=self.mostrar_inicio).pack(padx=20)

    def mostrar_panel_aprendiz(self, user):
        """Panel con calendario para que el aprendiz vea su actividad."""
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=75, corner_radius=0, fg_color=self.bg_light, border_width=1, border_color="#EEE"); head.pack(fill="x")
        def cerrar_aprendiz():
            if self.aprendiz_actual:
                try: self.db.registrar_auditoria(self.aprendiz_actual, "logout aprendiz")
                except: pass
            self.aprendiz_actual = None
            self.mostrar_inicio()
        ctk.CTkButton(head, text="🚪 CERRAR SESIÓN", fg_color="#FF5252", hover_color="#D32F2F", command=cerrar_aprendiz).pack(side="left", padx=25)
        ctk.CTkLabel(head, text=f"Aprendiz: {user['nombre_completo']}", font=("Segoe UI", 15, "bold")).pack(side="right", padx=35)

        body = ctk.CTkFrame(self.main_container, fg_color="transparent"); body.pack(fill="both", expand=True, padx=45, pady=25)
        left = ctk.CTkFrame(body, corner_radius=20, fg_color=self.bg_light, border_width=1, border_color="#DDD"); left.place(relx=0, rely=0, relwidth=0.64, relheight=1)
        cal = Calendar(left, selectmode='day', locale='es_ES', background=self.sena_green, headersbackground=self.sena_dark); cal.pack(fill="both", expand=True, padx=25, pady=25)
        right = ctk.CTkFrame(body, corner_radius=20, fg_color=self.bg_light, border_width=1, border_color="#DDD"); right.place(relx=0.66, rely=0, relwidth=0.34, relheight=1)
        lbl_info = ctk.CTkLabel(right, text="Actividad del día", font=("Segoe UI", 18, "bold")); lbl_info.pack(pady=20)
        
        container_cards = ctk.CTkScrollableFrame(right, fg_color="transparent"); container_cards.pack(fill="both", expand=True, padx=12, pady=8)

        def actualizar_cards(e=None):
            for w in container_cards.winfo_children(): w.destroy()
            fecha = cal.selection_get()
            regs = self.servicio.obtener_registros_dia(user['documento'], fecha)
            if not regs: ctk.CTkLabel(container_cards, text="Sin actividad este día", text_color="#AAA").pack(pady=60)
            else:
                for r in regs:
                    card = ctk.CTkFrame(container_cards, fg_color="#F8F9FA", corner_radius=12, border_width=1, border_color="#EEE"); card.pack(fill="x", pady=6, padx=8)
                    ctk.CTkLabel(card, text=f"📥 Ent: {r['fecha_registro'].strftime('%H:%M')}", font=("Segoe UI", 11)).pack(side="left", padx=15, pady=12)
                    if r['fecha_salida']: ctk.CTkLabel(card, text=f"📤 Sal: {r['fecha_salida'].strftime('%H:%M')}", font=("Segoe UI", 11), text_color="#E67E22").pack(side="right", padx=15)
        cal.bind("<<CalendarSelected>>", actualizar_cards); actualizar_cards()

    # --- VISTA 4: PANEL ADMINISTRATIVO ---
    def mostrar_login(self):
        """Pantalla de inicio de sesión para administradores."""
        self.limpiar_pantalla()
        f = ctk.CTkFrame(self.main_container, width=420, height=480, corner_radius=25, fg_color=self.bg_light); f.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f, text="ADMINISTRACIÓN", font=("Segoe UI", 24, "bold")).pack(pady=35)
        u_ent = ctk.CTkEntry(f, placeholder_text="Usuario", width=300, height=50); u_ent.pack(pady=12)
        p_ent = ctk.CTkEntry(f, placeholder_text="Contraseña", show="*", width=300, height=50); p_ent.pack(pady=12)
        def log_admin():
            usuario = u_ent.get()
            self.db.cursor.execute("SELECT * FROM usuarios_admin WHERE usuario=%s AND password=%s", (usuario, p_ent.get()))
            if self.db.cursor.fetchone():
                self.admin_actual = usuario
                try: self.db.registrar_auditoria(self.admin_actual, "login admin")
                except: pass
                self.mostrar_panel_admin_ui()
            else: messagebox.showerror("Denegado", "Usuario o clave incorrecta")
        ctk.CTkButton(f, text="ACCEDER AL PANEL", width=300, height=55, command=log_admin).pack(pady=35)
        ctk.CTkButton(f, text="VOLVER", fg_color="transparent", text_color="gray", command=self.mostrar_inicio).pack()

    def mostrar_panel_admin_ui(self):
        """Panel administrativo con pestañas."""
        self.limpiar_pantalla()
        head = ctk.CTkFrame(self.main_container, height=75, corner_radius=0, fg_color=self.sena_dark); head.pack(fill="x")
        def cerrar_admin():
            if self.admin_actual:
                try: self.db.registrar_auditoria(self.admin_actual, "logout admin")
                except: pass
            self.admin_actual = None
            self.mostrar_inicio()
        ctk.CTkButton(head, text="🔒 CERRAR", fg_color="#444", command=cerrar_admin).pack(side="right", padx=25)
        tabview = ctk.CTkTabview(self.main_container, segmented_button_selected_color=self.sena_green, fg_color=self.bg_light)
        tabview.pack(fill="both", expand=True, padx=25, pady=15)
        t_asis = tabview.add("🕒 HISTORIAL"); t_gest = tabview.add("👥 GESTIÓN"); t_reg = tabview.add("📝 REGISTRO"); t_pap = tabview.add("🗑️ PAPELERA")
        # match tab backgrounds to the app background
        for t in (t_asis, t_gest, t_reg, t_pap):
            t.configure(fg_color=self.bg_light)

        # -- Historial --
        def refresh_asis():
            for i in tv_asis.get_children(): tv_asis.delete(i)
            self.db.cursor.execute("SELECT a.id_asistencia, a.documento_estudiante, e.nombre_completo, a.fecha_registro, a.fecha_salida FROM asistencias a JOIN estudiantes e ON a.documento_estudiante = e.documento ORDER BY a.fecha_registro DESC LIMIT 100")
            for r in self.db.cursor.fetchall():
                sal = r['fecha_salida'].strftime('%H:%M') if r['fecha_salida'] else "PENDIENTE"
                tv_asis.insert("", "end", values=(r['documento_estudiante'], r['nombre_completo'], r['fecha_registro'].strftime('%d/%m %H:%M'), sal))
        tv_f1 = tk.Frame(t_asis, bg="#f7f7f7"); tv_f1.pack(fill="both", expand=True, padx=12, pady=12)
        tv_asis = ttk.Treeview(tv_f1, columns=("DOC", "NOMBRE", "IN", "OUT"), show="headings"); [tv_asis.heading(c, text=c) for c in ("DOC", "NOMBRE", "IN", "OUT")]; tv_asis.pack(fill="both", expand=True); refresh_asis()

        # -- Gestión --
        f_bus = ctk.CTkFrame(t_gest, fg_color="transparent"); f_bus.pack(fill="x", padx=20, pady=15)
        ent_bus = ctk.CTkEntry(f_bus, placeholder_text="Buscar aprendiz...", width=420); ent_bus.pack(side="left", padx=10)
        tv_f2 = tk.Frame(t_gest, bg=self.bg_light); tv_f2.pack(fill="both", expand=True, padx=20)
        tv_gest = ttk.Treeview(tv_f2, columns=("DOC", "NOMBRE", "FICHA"), show="headings", selectmode='extended'); [tv_gest.heading(c, text=c) for c in ("DOC", "NOMBRE", "FICHA")]; tv_gest.pack(fill="both", expand=True)
        def filtrar():
            for i in tv_gest.get_children(): tv_gest.delete(i)
            v = f"%{ent_bus.get()}%"
            self.db.cursor.execute("SELECT documento, nombre_completo, id_ficha FROM estudiantes WHERE documento LIKE %s OR nombre_completo LIKE %s", (v, v))
            for r in self.db.cursor.fetchall(): tv_gest.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))
        ctk.CTkButton(f_bus, text="🔍 FILTRAR", width=120, command=filtrar).pack(side="left"); filtrar()
        def mover_seleccion():
            docs = [tv_gest.item(i)['values'][0] for i in tv_gest.selection()]
            if not docs: return
            if messagebox.askyesno("Confirmar", f"¿Desea mover {len(docs)} aprendices a la papelera?"):
                for doc in docs:
                    self.servicio.mandar_a_papelera(doc)
                    try: self.db.registrar_auditoria(self.admin_actual, "mover a papelera", objeto=doc)
                    except: pass
                filtrar(); refresh_pap()
        ctk.CTkButton(t_gest, text="🗑️ MOVER A PAPELERA", fg_color="#E74C3C", command=mover_seleccion).pack(pady=10)

        # -- Registro --
        f_reg_m = ctk.CTkFrame(t_reg, corner_radius=20, fg_color=self.bg_light, border_width=1, border_color="#EEE"); f_reg_m.pack(pady=20, padx=50, fill="x")
        grid_f = tk.Frame(f_reg_m, bg=self.bg_light); grid_f.pack(pady=20, padx=25)
        fields = ["Documento", "Nombre Completo", "Correo"]; entries = {}
        for i, l in enumerate(fields):
            ctk.CTkLabel(grid_f, text=l, text_color="gray").grid(row=0, column=i, padx=12)
            e = ctk.CTkEntry(grid_f, width=190); e.grid(row=1, column=i, padx=5, pady=5); entries[l] = e
        cb_f = ttk.Combobox(grid_f, state="readonly", width=40); cb_f.grid(row=1, column=3, padx=12); cb_f['values'] = [f"{f['id_ficha']} | {f['codigo_ficha']}" for f in self.servicio.obtener_fichas()]
        def save():
            if self.servicio.guardar_aprendiz_manual({k: v.get() for k, v in entries.items()}, cb_f.get().split(" | ")[0] if cb_f.get() else None):
                messagebox.showinfo("OK", "Registrado"); [v.delete(0, 'end') for v in entries.values()]; filtrar()
        ctk.CTkButton(f_reg_m, text="💾 GUARDAR", command=save).pack(pady=15)
        ctk.CTkButton(t_reg, text="📂 CARGA EXCEL", fg_color="#333", command=self.servicio.importar_excel).pack()

        # -- Papelera --
        tv_f3 = tk.Frame(t_pap, bg=self.bg_light); tv_f3.pack(fill="both", expand=True, padx=20, pady=12)
        tv_pap = ttk.Treeview(tv_f3, columns=("DOC", "NOMBRE", "FICHA"), show="headings", selectmode='extended'); [tv_pap.heading(c, text=c) for c in ("DOC", "NOMBRE", "FICHA")]; tv_pap.pack(fill="both", expand=True)
        def refresh_pap():
            for i in tv_pap.get_children(): tv_pap.delete(i)
            self.db.cursor.execute("SELECT documento, nombre_completo, id_ficha FROM estudiantes_eliminados")
            for r in self.db.cursor.fetchall(): tv_pap.insert("", "end", values=(r['documento'], r['nombre_completo'], r['id_ficha']))
        btn_p = ctk.CTkFrame(t_pap, fg_color="transparent"); btn_p.pack(pady=10)
        def restaurar():
            docs = [tv_pap.item(i)['values'][0] for i in tv_pap.selection()]
            for d in docs: 
                self.servicio.restaurar_aprendiz(d)
                try: self.db.registrar_auditoria(self.admin_actual, "restaurar aprendiz", objeto=d)
                except: pass
            refresh_pap(); filtrar()
        def eliminar():
            docs = [tv_pap.item(i)['values'][0] for i in tv_pap.selection()]
            if messagebox.askyesno("Confirmar", "Esta acción es irreversible"):
                for d in docs: 
                    self.servicio.eliminar_permanente(d)
                    try: self.db.registrar_auditoria(self.admin_actual, "eliminar permanente", objeto=d)
                    except: pass
                refresh_pap()
        ctk.CTkButton(btn_p, text="♻️ RESTAURAR", fg_color=self.sena_green, command=restaurar).pack(side="left", padx=10)
        ctk.CTkButton(btn_p, text="🔥 ELIMINAR", fg_color="black", command=eliminar).pack(side="left", padx=10); refresh_pap()

    # --- SEGURIDAD ---
    def actualizar_password_ventana(self, documento):
        """Diálogo modal para el cambio de contraseña obligatorio."""
        v = tk.Toplevel(self.root); v.title("Seguridad C.R.G"); v.geometry("450x520"); v.configure(bg=self.bg_light); v.grab_set()
        tk.Label(v, text="🔒 CAMBIO OBLIGATORIO", font=("bold", 12), bg=self.bg_light, fg="#d32f2f").pack(pady=10)
        pass_var = tk.StringVar(); e = ttk.Entry(v, show="*", textvariable=pass_var, font=("Segoe UI", 12)); e.pack(pady=10, padx=40, fill="x")
        req_frame = tk.Frame(v, bg=self.bg_light); req_frame.pack(pady=10, padx=40, fill="x")
        requisitos = {
            "long":  tk.Label(req_frame, text="• Mínimo 8 caracteres", bg=self.bg_light, fg="red", anchor="w"),
            "upper": tk.Label(req_frame, text="• Al menos una mayúscula", bg=self.bg_light, fg="red", anchor="w"),
            "lower": tk.Label(req_frame, text="• Al menos una minúscula", bg=self.bg_light, fg="red", anchor="w"),
            "num":   tk.Label(req_frame, text="• Al menos un número", bg=self.bg_light, fg="red", anchor="w")
        }
        for lbl in requisitos.values(): lbl.pack(fill="x")
        def validar(*args):
            p = pass_var.get()
            cond = {"long": len(p)>=8, "upper": any(c.isupper() for c in p), "lower": any(c.islower() for c in p), "num": any(c.isdigit() for c in p)}
            for k, c in cond.items(): requisitos[k].config(fg="#39A900" if c else "red")
            return all(cond.values())
        pass_var.trace_add("write", validar)
        def save():
            if validar():
                self.db.cursor.execute("UPDATE estudiantes SET password=%s, cambio_pass=1 WHERE documento=%s", (pass_var.get(), documento))
                self.db.conexion.commit(); messagebox.showinfo("C.R.S", "Seguridad configurada"); v.destroy()
        tk.Button(v, text="GUARDAR Y ENTRAR", bg="#39A900", fg="white", command=save).pack(pady=20)

if __name__ == "__main__":
    root = ctk.CTk() 
    app = SistemaHSGSCRS(root)
    root.mainloop()