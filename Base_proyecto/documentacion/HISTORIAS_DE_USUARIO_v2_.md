# 📋 Historias de Usuario — C.R.S v2.0
## Chronos Registry System | SENA - Centro Industrial del Diseño y la Manufactura CIDM

---

## HU-001: Registrar Asistencia (Aprendiz — Terminal)

**Como** aprendiz  
**Quiero** marcar mi entrada o salida ingresando mi número de documento  
**Para que** mi asistencia quede registrada automáticamente en el sistema

**Criterios de aceptación:**
- [x] La pantalla terminal muestra un campo grande para ingresar el documento
- [x] Botón **MARCAR ENTRADA** registra `fecha_registro` con hora actual
- [x] Botón **MARCAR SALIDA** registra `fecha_salida` (solo si hay entrada activa)
- [x] Mensaje de confirmación: "✅ Entrada Registrada con éxito" o "✅ Salida Registrada correctamente"
- [x] Error si el documento no existe en el sistema
- [x] Error si el aprendiz está en la papelera: "Contacte al administrador"
- [x] Error si intenta marcar entrada sin haber cerrado la anterior

**Estado:** ✅ Implementado en `main.py` → `_procesar_asistencia()` + `logica.py` → `registrar_entrada/salida()`

---

## HU-002: Ver Mi Historial de Asistencias (Aprendiz — Panel Personal)

**Como** aprendiz registrado  
**Quiero** consultar mis asistencias en un calendario interactivo mensual  
**Para que** pueda verificar mis días de presencia, entradas y salidas

**Criterios de aceptación:**
- [x] Pantalla muestra calendario mensual con días marcados por asistencia
- [x] Al seleccionar un día, muestra tarjetas con hora de entrada y salida
- [x] Mensaje "Sin actividad este día" si no hay registros
- [x] Calendario actualiza automáticamente al cambiar de mes
- [x] Panel derecho muestra "Actividad del día" con tarjetas por registro
- [x] Registros de entrada y salida con formato de hora `HH:MM`

**Estado:** ✅ Implementado en `dashboard_password.py` → `CalendarioPersonalizado` + `logica.py` → `obtener_registros_dia/mes()`

---

## HU-003: Cambiar Contraseña Obligatorio al Primer Login

**Como** aprendiz o instructor nuevo  
**Quiero** ser forzado a cambiar mi contraseña al ingresar por primera vez  
**Para que** mi cuenta sea segura y no use credenciales por defecto (`sena123`)

**Criterios de aceptación:**
- [x] Sistema detecta si `cambio_pass = 0` o si la clave es `sena123`
- [x] Muestra ventana emergente de cambio de contraseña obligatorio
- [x] Validación mínima de 4 caracteres para aprendices; 6 caracteres para instructores
- [x] El sistema actualiza `cambio_pass = 1` en BD tras el cambio
- [x] El usuario accede al panel solo después de cambiar la contraseña
- [x] Aplica tanto a aprendices como a instructores
- [x] La ventana de cambio de contraseña bloquea el cierre con la "X" (no se puede omitir)

**Estado:** ✅ Implementado en `dashboard_password.py` → `PasswordManager` y `main.py` → `actualizar_password_instructor_ventana()`

---

## HU-004: Login Unificado (Admin, Instructor y Aprendiz)

**Como** usuario del sistema  
**Quiero** acceder con mis credenciales desde una pantalla única de login  
**Para que** el sistema me dirija automáticamente al panel correspondiente a mi rol

**Criterios de aceptación:**
- [x] Pantalla de login con dos columnas: decorativa (SENA orange) y formulario
- [x] Sistema valida primero en `usuarios_admin` (admin e instructor)
- [x] Si no coincide, valida en tabla `instructores`
- [x] Si no coincide, valida en tabla `estudiantes` (aprendiz)
- [x] Redirige automáticamente al panel correcto según rol
- [x] Muestra error "Credenciales incorrectas" si ningún rol coincide
- [x] Login registrado en tabla `auditoria`

**Estado:** ✅ Implementado en `main.py` → `_procesar_login()`

---

## HU-005: Administrador Crea Aprendiz Manualmente

**Como** administrador  
**Quiero** registrar un nuevo aprendiz ingresando sus datos en un formulario  
**Para que** pueda acceder al sistema sin necesidad de un archivo Excel

**Criterios de aceptación:**
- [x] Formulario con campos: documento, nombre completo, correo, ficha
- [x] Validación de documento único (no duplicados)
- [x] Validación de formato de correo electrónico (mediante `validadores.py`)
- [x] Contraseña por defecto: `sena123` (se fuerza cambio en primer login)
- [x] Confirmación: "✅ Aprendiz creado exitosamente"
- [x] Botón para limpiar el formulario
- [x] Acción registrada en auditoría

