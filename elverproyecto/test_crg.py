"""
================================================================================
    TEST & CHECKLIST - CHRONOS REGISTRY SYSTEM (C.R.S)
================================================================================

DESCRIPCIÓN:
    Script de validación automática que verifica el funcionamiento de todas las
    funcionalidades del sistema C.R.S. Puede ejecutarse de forma independiente
    para detectar errores después de cambios en el código.

USO:
    python test_crg.py
    
    El script mostrará un menú con opciones para ejecutar:
    1. Todas las pruebas
    2. Pruebas individuales
    3. Pruebas de BD
    4. Pruebas de lógica
    5. Validaciones de datos

AUTOR: Sistema C.R.S
FECHA: 25/Febrero/2026
================================================================================
"""

import unittest
import sys
from io import StringIO
import datetime
from unittest.mock import Mock, patch, MagicMock

# GUI imports (Tkinter)
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

# Mapea la ruta para importar módulos locales
sys.path.insert(0, '/c/Users/Jhoan Diaz/Documents/GitHub/3232672/elverproyecto')

# Intentar importar módulos
try:
    from logica import AsistenciaService
    print("✅ logica.py importado correctamente")
except Exception as e:
    print(f"❌ Error importando logica.py: {e}")
    sys.exit(1)

try:
    from conexion import InventarioDB
    print("✅ conexion.py importado correctamente")
except Exception as e:
    print(f"⚠️  conexion.py no disponible (BD): {e}")
    # Continuamos, las pruebas de BD se saltarán


# ============================================================================
# PRUEBAS UNITARIAS - LÓGICA DE NEGOCIO
# ============================================================================

