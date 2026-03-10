import re

# ===== VALIDACIONES =====
class Validador:
    
    @staticmethod
    def validar_documento(documento):
        """Valida formato de documento (números)"""
        if not documento or not str(documento).strip():
            return False, "Documento es requerido"
        if not str(documento).isdigit():
            return False, "Documento debe contener solo números"
        if len(str(documento)) < 6:
            return False, "Documento muy corto (mín. 6 dígitos)"
        return True, "OK"
    
    @staticmethod
    def validar_email(email):
        """Valida formato email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email:
            return False, "Email es requerido"
        if not re.match(patron, email):
            return False, "Email inválido"
        return True, "OK"
    
    @staticmethod
    def validar_nombre(nombre):
        """Valida que nombre no esté vacío y tenga formato"""
        if not nombre or not str(nombre).strip():
            return False, "Nombre es requerido"
        if len(str(nombre)) < 3:
            return False, "Nombre muy corto (mín. 3 caracteres)"
        if any(char.isdigit() for char in nombre[:1]):  # No puede empezar con número
            return False, "Nombre no puede empezar con número"
        return True, "OK"
    
    @staticmethod
    def validar_password(password):
        """Valida contraseña: 8+ chars, mayús, minús, números"""
        requisitos = {
            'longitud': len(password) >= 8,
            'mayuscula': any(c.isupper() for c in password),
            'minuscula': any(c.islower() for c in password),
            'numero': any(c.isdigit() for c in password)
        }
        
        if not all(requisitos.values()):
            falta = []
            if not requisitos['longitud']:
                falta.append("8+ caracteres")
            if not requisitos['mayuscula']:
                falta.append("mayúscula")
            if not requisitos['minuscula']:
                falta.append("minúscula")
            if not requisitos['numero']:
                falta.append("número")
            return False, f"Falta: {', '.join(falta)}"
        
        return True, "OK"
    
    @staticmethod
    def validar_credenciales(usuario, password):
        """Valida usuario y contraseña juntos"""
        if not usuario or not password:
            return False, "Usuario y contraseña son requeridos"
        if len(str(usuario)) < 3:
            return False, "Usuario muy corto"
        if len(password) < 4:
            return False, "Contraseña muy corta"
        return True, "OK"
    
    @staticmethod
    def validar_registro_aprendiz(datos_dict):
        """Valida diccionario de registro de aprendiz"""
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