**Estado:** ✅ Implementado en `admin_panel.py` → pestaña "REGISTRO" + `validadores.py` → `Validador`

---

## HU-006: Importar Aprendices desde Excel

**Como** administrador  
**Quiero** cargar un archivo `.xlsx` con múltiples aprendices  
**Para que** no tenga que ingresar manualmente cientos de registros

**Criterios de aceptación:**
- [x] Selector de archivo `.xlsx` con columnas: documento, nombre, correo, id_ficha
- [x] Preview de los datos antes de importar
- [x] Confirmación: "✅ N aprendices importados"
- [x] Validación de documentos duplicados
- [x] Rollback si hay error crítico durante la importación
- [x] Usa `pandas` y `openpyxl` para el procesamiento

**Estado:** ✅ Implementado en `logica.py` → `importar_excel()` + `admin_panel.py`

---

## HU-007: Gestión de Papelera (Admin)

**Como** administrador  
**Quiero** mover aprendices a una papelera en lugar de eliminarlos directamente  
**Para que** pueda recuperarlos si fue un error, manteniendo el historial

**Criterios de aceptación:**
- [x] Multiselección en tabla → botón "🗑️ MOVER A PAPELERA"
- [x] Confirmación antes de mover
- [x] Pestaña PAPELERA muestra aprendices desactivados (tabla `estudiantes_eliminados`)
- [x] Botón "♻️ RESTAURAR" devuelve el aprendiz al sistema activo
- [x] Botón "❌ ELIMINAR PERMANENTE" borra definitivamente
- [x] Todas las acciones registradas en auditoría

**Estado:** ✅ Implementado en `admin_panel.py` → pestaña "PAPELERA" + `logica.py` → `mandar_a_papelera()` / `restaurar_aprendiz()`

---

## HU-008: Instructor Registra Faltas ⭐ v2.0

**Como** instructor  
**Quiero** registrar las faltas de los aprendices de mis fichas asignadas  
**Para que** quede documentado el comportamiento de asistencia

**Criterios de aceptación:**
- [x] Instructor solo ve las fichas que tiene asignadas
- [x] Puede seleccionar un aprendiz de su ficha
- [x] Tres tipos de falta: **Inasistencia**, **Retardo**, **Justificada**
- [x] Campo opcional de observaciones/comentarios
- [x] La falta se guarda en tabla `faltas` con fecha, tipo y observación
- [x] Confirmación visual tras guardar
- [x] Acción registrada en auditoría

**Estado:** ✅ Implementado en `admin_panel.py` → `PantallaInstructor` → pestaña "REGISTRO DE FALTAS"

---

## HU-009: Instructor Consulta Historial de Sus Fichas ⭐ v2.0

**Como** instructor  
**Quiero** consultar el historial de asistencias de los aprendices de mis fichas  
**Para que** pueda hacer seguimiento sin necesidad del administrador

**Criterios de aceptación:**
- [x] Instructor ve solo sus fichas asignadas (no todas)
- [x] Tabla con registros de asistencia (entrada/salida) por ficha
- [x] Filtro por fecha para acotar resultados
- [x] Vista de aprendices asignados a cada ficha

**Estado:** ✅ Implementado en `admin_panel.py` → `PantallaInstructor` → pestaña "HISTORIAL"

---

## HU-010: Administrador Gestiona Instructores ⭐ v2.0

**Como** administrador  
**Quiero** crear instructores y asignarles fichas  
**Para que** cada instructor tenga acceso solo a sus grupos

**Criterios de aceptación:**
- [x] Formulario para crear instructor: documento, nombre, correo
- [x] Credenciales por defecto: `sena123` (cambio obligatorio al primer login)
- [x] Asignación de una o más fichas al instructor
- [x] Instructor solo ve y gestiona sus fichas asignadas
- [x] Registro en tabla `instructores` y relación en `fichas_asignadas`

**Estado:** ✅ Implementado en `admin_panel.py` → pestaña "GESTIÓN" + lógica de `logica.py`

---

## HU-011: Administrador Genera Reportes de Asistencia

**Como** administrador  
**Quiero** generar reportes visuales de asistencia por día, semana o mes  
**Para que** pueda analizar patrones y tomar decisiones informadas

