# Diagramas UML - Sistema CRS

## Diagrama de Casos de Uso

```
┌─────────────────────────────────────────────────────────────┐
│                      SISTEMA CRS                            │
│           (Chronos Registry System)                         │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────────┐                    ┌──────────────────┐
    │    APRENDIZ      │                    │  ADMINISTRADOR   │
    └────────┬─────────┘                    └────────┬─────────┘
             │                                       │
    ┌────────┴─────────────┐            ┌───────────┴──────────┐
    │                      │            │                      │
    ▼                      ▼            ▼                       ▼
┌─────────────┐    ┌─────────────┐  ┌──────────────┐  ┌────────────────┐
│ Registrar   │    │ Ver Mi      │  │ Generar      │  │ Gestionar      │
│ Entrada/    │    │ Historial   │  │ Reportes de  │  │ Aprendices     │
│ Salida      │    │ Asistencia  │  │ Asistencia   │  │ (CRUD)         │
└─────────────┘    └─────────────┘  └──────────────┘  └────────────────┘
                                            │
                                            ▼
                                     ┌──────────────┐
                                     │ Exportar a   │
                                     │ PDF / Excel  │
                                     └──────────────┘

┌──────────────────┐
│ SISTEMA          │◄──────────────┬──────────────┬─────────────┐
│ (BD, Auditoría)  │               │              │             │
└─────────────────┘    ┌──────────────┐  ┌──────────────┐  ┌──────────┐
                       │ Login / Auth  │  │   Auditoría  │  │ Calcular │
                       │               │  │   Cambios    │  │ Métricas │
                       └──────────────┘  └──────────────┘  └──────────┘
```

---

## Diagrama de Clases

```
┌────────────────────┐
│  InventarioDB      │
├────────────────────┤
│ - conexion         │
│ - cursor           │
├────────────────────┤
│ + registrar_entrada│
│ + registrar_salida │
│ + registrar_audit. │
│ + ejecutar_query   │
└────────────────────┘

┌────────────────────────┐
│  AsistenciaService     │
├────────────────────────┤
│ - db                   │
├────────────────────────┤
│ + registrar_entrada()  │
│ + registrar_salida()   │
│ + login_aprendiz()     │
│ + obtener_fichas()     │
│ + importar_excel()     │
│ + obtener_metricas_    │
│   reporte_multiple()   │
│ + mandar_a_papelera()  │
│ + restaurar_aprendiz() │
│ + _calcular_dias_      │
│   habiles()            │
│ + _calcular_sesiones_  │
│   esperadas()          │
└────────────────────────┘
         ▲
         │ usa
         │
┌────────────────────────┐
│ SistemaHSGSCRS (main)  │
├────────────────────────┤
│ - root                 │
│ - db                   │
│ - servicio             │
│ - canvas_rep           │
│ - items_seleccionados  │
├────────────────────────┤
│ + mostrar_login()      │
│ + mostrar_panel_admin()│
│ + crear_pestana_       │
│   reportes()           │
│ + lanzar_reporte()     │
│ + mostrar_selector_    │
│   rango()             │
└────────────────────────┘
```

---

## Diagrama de Secuencia - Generar Reporte

```
ADMIN          UI              SERVICIO          BD
  │              │                 │               │
  ├─ Click ───────────────────────►│               │
  │  Generar                       │               │
  │              │                 │               │
  │              ├─ Validar ──────►│               │
  │              │  Filtros        │               │
  │              │◄── OK ──────────┤               │
  │              │                 │               │
  │              ├─ obtener_       │               │
  │              │  metricas_      │               │
  │              │  reporte_       ├─ Query ──────►│
  │              │  multiple()     │ (ficha,fecha) │
  │              │                 │               │
  │              │                 │◄─ resultado ──┤
  │              │                 │  (A,F,R)      │
  │              │◄─ métricas ─────┤               │
  │              │                 │               │
  │              ├─ Dibujar ──────►│               │
  │              │  Canvas         │               │
  │              │  (barras)       │               │
  │              │                 │               │
  ◄──────────────┤ Mostrar ────────┤               │
  │  Reporte    │  Gráfico        │               │
  │  Visual     │                 │               │
```

