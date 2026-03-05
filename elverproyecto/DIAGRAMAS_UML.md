# 📐 Diagramas UML — C.R.S v2.0
## Chronos Registry System | SENA - Centro de Gestión Administrativa HSGS

---

## 1. Diagrama de Casos de Uso

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SISTEMA C.R.S v2.0                                   │
│                    (Chronos Registry System)                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────┐      ┌──────────────┐      ┌──────────────────────────────┐
  │   APRENDIZ  │      │  INSTRUCTOR  │      │       ADMINISTRADOR          │
  └──────┬──────┘      └──────┬───────┘      └──────────────┬───────────────┘
         │                    │                             │
    ┌────┴────┐          ┌────┴────┐                  ┌─────┴──────┐
    ▼         ▼          ▼         ▼                  ▼            ▼
┌───────┐ ┌───────┐ ┌─────────┐ ┌──────────┐  ┌──────────┐ ┌──────────────┐
│Marcar │ │  Ver  │ │Registrar│ │Consultar │  │ Gestión  │ │  Reportes /  │
│Entrada│ │  Mi   │ │ Faltas  │ │Historial │  │Aprendices│ │  Dashboard   │
│/Salida│ │Histor.│ │(Tipo)   │ │Su Ficha  │  │Instructo.│ │  PDF / Excel │
└───────┘ └───────┘ └─────────┘ └──────────┘  └──────────┘ └──────────────┘
                                                    │
                          ┌─────────────────────────┼──────────────────┐
                          ▼                         ▼                  ▼
                    ┌──────────┐             ┌──────────┐       ┌──────────┐
                    │ Importar │             │ Papelera │       │Auditoría │
                    │  Excel   │             │Restaurar │       │ Sistema  │
                    └──────────┘             └──────────┘       └──────────┘

 ◄── Todos los usuarios pasan primero por ──►
      ┌───────────────────────────┐
      │  LOGIN UNIFICADO + AUTH   │ ← valida rol y redirige al panel correcto
      │  (Admin / Instructor /    │
      │   Aprendiz)               │
      └───────────────────────────┘
              │
              ▼
      ┌───────────────────────────┐
      │  CAMBIO DE CONTRASEÑA     │ ← Obligatorio si cambio_pass = 0
      │  (Primer login)           │
      └───────────────────────────┘
```

---

## 2. Diagrama de Clases

```
┌──────────────────────────┐
│      InventarioDB        │   (conexion.py)
├──────────────────────────┤
│ - conexion               │
│ - cursor                 │
├──────────────────────────┤
│ + insertar()             │
│ + registrar_auditoria()  │
│ + ejecutar_query()       │
└────────────┬─────────────┘
             │ usa
             ▼
┌──────────────────────────────────┐
│        AsistenciaService         │   (logica.py)
├──────────────────────────────────┤
│ - db                             │
├──────────────────────────────────┤
│ + registrar_entrada()            │
│ + registrar_salida()             │
│ + login_aprendiz()               │
│ + login_instructor()             │
│ + actualizar_password()          │
│ + obtener_fichas()               │
│ + obtener_registros_dia()        │
│ + obtener_registros_mes()        │
│ + importar_excel()               │
│ + mandar_a_papelera()            │
│ + restaurar_aprendiz()           │
│ + obtener_metricas_reporte_      │
│   multiple()                     │
│ + _calcular_dias_habiles()       │
│ + _calcular_sesiones_esperadas() │
└──────────────┬───────────────────┘
               │ usa
               ▼
┌─────────────────────────────────────┐
│         SistemaHSGSCRS              │   (main.py)
├─────────────────────────────────────┤
│ - root                              │
│ - db: InventarioDB                  │
│ - servicio: AsistenciaService       │
│ - admin_actual                      │
│ - aprendiz_actual                   │
│ - instructor_actual                 │
│ - frames: dict                      │
│ - reportes_manager: ReportesManager │
│ - dashboard_manager: DashboardMgr   │
│ - password_manager: PasswordManager │
│ - _cache_fichas                     │
│ - _cache_aprendices                 │
├─────────────────────────────────────┤
│ + show_frame()                      │
│ + _procesar_login()                 │
│ + _procesar_asistencia()            │
│ + mostrar_panel_aprendiz()          │
│ + mostrar_panel_admin_ui()          │
│ + mostrar_panel_instructor_ui()     │
│ + exportar_reporte()                │
│ + obtener_fichas_cached()           │
│ + limpiar_cache()                   │
└──────────────┬──────────────────────┘
               │ delega en
    ┌──────────┼────────────┬──────────────┐
    ▼          ▼            ▼              ▼
