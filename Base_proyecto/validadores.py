import re

class Validador:
    @staticmethod
    def validar_documento(documento):
        if not documento or not str(documento).strip():
            return False, "Documento es requerido"
        if not str(documento).isdigit():
            return False, "Documento debe contener solo números"
        if len(str(documento)) < 6:
            return False, "Documento muy corto (mín. 6 dígitos)"
        return True, "OK"
    
    @staticmethod
    def validar_email(email):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email:
            return False, "Email es requerido"
        if not re.match(patron, email):
            return False, "Email inválido"
        return True, "OK"
    
    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not str(nombre).strip():
            return False, "Nombre es requerido"
        if len(str(nombre)) < 3:
            return False, "Nombre muy corto (mín. 3 caracteres)"
        if any(char.isdigit() for char in nombre[:1]):
            return False, "Nombre no puede empezar con número"
        return True, "OK"
    
    # Patrón Regex: mínimo 8 chars, mayúscula, minúscula, dígito y carácter especial
    REGEX_PASSWORD = re.compile(
        r'^(?=.*[A-Z])'          # al menos una mayúscula
        r'(?=.*[a-z])'           # al menos una minúscula
        r'(?=.*\d)'              # al menos un dígito
        r'(?=.*[!@#$%^&*()\-_=+\[\]{};:\'",.<>?/\\|`~])'  # al menos un especial
        r'.{8,}$'                # mínimo 8 caracteres
    )

    @staticmethod
    def validar_password(password):
        requisitos = {
            'longitud':  len(password) >= 8,
            'mayuscula': bool(re.search(r'[A-Z]', password)),
            'minuscula': bool(re.search(r'[a-z]', password)),
            'numero':    bool(re.search(r'\d', password)),
            'especial':  bool(re.search(r'[!@#$%^&*()\-_=+\[\]{};:\'",.<>?/\\|`~]', password)),
        }

        if not all(requisitos.values()):
            falta = []
            if not requisitos['longitud']:  falta.append("8+ caracteres")
            if not requisitos['mayuscula']: falta.append("mayúscula")
            if not requisitos['minuscula']: falta.append("minúscula")
            if not requisitos['numero']:    falta.append("número")
            if not requisitos['especial']:  falta.append("carácter especial (!@#$...)")
            return False, f"Falta: {', '.join(falta)}"
        return True, "OK"
    
    @staticmethod
    def validar_credenciales(usuario, password):
        if not usuario or not password:
            return False, "Usuario y contraseña son requeridos"
        if len(str(usuario)) < 3:
            return False, "Usuario muy corto"
        if len(password) < 4:
            return False, "Contraseña muy corta"
        return True, "OK"
    
    @staticmethod
    def validar_registro_aprendiz(datos_dict):
        doc_valido, msg = Validador.validar_documento(datos_dict.get('Documento'))
        if not doc_valido:
            return False, msg
        
        nombre_valido, msg = Validador.validar_nombre(datos_dict.get('Nombre Completo'))
        if not nombre_valido:
            return False, msg
        
        email_valido, msg = Validador.validar_email(datos_dict.get('Correo'))
        if not email_valido:
            return False, msg
        
        return True, "OK"