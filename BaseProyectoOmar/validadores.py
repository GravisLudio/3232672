"""
Módulo Validador
Centraliza toda la validación de datos en la aplicación
"""
import re


class Validador:
    """Proporciona métodos estáticos para validar diferentes tipos de datos."""
    
    @staticmethod
    def validar_documento(documento):
        """
        Valida formato del documento (solo números, 6+ dígitos)
        Returns: (bool, str) - (es_válido, mensaje)
        """
        if not documento or not documento.strip():
            return False, "El documento es requerido"
        
        if not documento.isdigit():
            return False, "El documento solo debe contener números"
        
        if len(documento) < 6:
            return False, "El documento debe tener al menos 6 dígitos"
        
        return True, "Documento válido"
    
    @staticmethod
    def validar_email(email):
        """
        Valida formato de correo electrónico (RFC 5322 simplificado)
        Returns: (bool, str)
        """
        if not email or not email.strip():
            return False, "El correo es requerido"
        
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            return False, "Correo inválido"
        
        return True, "Correo válido"
    
    @staticmethod
    def validar_nombre(nombre):
        """
        Valida nombre (mínimo 3 caracteres, no comienza con número)
        Returns: (bool, str)
        """
        if not nombre or not nombre.strip():
            return False, "El nombre es requerido"
        
        if len(nombre.strip()) < 3:
            return False, "El nombre debe tener al menos 3 caracteres"
        
        if nombre[0].isdigit():
            return False, "El nombre no puede comenzar con número"
        
        return True, "Nombre válido"
    
    @staticmethod
    def validar_password(password):
        """
        Valida contraseña: 8+ caracteres, mayúscula, minúscula, número
        Returns: (bool, str)
        """
        if not password:
            return False, "La contraseña es requerida"
        
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        if not any(c.isupper() for c in password):
            return False, "La contraseña debe contener al menos una mayúscula"
        
        if not any(c.islower() for c in password):
            return False, "La contraseña debe contener al menos una minúscula"
        
        if not any(c.isdigit() for c in password):
            return False, "La contraseña debe contener al menos un número"
        
        return True, "Contraseña válida"
    
    @staticmethod
    def validar_credenciales(usuario, password):
        """
        Valida par usuario/contraseña combinado
        Returns: (bool, str)
        """
        es_valido_user, msg_user = Validador.validar_nombre(usuario)
        if not es_valido_user:
            return False, f"Usuario: {msg_user}"
        
        if len(usuario) < 4:
            return False, "Usuario debe tener al menos 4 caracteres"
        
        es_valido_pass, msg_pass = Validador.validar_password(password)
        if not es_valido_pass:
            return False, f"Contraseña: {msg_pass}"
        
        return True, "Credenciales válidas"
    
    @staticmethod
    def validar_registro_aprendiz(datos):
        """
        Valida todos los datos de un registro de aprendiz
        Args: dict con keys documento, nombre_completo, email
        Returns: (bool, str)
        """
        es_valido, msg = Validador.validar_documento(datos.get('Documento', ''))
        if not es_valido:
            return False, msg
        
        es_valido, msg = Validador.validar_nombre(datos.get('Nombre Completo', ''))
        if not es_valido:
            return False, msg
        
        es_valido, msg = Validador.validar_email(datos.get('Correo', ''))
        if not es_valido:
            return False, msg
        
        return True, "Todos los datos son válidos"