┌──────────┐ ┌──────────┐ ┌────────────┐ ┌─────────────────┐
│Pantalla  │ │Pantalla  │ │Reportes    │ │DashboardManager │
│Administ. │ │Instructor│ │Manager     │ │PasswordManager  │
│(admin_   │ │(admin_   │ │(reportes   │ │(dashboard_      │
│panel.py) │ │panel.py) │ │.py)        │ │password.py)     │
└──────────┘ └──────────┘ └────────────┘ └─────────────────┘
```

---

## 3. Diagrama de Secuencia — Login y Acceso por Rol

```
USUARIO        main.py              logica.py            BD (MySQL)
   │               │                    │                    │
   ├─ ingresa ────►│                    │                    │
   │  usuario +    │                    │                    │
   │  contraseña   │                    │                    │
   │               ├─ query admin ─────────────────────────►│
   │               │                    │                    │
   │               │◄──────────────────────── resultado ─────┤
   │               │  (admin/instructor │    de BD           │
   │               │   o vacío)         │                    │
   │               │                    │                    │
   │               ├─ si no: login_instructor() ───────────►│
   │               │◄──────────────────────── resultado ─────┤
   │               │                    │                    │
   │               ├─ si no: login_aprendiz() ─────────────►│
   │               │◄──────────────────────── resultado ─────┤
   │               │                    │                    │
   │               ├─ registrar_auditoria("login X") ───────►│
   │               │                    │                    │
   │               ├─ ¿cambio_pass=0? ──►│                  │
   │               │◄── Sí/No ──────────┤                   │
   │               │                    │                    │
   │  ◄─ Panel de ─┤                    │                    │
   │    su rol     │                    │                    │
```

---

## 4. Diagrama de Secuencia — Registro de Asistencia (Terminal)

```
APRENDIZ        Terminal UI          AsistenciaService       BD
   │                │                      │                  │
   ├─ ingresa ─────►│                      │                  │
   │  documento      │                      │                  │
   │                 │                      │                  │
   ├─ click ─────────┤                      │                  │
   │  MARCAR ENTRADA │                      │                  │
   │                 ├─ registrar_entrada() ►│                  │
   │                 │                      ├─ SELECT exist ──►│
   │                 │                      │◄─ resultado ─────┤
   │                 │                      │                  │
   │                 │                      ├─ SELECT entrada  │
   │                 │                      │  activa? ───────►│
   │                 │                      │◄─ resultado ─────┤
   │                 │                      │                  │
   │                 │                      ├─ INSERT asist. ─►│
   │                 │◄─ True, "✅ Éxito" ──┤◄─ commit ────────┤
   │                 │                      │                  │
   │◄─ messagebox ───┤                      │                  │
   │  "Entrada OK"   │                      │                  │
```

---

## 5. Diagrama de Secuencia — Registro de Falta (Instructor) ⭐ v2.0

```
INSTRUCTOR     PantallaInstructor    AsistenciaService      BD
   │                 │                     │                 │
   ├─ selecciona ───►│                     │                 │
   │  ficha +        │                     │                 │
   │  aprendiz       │                     │                 │
   │                 │                     │                 │
   ├─ selecciona ───►│                     │                 │
   │  tipo de falta  │                     │                 │
   │  (Inasistencia/ │                     │                 │
   │   Retardo/      │                     │                 │
   │   Justificada)  │                     │                 │
   │                 │                     │                 │
   ├─ click ─────────┤                     │                 │
   │  REGISTRAR      ├─ INSERT faltas() ──►│                 │
   │                 │                     ├─ INSERT ───────►│
   │                 │                     │◄─ commit ───────┤
   │                 │                     │                 │
   │                 │                     ├─ registrar_     │
   │                 │                     │  auditoria() ──►│
   │◄─ confirmación ─┤                     │                 │
