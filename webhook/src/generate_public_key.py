
from cryptography.hazmat.primitives import serialization
from utils import load_private_key

def save_public_key(private_key):
    """
    Gera e salva a chave pública derivada da chave privada em um arquivo PEM.

    Args:
      private_key: A chave privada da qual a chave pública será derivada.
    """
    
    public_key = private_key.public_key()

    """
      Abre o arquivo 'public_key.pem' em modo binário de escrita e salva a chave pública.
      O formato usado para salvar a chave pública é PEM, com o formato SubjectPublicKeyInfo.
    """

    with open("public_key.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

"""
Carrega a chave privada do sistema e salva a chave pública correspondente.
"""
private_key = load_private_key()
save_public_key(private_key)