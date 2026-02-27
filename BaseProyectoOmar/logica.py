"""
================================================================================
    MÓDULO DE LÓGICA DE NEGOCIO - CHRONOS REGISTRY SYSTEM (C.R.G)
================================================================================

DESCRIPCIÓN GENERAL:
    Este módulo contiene la clase `AsistenciaService`, que encapsula toda la lógica
    de negocio de la aplicación de registro de asistencia. Proporciona métodos para:
    - Registrar entradas y salidas de aprendices
    - Gestionar credenciales y seguridad
    - Operaciones CRUD (Create, Read, Update, Delete) sobre aprendices
    - Importación masiva desde archivos Excel/CSV
    - Gestión de papelera (soft delete y restauración)

LIBRERÍAS UTILIZADAS:
    - pandas: Manipulación y lectura de datos desde archivos Excel/CSV
      * Se usa para leer archivos de importación masiva con estructura tabular
      * Proporciona DataFrames que iteramos para procesar cada registro
    
    - tkinter.messagebox: Cuadros de diálogo para mostrar mensajes al usuario
      * messagebox.showinfo(): Muestra mensajes informativos (éxito)
      * messagebox.showerror(): Muestra mensajes de error
    
    - tkinter.filedialog: Diálogos para seleccionar archivos
      * filedialog.askopenfilename(): Abre un cuadro de selección de archivos
    
    - datetime: Manejo de fechas y horas
      * Se usa para registrar timestamps de entrada/salida en la BD

ESTRUCTURA DE LA BASE DE DATOS (resumen de tablas importantes):
    - estudiantes: Tabla principal con datos de aprendices activos
      Campos: documento (PK), nombre_completo, correo, id_ficha, password, cambio_pass
    
    - asistencias: Histórico de marcación entrada/salida
      Campos: id_asistencia (PK), documento_estudiante (FK), fecha_registro, fecha_salida
    
    - fichas: Información de grupos/programas
      Campos: id_ficha (PK), codigo_ficha, nombre_programa
    
    - estudiantes_eliminados: Tabla de "papelera" (soft delete)
      Misma estructura que estudiantes pero para registros eliminados lógicamente

CONVENCIONES DEL CÓDIGO:
    - Retorno de métodos: Tupla (bool, str) = (éxito, mensaje)
    - Validaciones: Se realizan al inicio de cada método
    - Transacciones: Después de INSERT/UPDATE/DELETE se ejecuta commit()
    - Excepciones: Capturadas en try-except para no romper la GUI
================================================================================
"""

import pandas as pd
from tkinter import messagebox, filedialog
import datetime