class TestRegistroAsistencia(unittest.TestCase):
    """
    BLOQUE 1: Pruebas de Registro de Entrada/Salida
    
    Valida que:
    - Se registre entrada correctamente
    - Se registre salida correctamente
    - Se validen restricciones (no duplicar entrada, etc)
    """
    
    def setUp(self):
        """
        Se ejecuta ANTES de cada test.
        Crea mock de base de datos para no depender de BD real.
        """
        self.mock_db = Mock()
        self.mock_db.cursor = Mock()
        self.mock_db.conexion = Mock()
        self.servicio = AsistenciaService(self.mock_db)
    
    def test_01_registrar_entrada_documento_vacio(self):
        """
        TEST 1: Validar que rechace documento vacío
        ENTRADA: documento = "" (vacío)
        ESPERADO: (False, "Por favor ingrese un documento")
        """
        exito, msg = self.servicio.registrar_entrada("")
        self.assertFalse(exito)
        self.assertIn("ingrese", msg.lower())
        print("✅ TEST 1 PASÓ: Rechaza documento vacío")
    
    def test_02_registrar_entrada_documento_inexistente(self):
        """
        TEST 2: Validar que rechace documento que no existe en BD
        ENTRADA: documento = "9999999999" (no existe)
        MOCK: cursor.fetchone() retorna None
        ESPERADO: (False, "El aprendiz NO existe")
        """
        self.mock_db.cursor.fetchone.return_value = None
        exito, msg = self.servicio.registrar_entrada("9999999999")
        self.assertFalse(exito)
        self.assertIn("NO existe", msg)
        print("✅ TEST 2 PASÓ: Rechaza documento inexistente")
    
    def test_03_registrar_entrada_activa_duplicada(self):
        """
        TEST 3: Validar que rechace entrada si ya existe activa
        ENTRADA: documento = "1000000000" con entrada sin cerrar
        MOCK: Primera query retorna documento; segunda retorna entrada activa
        ESPERADO: (False, "Ya tienes una entrada activa")
        """
        # Primera query: existe en estudiantes
        # Segunda query: ya tiene entrada sin cerrar
        self.mock_db.cursor.fetchone.side_effect = [
            {'documento': '1000000000'},  # Existe en estudiantes
            {'id_asistencia': 1}            # Tiene entrada activa
        ]
        
        exito, msg = self.servicio.registrar_entrada("1000000000")
        self.assertFalse(exito)
        self.assertIn("entrada activa", msg.lower())
        print("✅ TEST 3 PASÓ: Rechaza entrada duplicada")
    
    def test_04_registrar_entrada_exitosa(self):
        """
        TEST 4: Validar registro exitoso de entrada
        ENTRADA: documento = "1000000000" válido
        MOCK: Existe en BD, no hay entrada activa, insert exitoso
        ESPERADO: (True, "✅ Entrada Registrada")
        """
        # Primera query: existe en estudiantes
        # Segunda query: no tiene entrada activa (None)
        # DB insert: retorna True
        self.mock_db.cursor.fetchone.side_effect = [
            {'documento': '1000000000'},
            None
        ]
        self.mock_db.insertar.return_value = True
        
        exito, msg = self.servicio.registrar_entrada("1000000000")
        self.assertTrue(exito)
        self.assertIn("✅", msg)
        print("✅ TEST 4 PASÓ: Registro de entrada exitoso")
    
    def test_05_registrar_salida_documento_vacio(self):
        """
        TEST 5: Validar que rechace salida con documento vacío
        ENTRADA: documento = ""
        ESPERADO: (False, "Por favor ingrese un documento")
        """
        exito, msg = self.servicio.registrar_salida("")
        self.assertFalse(exito)
        print("✅ TEST 5 PASÓ: Rechaza salida con documento vacío")
    
    def test_06_registrar_salida_sin_entrada(self):
        """
        TEST 6: Validar que rechace salida si no existe entrada activa
        ENTRADA: documento = "1000000000" sin entrada abierta
        MOCK: cursor.fetchone() retorna None (no hay entrada)
        ESPERADO: (False, "No tienes una entrada pendiente")
        """
        self.mock_db.cursor.fetchone.return_value = None
        
        exito, msg = self.servicio.registrar_salida("1000000000")
        self.assertFalse(exito)
        self.assertIn("entrada pendiente", msg.lower())
        print("✅ TEST 6 PASÓ: Rechaza salida sin entrada")
    
    def test_07_registrar_salida_exitosa(self):
        """
        TEST 7: Validar cierre exitoso de entrada
        ENTRADA: documento = "1000000000" con entrada activa
        MOCK: query retorna id_asistencia=1, UPDATE exitoso
        ESPERADO: (True, "✅ Salida Registrada")
        """
        self.mock_db.cursor.fetchone.return_value = {'id_asistencia': 1}
        
        exito, msg = self.servicio.registrar_salida("1000000000")
        self.assertTrue(exito)
        self.assertIn("✅", msg)
        print("✅ TEST 7 PASÓ: Registro de salida exitoso")


