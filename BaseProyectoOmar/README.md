# Proyecto CRS

Aplicación de escritorio para registro y reporte de asistencias (Chronos Registry System).

## Requisitos

- Python 3.11+
- MySQL (ej. WAMP/XAMPP) base de datos `TechSenaHSGS`
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Funcionalidades principales

- Terminal de aprendices para marcar entrada/salida.
- Panel administrativo con:
  - Historial de asistencias
  - Gestión de aprendices (crear, importar Excel, papelera, restaurar)
  - Generación de reportes por día/semana/mes con gráficos A/F/R
  - Exportar reportes a PDF/Excel
  - Dashboard de KPIs (hoy, semana, mes)
  - Auditoría de acciones

## Migraciones

Para actualizar esquema:

```sql
-- agregar fecha_inicio a fichas
ALTER TABLE `fichas` ADD COLUMN `fecha_inicio` date DEFAULT NULL;

-- crear relación ficha_competencias
-- ejecutar script migrate_ficha_competencias.sql
```

## Cómo ejecutar

```bash
python main.py
```

Iniciar sesión admin con `admin/admin123`.
