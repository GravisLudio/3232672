# SISTEMA DE INSTRUCTORES Y REGISTRO DE FALTAS - IMPLEMENTACIÓN COMPLETA

## ✅ CAMBIOS REALIZADOS

### 1. **ACTUALIZACIÓN DE BASE DE DATOS** (techsenahsgs.sql)

#### Tabla `usuarios_admin` - ACTUALIZADA
- Agregar columna `tipo_usuario` (enum: 'admin', 'instructor')
- Permite que admin principal actúe como instructor

#### Nueva Tabla `instructores`
```sql
CREATE TABLE instructores (
  id_instructor INT AUTO_INCREMENT PRIMARY KEY,
  documento VARCHAR(20) UNIQUE NOT NULL,
  nombre_completo VARCHAR(150) NOT NULL,
  correo VARCHAR(100),
  especialidad VARCHAR(150),
  usuario VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(255) DEFAULT 'sena123',
  cambio_pass TINYINT DEFAULT 0,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Nueva Tabla `fichas_asignadas`
```sql
CREATE TABLE fichas_asignadas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_instructor INT NOT NULL,
  id_ficha INT NOT NULL,
  fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY (id_instructor, id_ficha),
  FOREIGN KEY (id_instructor) REFERENCES instructores(id_instructor),
  FOREIGN KEY (id_ficha) REFERENCES fichas(id_ficha)
)
```

#### Nueva Tabla `faltas`
```sql
CREATE TABLE faltas (
  id_falta INT AUTO_INCREMENT PRIMARY KEY,
  documento_estudiante VARCHAR(20) NOT NULL,
  id_ficha INT NOT NULL,
  id_competencia INT NOT NULL,
  fecha_falta DATE NOT NULL,
  tipo_falta ENUM('Inasistencia', 'Retardo', 'Justificada') DEFAULT 'Inasistencia',
  razon TEXT,
  registrado_por VARCHAR(50) NOT NULL,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY (documento_estudiante, fecha_falta, id_competencia),
  FOREIGN KEY (documento_estudiante) REFERENCES estudiantes(documento),
  FOREIGN KEY (id_ficha) REFERENCES fichas(id_ficha),
  FOREIGN KEY (id_competencia) REFERENCES competencias(id_competencia)
)
```

### 2. **MÉTODOS NUEVOS EN logica.py**

```python
# Autenticación de instructor
def login_instructor(usuario, password)
    → Autentica instructor contra tabla instructores

# Obtener fichas del instructor
def obtener_fichas_instructor(id_instructor)
    → Retorna fichas asignadas al instructor

# Obtener estudiantes de una ficha
def obtener_estudiantes_ficha(id_ficha)
    → Retorna lista de estudiantes

# Registrar faltas
def registrar_falta(documento, id_ficha, id_competencia, fecha_falta, tipo_falta, razon, registrado_por)
    → Registra una falta en el sistema

# Obtener faltas de una ficha
def obtener_faltas_ficha(id_ficha, fecha_inicio, fecha_fin)
    → Retorna faltas en rango de fechas

# Obtener faltas de un estudiante
def obtener_faltas_estudiante(documento_estudiante, id_ficha)
    → Retorna ALL faltas del estudiante

# Resumen de faltas
def obtener_resumen_faltas(id_ficha, fecha_inicio, fecha_fin)
    → Retorna cuenta de faltas por tipo
```

### 3. **ACTUALIZACIÓN DE main.py**

#### Cambios en `_procesar_login()`
- Intenta login como admin/instructor en `usuarios_admin` (verificando `tipo_usuario`)
- Intenta login como instructor en tabla `instructores`
- Intenta login como aprendiz en tabla `estudiantes`
- Diferencia entre admin (panel completo) e instructor (panel limitado)

#### Nuevas Variables de Instancia
```python
self.instructor_actual = None  # Usuario instructor actual
```

#### Nuevos Métodos
```python
# Panel del instructor (login desde usuarios_admin como instructor)
def mostrar_panel_instructor(admin_data)

# Panel del instructor (login desde tabla instructores)
def mostrar_panel_instructor_ui(instructor)