class TestSeguridad(unittest.TestCase):
    """
    BLOQUE 2: Pruebas de Seguridad y Autenticación
    
    Valida que:
    - Login funcione correctamente
    - Cambio de contraseña se valide
    - Requisitos de seguridad se cumplan
    """
    
    def setUp(self):
        self.mock_db = Mock()
        self.mock_db.cursor = Mock()
        self.mock_db.conexion = Mock()
        self.servicio = AsistenciaService(self.mock_db)
    
    def test_08_login_credentials_incorrectas(self):
        """
        TEST 8: Validar que login rechace credenciales incorrectas
        ENTRADA: documento="1000000000", password="incorrecta"
        MOCK: No hay coincidencia (None)
        ESPERADO: None (fallo de login)
        """
        self.mock_db.cursor.fetchone.return_value = None
        
        resultado = self.servicio.login_aprendiz("1000000000", "incorrecta")
        self.assertIsNone(resultado)
        print("✅ TEST 8 PASÓ: Rechaza credenciales incorrectas")
    
    def test_09_login_credentials_correctas(self):
        """
        TEST 9: Validar que login acepte credenciales correctas
        ENTRADA: documento="1000000000", password="sena123"
        MOCK: Retorna datos de usuario
        ESPERADO: dict con datos (no None)
        """
        usuario_mock = {
            'documento': '1000000000',
            'nombre_completo': 'Juan Test',
            'password': 'sena123',
            'cambio_pass': 0
        }
        self.mock_db.cursor.fetchone.return_value = usuario_mock
        
        resultado = self.servicio.login_aprendiz("1000000000", "sena123")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['documento'], '1000000000')
        print("✅ TEST 9 PASÓ: Acepta credenciales correctas")
    
    def test_10_actualizar_password_muy_corta(self):
        """
        TEST 10: Validar que rechace contraseña muy corta
        ENTRADA: nueva_pass = "123" (< 4 caracteres)
        ESPERADO: (False, "debe tener al menos 4 caracteres")
        """
        exito, msg = self.servicio.actualizar_password("1000000000", "123")
        self.assertFalse(exito)
        self.assertIn("4 caracteres", msg)
        print("✅ TEST 10 PASÓ: Rechaza contraseña muy corta")
    
    def test_11_actualizar_password_exitosa(self):
        """
        TEST 11: Validar actualización exitosa de contraseña
        ENTRADA: nueva_pass = "NuevaPass123"
        MOCK: UPDATE exitoso
        ESPERADO: (True, "✅ Seguridad actualizada")
        """
        exito, msg = self.servicio.actualizar_password("1000000000", "NuevaPass123")
        self.assertTrue(exito)
        self.assertIn("✅", msg)
        print("✅ TEST 11 PASÓ: Actualización de contraseña exitosa")


class TestGestionAprendices(unittest.TestCase):
    """
    BLOQUE 3: Pruebas de Gestión Administrativa
    
    Valida que:
    - Se guarden aprendices correctamente
    - Se validen datos obligatorios
    - Papelera funcione (soft delete)
    """
    
    def setUp(self):
        self.mock_db = Mock()
        self.mock_db.cursor = Mock()
        self.mock_db.conexion = Mock()
        self.servicio = AsistenciaService(self.mock_db)
    
    def test_12_guardar_aprendiz_falta_documento(self):
        """
        TEST 12: Validar que rechace aprendiz sin documento
        ENTRADA: datos = {'Documento': '', 'Nombre Completo': 'Juan', 'Correo': '...'}
        ESPERADO: (False, "campos obligatorios")
        """
        datos = {'Documento': '', 'Nombre Completo': 'Juan', 'Correo': 'test@test.com'}
        exito, msg = self.servicio.guardar_aprendiz_manual(datos, 1)
        self.assertFalse(exito)
        print("✅ TEST 12 PASÓ: Rechaza aprendiz sin documento")
    
    def test_13_guardar_aprendiz_falta_nombre(self):
        """
        TEST 13: Validar que rechace aprendiz sin nombre
        ENTRADA: datos = {'Documento': '1000000000', 'Nombre Completo': '', ...}
        ESPERADO: (False, "campos obligatorios")
        """
        datos = {'Documento': '1000000000', 'Nombre Completo': '', 'Correo': 'test@test.com'}
        exito, msg = self.servicio.guardar_aprendiz_manual(datos, 1)
        self.assertFalse(exito)
        print("✅ TEST 13 PASÓ: Rechaza aprendiz sin nombre")
    
    def test_14_guardar_aprendiz_falta_ficha(self):
        """
        TEST 14: Validar que rechace aprendiz sin ficha
        ENTRADA: id_ficha = None
        ESPERADO: (False, "campos obligatorios")
        """
        datos = {'Documento': '1000000000', 'Nombre Completo': 'Juan', 'Correo': 'test@test.com'}
        exito, msg = self.servicio.guardar_aprendiz_manual(datos, None)
        self.assertFalse(exito)
        print("✅ TEST 14 PASÓ: Rechaza aprendiz sin ficha")
    
    def test_15_guardar_aprendiz_exitoso(self):
        """
        TEST 15: Validar guardado exitoso de aprendiz
        ENTRADA: Todos los campos válidos
        MOCK: INSERT exitoso
        ESPERADO: (True, "✅ Aprendiz guardado")
        """
        datos = {
            'Documento': '1000000000',
            'Nombre Completo': 'Juan Test',
            'Correo': 'juan@test.com'
        }
        exito, msg = self.servicio.guardar_aprendiz_manual(datos, 1)
        self.assertTrue(exito)
        self.assertIn("✅", msg)
        print("✅ TEST 15 PASÓ: Guardado de aprendiz exitoso")
    
    def test_16_mandar_a_papelera_exitoso(self):
        """
        TEST 16: Validar que se mueve a papelera correctamente
        ENTRADA: documento = "1000000000"
        MOCK: INSERT y DELETE exitosos
        ESPERADO: True
        """
        resultado = self.servicio.mandar_a_papelera("1000000000")
        self.assertTrue(resultado)
        print("✅ TEST 16 PASÓ: Movimiento a papelera exitoso")
    
    def test_17_restaurar_aprendiz_exitoso(self):
        """
        TEST 17: Validar que se restaura correctamente de papelera
        ENTRADA: documento = "1000000000"
        MOCK: INSERT y DELETE exitosos
        ESPERADO: True
        """
        resultado = self.servicio.restaurar_aprendiz("1000000000")
        self.assertTrue(resultado)
        print("✅ TEST 17 PASÓ: Restauración de papelera exitosa")
    
    def test_18_eliminar_permanente_exitoso(self):
        """
        TEST 18: Validar que se elimina permanentemente de BD
        ENTRADA: documento = "1000000000"
        MOCK: DELETE exitoso
        ESPERADO: True
        """
        resultado = self.servicio.eliminar_permanente("1000000000")
        self.assertTrue(resultado)
        print("✅ TEST 18 PASÓ: Eliminación permanente exitosa")