**Criterios de aceptación:**
- [x] Filtro por modo: Ficha o Aprendiz individual
- [x] Filtro por rango: Día / Semana / Mes
- [x] Gráfico de barras con métricas: Asistencias (A), Faltas (F), Retardos (R)
- [x] Colores: verde (>80%), naranja (30-80%), rojo (<30%)
- [x] Sesiones esperadas calculadas automáticamente con días hábiles
- [x] Exportación a PDF y Excel
- [x] Acción registrada en auditoría

**Estado:** ✅ Implementado en `reportes.py` → `ReportesManager` + `logica.py` → `obtener_metricas_reporte_multiple()`

---

## HU-012: Administrador Consulta Dashboard de KPIs

**Como** administrador  
**Quiero** ver un panel resumen con métricas de hoy, esta semana y este mes  
**Para que** tenga una visión rápida del estado de asistencia

**Criterios de aceptación:**
- [x] Ventana emergente con 3 columnas: HOY / SEMANA / MES
- [x] Métricas: Asistencias, Faltas, Retardos por período
- [x] Selector de fecha de referencia con calendario interactivo
- [x] Colores adaptativos: verde si buena asistencia, rojo si baja
- [x] Cálculo automático de semana laboral (lunes–viernes)

**Estado:** ✅ Implementado en `dashboard_password.py` → `DashboardManager`

---

## HU-013: Exportar Reporte a PDF o Excel

**Como** administrador  
**Quiero** descargar el reporte generado en PDF o Excel  
**Para que** pueda enviarlo o imprimirlo

**Criterios de aceptación:**
- [x] Botón "📥 DESCARGAR" disponible tras generar reporte
- [x] Selector de formato: `.pdf` o `.xlsx`
- [x] PDF generado con `reportlab`: título, período, métricas por fila
- [x] Excel generado con `pandas`: columnas Periodo, Esperado, Asistencias, Faltas, Retardos
- [x] Dialogo nativo para elegir ubicación del archivo
- [x] Confirmación: "Reporte guardado en [ruta]"

**Estado:** ✅ Implementado en `main.py` → `exportar_reporte()`

---

## HU-014: Administrador Consulta Auditoría del Sistema

**Como** administrador  
**Quiero** ver un registro de todas las acciones realizadas en el sistema  
**Para que** pueda auditar cambios y detectar anomalías

**Criterios de aceptación:**
- [x] Tabla: usuario, acción, objeto, fecha, detalles
- [x] Registra: login, logout, creación, modificación, eliminación, reportes
- [x] Filtro por usuario y rango de fechas
- [x] Visualización de las últimas 100+ acciones
- [x] Cada acción registrada automáticamente desde cualquier módulo

**Estado:** ✅ Implementado en `admin_panel.py` → pestaña "AUDITORÍA" + `conexion.py` → `registrar_auditoria()`

---

## HU-015: Cierre de Sesión con Registro de Auditoría ⭐ v2.0

**Como** usuario autenticado (aprendiz, instructor o administrador)  
**Quiero** que al cerrar sesión el sistema registre mi logout  
**Para que** quede trazabilidad completa de los accesos y salidas del sistema

**Criterios de aceptación:**
- [x] Botón "CERRAR SESIÓN" visible en el header de cada panel de usuario
- [x] Al cerrar sesión de aprendiz: registra `"logout aprendiz"` en auditoría
- [x] Al cerrar sesión de instructor: registra `"logout instructor"` en auditoría
- [x] Al cerrar sesión de administrador: redirige a pantalla de inicio
- [x] Se limpia la variable de sesión activa (`aprendiz_actual`, `instructor_actual`, `admin_actual`)
- [x] Si el registro de auditoría falla, se registra un warning en el log pero no se bloquea el cierre

**Estado:** ✅ Implementado en `main.py` → `mostrar_panel_aprendiz()` (función `cerrar_aprendiz`) y `mostrar_panel_instructor_ui()` (función `cerrar_instructor`)

---

## Matriz de Trazabilidad

| Módulo | HU-01 | HU-02 | HU-03 | HU-04 | HU-05 | HU-06 | HU-07 | HU-08 | HU-09 | HU-10 | HU-11 | HU-12 | HU-13 | HU-14 | HU-15 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `main.py` | ✓ | | ✓ | ✓ | | | | | | | | | ✓ | | ✓ |
| `logica.py` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `admin_panel.py` | | | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | | | ✓ | |
| `dashboard_password.py` | | ✓ | ✓ | | | | | | | | | ✓ | | | |
| `reportes.py` | | | | | | | | | | | ✓ | | ✓ | | |
| `conexion.py` | ✓ | ✓ | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ |
| `validadores.py` | | | ✓ | | ✓ | | | | | | | | | | |

---

*Última actualización: 10 de Marzo de 2026 — C.R.S v2.0*