```

---

## 6. Diagrama de Secuencia — Generación de Reporte

```
ADMIN          ReportesManager       AsistenciaService         BD
  │                  │                      │                   │
  ├─ selecciona ────►│                      │                   │
  │  filtros         │                      │                   │
  │  (modo, rango,   │                      │                   │
  │   fecha)         │                      │                   │
  │                  │                      │                   │
  ├─ click ──────────┤                      │                   │
  │  GENERAR         ├─ obtener_metricas_  ►│                   │
  │                  │  reporte_multiple()  ├─ query ──────────►│
  │                  │                      │  (asistencias,    │
  │                  │                      │   faltas, horas)  │
  │                  │                      │◄─ resultados ─────┤
  │                  │◄─ {A, F, R,          │                   │
  │                  │   esperadas} ────────┤                   │
  │                  │                      │                   │
  │                  ├─ dibujar canvas ────►│                   │
  │                  │  (barras A/F/R)      │                   │
  │◄─ gráfico ───────┤                      │                   │
  │  visible         │                      │                   │
  │                  │                      │                   │
  ├─ click ──────────┤                      │                   │
  │  EXPORTAR        ├─ exportar_reporte() ►│                   │
  │                  │  (PDF / Excel)       │                   │
  │◄─ archivo ───────┤                      │                   │
  │  descargado      │                      │                   │
```

---

## 7. Modelo de Base de Datos — Diagrama ER Completo (v2.0)

```
┌──────────────────┐           ┌──────────────────────┐
│    FICHAS        │           │   COMPETENCIAS       │
├──────────────────┤           ├──────────────────────┤
│ id_ficha (PK)    │           │ id_competencia (PK)  │
│ codigo_ficha     │           │ nombre_competencia   │
│ nombre_programa  │           │ horas_totales        │
│ jornada          │           │ tipo (Técnica/Compl.)│
│ fecha_inicio     │           └──────────┬───────────┘
└────────┬─────────┘                      │
         │ 1                              │ N
         │ N                              │
         └────────────┬───────────────────┘
                      │
              ┌───────┴──────────────┐
              │  FICHA_COMPETENCIAS  │
              ├──────────────────────┤
              │ id (PK)              │
              │ id_ficha (FK)        │
              │ id_competencia (FK)  │
              │ orden                │
              └──────────────────────┘

┌──────────────────────┐           ┌─────────────────────────┐
│    ESTUDIANTES       │           │      INSTRUCTORES ⭐     │
├──────────────────────┤           ├─────────────────────────┤
│ id_estudiante (PK)   │           │ id_instructor (PK)      │
│ documento (UQ)       │           │ documento (UQ)          │
│ nombre_completo      │           │ nombre_completo         │
│ correo               │           │ correo                  │
│ password             │           │ password                │
│ id_ficha (FK) ───────┼───┐       │ cambio_pass             │
│ cambio_pass          │   │       └────────────┬────────────┘
│ estado               │   │                    │ 1
└──────────┬───────────┘   │                    │ N
           │ 1             │       ┌────────────┴────────────┐
           │ N             │       │   FICHAS_ASIGNADAS ⭐   │
           │               │       ├─────────────────────────┤
┌──────────┴───────────┐   │       │ id (PK)                 │
│    ASISTENCIAS       │   │       │ id_instructor (FK)      │
├──────────────────────┤   │       │ id_ficha (FK) ──────────┼──► FICHAS
│ id_asistencia (PK)   │   │       └─────────────────────────┘
│ documento_est. (FK)  │   │
│ id_competencia (FK)  │   └───────► FICHAS
│ fecha_registro       │
│ fecha_salida         │   ┌─────────────────────┐
│ observaciones        │   │     FALTAS ⭐        │
└──────────────────────┘   ├─────────────────────┤
                           │ id_falta (PK)        │
