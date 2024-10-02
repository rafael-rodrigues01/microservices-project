import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from utils import load_public_key, log

"""
Carrega a chave pública do sistema.
A chave pública é usada para criptografar os dados sensíveis.
"""
public_key = load_public_key()

"""
Dados sensíveis que serão criptografados.
Inclui informações pessoais como nome, email, gênero, data de nascimento, endereço, salário e CPF.
"""
data_to_encrypt = '{"name": "Rafael Rodrigues", "email": "rafa@example.com", "gender": "male", "birth_date": "1990-01-01", "address": "123 Main St", "salary": 50000, "cpf": "12345678901"}'

"""
Criptografa os dados utilizando a chave pública com OAEP (Optimal Asymmetric Encryption Padding).
A criptografia usa SHA-256 como algoritmo de hash.
"""
encrypted_data = public_key.encrypt(
    data_to_encrypt.encode('utf-8'),  # Codifica a string de dados para bytes
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Função de geração de máscara usando SHA-256
        algorithm=hashes.SHA256(),  # Algoritmo de hash SHA-256 para OAEP
        label=None  # Nenhum rótulo adicional
    )
)

"""
Codifica os dados criptografados em base64 para facilitar o armazenamento ou transporte.
"""
encrypted_base64_data = base64.b64encode(encrypted_data).decode('utf-8')

"""
Loga os dados criptografados em base64.
"""
log(encrypted_base64_data)