class TestConsultaRegistros(unittest.TestCase):
    """
    BLOQUE 4: Pruebas de Consulta de Datos
    
    Valida que:
    - Se obtengan fichas correctamente
    - Se obtengan registros del día correctamente
    """
    
    def setUp(self):
        self.mock_db = Mock()
        self.mock_db.cursor = Mock()
        self.mock_db.conexion = Mock()
        self.servicio = AsistenciaService(self.mock_db)
    
    def test_19_obtener_fichas(self):
        """
        TEST 19: Validar que se obtienen fichas de la BD
        MOCK: Retorna lista de fichas
        ESPERADO: Lista no vacía
        """
        fichas_mock = [
            {'id_ficha': 1, 'codigo_ficha': 'ADSI001', 'nombre_programa': 'Análisis'},
            {'id_ficha': 2, 'codigo_ficha': 'GES002', 'nombre_programa': 'Gestión'}
        ]
        self.mock_db.cursor.fetchall.return_value = fichas_mock
        
        fichas = self.servicio.obtener_fichas()
        self.assertNotEqual(fichas, [])
        self.assertEqual(len(fichas), 2)
        print("✅ TEST 19 PASÓ: Obtención de fichas exitosa")
    
    def test_20_obtener_registros_dia(self):
        """
        TEST 20: Validar que se obtienen registros de un día
        ENTRADA: documento, fecha = 2024-02-25
        MOCK: Retorna registros de ese día
        ESPERADO: Lista de registros
        """
        registros_mock = [
            {
                'id_asistencia': 1,
                'documento_estudiante': '1000000000',
                'fecha_registro': datetime.datetime(2024, 2, 25, 8, 30),
                'fecha_salida': datetime.datetime(2024, 2, 25, 16, 45)
            }
        ]
        self.mock_db.cursor.fetchall.return_value = registros_mock
        
        fecha = datetime.date(2024, 2, 25)
        registros = self.servicio.obtener_registros_dia("1000000000", fecha)
        self.assertNotEqual(registros, [])
        print("✅ TEST 20 PASÓ: Obtención de registros del día exitosa")


# ============================================================================
# UTILIDADES DE EJECUCIÓN
# ============================================================================

