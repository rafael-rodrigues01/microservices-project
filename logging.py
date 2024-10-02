import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log(message: any):
    """
    Loga uma mensagem no nível de informação.

    Args:
        message (any): A mensagem a ser logada.
    """
    logger.info(message)