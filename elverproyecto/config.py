"""
Configuración centralizada para C.R.S (Chronos Registry System)
Colores, constantes y valores por defecto
"""

# ===== COLORES SENA =====
COLORES = {
    'SENA_GREEN': '#39A900',
    'SENA_DARK': '#2D5A27',
    'SENA_ORANGE': '#D46C11',
    'BG_LIGHT': '#FFFFFF',
    'BG_DARK': '#1a1a1a',
    'ERROR': '#E74C3C',
    'WARNING': '#FF9800',
    'SUCCESS': '#39A900',
    'ACCENT': '#E67E22',
    'TEXT_GRAY': '#888888',
    'TEXT_LIGHT_GRAY': '#AAAAAA',
    'BORDER_LIGHT': '#E0E0E0',
    'BORDER_GRAY': '#DDD',
}

# ===== FUENTES =====
FUENTES = {
    'TITULO': ('Segoe UI', 28, 'bold'),
    'SUBTITULO': ('Segoe UI', 16, 'bold'),
    'HEADER': ('Segoe UI', 24, 'bold'),
    'BOTON': ('Segoe UI', 14, 'bold'),
    'NORMAL': ('Segoe UI', 11),
    'SMALL': ('Segoe UI', 10),
    'TINY': ('Segoe UI', 8),
    'LABEL': ('Segoe UI', 13, 'bold'),
}

# ===== DIMENSIONES =====
DIMENSIONES = {
    'BTN_HEIGHT': 65,
    'BTN_WIDTH': 450,
    'VENTANA_LOGIN_WIDTH': 450,
    'VENTANA_LOGIN_HEIGHT': 520,
    'VENTANA_DASHBOARD_WIDTH': 1000,
    'VENTANA_DASHBOARD_HEIGHT': 550,
    'TAB_BORDER_WIDTH': 1,
    'CORNER_RADIUS': 20,
}

# ===== TEXTO Y ETIQUETAS =====
TEXTOS = {
    'TITULO_APP': 'C.R.S - Chronos Registry System',
    'SUBTITULO_APP': 'Sistema Integrado de Registro de Asistencia | High Softwares',
    'WELCOME_SUBTITLE': 'Selecciona tu rol para continuar',
    'ACCESO_SISTEMA': 'ACCESO AL SISTEMA',
    'LOGIN_TITULO': 'LOGIN SEGURO',
    'REG_ASISTENCIA': 'REGISTRO DE ASISTENCIA',
}

# ===== MENSAJES DE ERROR =====
MENSAJES = {
    'SIN_DOC': 'Por favor ingrese un documento.',
    'APRENDIZ_NO_EXISTE': 'El aprendiz NO existe en el sistema.',
    'APRENDIZ_PAPELERA': 'El aprendiz está en la PAPELERA. Contacte al administrador.',
    'ENTRADA_REGISTRADA': 'Entrada registrada correctamente.',
    'SALIDA_REGISTRADA': 'Salida registrada correctamente.',
    'CREDENCIALES_INVALIDAS': 'Credenciales incorrectas',
    'USUARIO_PASS_REQUERIDOS': 'Usuario y contraseña son requeridos',
    'SIN_REGISTROS': 'No hay registros para esta selección',
    'SIN_SELECCION': 'Debe seleccionar al menos una ficha o aprendiz',
    'ACCION_IRREVERSIBLE': 'Esta acción es irreversible',
}

# ===== CACHÉ Y RENDIMIENTO =====
CACHE = {
    'FICHAS_TTL': 3600,  # 1 hora en segundos
    'APRENDICES_TTL': 1800,  # 30 minutos
    'REGISTROS_POR_PAGINA': 100,
}

# ===== CONEXIÓN BD =====
BD = {
    'HOST': 'localhost',
    'USER': 'root',
    'PASSWORD': '',
    'DATABASE': 'TechSenaHSGS',
}

# ===== FEATURES =====
FEATURES = {
    'MODAL_LOGIN_OBLIGATORIO': True,
    'EXPORTAR_PDF': True,
    'EXPORTAR_EXCEL': True,
    'AUDITAR_ACCIONES': True,
    'REQUIERE_CAMBIO_PASS': True,
}