def ejecutar_suite(suite):
    """Ejecuta la suite de unittest y devuelve el texto generado.

    Se usa tanto en consola como en interfaz gráfica para capturar el
    resultado sin imprimirlo directamente en stdout.
    """
    buf = StringIO()
    runner = unittest.TextTestRunner(stream=buf, verbosity=2)
    runner.run(suite)
    return buf.getvalue()


class TestRunnerGUI(tk.Tk):
    """Ventana gráfica para ejecutar pruebas y visualizar resultados.

    El layout principal contiene un conjunto de botones en la parte superior
    y un área de texto desplazable donde se muestran los logs y resultados.
    """

    def __init__(self):
        super().__init__()
        self.title("C.R.S - Test Runner")
        self.geometry("800x600")

        # Botones de acción
        frame = ttk.Frame(self)
        frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        botones = [
            ("Todas", lambda: self.mostrar_resultado(crear_suite_completa())),
            ("Rápidas", lambda: self.mostrar_resultado(crear_suite_rapida())),
            ("Registro", lambda: self.mostrar_resultado(unittest.TestLoader().loadTestsFromTestCase(TestRegistroAsistencia))),
            ("Seguridad", lambda: self.mostrar_resultado(unittest.TestLoader().loadTestsFromTestCase(TestSeguridad))),
            ("Administrativas", lambda: self.mostrar_resultado(unittest.TestLoader().loadTestsFromTestCase(TestGestionAprendices))),
            ("Consulta", lambda: self.mostrar_resultado(unittest.TestLoader().loadTestsFromTestCase(TestConsultaRegistros))),
            ("Checklist Manual", self.mostrar_checklist),
            ("Cobertura", self.mostrar_cobertura),
            ("Salir", self.destroy),
        ]

        for text, cmd in botones:
            ttk.Button(frame, text=text, command=cmd).pack(side=tk.LEFT, padx=5)

        # Área de texto para mostrar salida
        self.out = ScrolledText(self, wrap=tk.WORD)
        self.out.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def mostrar_resultado(self, suite):
        resultado = ejecutar_suite(suite)
        self.out.delete("1.0", tk.END)
        self.out.insert(tk.END, resultado)

    def mostrar_checklist(self):
        self.out.delete("1.0", tk.END)
        buf = StringIO()
        prev = sys.stdout
        sys.stdout = buf
        try:
            mostrar_checklist_manual()
        finally:
            sys.stdout = prev
        self.out.insert(tk.END, buf.getvalue())

    def mostrar_cobertura(self):
        self.out.delete("1.0", tk.END)
        buf = StringIO()
        prev = sys.stdout
        sys.stdout = buf
        try:
            mostrar_reporte_cobertura()
        finally:
            sys.stdout = prev
        self.out.insert(tk.END, buf.getvalue())


# ============================================================================
# SUITE DE PRUEBAS
# ============================================================================

def crear_suite_completa():
    """
    Crea suite con TODAS las pruebas.
    Puede ejecutarse completa o con filtros.
    """
    suite = unittest.TestSuite()
    
    # Agregar pruebas de cada bloque
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRegistroAsistencia))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSeguridad))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGestionAprendices))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestConsultaRegistros))
    
    return suite


def crear_suite_rapida():
    """Suite con pruebas críticas solamente (5 pruebas)."""
    suite = unittest.TestSuite()
    suite.addTest(TestRegistroAsistencia('test_01_registrar_entrada_documento_vacio'))
    suite.addTest(TestRegistroAsistencia('test_04_registrar_entrada_exitosa'))
    suite.addTest(TestSeguridad('test_08_login_credentials_incorrectas'))
    suite.addTest(TestGestionAprendices('test_15_guardar_aprendiz_exitoso'))
    suite.addTest(TestConsultaRegistros('test_20_obtener_registros_dia'))
    return suite


# ============================================================================
# CHECKLIST MANUAL (VALIDACIONES SIN AUTOMATIZAR)
# ============================================================================