class AsistenciaService:
    """
    Servicio de Asistencia - Capa de Lógica de Negocio
    
    Encapsula todas las operaciones relacionadas con asistencia, registro de aprendices,
    seguridad y administración de datos. Actúa como intermediario entre la GUI (main.py)
    y la base de datos (a través de InventarioDB en conexion.py).
    
    RESPONSABILIDADES:
    1. Validar entradas de datos antes de interactuar con la BD
    2. Ejecutar consultas SQL de forma segura (usando parámetros)
    3. Manejar errores y transacciones
    4. Retornar resultados en formato consistente (tupla de éxito/mensaje)
    5. Mantener la lógica de negocio separada de la presentación (GUI)
    
    PATRÓN DE DISEÑO:
    - Patrón Service Layer: Separa la lógica del acceso a datos
    - Retorna tuplas (bool, str) para codificar resultado + descripción
    - Usa conexión compartida (inyección de dependencia via __init__)
    """
    def __init__(self, db_conexion):
        """
        Constructor de AsistenciaService
        
        PARÁMETROS:
            db_conexion (InventarioDB): Instancia de la clase InventarioDB que proporciona
                                       acceso a la base de datos MySQL. Esta conexión debe
                                       estar inicializada y funcional.
        
        ATRIBUTOS ASIGNADOS:
            self.db: Almacena la referencia a la conexión de BD para usarla en todos
                    los métodos de la clase
        
        NOTA IMPORTANTE:
            Esta clase NO crea su propia conexión; recibe una ya existente.
            Esto es una buena práctica (patrón de Inyección de Dependencia) porque:
            - Permite compartir una sola conexión con toda la app
            - Facilita las pruebas unitarias
            - Evita múltiples conexiones simultáneas
        
        EJEMPLO DE USO (desde main.py):
            self.db = InventarioDB()  # Crea la conexión
            self.servicio = AsistenciaService(self.db)  # Inyecta la conexión
        """
        self.db = db_conexion

    # ============================================================================
    # BLOQUE 1: LÓGICA DE ASISTENCIA (TERMINAL DE MARCACIÓN)
    # ============================================================================
    # Estos métodos manejan la funcionalidad principal: marcar entrada y salida.
    # Son llamados desde mostrar_terminal() en main.py cuando el usuario ingresa
    # su documento en el entry y presiona los botones de entrada/salida.
    
    def registrar_entrada(self, documento):
        """
        PROPÓSITO:
            Registra la entrada de un aprendiz al sistema. Crea un nuevo registro
            en la tabla 'asistencias' con fecha_registro = NOW() y fecha_salida = NULL.
        
        FLUJO DE VALIDACIÓN:
            1. Verifica que el documento no esté vacío
            2. Valida que el aprendiz existe en tabla 'estudiantes' (NO en papelera)
            3. Si existe en papelera, advierte al usuario
            4. Verifica que no haya una entrada activa sin cerrar (sin fecha_salida)
            5. Inserta el registro en 'asistencias'
        
        PARÁMETROS:
            documento (str): Número de cédula/documento del aprendiz (ej: "1023456789")
        
        RETORNA:
            Tupla (bool, str):
                - (True, "✅ Entrada Registrada...") si éxito
                - (False, "❌ Mensaje de error") si falla
        
        ERRORES POSIBLES:
            - Documento vacío o None
            - Aprendiz no existe en el sistema
            - Aprendiz está en la papelera
            - Ya existe una entrada activa (sin fecha_salida)
            - Error de conexión con BD
        
        ESTRUCTURA DE DATOS AFECTADOS:
            Inserta en tabla 'asistencias':
            - documento_estudiante: parámetro recibido
            - fecha_registro: NOW() (hora actual del servidor MySQL)
            - fecha_salida: NULL (se llena luego con registrar_salida)
            - id_competencia: 1 (por defecto según lógica de negocio)
        
        NOTAS TÉCNICAS:
            - "fecha_salida IS NULL" se usa para detectar entradas abiertas
            - INSERT IGNORE evitaría duplicados, pero aquí se usa INSERT normal
            - self.db.insertar() es un método wrapper de InventarioDB
        """
        if not documento:
            return False, "Por favor ingrese un documento."
        
        # Validar existencia en tabla activa
        self.db.cursor.execute("SELECT documento FROM estudiantes WHERE documento=%s", (documento,))
        if not self.db.cursor.fetchone():
            # Verificar si está en papelera para dar un aviso más preciso
            self.db.cursor.execute("SELECT documento FROM estudiantes_eliminados WHERE documento=%s", (documento,))
            if self.db.cursor.fetchone():
                return False, "⚠️ El aprendiz está en la PAPELERA. Contacte al administrador."
            return False, "❌ El aprendiz NO existe en el sistema."

        # Validar si ya tiene una entrada abierta (sin fecha de salida)
        self.db.cursor.execute("SELECT id_asistencia FROM asistencias WHERE documento_estudiante=%s AND fecha_salida IS NULL", (documento,))
        if self.db.cursor.fetchone():
            return False, "⚠️ Ya tienes una entrada activa. Debes registrar SALIDA primero."
        
        # Insertar registro (id_competencia 1 por defecto según BD)
        if self.db.insertar(documento, 1):
            return True, "✅ Entrada Registrada con éxito."
        return False, "❌ Error técnico al conectar con la base de datos."

    def registrar_salida(self, documento):
        """
        PROPÓSITO:
            Cierra una sesión de asistencia activa (llena el campo fecha_salida).
            Busca el registro de entrada sin cerrar y le asigna la hora actual de salida.
        
        FLUJO:
            1. Valida que documento no esté vacío
            2. Busca un registro donde: documento_estudiante = documento Y fecha_salida IS NULL
            3. Si existe, actualiza el registro asignando fecha_salida = NOW()
            4. Si no existe, retorna error (no hay entrada abierta)
        
        PARÁMETROS:
            documento (str): Número de documento del aprendiz
        
        RETORNA:
            Tupla (bool, str):
                - (True, "✅ Salida Registrada...") si éxito
                - (False, "❌ Mensaje de error") si falla
        
        ERRORES POSIBLES:
            - Documento vacío
            - No hay entrada activa (el aprendiz no marcó entrada)
            - Error en la actualización (problemas BD)
        
        ESTRUCTURA SQL UTILIZADA:
            SELECT id_asistencia FROM asistencias 
            WHERE documento_estudiante = ? AND fecha_salida IS NULL
            -> id_asistencia es la PK del registro abierto
            
            UPDATE asistencias 
            SET fecha_salida = NOW() 
            WHERE id_asistencia = ?
            -> Cierra el registro con la hora actual del servidor
        
        LÓGICA DE NEGOCIO:
            - Un aprendiz NO puede marcar salida sin antes marcar entrada
            - Un aprendiz NO puede tener múltiples entradas sin cerrar
            - El tiempo calculado (permanencia) = fecha_salida - fecha_registro
        
        CASO DE USO:
            Usuario llega al trabajo y marca entrada
            -> Más tarde marca salida
            -> Sistema calcula horas de asistencia ese día
        """
        if not documento:
            return False, "Por favor ingrese un documento."

        self.db.cursor.execute("SELECT id_asistencia FROM asistencias WHERE documento_estudiante=%s AND fecha_salida IS NULL", (documento,))
        res = self.db.cursor.fetchone()
        
        if res:
            try:
                self.db.cursor.execute("UPDATE asistencias SET fecha_salida=NOW() WHERE id_asistencia=%s", (res['id_asistencia'],))
                self.db.conexion.commit()
                return True, "✅ Salida Registrada correctamente."
            except Exception as e:
                return False, f"❌ Error al actualizar salida: {str(e)}"
        else:
            return False, "❌ No tienes una entrada pendiente para cerrar."

    # ============================================================================
    # BLOQUE 2: LÓGICA DE USUARIO Y SEGURIDAD
    # ============================================================================
    # Control de acceso, autenticación y manejo de credenciales de aprendices.
    # Estos métodos son llamados desde login_aprendiz_view() y actualizar_password_ventana()
    
    def login_aprendiz(self, documento, password):
        """
        PROPÓSITO:
            Verifica que las credenciales del aprendiz sean correctas.
            Implementa autenticación básica comparando credentials contra la BD.
        
        FLUJO:
            1. Busca en tabla 'estudiantes' un registro con documento Y password coincidentes
            2. Retorna el registro completo si existe, None si no
        
        PARÁMETROS:
            documento (str): Documento del aprendiz (ej: "1023456789")
            password (str): Contraseña ingresada por el usuario
        
        RETORNA:
            - dict con datos del estudiante si credenciales coinciden
            - None si no coinciden
        
        ESTRUCTURA DE DATOS RETORNADO (si éxito):
            {
                'documento': '1023456789',
                'nombre_completo': 'Juan Pérez',
                'correo': 'juan@sena.edu.co',
                'id_ficha': 1,
                'password': 'miPass123',  # Almacenado en BD
                'cambio_pass': 0 o 1  # Flag: 0=debe cambiar, 1=ya cambió
            }
        
        LÓGICA DE NEGOCIO:
            - Field 'cambio_pass' = 0 indica que es la primera vez que entra
              (contraseña por defecto desde registro manual)
            - Si 'cambio_pass' = 0 o password = 'sena123', se fuerza cambio en
              actualizar_password_ventana()
        
        SEGURIDAD (IMPORTANTE - SOLO PARA EDUCACIÓN):
            ⚠️ ADVERTENCIA: Las contraseñas se almacenan en TEXTO PLANO en la BD
               Esto NO es seguro para producción.
               EN PRODUCCIÓN SE DEBE USAR:
               - Hash (bcrypt, Argon2, PBKDF2)
               - Salting
               - Validación en backend
               - HTTPS para transmisión
        
        CÓDIGO SQL:
            SELECT * FROM estudiantes 
            WHERE documento = %s AND password = %s
        """
        q = "SELECT * FROM estudiantes WHERE documento=%s AND password=%s"
        self.db.cursor.execute(q, (documento, password))
        return self.db.cursor.fetchone()

    def actualizar_password(self, documento, nueva_pass):
        """
        PROPÓSITO:
            Cambia la contraseña de un aprendiz y marca que ya realizó el cambio
            obligatorio (cambio_pass = 1).
        
        VALIDACIONES:
            - Mínimo 4 caracteres (aunque en GUI se exigen más requisitos)
            - Documento debe existir en la BD
        
        PARÁMETROS:
            documento (str): Documento del aprendiz
            nueva_pass (str): Nueva contraseña a asignar
        
        RETORNA:
            Tupla (bool, str):
                - (True, "✅ Seguridad actualizada.") si éxito
                - (False, "Error: ...") si falla
        
        EFECTOS EN BD:
            UPDATE estudiantes 
            SET password = %s, cambio_pass = 1 
            WHERE documento = %s
            
            Actualiza:
            - password: Nueva contraseña ingresada
            - cambio_pass: Marca como 1 (ya cambió contraseña)
        
        VALIDACIÓN EN MÚLTIPLES CAPAS:
            CAPA 1 (aquí): Valida longitud mínima (4 chars)
            CAPA 2 (GUI en main.py): Valida que incluya mayúscula, minúscula, número
            RECOMENDACIÓN: Agregar regex o librería validator
        
        NOTA:
            cambio_pass = 0: Flag que indica primera vez (contraseña por defecto)
            cambio_pass = 1: Usuario ya cambió su contraseña
            Se usa en login_aprendiz_view para forzar cambio al primer ingreso
        """
        if len(nueva_pass) < 4:
            return False, "La contraseña debe tener al menos 4 caracteres."
        try:
            # En la tabla estudiantes debe existir la columna cambio_pass (tinyint)
            self.db.cursor.execute("UPDATE estudiantes SET password=%s, cambio_pass=1 WHERE documento=%s", (nueva_pass, documento))
            self.db.conexion.commit()
            return True, "✅ Seguridad actualizada."
        except Exception as e:
            return False, f"Error: {str(e)}"

    # ============================================================================
    # BLOQUE 3: LÓGICA ADMINISTRATIVA
    # ============================================================================
    # Operaciones CRUD (Create, Read, Update, Delete) sobre aprendices.
    # Métodos utilizados desde mostrar_panel_admin_ui() en main.py
    # Se llaman desde la interfaz de Administrador para gestionar estudiantes.
    
    def obtener_fichas(self):
        """
        PROPÓSITO:
            Carga la lista de fichas/programas disponibles para asignar a aprendices.
            Se usa para llenar dropdowns/combobox en formularios de registro.
        
        RETORNA:
            List[dict]: Lista de diccionarios con información de fichas
            Ejemplo de estructura:
            [
                {'id_ficha': 1, 'codigo_ficha': 'ADSI001', 'nombre_programa': 'Análisis y Desarrollo'},
                {'id_ficha': 2, 'codigo_ficha': 'GES002', 'nombre_programa': 'Gestión Empresarial'},
                ...
            ]
        
        TABLA UTILIZADA:
            SELECT * FROM fichas
            Tabla maestro que contiene los programas/fichas disponibles
            Típicamente tiene datos como:
            - id_ficha (PK): Identificador único
            - codigo_ficha: Código corto del programa (ej: ADSI001)
            - nombre_programa: Descripción del programa formativo
        
        CASO DE USO:
            Cuando admin quiere registrar un nuevo aprendiz, necesita seleccionar
            a qué ficha pertenece (ej: grupo ADSI-2024-01)
        
        EFICIENCIA:
            Se carga una sola vez al abrir el panel admin.
            Considerar cachéar si cambia rara vez.
        """
        self.db.cursor.execute("SELECT id_ficha, codigo_ficha, nombre_programa FROM fichas")
        return self.db.cursor.fetchall()

    def guardar_aprendiz_manual(self, datos, id_ficha):

        documento = datos.get("Documento", "").strip()
        
        if not documento or not datos["Nombre Completo"] or not id_ficha:
            return False, "Documento, Nombre y Ficha son campos obligatorios."
        
        if len(documento) > 10:
            return False, "❌ El documento no puede tener más de 10 dígitos."
        
        if not documento.isdigit():
            return False, "❌ El documento debe contener solo números."

        try:
            # Intentamos la inserción
            self.db.cursor.execute(
                "INSERT INTO estudiantes (documento, nombre_completo, correo, id_ficha) VALUES (%s, %s, %s, %s)", 
                (datos["Documento"], datos["Nombre Completo"], datos.get("Correo", ""), id_ficha)
            )
            self.db.conexion.commit()
            return True, "✅ Aprendiz guardado en el sistema."
        
        except Exception as e:
            # Si el error es por duplicado (código 1062 en MySQL)
            if "Duplicate entry" in str(e) or "1062" in str(e):
                return False, f"❌ El documento {datos['Documento']} ya se encuentra registrado."
            return False, f"❌ Error al guardar: {str(e)}"

    def importar_excel(self):
        """
        PROPÓSITO:
            Realiza carga masiva de aprendices desde archivo Excel (.xlsx) o CSV.
            Permite poblar rápidamente la BD desde listas exportadas de SENA.
        
        FLUJO:
            1. Abre diálogo de selección de archivos
            2. Si usuario selecciona archivo, lo lee con pandas
            3. Itera sobre cada fila y valida estructura
            4. Inserta registros en lotes (utiliza INSERT IGNORE para evitar duplicados)
            5. Muestra resumen de operación
        
        PARÁMETROS:
            Ninguno (abre diálogo filedialog.askopenfilename)
        
        RETORNA:
            bool: True si completó, False si usuario canceló o error
        
        LIBRERÍAS CLAVE - PANDAS:
            pandas.read_excel(path):
                Carga archivo Excel en un DataFrame (tabla en memoria)
                Soporta .xlsx y .xls
                Retorna estructura similar a SQL table
                
            pandas.read_csv(path):
                Similar a read_excel pero para CSV (comma-separated)
            
            DataFrame.iterrows():
                Itera sobre filas; cada fila es (índice, Serie de datos)
                Permite acceso columnar: r['documento'], r['nombre_completo']
        
        ESTRUCTURA ESPERADA DEL ARCHIVO:
            Debe tener columnas (en cualquier orden):
            - documento        (str): Cédula del aprendiz
            - nombre_completo  (str): Nombre
            - correo           (str): Email
            - id_ficha         (int): ID de ficha
            
            Ejemplo:
            | documento  | nombre_completo | correo          | id_ficha |
            |------------|-----------------|-----------------|----------|
            | 1023456789 | Juan Pérez      | juan@sena.edu   | 1        |
            | 9876543210 | María García    | maria@sena.edu  | 2        |
        
        SQL GENERADO:
            INSERT IGNORE INTO estudiantes 
            (documento, nombre_completo, correo, id_ficha) 
            VALUES (%s, %s, %s, %s)
            
            INSERT IGNORE: Si documento ya existe (PK), ignora silenciosamente
            (forma segura de hacer carga idempotente)
        
        MANEJO DE ERRORES:
            - Archivo no válido: Captura Exception y muestra diálogo error
            - Estructura incorrecta: Si faltan columnas, KeyError es capturado
            - Cancelación: Si usuario cierra diálogo sin seleccionar = No hace nada
        
        MENSAJE DE ÉXITO:
            Muestra cuántos registros se procesaron (no necesariamente insertados,
            algunos pueden ser ignorados por INSERT IGNORE)
        
        CASOS DE USO:
            1. Carga inicial de todos los aprendices de una ficha
            2. Importar listado desde Excel del departamento de admisiones
            3. Integración con sistemas externos (exportar datos, procesar, reimportar)
        
        EJEMPLO DE ARCHIVO CSV:
            documento,nombre_completo,correo,id_ficha
            1023456789,Juan Pérez,juan@mail.com,1
            9876543210,María García,maria@mail.com,1
        
        CONSIDERACIONES DE RENDIMIENTO:
            - Para archivos muy grandes (>10K registros):
              Considerar usar LOAD DATA INFILE (MySQL) para mayor velocidad
            - Actualmente hace INSERT fila por fila (lento pero seguro)
        """
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")])
        if path:
            try:
                df = pd.read_excel(path) if path.endswith('.xlsx') else pd.read_csv(path)
                # Requiere columnas: documento, nombre_completo, correo, id_ficha
                count = 0
                for _, r in df.iterrows():
                    self.db.cursor.execute(
                        "INSERT IGNORE INTO estudiantes (documento, nombre_completo, correo, id_ficha) VALUES (%s, %s, %s, %s)", 
                        (r['documento'], r['nombre_completo'], r['correo'], r['id_ficha'])
                    )
                    count += 1
                self.db.conexion.commit()
                messagebox.showinfo("C.R.G", f"✅ Importación finalizada. Se procesaron {count} registros.")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al leer el archivo: {str(e)}")
                return False
        return False

    def mandar_a_papelera(self, documento):
        """
        PROPÓSITO:
            Implementa "soft delete" (eliminación lógica) de un aprendiz.
            No borra datos de la BD sino los mueve a tabla separada (estudiantes_eliminados)
            permitiendo recuperación posterior.
        
        PATRÓN DE DISEÑO - SOFT DELETE:
            Ventajas:
            - Preserva historial de asistencia (foreignkeys mantienen integridad)
            - Permite auditoría y recuperación
            - No afecta registros históricos en asistencias
            
            Desventajas:
            - Requiere atender a 2 tablas
            - Queries más complejas (WHERE deleted_at IS NULL)
            
            Alternativa (no usada aquí):
            - Hard delete: DELETE definitivo
            - Soft delete con timestamp: Agregar columna deleted_at
            - Tabla audit: Guardar cambios históricos
        
        FLUJO:
            1. Busca aprendiz en tabla 'estudiantes'
            2. Inserta ese registro en 'estudiantes_eliminados'
            3. Elimina de tabla 'estudiantes'
            4. Commit de transacción
        
        PARÁMETROS:
            documento (str): Documento del aprendiz a eliminar
        
        RETORNA:
            bool: True si éxito, False si error
        
        SQL GENERADO (en orden):
            -- 1. Copiar a papelera
            INSERT INTO estudiantes_eliminados 
            (documento, nombre_completo, correo, id_ficha, ...) 
            SELECT documento, nombre_completo, correo, id_ficha, ... 
            FROM estudiantes 
            WHERE documento = %s
            
            -- 2. Eliminar de tabla activa
            DELETE FROM estudiantes WHERE documento = %s
        
        ESTRUCTURA DE DATOS:
            estudiantes_eliminados tiene la MISMA estructura que estudiantes
            Esto facilita:
            - INSERT INTO ... SELECT FROM (mismas columnas)
            - Recuperación idéntica en restaurar_aprendiz()
        
        REFERENCIA EN BD:
            - asistencias.documento_estudiante referencia a estudiantes.documento
            - Si se hace hard delete sin borrar asistencias, FK se rompe
            - Aquí se preserva: si se restaura, los registros quedan intactos
        
        MANEJO DE ERRORES:
            - Captura excepciones SQL genéricas
            - Retorna False silenciosamente (la GUI no rompe)
            - Ideal mejorar con logging
        
        AUDITORÍA (recomendación para mejorar):
            Agregar:
            - Fecha de eliminación
            - Usuario que eliminó
            - Motivo
            - Permitir reversión por admin
        """
        try:
            self.db.cursor.execute(
                "INSERT INTO estudiantes_eliminados (documento, nombre_completo, correo, id_ficha) "
                "SELECT documento, nombre_completo, correo, id_ficha FROM estudiantes WHERE documento=%s", 
                (documento,)
            )
            self.db.cursor.execute("DELETE FROM estudiantes WHERE documento=%s", (documento,))
            self.db.conexion.commit()
            return True
        except Exception:
            return False

    def restaurar_aprendiz(self, documento):
        """
        PROPÓSITO:
            Recupera un aprendiz desde la papelera.
            Invierte la operación de mandar_a_papelera() sin perder datos.
        
        FLUJO:
            1. Busca aprendiz en 'estudiantes_eliminados'
            2. Inserta en 'estudiantes' (tabla activa)
            3. Elimina de 'estudiantes_eliminados'
            4. Commit
        
        PARÁMETROS:
            documento (str): Documento del aprendiz a restaurar
        
        RETORNA:
            bool: True si éxito, False si error
        
        SQL GENERADO (en orden):
            -- 1. Recuperar a tabla activa (mismo que insertar desde papelera)
            INSERT INTO estudiantes 
            (documento, nombre_completo, correo, id_ficha, ...) 
            SELECT documento, nombre_completo, correo, id_ficha, ... 
            FROM estudiantes_eliminados 
            WHERE documento = %s
            
            -- 2. Eliminar de papelera
            DELETE FROM estudiantes_eliminados WHERE documento = %s
        
        OPERACIÓN INVERSA DE:
            mandar_a_papelera() = Copiar a papelera + Eliminar de activos
            restaurar_aprendiz() = Copiar de papelera + Eliminar de papelera
        
        IDEMPOTENCIA:
            - Si se ejecuta dos veces, segunda falla (documento no en papelera)
            - Pero retorna False, no rompe la app
            - Ideal agregar try-except específico para FK violations
        
        CASO DE USO:
            Admin elimina aprendiz por error
            -> Nota que falta en la próxima clase
            -> Va a papelera, selecciona "Restaurar"
            -> Aprendiz vuelve inmediatamente a tabla activa
        
        INTEGRIDAD DE DATOS:
            - Registros en 'asistencias' NO se afectan (documento sigue existiendo)
            - Historial de asistencia permanece intacto
            - El aprendiz recuperado tiene TODO su historial
        
        LIMITACIÓN ACTUAL:
            No hay auditoría de quién/cuándo se restauró
            Mejora: Agregar log de cambios
        """
        try:
            self.db.cursor.execute(
                "INSERT INTO estudiantes (documento, nombre_completo, correo, id_ficha) "
                "SELECT documento, nombre_completo, correo, id_ficha FROM estudiantes_eliminados WHERE documento=%s", 
                (documento,)
            )
            self.db.cursor.execute("DELETE FROM estudiantes_eliminados WHERE documento=%s", (documento,))
            self.db.conexion.commit()
            return True
        except Exception:
            return False

    def eliminar_permanente(self, documento):
        """
        PROPÓSITO:
            Realiza hard delete (eliminación definitiva) de la papelera.
            Una vez ejecutado, los datos NO pueden recuperarse (salvo backup).
        
        ⚠️ ADVERTENCIA DE SEGURIDAD:
            Este es un punto crítico. Considerar:
            - Confirmación de usuario (¿realmente desea? x2)
            - Rol administrativo con permisos (no todos pueden hacer esto)
            - Auditoría de quién/cuándo (guardar logs antes de borrar)
            - Backup automático previo
            - Período de gracia (keep en papelera 30 días antes de borrar)
        
        FLUJO:
            1. Busca aprendiz en 'estudiantes_eliminados'
            2. DELETE definitivo
            3. Commit
        
        PARÁMETROS:
            documento (str): Documento del aprendiz a eliminar permanentemente
        
        RETORNA:
            bool: True si éxito, False si error
        
        SQL:
            DELETE FROM estudiantes_eliminados WHERE documento = %s
        
        CONSECUENCIAS DE EJECUCIÓN:
            - Registro IRREVERSIBLE: No vuelve de backup
            - Si se tienen accesos a asistencias de este estudiante, pueden quedar huérfanos
              (depende si hay FK constraint; típicamente no hay para historial)
            - Datos perdidos para siempre (cumplimiento normativo?)
        
        MEJOR PRÁCTICA (NO implementado aquí):
            
            -- En lugar de DELETE, marcar como archivado:
            UPDATE estudiantes_eliminados 
            SET fecha_eliminacion_definitiva = NOW(), eliminado_por = user_id
            WHERE documento = %s
            
            -- Nunca hacer DELETE real, mantener para auditoría
            -- Permitir restaurar solo si hace menos de X días
        
        CONSIDERACIONES LEGALES:
            - GDPR/CNDP: Right to be forgotten
            - Pero auditoría de educación exige mantener registros X años
            - Solución: Anonimizar en lugar de borrar
        
        DEFENSA EN PROFUNDIDAD:
            Nivel 1 (aquí): DELETE de papelera
            Nivel 2 (DB): FK constraints previenen orfandad
            Nivel 3 (App): Confirmaciones en GUI
            Nivel 4 (Org): Políticas de retención de datos
            Nivel 5 (Backup): Restaurables desde backup
        
        CASO DE USO:
            Admin quiere liberar espacio definitivamente
            Aprendiz solicita GDPR right to be forgotten
            Período de retención legal vencido (ej: 5 años)
        """
        try:
            self.db.cursor.execute("DELETE FROM estudiantes_eliminados WHERE documento=%s", (documento,))
            self.db.conexion.commit()
            return True
        except Exception:
            return False

    def obtener_registros_dia(self, documento, fecha):
        """
        PROPÓSITO:
            Recupera los registros de asistencia de un aprendiz para una fecha específica.
            Se usa para mostrar la actividad en el calendario del panel de aprendiz.
        
        FLUJO:
            1. Recibe documento del aprendiz y fecha seleccionada en calendario
            2. Busca todos los registros en asistencia donde:
               - documento_estudiante coincida
               - fecha del registro coincida (ignorando hora)
            3. Retorna lista de registros
        
        PARÁMETROS:
            documento (str): Documento del aprendiz
            fecha (datetime.date): Fecha seleccionada (sin hora; ej: 2024-02-25)
        
        RETORNA:
            List[dict]: Lista vacía [] si no hay registros, o:
            [
                {
                    'id_asistencia': 1,
                    'documento_estudiante': '1023456789',
                    'fecha_registro': datetime(2024, 2, 25, 8, 30, 0),
                    'fecha_salida': datetime(2024, 2, 25, 16, 45, 0),
                    'id_competencia': 1,
                    ...
                },
                ...
            ]
        
        SQL UTILIZADO:
            SELECT * FROM asistencias 
            WHERE documento_estudiante = %s 
            AND DATE(fecha_registro) = %s
            
            DATE(fecha_registro):
            - Extrae solo la fecha (YYYY-MM-DD) ignorando hora
            - Permite comparar directamente con parámetro fecha
            - Ej: Buscar todos registros del día 2024-02-25, sin importar hora
        
        CASO DE USO:
            1. Aprendiz abre su panel de asistencia
            2. Selecciona una fecha en el calendario (click en día específico)
            3. Sistema llama a este método
            4. Muestra tarjetas con entrada/salida de ese día
        
        VISUALIZACIÓN EN GUI (main.py):
            Se reciben los registros y se crean tarjetas:
            
            Tarjeta 1:
            📥 Ent: 08:30 (fecha_registro hora)
            📤 Sal: 16:45 (fecha_salida hora)
            
            Días sin asistencia -> "Sin actividad este día"
        
        LÓGICA DE TARJETAS:
            - Si fecha_salida IS NULL -> Solo muestra entrada (sin salida)
            - Si fecha_salida NO NULL -> Muestra ambas
            - Permite calcular horas trabajadas: salida - entrada
        
        CONSIDERACIONES TÉCNICAS:
            - cursor retorna lista de diccionarios (dict=True en cursor config)
            - datetime.date vs datetime.datetime:
              * fecha es date (sin hora)
              * fecha_registro es datetime (con hora)
              * DATE() convierte a compatibilidad
        
        MEJORA SUGERIDA:
            Cachear resultados del mes entero al abrir panel
            Reducir queries a BD cuando cambia de día
        
        RELACIÓN CON CALENDARIO:
            - Calendar widget en tkcalendar genera evento <<CalendarSelected>>
            - main.py conecta ese evento a actualizar_cards()
            - actualizar_cards() llama a este método
            - Se actualizan tarjetas dinámicamente
        """
        query = "SELECT * FROM asistencias WHERE documento_estudiante = %s AND DATE(fecha_registro) = %s"
        self.db.cursor.execute(query, (documento, fecha))
        return self.db.cursor.fetchall()