---

## Flujo de Proceso - Reporte Mes

```
     ┌─────────────────┐
     │ Administrador   │
     │ Selecciona      │
     │ MES (sin       │
     │ especificar)    │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ Detectar mes    │
     │ actual (hoy=    │
     │ 2 marzo 2026)   │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────────────────┐
     │ Generar loop 1-3 (ene-mar)  │
     │ Solo until month(today)     │
     └────────┬────────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │ Para cada mes:               │
   │ ├─ Llamar                    │
   │ │  obtener_metricas_         │
   │ │  reporte_multiple()        │
   │ ├─ Recibir A, F, R          │
   │ └─ Acumular datos            │
   └────────┬─────────────────────┘
            │
            ▼
   ┌──────────────────────────────┐
   │ Dibujar en Canvas 3 barras:  │
   │ ├─ Enero: A:10 F:2 R:1      │
   │ ├─ Febrero: A:12 F:1 R:3    │
   │ └─ Marzo: A:5 F:3 R:0       │
   └────────┬─────────────────────┘
            │
            ▼
   ┌──────────────────────────────┐
   │ Mostrar Gráfico al Admin     │
   └──────────────────────────────┘
```

---

## Modelo de Base de Datos (ER Simplificado)

```
┌──────────────────┐
│     FICHAS       │
├──────────────────┤
│ id_ficha (PK)    │
│ codigo_ficha     │
│ nombre_programa  │
│ jornada          │
│ fecha_inicio     │
└────────┬─────────┘
         │ 1
         │
         │ N
┌────────┴──────────────────┐
│  FICHA_COMPETENCIAS       │
├───────────────────────────┤
│ id (PK)                   │
│ id_ficha (FK)             │
│ id_competencia (FK)       │
│ orden                     │
└────────┬──────────────────┘
         │
         └──────────────────────┐
                                │ N
                                │
                        ┌───────┴──────────────┐
                        │   COMPETENCIAS       │
                        ├──────────────────────┤
                        │ id_competencia (PK)  │
                        │ nombre_competencia   │
                        │ horas_totales        │
                        │ tipo (Técnica/Compl.)│
                        └──────────────────────┘

┌────────────────────┐
│  ESTUDIANTES       │
├────────────────────┤
│ id_estudiante (PK) │
│ documento (UQ)     │
│ nombre_completo    │
│ correo             │
│ password           │
│ id_ficha (FK)  ───────────┐
│ cambio_pass        │       │
└────────────────────┘       │
         │ 1                 │
         │                   │
         │ N                 │
         │ ┌─────────────────┘
         │ │
┌────────┴┴─────────────┐
│   ASISTENCIAS         │
├───────────────────────┤
│ id_asistencia (PK)    │
│ documento_est. (FK)   │
│ id_competencia (FK)   │
│ fecha_registro        │
│ fecha_salida          │
│ observaciones         │
└───────────────────────┘

┌───────────────────────┐
│   AUDITORIA           │
├───────────────────────┤
│ id (PK)               │
│ usuario               │
│ accion                │
│ objeto                │
│ detalles              │
│ fecha (TIMESTAMP)     │
└───────────────────────┘
```

---

## Notas Arquitectónicas

1. **Separación de capas:**
   - **Presentación:** `main.py` (tkinter/customtkinter)
   - **Lógica:** `logica.py` (AsistenciaService)
   - **Datos:** `conexion.py` (InventarioDB)

2. **Cálculo de Métricas:**
   - **Sesiones esperadas** = SUM(horas_competencias) / 6 (solo días hábiles)
   - **Asistencia** = registro entrada en fecha
   - **Falta** = sesión esperada - asistencia
   - **Retardo** = entrada > umbral por jornada

3. **Relación Ficha-Competencia:**
   - Tabla relacional `ficha_competencias` permite N:M
   - Cada ficha puede tener múltiples competencias
   - SUM(horas) proporciona duración total programa