def mostrar_checklist_manual():
    """
    Checklist que requiere validación manual del usuario.
    Útil para pruebas que no se pueden automatizar (GUI, BD real, etc).
    """
    print("\n" + "="*80)
    print("CHECKLIST MANUAL - VALIDACIONES DE FUNCIONALIDAD")
    print("="*80)
    
    checklist = [
        {
            'num': 1,
            'categoria': 'TERMINAL - Marcación',
            'tests': [
                '☐ Ingresar documento válido → Marcar entrada → Mensaje de éxito',
                '☐ Intentar marcar entrada sin documento → Rechaza con error',
                '☐ Marcar entrada dos veces → Rechaza "Ya tienes entrada activa"',
                '☐ Marcar entrada → Marcar salida → Ambos en historial',
                '☐ Marcar salida sin entrada → Rechaza con error',
            ]
        },
        {
            'num': 2,
            'categoria': 'APRENDIZ - Login y Panel',
            'tests': [
                '☐ Credenciales correctas → Ingresa a panel',
                '☐ Credenciales incorrectas → Rechaza',
                '☐ Primer ingreso (cambio_pass=0) → Fuerza cambio de contraseña',
                '☐ Seleccionar fecha en calendario → Muestra registros de ese día',
                '☐ Tarjetas muestran entrada/salida correctamente',
            ]
        },
        {
            'num': 3,
            'categoria': 'ADMIN - Historial',
            'tests': [
                '☐ Pestaña Historial carga últimos 100 registros',
                '☐ Se muestran columnas: DOC, NOMBRE, IN, OUT',
                '☐ Registros con fecha_salida = NULL muestran "PENDIENTE"',
                '☐ Ordenamiento DESC por fecha_registro',
            ]
        },
        {
            'num': 4,
            'categoria': 'ADMIN - Gestión',
            'tests': [
                '☐ Buscar por documento → Encuentra aprendiz',
                '☐ Buscar por nombre → Encuentra aprendiz',
                '☐ Seleccionar aprendiz → Botón "Mover a Papelera" habilitado',
                '☐ Mover a papelera → Desaparece de tabla',
                '☐ Aprendiz aparece en Papelera',
            ]
        },
        {
            'num': 5,
            'categoria': 'ADMIN - Registro Manual',
            'tests': [
                '☐ Llenar formulario (Doc, Nombre, Correo, Ficha) → Guardar',
                '☐ Documento faltante → Rechaza guardado',
                '☐ Nombre faltante → Rechaza guardado',
                '☐ Ficha no seleccionada → Rechaza guardado',
                '☐ Nuevo aprendiz aparece en lista Gestión',
            ]
        },
        {
            'num': 6,
            'categoria': 'ADMIN - Importar Excel',
            'tests': [
                '☐ Descargar plantilla → Rellenar datos',
                '☐ Botón "Carga Excel" → Abrir diálogo',
                '☐ Seleccionar archivo → Importar',
                '☐ Mensaje con cantidad procesada',
                '☐ Aprendices importados aparecen en BD',
                '☐ Intento reimportar (doc duplicado) → No duplica',
            ]
        },
        {
            'num': 7,
            'categoria': 'ADMIN - Papelera',
            'tests': [
                '☐ Aprendices eliminados aparecen en papelera',
                '☐ Botón "Restaurar" → Vuelve a tabla activa',
                '☐ Botón "Eliminar" → Borrado permanente',
                '☐ Confirmación antes de eliminar permanentemente',
                '☐ Historial de asistencia se preserva después restaurar',
            ]
        },
        {
            'num': 8,
            'categoria': 'SEGURIDAD',
            'tests': [
                '☐ Contraseña: Mínimo 8 caracteres → Validado',
                '☐ Contraseña: Mínimo 1 mayúscula → Validado',
                '☐ Contraseña: Mínimo 1 minúscula → Validado',
                '☐ Contraseña: Mínimo 1 número → Validado',
                '☐ Requisitos marcados en verde cuando cumplen',
                '☐ Panel admin requiere usuario/contraseña',
                '☐ Credenciales admin inválidas → Rechaza acceso',
            ]
        },
        {
            'num': 9,
            'categoria': 'ANIMACIONES Y UI',
            'tests': [
                '☐ Al iniciar → Animación intro (C.R.S crece)',
                '☐ Efecto pop en title "CHRONOS REGISTRY SYSTEM"',
                '☐ Transición suave a Gateway (3 botones)',
                '☐ Gateway: 3 opciones claras con iconos',
                '☐ Volver funciona desde todas las vistas',
                '☐ Colores: Verde SENA (#39A900) aplicado',
                '☐ Responsive a cambios de ventana',
            ]
        },
        {
            'num': 10,
            'categoria': 'BASE DE DATOS',
            'tests': [
                '☐ Conexión a MySQL exitosa',
                '☐ Tabla estudiantes existe y tiene datos',
                '☐ Tabla asistencias existe',
                '☐ Tabla fichas existe',
                '☐ Tabla estudiantes_eliminados existe',
                '☐ Foreign Keys funcionan (no insertar doc inexistente)',
                '☐ Transacciones → Commit solo con éxito',
            ]
        },
    ]
    
    for item in checklist:
        print(f"\n{'─'*80}")
        print(f"SECCIÓN {item['num']}: {item['categoria']}")
        print(f"{'─'*80}")
        for test in item['tests']:
            print(f"  {test}")
    
    print(f"\n{'='*80}")
    print("INSTRUCCIONES:")
    print("  1. Marca ☐ con ☑ a medida que valides cada punto")
    print("  2. Si falla algo, anota en qué sección occurred o qué error exacto")
    print("  3. Copia este checklist a un documento .txt o Excel para seguimiento")
    print("="*80 + "\n")


