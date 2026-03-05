# 📱 **C.R.S - CHRONOS REGISTRY SYSTEM**

## Sistema Integrado de Gestión de Asistencia y Registro de Faltas

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-green)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-orange)
![License](https://img.shields.io/badge/License-SENA-brightgreen)

---

## 📌 **DESCRIPCIÓN DEL PROYECTO**

**C.R.S** es un sistema desktop de gestión de asistencia desarrollado para el **SENA - Centro de Gestión Administrativa (HSGS)** que permite:

✅ Registro de entrada/salida de aprendices  
✅ Gestión de fichas y competencias  
✅ Panel de aprendiz con calendario interactivo  
✅ Panel de instructor con registro de faltas  
✅ Panel de administrador con gestión total  
✅ Generación de reportes de asistencia  
✅ Auditoría completa de todas las acciones  

**Versión Actual**: 2.0 (Con sistema de Instructores y Registro de Faltas)

---

## 🎯 **CARACTERÍSTICAS PRINCIPALES**

### 👨‍💻 **Panel de Aprendiz**
- 📅 Calendario interactivo mensual con asistencias
- 📊 Visualización de entrada/salida por día
- 🔐 Cambio de contraseña automática al primer login
- 📱 Interfaz intuitiva y responsiva

### 👨‍🏫 **Panel de Instructor** ⭐ NUEVO
- 📋 Historial de asistencias por ficha
- ❌ **Registro de faltas** (Inasistencia, Retardo, Justificada)
- 📊 Reportes de asistencia
- 🎓 Gestión de estudiantes asignados

### 👨‍💼 **Panel de Administrador**
- 📋 Historial completo de asistencias
- 👥 Gestión de aprendices (CRUD)
- ➕ Registro manual y importación Excel
- 📊 Generación de reportes avanzados
- 🗑️ Papelera con restauración
- 🔍 Auditoría de todas las acciones
- 👥 Gestión de instructores

---

## 🗄️ **ESTRUCTURA DE BASE DE DATOS**

### Tablas Principales
- `estudiantes` - Información de aprendices
- `fichas` - Fichas técnicas/programas
- `competencias` - Competencias técnicas y complementarias
- `asistencias` - Registros de entrada/salida
- `horarios` - Horarios de clases por competencia
- `usuarios_admin` - Administradores (con tipo_usuario)

### Tablas Nuevas (v2.0) ⭐
- `instructores` - Información de instructores
- `fichas_asignadas` - Relación instructor-fichas
- `faltas` - Registro de faltas con tipos

### Tabla de Auditoría
- `auditoria` - Registro de todas las acciones del sistema

---

## 🔐 **TIPOS DE USUARIOS Y ACCESO**

| Usuario | Usuario/Pass | Acceso | Funcionalidades |
|---------|-------------|--------|-----------------|
| **Admin** | admin / admin123 | Panel Completo | Todas las del sistema |
| **Instructor** | instructor1 / sena123 | Panel Limitado | Historial, Reportes, **Registro de Faltas** |
| **Aprendiz** | 1010101 / pass123 | Panel Personal | Calendario, Historial propio |

---

## 💻 **REQUISITOS DEL SISTEMA**

### Hardware
- Procesador: Intel i5 o equivalente
- RAM: 4 GB mínimo
- Almacenamiento: 500 MB libres

### Software
- **Python 3.10 o superior**
- **MySQL 8.0 o superior**
- **Windows 10/11** (Sistema Operativo)

---

## 📦 **INSTALACIÓN**

### 1. **Clonar/Descargar el Proyecto**
```bash
git clone <repositorio>
cd elverproyecto
```

### 2. **Crear Entorno Virtual (Recomendado)**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### 4. **Configurar Base de Datos**

#### a) Crear la BD
```bash
mysql -u root -p < techsenahsgs.sql
```

#### b) Actualizar archivo `.env`
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=TechSenaHSGS
```

### 5. **Ejecutar la Aplicación**
```bash
python main.py
```

---

## 📋 **DEPENDENCIAS**

```
mysql-connector-python==8.2.0      # Conexión MySQL
customtkinter==5.2.1                # UI moderna
pandas==2.0.3                       # Manejo de datos
tkcalendar==1.6.1                   # Widget calendario
openpyxl==3.1.2                     # Excel
reportlab==4.0.7                    # Generador PDF
python-dotenv==1.0.0                # Variables de entorno
Pillow==10.0.0                      # Procesamiento de imágenes
```

---

## 🚀 **USO RÁPIDO**

### Flujo General
1. **Ejecutar** `python main.py`
2. **Login** con credenciales del tipo de usuario
3. **Navegar** según el panel correspondiente
4. **Cerrar sesión** para mantener la auditoría

### Flujo De Instructor (Nuevo)
1. Login como instructor
2. Seleccionar ficha asignada
3. Registrar faltas de estudiantes
4. Consultar reportes

### Flujo De Administrador
1. Login como admin
2. Acceder a panel completo
3. Gestionar aprendices/instructores
4. Generar reportes
5. Consultar auditoría

---

## 📊 **REQUISITOS FUNCIONALES Y NO FUNCIONALES**

### ✅ **REQUISITOS FUNCIONALES**

#### Autenticación
- RF-001: Sistema debe validar usuario y contraseña (admin, instructor, aprendiz)
- RF-002: Sistema debe cambiar contraseña al primer login con credenciales por defecto
- RF-003: Sistema debe registrar login/logout en auditoría

#### Gestión de Asistencia
- RF-004: Registrar entrada de aprendiz
- RF-005: Registrar salida de aprendiz
- RF-006: Consultar historial de asistencias
- RF-007: Visualizar calendario mensual con asistencias

#### Gestión de Faltas (v2.0)
- RF-008: Instructor puede registrar faltas (Inasistencia, Retardo, Justificada)
- RF-009: Instructor puede consultar faltas por ficha
- RF-010: Admin puede consultar faltas de todos

#### Gestión de Aprendices
- RF-011: Crear aprendiz manualmente
- RF-012: Importar aprendices desde Excel
- RF-013: Modificar datos de aprendiz
- RF-014: Eliminar aprendiz (a papelera)
- RF-015: Restaurar aprendiz desde papelera
- RF-016: Eliminar permanentemente aprendiz

#### Gestión de Instructores (v2.0)
- RF-017: Admin puede crear instructores
- RF-018: Admin puede asignar fichas a instructores
- RF-019: Instructor puede ver solo sus fichas asignadas
- RF-020: Instructor puede ver estudiantes de sus fichas

#### Reportes
- RF-021: Generar reportes por día/semana/mes
- RF-022: Filtrar reportes por ficha o aprendiz individual
- RF-023: Exportar reportes a PDF/Excel
- RF-024: Consultar auditoría completa

---

### 🔧 **REQUISITOS NO FUNCIONALES**

#### Rendimiento
- RNF-001: Interfaz debe responder en <500ms
- RNF-002: Carga de calendarios en <1 segundo
- RNF-003: Generación de reportes en <5 segundos
- RNF-004: Soporte para mínimo 1000 registros de asistencia

#### Seguridad
- RNF-005: Contraseñas almacenadas de forma segura
- RNF-006: Auditoría de todas las acciones
- RNF-007: Validación de entrada en todos los campos
- RNF-008: Sin acceso directo a BD desde interfaz

#### Confiabilidad
- RNF-009: 99% de disponibilidad en horario laboral
- RNF-010: Recuperación automática de conexión perdida
- RNF-011: Rollback de fallos en transacciones
- RNF-012: Backup automático recomendado

#### Usabilidad
- RNF-013: Interfaz intuitiva sin necesidad de capacitación
- RNF-014: Mensajes de error claros en español
- RNF-015: Tema visual consistente (colores SENA)
- RNF-016: Navegación rápida entre secciones

#### Mantenibilidad
- RNF-017: Código modular y documentado
- RNF-018: Separación de capas (BD, Lógica, UI)
- RNF-019: Fácil adición de nuevas funcionalidades
- RNF-020: Uso de patrones de diseño establecidos

#### Compatibilidad
- RNF-021: Compatible con MySQL 8.0+
- RNF-022: Compatible con Python 3.10+
- RNF-023: Compatible con Windows 10/11
- RNF-024: UI escalable a diferentes resoluciones

#### Escalabilidad
- RNF-025: Soporte para múltiples fichas
- RNF-026: Soporte para múltiples instructores
- RNF-027: Soporte para múltiples sedes (preparado para futura expansión)

---

## 📁 **ESTRUCTURA DE ARCHIVOS**

```
elverproyecto/
├── main.py                      ← Programa principal
├── conexion.py                  ← Conexión a BD
├── logica.py                    ← Lógica de negocios
├── admin_panel.py               ← Panel admin + Instructor
├── dashboard_password.py        ← Panel aprendiz
├── reportes.py                  ← Generador de reportes
├── config.py                    ← Configuración
├── logging_config.py            ← Sistema de logs
├── ui_helper.py                 ← Funciones auxiliares
├── validadores.py               ← Validaciones
├── .env                         ← Variables de entorno
├── requirements.txt             ← Dependencias
├── techsenahsgs.sql             ← Script BD
├── images/                      ← Imágenes
├── README.md                    ← Este archivo
├── PRESENTACION.md              ← Presentación
├── DIAGRAMAS_UML.md             ← Diagramas
└── HISTORIAS_DE_USUARIO.md      ← Historias Usuario
```

---

## 🔍 **SOLUCIÓN DE PROBLEMAS**

| Error | Solución |
|-------|----------|
| ModuleNotFoundError customtkinter | `pip install --upgrade customtkinter` |
| Connection refused en BD | Verificar MySQL corriendo y `.env` correcto |
| No such file or directory (imágenes) | Verificar carpeta `images/` existe |
| Interfaz lenta | Aumentar RAM, cerrar aplicaciones |

---

## 📈 **HISTORIAL DE VERSIONES**

| Versión | Fecha | Cambios |
|---------|-------|---------|
| **1.0** | Feb 2026 | Versión inicial - Gestión de asistencia |
| **2.0** | Mar 2026 | Sistema de instructores + Registro de faltas |

---

**Última actualización**: 5 de Marzo de 2026