┌──────────────────────┐   │ documento_est. (FK) ─┼──► ESTUDIANTES
│    USUARIOS_ADMIN    │   │ id_instructor (FK) ──┼──► INSTRUCTORES
├──────────────────────┤   │ tipo_falta           │
│ id (PK)              │   │ (Inasistencia/       │
│ usuario              │   │  Retardo/Justificada)│
│ password             │   │ fecha_falta          │
│ tipo_usuario         │   │ observacion          │
│ (admin/instructor)   │   └─────────────────────┘
└──────────────────────┘
                           ┌─────────────────────┐
                           │    AUDITORIA        │
                           ├─────────────────────┤
                           │ id (PK)             │
                           │ usuario             │
                           │ accion              │
                           │ objeto              │
                           │ detalles            │
                           │ fecha (TIMESTAMP)   │
                           └─────────────────────┘
```

---

## 8. Diagrama de Arquitectura por Capas

```
┌─────────────────────────────────────────────────────────┐
│                  CAPA DE PRESENTACIÓN                    │
│                                                         │
│   main.py          admin_panel.py    dashboard_         │
│   SistemaHSGSCRS   PantallaAdmin     password.py        │
│   (UI Principal)   PantallaInstructor DashboardMgr      │
│                                      PasswordManager    │
│                    reportes.py        CalendarioCustom   │
│                    ReportesManager                      │
│                                                         │
│   Librerías UI: customtkinter, tkinter, tkcalendar      │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   CAPA DE LÓGICA                         │
│                                                         │
│   logica.py → AsistenciaService                         │
│   validadores.py → Validador                            │
│   config.py → COLORES, FUENTES, CACHE                   │
│   logging_config.py → configure_logging()               │
│   ui_helper.py → funciones auxiliares UI                │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE DATOS                         │
│                                                         │
│   conexion.py → InventarioDB                            │
│   .env → credenciales BD (python-dotenv)                │
│   MySQL 8.0 → techsenahsgs.sql                          │
│                                                         │
│   Tablas: estudiantes, instructores, asistencias,       │
│   fichas, competencias, ficha_competencias,             │
│   fichas_asignadas, faltas, usuarios_admin, auditoria   │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Diagrama de Flujo — Flujo General del Sistema

```
                    ┌──────────────┐
                    │  Inicio App  │
                    │  python      │
                    │  main.py     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Animación   │
                    │  C.R.S intro │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Pantalla    │
                    │  de Inicio   │
                    └──────┬───────┘
                           │
             ┌─────────────┼──────────────┐
             ▼             ▼              ▼
      ┌────────────┐ ┌──────────┐   ┌──────────┐
      │  Terminal  │ │  LOGIN   │   │  SALIR   │
      │ Asistencia │ │Unificado │   └──────────┘
      └─────┬──────┘ └────┬─────┘
            │             │
            ▼             ▼
      ┌──────────┐  ┌──────────────────────────────┐
      │ Ingresa  │  │ Valida en BD                 │
      │documento │  │ ¿Admin? → Panel Admin        │
      └─────┬────┘  │ ¿Instructor? → Panel Instr.  │
            │       │ ¿Aprendiz? → Panel Aprendiz  │
            ▼       │ ¿Nadie? → Error login        │
      ┌──────────┐  └──────────────────────────────┘
      │ Entrada  │
      │ o Salida │
      │ en BD    │
      └──────────┘
```

---

## Notas Arquitectónicas

**Patrón de diseño:** El sistema sigue una arquitectura en 3 capas (Presentación / Lógica / Datos) con delegación por clases especializadas.

**Caché:** `SistemaHSGSCRS` implementa caché para fichas (TTL: 1 hora) y aprendices (TTL: 30 min) para mejorar rendimiento en consultas frecuentes.

**Auditoría:** Toda acción relevante llama a `InventarioDB.registrar_auditoria()`, garantizando trazabilidad completa del sistema.

**Tablas nuevas en v2.0:** `instructores`, `fichas_asignadas`, `faltas` permiten el sistema de gestión de faltas por instructores sin modificar la estructura original.

---

*Última actualización: 5 de Marzo de 2026 — C.R.S v2.0*