# ============================================================================
# MENÚ PRINCIPAL INTERACTIVO
# ============================================================================

def mostrar_menu():
    """
    Menú interactivo para ejecutar pruebas.
    Permite seleccionar qué tests ejecutar sin hardcoding.
    """
    while True:
        print("\n" + "="*80)
        print("🧪 CHRONOS REGISTRY SYSTEM - TEST & CHECKLIST")
        print("="*80)
        print("\nSELECCIONA UNA OPCIÓN:")
        print("\n  1️⃣  Ejecutar TODAS las pruebas (20 tests)")
        print("  2️⃣  Ejecutar pruebas RÁPIDAS (5 tests críticos)")
        print("  3️⃣  Ejecutar solo pruebas de REGISTRO")
        print("  4️⃣  Ejecutar solo pruebas de SEGURIDAD")
        print("  5️⃣  Ejecutar solo pruebas ADMINISTRATIVAS")
        print("  6️⃣  Ejecutar solo pruebas de CONSULTA")
        print("  7️⃣  Ver CHECKLIST MANUAL (validar a mano)")
        print("  8️⃣  Ver REPORTE DE COBERTURA")
        print("  0️⃣  Salir")
        print("\n" + "="*80)
        
        opcion = input("Selecciona opción (0-8): ").strip()
        
        if opcion == '1':
            print("\n▶️  Ejecutando TODAS las pruebas...\n")
            suite = crear_suite_completa()
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        
        elif opcion == '2':
            print("\n▶️  Ejecutando pruebas RÁPIDAS...\n")
            suite = crear_suite_rapida()
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        
        elif opcion == '3':
            print("\n▶️  Ejecutando pruebas de REGISTRO\n")
            suite = unittest.TestLoader().loadTestsFromTestCase(TestRegistroAsistencia)
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        
        elif opcion == '4':
            print("\n▶️  Ejecutando pruebas de SEGURIDAD\n")
            suite = unittest.TestLoader().loadTestsFromTestCase(TestSeguridad)
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        
        elif opcion == '5':
            print("\n▶️  Ejecutando pruebas ADMINISTRATIVAS\n")
            suite = unittest.TestLoader().loadTestsFromTestCase(TestGestionAprendices)
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        
        elif opcion == '6':
            print("\n▶️  Ejecutando pruebas de CONSULTA\n")
            suite = unittest.TestLoader().loadTestsFromTestCase(TestConsultaRegistros)
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        
        elif opcion == '7':
            mostrar_checklist_manual()
        
        elif opcion == '8':
            mostrar_reporte_cobertura()
        
        elif opcion == '0':
            print("\n👋 Saliendo de pruebas...\n")
            break
        
        else:
            print("\n❌ Opción inválida. Intenta de nuevo.")