# Actualizar contraseña del instructor
def actualizar_password_instructor_ventana(documento)
```

### 4. **NUEVA CLASE: PantallaInstructor EN admin_panel.py**

Clase que gestiona el panel del instructor con 3 pestañas principales:

#### Pestaña 1: 📋 HISTORIAL
- Seleccionar ficha asignada
- Ver asistencia de estudiantes (mes actual)
- Tabla: Estudiante, Documento, Fecha, Entrada, Salida

#### Pestaña 2: 📊 REPORTES
- Acceso a reportes de asistencia
- Mismo sistema que el panel admin

#### Pestaña 3: ❌ REGISTRO DE FALTAS
- Seleccionar ficha
- Seleccionar estudiante
- Tipo de falta: Inasistencia, Retardo, Justificada
- Fecha y razón opcional
- Tabla live de faltas registradas

### 5. **FLUJO DE ACCESO**

#### Para ADMIN Principal:
- Login: usuario='admin', password='admin123'
- Tipo de usuario: 'admin'
- Acceso: Panel admin completo (Historial, Gestión, Registro, Reportes, Papelera)

#### Para INSTRUCTOR:
**Opción A - Via usuarios_admin:**
- crear registro en usuarios_admin con tipo_usuario='instructor'
- Login con ese usuario/pass
-  Acceso: Panel limitado (Historial, Reportes, Registro de Faltas)

**Opción B - Via tabla instructores:**
- Crear registro en tabla instructores
- Login con usuario/password
- Acceso: Panel limitado (Historial, Reportes, Registro de Faltas)

#### Para APRENDIZ:
- Igual que antes (sin cambios)

## 🔧 CÓMO USAR

### 1. CREAR INSTRUCTOR EN BD
```sql
-- Opción A: Como admin en usuarios_admin
INSERT INTO usuarios_admin (usuario, password, nombre, tipo_usuario) 
VALUES ('instructor1', 'pass123', 'Juan Pérez', 'instructor');

-- Opción B: En tabla instructores
INSERT INTO instructores (documento, nombre_completo, usuario, password, especialidad)
VALUES ('12345678', 'Juan Pérez', 'instructor1', 'pass123', 'Sistemas');
```

### 2. ASIGNAR FICHAS AL INSTRUCTOR
```sql
INSERT INTO fichas_asignadas (id_instructor, id_ficha)
VALUES (1, 5);  -- Asigna ficha 5 al instructor 1
```

### 3. INSTRUCTOR HACE LOGIN
- Pantalla de login
- Usuario: instructor1
- Contraseña: pass123
- Accede a panel de instructor

### 4. INSTRUCTOR REGISTRA FALTAS
- Abre pestaña "REGISTRO DE FALTAS"
- Selecciona ficha asignada
- Selecciona estudiante
- Especifica tipo de falta y fecha
- Sistema registra en tabla `faltas`

## 📊 ESTRUCTURA DE DATOS

### Relación de Tablas
```
usuarios_admin (tipo_usuario='instructor')
        ↓
instructores (tabla separada, alternativa)
        ↓
fichas_asignadas ← id_instructor, id_ficha
        ↓
fichas ← estudiantes
        ↓
faltas ← documento_estudiante, id_ficha, id_competencia
```

## ⚙️ CARACTERÍSTICAS

✅ **Control de acceso por rol:**
- Admin: acceso total
- Instructor: acceso limitado (historial, reportes, registro de faltas)
- Aprendiz: acceso propio (sin cambios)

✅ **Registro de faltas:**
- Tres tipos: Inasistencia, Retardo, Justificada
- Comentarios/razones opcionales
- Rastreo de quién registra y cuándo

✅ **Auditoria completa:**
- Login/logout instructor registrado
- Cambios de contraseña
- Registros de faltas

✅ **Interfaz moderna:**
- Diseño consistente con resto del sistema
- Navegación por pestañas
- Tablas intuitivas

## 🚀 PRÓXIMOS PASOS (OPCIONAL)

1. Crear vista de "Resumen de Faltas por Estudiante" para instructores
2. Notificaciones cuando estudiante alcanza X faltas
3. Reportes automáticos de faltas para el admin
4. Descarga de reportes de faltas en PDF/Excel
5. Histoiral de cambios en registros de faltas

## ✅ VALIDADO

- ✅ Sintaxis Python verificada (sin errores)
- ✅ Tablas SQL creadas correctamente
- ✅ Métodos de logica.py implementados
- ✅ Login unificado actualizado
- ✅ Panel instructor creado y funcional
- ✅ Registro de faltas completo
