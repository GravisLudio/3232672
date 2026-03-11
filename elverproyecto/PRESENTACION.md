# 📊 **PRESENTACIÓN DEL PROYECTO C.R.S**

## **CHRONOS REGISTRY SYSTEM**
### Sistema Integrado de Gestión de Asistencia y Registro de Faltas - SENA

---

## 📋 **TABLA DE CONTENIDOS**

1. [Visión General](#visión-general)
2. [Objetivos del Proyecto](#objetivos-del-proyecto)
3. [Requisitos Funcionales](#requisitos-funcionales)
4. [Requisitos No Funcionales](#requisitos-no-funcionales)
5. [Tipos de Usuarios](#tipos-de-usuarios-y-paneles)
6. [Historias de Usuario](#historias-de-usuario)
7. [Diagramas UML](#diagramas-uml)
8. [Arquitectura del Sistema](#arquitectura-del-sistema)
9. [Instalación y Uso](#instalación-y-uso)

---

## 🎯 **VISIÓN GENERAL**

**C.R.S** es una solución integral de software desktop desarrollada para el **SENA - Centro de Gestión Administrativa (HSGS)** que proporciona:

- ✅ **Registro automático** de asistencia (entrada/salida)
- ✅ **Gestión integral** de aprendices, fichas y competencias
- ✅ **Panel personalizado** para cada tipo de usuario
- ✅ **Control de faltas** registradas por instructores
- ✅ **Reportes avanzados** con exportación PDF/Excel
- ✅ **Auditoría completa** de todas las operaciones

**Versión Actual**: 2.0 (Marzo 2026)

### 📊 Características Destacadas
- Interfaz moderna y amigable con CustomTkinter
- Base de datos MySQL para escalabilidad
- Soporte multi-usuario (Aprendiz, Instructor, Administrador)
- Sistema de auditoría de todas las acciones
- Generación de reportes visuales con gráficos
- Exportación a PDF y Excel

---

## 🎯 **OBJETIVOS DEL PROYECTO**

### Objetivo General
Desarrollar un sistema desktop que automatice el registro de asistencia y gestión de faltas en el SENA, mejorando la eficiencia administrativa y proporcionando información en tiempo real.

### Objetivos Específicos
1. **Automatizar** el registro de entrada/salida de aprendices
2. **Facilitar** a instructores el registro de faltas y retardos
3. **Proporcionar** a administradores herramientas de gestión integral
4. **Generar** reportes de asistencia por múltiples criterios
5. **Auditar** todas las acciones del sistema para cumplimiento normativo
6. **Mejorar** la experiencia del usuario con interfaz intuitiva

---

## ✅ **REQUISITOS FUNCIONALES**

### Autenticación y Seguridad (RF-001 a RF-003)
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RF-001 | Validación de Usuario | Sistema valida usuario y contraseña (admin, instructor, aprendiz) |
| RF-002 | Cambio de Contraseña | Contraseña por defecto se cambia en primer login |
| RF-003 | Auditoría de Sesiones | Login/logout registrado en auditoría |

### Gestión de Asistencia (RF-004 a RF-007)
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RF-004 | Registrar Entrada | Aprendiz registra entrada con documento de identidad |
| RF-005 | Registrar Salida | Aprendiz registra salida (solo si hay entrada activa) |
| RF-006 | Consultar Historial | Visualizar historial personal de asistencias |
| RF-007 | Calendario Mensual | Mostrar calendario interactivo con asistencias |

### Gestión de Faltas (RF-008 a RF-010) ⭐ NUEVO
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RF-008 | Registrar Faltas | Instructor registra: Inasistencia, Retardo, Justificada |
| RF-009 | Consultar Faltas | Instructor ve faltas de su ficha asignada |
| RF-010 | Admin Consulta Faltas | Administrador tiene acceso a todas las faltas |

### Gestión de Aprendices (RF-011 a RF-016)
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RF-011 | Crear Aprendiz Manual | Admin crea aprendiz con documento, nombre, correo, ficha |
| RF-012 | Importar desde Excel | Admin carga múltiples aprendices con archivo .xlsx |
| RF-013 | Modificar Aprendiz | Editar datos de aprendiz existente |
| RF-014 | Mover a Papelera | Desactivar aprendiz sin borrar datos |
| RF-015 | Restaurar Aprendiz | Recuperar aprendiz desde papelera |
| RF-016 | Eliminar Permanente | Borrado definitivo de aprendiz |

### Gestión de Instructores (RF-017 a RF-020) ⭐ NUEVO
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RF-017 | Crear Instructor | Admin crea instructor con documento, nombre, correo |
| RF-018 | Asignar Fichas | Admin asigna una o más fichas a instructor |
| RF-019 | Ver Fichas Asignadas | Instructor solo ve sus fichas y aprendices |
| RF-020 | Gestionar Estudiantes | Instructor accede a lista de estudiantes de su ficha |

### Reportes (RF-021 a RF-024)
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RF-021 | Reportes Temporales | Generar reportes por día, semana, mes |
| RF-022 | Filtrar Reportes | Filtrar por ficha o aprendiz individual |
| RF-023 | Exportación Múltiple | Exportar a PDF, Excel con gráficos |
| RF-024 | Auditoría Completa | Consultar log de todas las acciones del sistema |

---

## 🔧 **REQUISITOS NO FUNCIONALES**

### Rendimiento (RNF-001 a RNF-004)
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-001 | Respuesta UI | Interfaz debe responder en <500ms |
| RNF-002 | Carga de Calendarios | Calendarios interactivos cargan en <1 segundo |
| RNF-003 | Generación de Reportes | Reportes se generan en <5 segundos |
| RNF-004 | Volumen de Datos | Soporte para mínimo 1000 registros de asistencia |

### Seguridad (RNF-005 a RNF-008)
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-005 | Almacenamiento Seguro | Contraseñas hasheadas en base de datos |
| RNF-006 | Auditoría Completa | Registro de cada acción en tabla de auditoría |
| RNF-007 | Validación de Entrada | Validación en todos los campos de formularios |
| RNF-008 | Acceso a BD | Sin acceso directo a BD desde interfaz de usuario |

### Confiabilidad (RNF-009 a RNF-012)
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-009 | Disponibilidad | 99% de disponibilidad en horario laboral |
| RNF-010 | Recuperación | Recuperación automática de conexión perdida |
| RNF-011 | Transacciones | Rollback automático en fallos de transacciones |
| RNF-012 | Backup | Recomendación de backup automático |

### Usabilidad (RNF-013 a RNF-016)
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-013 | Interfaz Intuitiva | Uso sin necesidad de capacitación mayor |
| RNF-014 | Mensajes Claros | Mensajes de error claros en español |
| RNF-015 | Tema Visual | Consistencia visual con colores SENA |
| RNF-016 | Navegación Rápida | Acceso rápido a secciones principales |

### Mantenibilidad (RNF-017 a RNF-020)
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-017 | Código Modular | Código bien organizado y documentado |
| RNF-018 | Separación de Capas | BD, Lógica, UI completamente separadas |
| RNF-019 | Extensibilidad | Fácil adición de nuevas funcionalidades |
| RNF-020 | Patrones Diseño | Uso de patrones establecidos (MVC, Singleton) |

### Compatibilidad (RNF-021 a RNF-024)
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-021 | MySQL | Compatible con MySQL 8.0+ |
| RNF-022 | Python | Compatible con Python 3.10+ |
| RNF-023 | Windows | Compatible con Windows 10/11 |
| RNF-024 | Resoluciones | UI escalable a diferentes resoluciones |

### Escalabilidad (RNF-025 a RNF-027)
| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-025 | Múltiples Fichas | Soporte para múltiples fichas simultáneamente |
| RNF-026 | Múltiples Instructores | Soporte para gestión multi-instructor |
| RNF-027 | Sedes Futuras | Preparado para expansión a múltiples sedes |

---

## 👥 **TIPOS DE USUARIOS Y PANELES**

### 1️⃣ **PANEL DE APRENDIZ**
```
┌─────────────────────────────────────┐
│  👨‍💻 PANEL DEL APRENDIZ              │
├─────────────────────────────────────┤
│  • 📅 Calendario interactivo        │
│  • 📊 Visualizar asistencias        │
│  • ⏰ Ver entrada/salida por día     │
│  • 🔐 Cambiar contraseña            │
└─────────────────────────────────────┘
```

**Características:**
- Calendario mensual interactivo mostrando asistencias
- Click en day para ver entrada/salida
- Visualización de horas exactas
- Cambio de contraseña automático en primer login
- Interfaz simple y amigable

---

### 2️⃣ **PANEL DE INSTRUCTOR** ⭐ NUEVO

```
┌─────────────────────────────────────┐
│  👨‍🏫 PANEL DEL INSTRUCTOR           │
├─────────────────────────────────────┤
│  📋 Pestaña 1: HISTORIAL            │
│    • Ver fichas asignadas           │
│    • Consultar asistencias          │
│                                     │
│  📊 Pestaña 2: REPORTES             │
│    • Generar reportes               │
│    • Exportar datos                 │
│                                     │
│  ❌ Pestaña 3: REGISTRO DE FALTAS   │
│    • Registrar faltas               │
│    • Especificar tipo               │
│    • Agregar comentarios            │
└─────────────────────────────────────┘
```

**Características:**
- Acceso limitado a solo sus fichas asignadas
- Visualización de historial de asistencias
- **Registro de faltas** con 3 tipos:
  - Inasistencia
  - Retardo
  - Justificada
- Interfaz profesional con auditoría integrada

---

### 3️⃣ **PANEL DE ADMINISTRADOR**

```
┌──────────────────────────────────────┐
│  👨‍💼 PANEL ADMINISTRATIVO            │
├──────────────────────────────────────┤
│  📋 HISTORIAL                        │
│     → Ver todas las asistencias      │
│                                      │
│  👥 GESTIÓN                          │
│     → Crear/editar aprendices        │
│     → Importar desde Excel           │
│     → Crear instructores             │
│     → Asignar fichas                 │
│                                      │
│  ➕ REGISTRO                         │
│     → Registro manual                │
│     → Importación masiva             │
│                                      │
│  📊 REPORTES                         │
│     → Por día/semana/mes             │
│     → Por ficha o individual         │
│     → Exportar PDF/Excel             │
│                                      │
│  🗑️ PAPELERA                        │
│     → Restaurar aprendices           │
│     → Eliminar permanente            │
│                                      │
│  🔍 AUDITORÍA                        │
│     → Historial de acciones          │
│     → Quién hizo qué y cuándo        │
└──────────────────────────────────────┘
```

**Características:**
- Acceso completo a todas las funcionalidades
- Gestión de aprendices e instructores
- Generación de reportes complejos
- Seguimiento de auditoría
- Control total del sistema

---

## 🗄️ **ARQUITECTURA DE BASE DE DATOS**

```
USUARIOS
├── usuarios_admin (Admin/Instructor)
├── estudiantes (Aprendices)
└── instructores (Instructores) ⭐ NUEVO

ESTRUCTURA EDUCATIVA
├── fichas (Programas de formación)
├── competencias (Habilidades requeridas)
├── ficha_competencias (Relación)
├── horarios (Horarios de clases)
├── fichas_asignadas (Fichas → Instructores) ⭐ NUEVO

REGISTROS
├── asistencias (Entrada/Salida)
├── faltas (Registro de faltas) ⭐ NUEVO
└── auditoria (Auditoría de acciones)
```

---

## 🔄 **FLUJOS DE OPERACIÓN**

### **Flujo 1: Aprendiz registra asistencia**
```
Aprendiz login → Panel aprendiz → Ver calendario → Consultar historial
```

### **Flujo 2: Instructor registra faltas** ⭐ NUEVO
```
Instructor login → Selecciona ficha → Selecciona estudiante 
→ Elige tipo falta → Registra en BD → Auditoría registrada
```

### **Flujo 3: Admin gestiona sistema**
```
Admin login → Selecciona pestaña → Realiza acción 
→ BD se actualiza → Auditoría registrada → Admin consulta
```

### **Flujo 4: Admin genera reportes**
```
Admin → Reportes → Selecciona parámetros (día/semana/mes)
→ Aplica filtros → Genera PDF/Excel → Descarga
```

---

## 💾 **TECNOLOGÍAS UTILIZADAS**

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| **Lenguaje** | Python | 3.10+ |
| **GUI** | CustomTkinter | 5.2.1+ |
| **BD** | MySQL | 8.0+ |
| **Conector** | mysql-connector-python | 8.2.0+ |
| **Datos** | pandas | 2.0.3+ |
| **Excel** | openpyxl | 3.1.2+ |
| **PDF** | reportlab | 4.0.7+ |
| **Calendario** | tkcalendar | 1.6.1+ |
| **Imágenes** | Pillow | 10.0.0+ |
| **Entorno** | python-dotenv | 1.0.0+ |

---

## 🔐 **SEGURIDAD Y AUDITORÍA**

### **Control de Acceso**
```
┌─ Admin (superusuario)
│  ├─ Acceso total
│  └─ Auditoría completa
│
├─ Instructor (acceso limitado) ⭐
│  ├─ Solo sus fichas
│  ├─ Registro de faltas
│  └─ Auditoría personal
│
└─ Aprendiz (acceso personal)
   ├─ Solo su historial
   └─ Cambio de contraseña
```

### **Auditoría Integrada**
- ✅ Login/logout registrado
- ✅ Cambios de contraseña
- ✅ Creación de registros
- ✅ Modificaciones
- ✅ Eliminaciones
- ✅ Acciones por usuario y hora

---

## 📊 **MÉTRICAS Y KPIs**

El sistema genera automáticamente:

- **Sesiones esperadas**: Basado en horas y días hábiles
- **Presencias**: Registros de entrada
- **Faltas**: Sesiones no asistidas
- **Retardos**: Llegadas tardías
- **Tasa de asistencia**: Porcentaje
- **Resumen por período**: Día/Semana/Mes

---

## 🚀 **FLUJO DE INSTALACIÓN**

```
1. Descargar/clonar proyecto
   ↓
2. Crear entorno virtual
   ↓
3. pip install -r requirements.txt
   ↓
4. Crear BD: mysql < techsenahsgs.sql
   ↓
5. Configurar .env
   ↓
6. python main.py
   ↓
✅ Sistema listo para usar
```

---

## 📁 **COMPONENTES PRINCIPALES**

### **Archivos Python**
```
✅ main.py              Entrada principal + Gestión de UI
✅ conexion.py          Capa de base de datos
✅ logica.py            Lógica de negocios (con métodos de instructor)
✅ admin_panel.py       Panel admin + Instructor
✅ dashboard_password.py Panel de aprendiz
✅ reportes.py          Generador de reportes
✅ config.py            Configuración
✅ logging_config.py    Sistema de logs
✅ ui_helper.py         Funciones de UI
✅ validadores.py       Validaciones
```

### **Archivos de Configuración**
```
✅ .env                 Credenciales de BD
✅ requirements.txt     Dependencias
✅ techsenahsgs.sql     Script BD con tablas nuevas
```

### **Recursos**
```
✅ images/              Logos e imágenes
✅ Documentación/       Diagramas y guías
```

---

## 📈 **VERSIONES Y ROADMAP**

| Versión | Estado | Cambios |
|---------|--------|---------|
| **1.0** | ✅ Completada | Gestión de asistencia básica |
| **2.0** | ✅ Completada | Sistema de instructores + Faltas |
| **2.1** | 🔮 Planeada | Reportes avanzados, notificaciones |
| **3.0** | 🔮 Planeada | Sistema multi-sede, App móvil |

---

## 🎓 **BENEFICIOS**

### Para **Aprendices**
- ✅ Visualización clara de asistencia
- ✅ Conocimiento de faltas registradas
- ✅ Control de acceso seguro

### Para **Instructores**
- ✅ Registro fácil de faltas
- ✅ Consulta de historial
- ✅ Auditoría de sus acciones

### Para **Administrador**
- ✅ Control total del sistema
- ✅ Reportes y análisis
- ✅ Gestión centralizada
- ✅ Auditoría completa

### Para **SENA HSGS**
- ✅ Automatización de procesos
- ✅ Reducción de errores manual
- ✅ Mejora en la gestión
- ✅ Trazabilidad completa

---

## 🔍 **REQUISITOS CUMPLIDOS**

### ✅ **FUNCIONALES (24/24)**
- RF-001 a RF-024: Todos los requisitos funcionales implementados

### ✅ **NO FUNCIONALES (27/27)**
- RNF-001 a RNF-027: Todos los requisitos no funcionales cumplidos

> **Ver README.md** para detalle completo de requisitos

---

## 📞 **INFORMACIÓN TÉCNICA**

**Desenvolvedor**: Equipo SENA HSGS  
**Lenguaje**: Python 3.10+  
**Base de Datos**: MySQL 8.0+  
**Framework UI**: CustomTkinter 5.2+  
**Licencia**: SENA (Uso educativo/administrativo)  
**Última Actualización**: 5 de Marzo de 2026  

---

**Estado del Proyecto**: ✅ **LISTO PARA PRODUCCIÓN**

El sistema está completamente funcional, documentado y listo para ser desplegado en ambiente de producción.

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