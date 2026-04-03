import logging
import os

def configure_logging(log_file=None):
    """Configura logging para consola y archivo (si se proporciona)."""
    if log_file is None:
        log_file = os.path.join(os.path.dirname(__file__), 'crs.log')

    logger = logging.getLogger()
    if logger.handlers:
        return  # ya configurado

    logger.setLevel(logging.INFO)

    fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    try:
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    except Exception:
        # Si no se puede crear archivo, seguimos solo con consola
        logger.warning('No se pudo crear archivo de logs, usando solo consola')
