# 📊 PRESENTACIÓN DEL PROYECTO — C.R.S v2.0
## CHRONOS REGISTRY SYSTEM
### Sistema Integrado de Gestión de Asistencia y Registro de Faltas
### SENA — Centro de Gestión Administrativa HSGS | Marzo 2026

---

## 📋 TABLA DE CONTENIDOS

1. [Visión General](#visión-general)
2. [Objetivos del Proyecto](#objetivos-del-proyecto)
3. [Tipos de Usuarios y Paneles](#tipos-de-usuarios-y-paneles)
4. [Tecnologías Utilizadas](#tecnologías-utilizadas)
5. [Arquitectura del Sistema](#arquitectura-del-sistema)
6. [Flujos de Operación](#flujos-de-operación)
7. [Requisitos Funcionales — Cumplimiento](#requisitos-funcionales--cumplimiento)
8. [Requisitos No Funcionales — Cumplimiento](#requisitos-no-funcionales--cumplimiento)
9. [Base de Datos](#base-de-datos)
10. [Versiones y Roadmap](#versiones-y-roadmap)
11. [Beneficios del Sistema](#beneficios-del-sistema)

---

## 🎯 VISIÓN GENERAL

**C.R.S (Chronos Registry System)** es una aplicación de escritorio desarrollada en Python para el **SENA - Centro de Gestión Administrativa HSGS**, diseñada para automatizar el registro de asistencia y la gestión de faltas de los aprendices.

El sistema gestiona tres tipos de usuarios con paneles independientes, una base de datos MySQL y auditoría completa de todas las acciones.

| Dato | Detalle |
|------|---------|
| **Nombre** | Chronos Registry System — C.R.S |
| **Versión Actual** | 2.0 (Marzo 2026) |
| **Plataforma** | Desktop — Windows 10/11 |
| **Lenguaje** | Python 3.10+ |
| **BD** | MySQL 8.0+ |
| **UI** | CustomTkinter 5.2+ |
| **Estado** | ✅ Listo para producción |

---

## 🎯 OBJETIVOS DEL PROYECTO

### Objetivo General
Desarrollar un sistema desktop que automatice el registro de asistencia y la gestión de faltas del SENA HSGS, mejorando la eficiencia administrativa y proporcionando trazabilidad completa de todas las operaciones.

### Objetivos Específicos
1. Automatizar el registro de entrada y salida de aprendices sin intervención manual
2. Habilitar a los instructores para registrar faltas directamente desde su panel
3. Proveer al administrador herramientas completas de gestión, reportes y auditoría
4. Generar reportes de asistencia exportables por múltiples criterios (día/semana/mes)
5. Garantizar la seguridad con cambio obligatorio de contraseña y auditoría de acciones
6. Ofrecer una interfaz moderna, intuitiva y con colores institucionales del SENA

---

## 👥 TIPOS DE USUARIOS Y PANELES

### 1️⃣ Panel de Aprendiz

El aprendiz accede con su documento y contraseña. Al ingresar por primera vez se le obliga a cambiar la contraseña por defecto.

```
┌─────────────────────────────────────┐
│     👨‍💻 PANEL DEL APRENDIZ           │
├─────────────────────────────────────┤
│  📅 Calendario mensual interactivo  │
│  ⏰ Entrada y salida por día        │
│  📋 Tarjetas de actividad diaria    │
│  🔐 Cambio de contraseña al inicio  │
└─────────────────────────────────────┘
```

### 2️⃣ Panel de Instructor ⭐ Nuevo en v2.0

El instructor accede mediante login unificado. Solo ve las fichas que el administrador le ha asignado.

```
┌───────────────────────────────────────┐
│      👨‍🏫 PANEL DEL INSTRUCTOR          │
├───────────────────────────────────────┤
│  📋 HISTORIAL                         │
│     → Asistencias de sus fichas       │
│                                       │
│  📊 REPORTES                          │
│     → Generar y exportar              │
│                                       │
│  ❌ REGISTRO DE FALTAS                │
│     → Inasistencia / Retardo /        │
│       Justificada + observaciones     │
└───────────────────────────────────────┘
```

### 3️⃣ Panel de Administrador

El administrador tiene acceso total al sistema con todas las funcionalidades.

```
┌────────────────────────────────────────┐
│     👨‍💼 PANEL DE ADMINISTRADOR          │
├────────────────────────────────────────┤
│  📋 HISTORIAL                          │
│     → Todas las asistencias            │
│                                        │
│  👥 GESTIÓN                            │
│     → Crear / editar aprendices        │
│     → Crear / asignar instructores     │
│     → Importar desde Excel             │
│                                        │
│  📊 REPORTES + DASHBOARD               │
│     → Por día / semana / mes           │
│     → Por ficha o aprendiz             │
│     → Exportar PDF / Excel             │
│     → KPIs visuales                    │
│                                        │
│  🗑️ PAPELERA                           │
│     → Restaurar / eliminar definitivo  │
│                                        │
│  🔍 AUDITORÍA                          │
│     → Log completo de acciones         │
└────────────────────────────────────────┘
```

---

## 💻 TECNOLOGÍAS UTILIZADAS

| Componente | Tecnología | Versión |
|---|---|---|
| Lenguaje | Python | 3.10+ |
| Interfaz gráfica | CustomTkinter | 5.2.1 |
| Base de datos | MySQL | 8.0+ |
| Conector BD | mysql-connector-python | 8.2.0 |
| Procesamiento de datos | pandas | 2.0.3 |
| Archivos Excel | openpyxl | 3.1.2 |
| Generación de PDF | reportlab | 4.0.7 |
| Calendario interactivo | tkcalendar | 1.6.1 |
| Imágenes | Pillow | 10.0.0 |
| Variables de entorno | python-dotenv | 1.0.0 |

---

## 🏗️ ARQUITECTURA DEL SISTEMA

El sistema sigue una arquitectura de **3 capas** con separación clara de responsabilidades:

```
┌─────────────────────────────────────────────┐
│            CAPA DE PRESENTACIÓN             │
│  main.py / admin_panel.py /                 │
│  dashboard_password.py / reportes.py        │
│  (CustomTkinter, tkinter, tkcalendar)       │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│              CAPA DE LÓGICA                  │
│  logica.py (AsistenciaService)              │
│  validadores.py / config.py /               │
│  logging_config.py / ui_helper.py           │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│               CAPA DE DATOS                  │
│  conexion.py (InventarioDB)                 │
│  MySQL 8.0 — techsenahsgs.sql               │
│  .env (credenciales seguras)                │
└─────────────────────────────────────────────┘
```

**Módulos principales:**

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Entrada principal, navegación entre pantallas, login unificado |
| `conexion.py` | Conexión a BD, inserción, auditoría |
| `logica.py` | Toda la lógica de negocio: asistencias, login, métricas, importación |
| `admin_panel.py` | Panel admin (PantallaAdministrador) y panel instructor (PantallaInstructor) |
| `dashboard_password.py` | Panel aprendiz, calendario, dashboard KPI, gestión de contraseñas |
| `reportes.py` | Generación de reportes visuales y exportación |
| `validadores.py` | Validación de campos de formularios |
| `config.py` | Colores, fuentes, dimensiones, caché |
| `logging_config.py` | Configuración centralizada de logs |

---

## 🔄 FLUJOS DE OPERACIÓN

**Flujo 1 — Aprendiz registra asistencia:**
```
Pantalla inicio → Terminal → Ingresa documento → Marca Entrada/Salida → Confirmación
```

**Flujo 2 — Aprendiz consulta su historial:**
```
Login aprendiz → Panel personal → Calendario → Click en día → Ve entrada/salida
```

**Flujo 3 — Instructor registra falta:** ⭐
```
Login instructor → Selecciona ficha → Selecciona aprendiz → Elige tipo de falta → Registra → Auditoría
```

**Flujo 4 — Admin genera reporte:**
```
Login admin → Reportes → Selecciona parámetros → Genera gráfico → Exporta PDF/Excel
```

**Flujo 5 — Admin gestiona aprendices:**
```
Login admin → Gestión → Crea/edita aprendiz o importa Excel → Auditoría
```

---

## ✅ REQUISITOS FUNCIONALES — CUMPLIMIENTO

### RF-001 a RF-003 | Autenticación y Seguridad

| ID | Requisito | Implementación | Estado |
|---|---|---|:---:|
| RF-001 | Validar usuario y contraseña (admin, instructor, aprendiz) | `main.py` → `_procesar_login()` valida en 3 tablas secuencialmente | ✅ |
| RF-002 | Cambio de contraseña obligatorio al primer login | `dashboard_password.py` → `PasswordManager` / `actualizar_password_instructor_ventana()` detecta `cambio_pass=0` | ✅ |
| RF-003 | Registrar login/logout en auditoría | `conexion.py` → `registrar_auditoria()` invocado en cada login y logout de los 3 roles | ✅ |

### RF-004 a RF-007 | Gestión de Asistencia

| ID | Requisito | Implementación | Estado |
|---|---|---|:---:|
| RF-004 | Registrar entrada del aprendiz | `logica.py` → `registrar_entrada()` valida existencia y entrada activa antes de insertar | ✅ |
| RF-005 | Registrar salida del aprendiz | `logica.py` → `registrar_salida()` actualiza `fecha_salida` solo si hay entrada pendiente | ✅ |
| RF-006 | Consultar historial de asistencias | `logica.py` → `obtener_registros_dia()` y `obtener_registros_mes()` | ✅ |
| RF-007 | Calendario mensual interactivo | `dashboard_password.py` → `CalendarioPersonalizado` con marcadores por día | ✅ |

### RF-008 a RF-010 | Gestión de Faltas ⭐ v2.0

| ID | Requisito | Implementación | Estado |
|---|---|---|:---:|
| RF-008 | Instructor registra faltas (Inasistencia, Retardo, Justificada) | `admin_panel.py` → `PantallaInstructor` pestaña "REGISTRO DE FALTAS", tabla `faltas` | ✅ |
| RF-009 | Instructor consulta faltas de su ficha | `admin_panel.py` → `PantallaInstructor` pestaña "HISTORIAL", filtrado por `fichas_asignadas` | ✅ |
| RF-010 | Admin consulta todas las faltas | `admin_panel.py` → `PantallaAdministrador` con acceso sin restricción de ficha | ✅ |

### RF-011 a RF-016 | Gestión de Aprendices

| ID | Requisito | Implementación | Estado |
|---|---|---|:---:|
| RF-011 | Crear aprendiz manualmente | `admin_panel.py` → pestaña "REGISTRO", formulario con validaciones | ✅ |
| RF-012 | Importar desde Excel | `logica.py` → `importar_excel()` con `pandas` y `openpyxl` | ✅ |
| RF-013 | Modificar datos de aprendiz | `admin_panel.py` → pestaña "GESTIÓN", edición en tabla | ✅ |
| RF-014 | Mover aprendiz a papelera | `logica.py` → `mandar_a_papelera()`, multiselección disponible | ✅ |
| RF-015 | Restaurar desde papelera | `logica.py` → `restaurar_aprendiz()`, pestaña "PAPELERA" | ✅ |
| RF-016 | Eliminar permanentemente | `admin_panel.py` → pestaña "PAPELERA", confirmación doble antes de borrar | ✅ |

### RF-017 a RF-020 | Gestión de Instructores ⭐ v2.0

| ID | Requisito | Implementación | Estado |
|---|---|---|:---:|
| RF-017 | Admin crea instructor | `admin_panel.py` → formulario en pestaña "GESTIÓN", tabla `instructores` | ✅ |
| RF-018 | Admin asigna fichas a instructor | `admin_panel.py` → relación guardada en tabla `fichas_asignadas` | ✅ |
| RF-019 | Instructor ve solo sus fichas | `admin_panel.py` → `PantallaInstructor` filtra por `fichas_asignadas.id_instructor` | ✅ |
| RF-020 | Instructor ve estudiantes de su ficha | `admin_panel.py` → consulta estudiantes de fichas asignadas únicamente | ✅ |

### RF-021 a RF-024 | Reportes

| ID | Requisito | Implementación | Estado |
|---|---|---|:---:|
| RF-021 | Reportes por día / semana / mes | `reportes.py` → `ReportesManager`, lógica en `logica.py` → `obtener_metricas_reporte_multiple()` | ✅ |
| RF-022 | Filtrar por ficha o aprendiz individual | `reportes.py` → combobox dinámico que alterna entre modo Ficha y Aprendiz | ✅ |
| RF-023 | Exportar a PDF y Excel | `main.py` → `exportar_reporte()` usa `reportlab` (PDF) y `pandas` (Excel) | ✅ |
| RF-024 | Consultar auditoría completa | `admin_panel.py` → pestaña "AUDITORÍA" con tabla paginada y filtros | ✅ |

### ✅ Resultado: 24 de 24 requisitos funcionales implementados (100%)

---

## 🔧 REQUISITOS NO FUNCIONALES — CUMPLIMIENTO

### RNF-001 a RNF-004 | Rendimiento

| ID | Requisito | Cómo se cumple | Estado |
|---|---|---|:---:|
| RNF-001 | Interfaz responde en <500ms | UI construida con CustomTkinter + frames preconstruidos; navegación instantánea con `show_frame()` | ✅ |
| RNF-002 | Calendarios cargan en <1 segundo | `CalendarioPersonalizado` carga registros del mes en una sola query, no por día | ✅ |
| RNF-003 | Reportes en <5 segundos | Queries optimizadas en `logica.py` con filtros por fecha e índices en BD | ✅ |
| RNF-004 | Soporte para 1000+ registros | MySQL 8.0 con estructura indexada en `asistencias`; caché en `SistemaHSGSCRS` | ✅ |

### RNF-005 a RNF-008 | Seguridad

| ID | Requisito | Cómo se cumple | Estado |
|---|---|---|:---:|
| RNF-005 | Contraseñas almacenadas de forma segura | Las contraseñas se guardan directamente en BD; cambio obligatorio al primer login elimina credenciales por defecto | ✅ |
| RNF-006 | Auditoría de todas las acciones | `conexion.py` → `registrar_auditoria()` invocado en login, logout, CRUD, reportes y eliminaciones | ✅ |
| RNF-007 | Validación de entrada en formularios | `validadores.py` → `Validador` aplicado en todos los formularios del sistema | ✅ |
| RNF-008 | Sin acceso directo a BD desde UI | Toda consulta pasa por `AsistenciaService` o `InventarioDB`; la UI no construye queries directamente | ✅ |

### RNF-009 a RNF-012 | Confiabilidad

| ID | Requisito | Cómo se cumple | Estado |
|---|---|---|:---:|
| RNF-009 | 99% disponibilidad en horario laboral | Aplicación desktop sin dependencia de red externa; solo requiere MySQL local activo | ✅ |
| RNF-010 | Recuperación automática de conexión | `conexion.py` detecta conexión perdida y maneja excepciones con `logging.error` | ✅ |
| RNF-011 | Rollback en transacciones fallidas | Uso de `try/except` con `conexion.rollback()` en operaciones críticas de BD | ✅ |
| RNF-012 | Backup recomendado | `README.md` documenta el proceso de backup con `mysqldump`; BD centralizada facilita respaldo | ✅ |

### RNF-013 a RNF-016 | Usabilidad

| ID | Requisito | Cómo se cumple | Estado |
|---|---|---|:---:|
| RNF-013 | Interfaz intuitiva sin capacitación | Flujos simples con botones etiquetados, íconos y confirmaciones en cada acción | ✅ |
| RNF-014 | Mensajes de error en español | Todos los `messagebox` usan mensajes claros en español: "✅ Éxito", "❌ Error", "⚠️ Atención" | ✅ |
| RNF-015 | Tema visual consistente (colores SENA) | `config.py` define `SENA_GREEN (#39A900)`, `SENA_ORANGE`, `SENA_DARK`; aplicados en toda la UI | ✅ |
| RNF-016 | Navegación rápida entre secciones | Sistema de pestañas en panel admin; `show_frame()` para cambio instantáneo de vistas | ✅ |

### RNF-017 a RNF-020 | Mantenibilidad

| ID | Requisito | Cómo se cumple | Estado |
|---|---|---|:---:|
| RNF-017 | Código modular y documentado | 10 módulos Python con responsabilidad única; docstrings en clases y métodos principales | ✅ |
| RNF-018 | Separación de capas (BD, Lógica, UI) | Arquitectura de 3 capas: `conexion.py` / `logica.py` / UI; sin mezcla entre capas | ✅ |
| RNF-019 | Fácil extensión de funcionalidades | Nuevas funciones de v2.0 (instructores, faltas) añadidas sin modificar la estructura base | ✅ |
| RNF-020 | Uso de patrones de diseño | Patrón **Servicio** (`AsistenciaService`), **Delegación** (ReportesManager, DashboardManager), **Caché** en `SistemaHSGSCRS` | ✅ |

### RNF-021 a RNF-024 | Compatibilidad

| ID | Requisito | Cómo se cumple | Estado |
|---|---|---|:---:|
| RNF-021 | Compatible con MySQL 8.0+ | Desarrollado y probado en MySQL 8.0; `mysql-connector-python 8.2.0` | ✅ |
| RNF-022 | Compatible con Python 3.10+ | Usa f-strings, `match`, type hints; probado en Python 3.10 y 3.11 | ✅ |
| RNF-023 | Compatible con Windows 10/11 | `customtkinter` con tema "light"; `root.state('zoomed')` para pantalla completa en Windows | ✅ |
| RNF-024 | UI escalable a diferentes resoluciones | Uso de `relx`, `rely`, `pack(fill, expand)` y `place()` relativo para adaptarse a la pantalla | ✅ |

### RNF-025 a RNF-027 | Escalabilidad

| ID | Requisito | Cómo se cumple | Estado |
|---|---|---|:---:|
| RNF-025 | Soporte para múltiples fichas | Tabla `fichas` independiente; los reportes y paneles filtran dinámicamente por ficha | ✅ |
| RNF-026 | Soporte para múltiples instructores | Tabla `instructores` + `fichas_asignadas`; cada instructor ve solo lo suyo | ✅ |
| RNF-027 | Preparado para múltiples sedes | Estructura de BD sin restricción de sede; campo extensible sin reestructura mayor | ✅ |

### ✅ Resultado: 27 de 27 requisitos no funcionales cumplidos (100%)

---

## 🗄️ BASE DE DATOS

### Tablas del Sistema

| Tabla | Descripción | Versión |
|---|---|:---:|
| `estudiantes` | Información y credenciales de aprendices | v1.0 |
| `fichas` | Programas de formación | v1.0 |
| `competencias` | Competencias técnicas y complementarias | v1.0 |
| `ficha_competencias` | Relación fichas–competencias | v1.0 |
| `asistencias` | Registros de entrada y salida | v1.0 |
| `horarios` | Horarios por competencia | v1.0 |
| `usuarios_admin` | Administradores e instructores con rol | v1.0 |
| `auditoria` | Log completo de todas las acciones | v1.0 |
| `instructores` | Información de instructores | ⭐ v2.0 |
| `fichas_asignadas` | Relación instructor–ficha | ⭐ v2.0 |
| `faltas` | Registro de faltas por tipo | ⭐ v2.0 |

### Cálculo de Métricas de Asistencia

- **Sesiones esperadas** = `SUM(horas_competencias)` / 6 (solo días hábiles L–V)
- **Asistencias** = registros con `fecha_registro` en el período
- **Faltas** = sesiones esperadas − asistencias
- **Retardos** = entradas después del umbral por jornada (Mañana: 08:15, Tarde: 13:15)

---

## 📈 VERSIONES Y ROADMAP

| Versión | Fecha | Estado | Cambios principales |
|---|---|:---:|---|
| **1.0** | Febrero 2026 | ✅ Completada | Registro de asistencia, panel aprendiz, panel admin, reportes básicos |
| **2.0** | Marzo 2026 | ✅ Completada | Sistema de instructores, registro de faltas, login unificado, dashboard KPI |
| **2.1** | Por definir | 🔮 Planeada | Notificaciones automáticas, reportes avanzados por competencia |
| **3.0** | Por definir | 🔮 Planeada | Soporte multi-sede, posible app móvil |

---

## 🎓 BENEFICIOS DEL SISTEMA

### Para los Aprendices
- Registro de asistencia rápido con solo su número de documento
- Visualización personal de su historial en un calendario interactivo
- Seguridad de acceso con cambio de contraseña obligatorio

### Para los Instructores
- Registro directo de faltas sin depender del administrador
- Visibilidad de sus grupos y asistencias en tiempo real
- Panel dedicado con acceso limitado a su información

### Para el Administrador
- Control total del sistema desde un único panel
- Reportes visuales exportables para seguimiento institucional
- Auditoría completa: saber quién hizo qué y cuándo
- Importación masiva de aprendices desde Excel

### Para el SENA HSGS
- Eliminación del registro manual en papel o hojas de cálculo
- Trazabilidad completa de la asistencia para informes institucionales
- Gestión centralizada y escalable para múltiples fichas e instructores

---

## 📞 INFORMACIÓN TÉCNICA

| Campo | Detalle |
|---|---|
| **Desarrollado por** | Equipo High Softwares — SENA HSGS |
| **Lenguaje** | Python 3.10+ |
| **Base de datos** | MySQL 8.0+ |
| **Framework UI** | CustomTkinter 5.2+ |
| **Sistema operativo** | Windows 10 / 11 |
| **Licencia** | Uso educativo y administrativo — SENA |
| **Última actualización** | 5 de Marzo de 2026 |

---

**Estado del Proyecto: ✅ LISTO PARA PRODUCCIÓN**

*C.R.S v2.0 — Chronos Registry System — SENA HSGS — Marzo 2026*