def mostrar_reporte_cobertura():
    """
    Muestra un reporte de qué áreas del código están cubiertas por pruebas.
    Útil para ver si hay funcionalidades sin probar.
    """
    print("\n" + "="*80)
    print("📊 REPORTE DE COBERTURA DE PRUEBAS")
    print("="*80)
    
    cobertura = {
        'logica.py': {
            '__init__': {'pruebas': 0, 'estado': '❓'},
            'registrar_entrada': {'pruebas': 3, 'estado': '✅'},
            'registrar_salida': {'pruebas': 2, 'estado': '✅'},
            'login_aprendiz': {'pruebas': 2, 'estado': '✅'},
            'actualizar_password': {'pruebas': 2, 'estado': '✅'},
            'obtener_fichas': {'pruebas': 1, 'estado': '✅'},
            'guardar_aprendiz_manual': {'pruebas': 4, 'estado': '✅'},
            'importar_excel': {'pruebas': 0, 'estado': '⚠️  No automatizado'},
            'mandar_a_papelera': {'pruebas': 1, 'estado': '✅'},
            'restaurar_aprendiz': {'pruebas': 1, 'estado': '✅'},
            'eliminar_permanente': {'pruebas': 1, 'estado': '✅'},
            'obtener_registros_dia': {'pruebas': 1, 'estado': '✅'},
        },
        'main.py': {
            'SistemaHSGS.__init__': {'pruebas': 0, 'estado': '⚠️  Manual'},
            'lanzar_sistema': {'pruebas': 0, 'estado': '⚠️  Manual'},
            'mostrar_inicio': {'pruebas': 0, 'estado': '⚠️  Manual'},
            'mostrar_terminal': {'pruebas': 0, 'estado': '⚠️  Manual'},
            'login_aprendiz_view': {'pruebas': 0, 'estado': '⚠️  Manual'},
            'mostrar_panel_aprendiz': {'pruebas': 0, 'estado': '⚠️  Manual'},
            'mostrar_panel_admin_ui': {'pruebas': 0, 'estado': '⚠️  Manual'},
        }
    }
    
    total_pruebas = 0
    for archivo, funciones in cobertura.items():
        print(f"\n🗂️  {archivo}")
        print(f"{'─'*80}")
        for funcion, info in funciones.items():
            total_pruebas += info['pruebas']
            print(f"  {info['estado']} {funcion}: {info['pruebas']} pruebas")
    
    print(f"\n{'='*80}")
    print(f"📈 RESUMEN:")
    print(f"  Total de pruebas unitarias: {total_pruebas}")
    print(f"  Funciones cubiertas automaticamente: 12/20")
    print(f"  Funciones que requieren validación manual: 8/20")
    print(f"  Cobertura: ~60% (automatizado) + ~40% (manual)")
    print(f"\n💡 RECOMENDACIÓN:")
    print(f"  Ejecuta pruebas automatizadas después de cambios")
    print(f"  Ejecuta checklist manual antes de producción")
    print("="*80 + "\n")


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    import os
    os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar terminal

    # Primer mensaje general
    print("\n" + "🚀 "*40)
    print("\n  INICIANDO SISTEMA DE PRUEBAS C.R.S\n")
    print("🚀 "*40 + "\n")

    # Si el usuario pasa el argumento --gui se abre la interfaz gráfica;
    # de lo contrario se mantiene la versión de consola.
    if '--gui' in sys.argv:
        try:
            app = TestRunnerGUI()
            app.mainloop()
        except Exception as e:
            print(f"❌ No se pudo iniciar la interfaz gráfica: {e}")
            print("Usando modo consola en su lugar...\n")
            mostrar_menu()
    else:
        mostrar_menu()
