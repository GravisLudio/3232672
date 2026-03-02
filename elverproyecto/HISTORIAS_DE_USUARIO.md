# Historias de Usuario - Sistema CRS (Chronos Registry System)

## HU-001: Registrar Asistencia (Aprendiz)
**Como** aprendiz  
**Quiero** marcar mi entrada/salida mediante documento  
**Para que** se registre automáticamente mi asistencia

**Criterios de aceptación:**
- [ ] Pantalla terminal muestra input documento
- [ ] Entrada: registra fecha_registro + compara con horario esperado
- [ ] Salida: registra fecha_salida (solo si hay entrada activa)
- [ ] Mensaje: "✓ Entrada registrada 07:45" o "⚠ Retardo 08:32"
- [ ] Error si documento no existe o está en papelera

---

## HU-002: Ver Mi Historial de Asistencias (Aprendiz)
**Como** aprendiz registrado  
**Quiero** consultar mis asistencias por día/semana  
**Para que** pueda verificar mi desempeño

**Criterios de aceptación:**
- [ ] Pantalla muestra calendario seleccionable
- [ ] Seleccionar día → muestra entrada/salida de ese día
- [ ] Card con hora entrada (📥) y salida (📤)
- [ ] "Sin actividad este día" si no hay registros
- [ ] Ordenado DESC por fecha_registro

---

## HU-003: Administrador Genera Reporte de Asistencias (Admin)
**Como** administrador  
**Quiero** generar reportes de asistencia por día/semana/mes para fichas o individuos  
**Para que** evalúe desempeño y detecte patrones de inasistencia

**Criterios de aceptación:**
- [ ] Segmentado: selecciona rango (Día/Semana/Mes)
- [ ] Filtros: Fichas O Aprendices individuales
- [ ] Canvas muestra:
  - **Día:** A (asistencias), F (faltas), R (retardos) en 1 barra
  - **Semana:** 4 barras (semanas mes) con A/F/R c/u
  - **Mes:** 12 barras (meses año) con A/F/R c/u
- [ ] Colores: verde (>80%), naranja (30-80%), rojo (<30%)
- [ ] Cálculo: Sesiones esperadas = días_hábiles × (horas_ficha / 6)

---

## HU-004: Registrar Aprendiz Manual (Admin)
**Como** administrador  
**Quiero** crear estudiante nuevo manualmente sin Excel  
**Para que** entre al sistema rápidamente

**Criterios de aceptación:**
- [ ] Form: documento, nombre_completo, correo, id_ficha
- [ ] Validación: documento único, email formato
- [ ] Botón guardar → "✓ Aprendiz creado"
- [ ] Contraseña default: sena123 → força cambio al login
- [ ] Botón limpiar vacia todos campos

---

## HU-005: Importar Aprendices desde Excel (Admin)
**Como** administrador  
**Quiero** cargar múltiples estudiantes de Excel  
**Para que** no ingrese manualmente 100+ registros

**Criterios de aceptación:**
- [ ] Selector archivo: .xlsx con columnas [documento, nombre, correo, id_ficha]
- [ ] Preview: muestra N registros a importar
- [ ] Botón importar → "✓ 45 aprendices cargados"
- [ ] Validar: documento duplicado, email formato
- [ ] Rollback si hay error crítico

---

## HU-006: Mover Aprendiz a Papelera (Admin)
**Como** administrador  
**Quiero** desactivar aprendices sin borrar datos  
**Para que** mantenga historial auditble

**Criterios de aceptación:**
- [ ] Multiselect en tabla → botón "🗑️ MOVER A PAPELERA"
- [ ] Confirmación: "¿Desea mover 3 aprendices?"
- [ ] Registra: auditoria (usuario, acción, fecha)
- [ ] Tab PAPELERA muestra aprendices "borrados"
- [ ] Botón "♻️ RESTAURAR" devuelve a estudantes

---

## HU-007: Cambiar Contraseña Obligatorio (Aprendiz)
**Como** aprendiz nuevo  
**Quiero** cambiar mi contraseña al primer login  
**Para que** mi cuenta sea segura

**Criterios de aceptación:**
- [ ] Modal popup al login (si cambio_pass = 0)
- [ ] Validar: ≥8 caracteres, 1 mayúscula, 1 minúscula, 1 número
- [ ] Indicador: ✓ verde cuando cumple todo
- [ ] Guardar → actualiza BD, entra al panel
- [ ] Atrás → cierra sesión

---

## HU-008: Ver Auditoría de Acciones Admin (Admin)
**Como** administrador  
**Quiero** ver historial de quién hizo qué y cuándo  
**Para que** audite cambios y detecte anomalías

**Criterios de aceptación:**
- [ ] Tabla: usuario, acción, objeto, fecha, detalles
- [ ] Filtros: por usuario, rango fechas
- [ ] 100 últimas acciones visible
- [ ] Exportar a CSV disponible
- [ ] Acciones: login, logout, crear aprendiz, mover papelera, etc.

---

## HU-009: Exportar Reporte a PDF (Admin)
**Como** administrador  
**Quiero** descargar reporte de asistencias en PDF  
**Para que** lo envíe por correo o imprima

**Criterios de aceptación:**
- [ ] Botón "📥 DESCARGAR PDF" en reporte
- [ ] PDF contiene: título, fecha, filtros, gráfico, tabla de detalles
- [ ] Nombrado: reporte_asistencias_2026-03-02.pdf
- [ ] Logo SENA en encabezado

---

## HU-010: Calcular Sesiones Esperadas Automáticamente (System)
**Como** sistema  
**Quiero** que se calculen sesiones esperadas automáticamente  
**Para que** faltas y retardos sean precisos

**Criterios de aceptación:**
- [ ] Sesión = 6 horas (estándar)
- [ ] Sesiones esperadas = SUM(horas_competencias_ficha) / 6
- [ ] Solo cuenta días hábiles (lunes-viernes)
- [ ] Limita hasta fecha_inicio + fecha_hoy
- [ ] Retardo detectado por jornada: Mañana 08:15, Tarde 13:15

---

## Matriz de Trazabilidad (Módulo → HU)

| Módulo | HU-001 | HU-002 | HU-003 | HU-004 | HU-005 | HU-006 | HU-007 | HU-008 | HU-009 | HU-010 |
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| Terminal Aprendices | ✓ | | | | | | | | | |
| Panel Aprendiz | | ✓ | | | | | ✓ | | | |
| Panel Admin - Gestión | | | | ✓ | ✓ | ✓ | | ✓ | | |
| Panel Admin - Reportes | | | ✓ | | | | | | ✓ | ✓ |
| Backend (logica.py) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

