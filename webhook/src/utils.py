import base64
from datetime import date
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import pika
from models import PersonEvent
from database import async_session
from logging import log

def load_private_key():
    """
    Carrega a chave privada do arquivo PEM.

    Returns:
        private_key: A chave privada carregada do arquivo.
    """
    with open("./webhook/src/private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key

def load_public_key():
    """
    Carrega a chave pública do arquivo PEM.

    Returns:
        public_key: A chave pública carregada do arquivo.
    """
    with open("./webhook/src/public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
    return public_key

def decrypt_body(encrypted_body: str, private_key) -> str:
    """
    Descriptografa um corpo de mensagem criptografado usando uma chave privada.

    Args:
        encrypted_body (str): O corpo da mensagem criptografado em base64.
        private_key: A chave privada usada para descriptografar a mensagem.

    Returns:
        str: O corpo da mensagem descriptografado.
    """
    decrypted_body = private_key.decrypt(
        base64.b64decode(encrypted_body),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Função de geração de máscara usando SHA-256
            algorithm=hashes.SHA256(),  # Algoritmo de hash SHA-256 para OAEP
            label=None  # Nenhum rótulo adicional
        )
    )
    return decrypted_body.decode('utf-8')

def serialize_data(data: dict):
    """
    Serializa os dados, convertendo tipos como datetime.date em strings.
    
    Args:
        data (dict): O dicionário contendo os dados a serem serializados.

    Returns:
        dict: O dicionário com os valores serializados.
    """
    serialized_data = {}
    for key, value in data.items():
        if isinstance(value, date):
            serialized_data[key] = value.isoformat()  # Converte data para string no formato 'YYYY-MM-DD'
        else:
            serialized_data[key] = value
    return serialized_data

def send_to_rabbitmq(queue_name: str, message: dict):
    """
    Envia uma mensagem para a fila RabbitMQ.

    Args:
        message (dict): A mensagem a ser enviada para a fila.
    """
    try:
        """Estabelece conexão com o RabbitMQ"""
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()

        """Declara uma fila chamada 'person_events'"""
        channel.queue_declare(queue=queue_name, durable=True)

        """Publica a mensagem na fila"""
        channel.basic_publish(
            exchange='',
            routing_key= queue_name,
            body=str(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Faz com que a mensagem seja persistida
            )
        )

        """Fecha a conexão"""
        connection.close()
        log("Mensagem enviada para RabbitMQ")

    except Exception as e:
        log(f"Erro ao enviar a mensagem para RabbitMQ: {str(e)}")

async def insert_person_event(person_event: dict):
    """
    Insere um evento de pessoa no banco de dados usando SQLAlchemy.

    Args:
        person_event (dict): Dados do evento da pessoa.

    Returns:
        None
    """
    async with async_session() as session:
        async with session.begin():
            # Cria um objeto do tipo PersonEvent
            new_person = PersonEvent(
                name=person_event['name'],
                email=person_event['email'],
                gender=person_event['gender'],
                birth_date=person_event['birth_date'],
                address=person_event['address'],
                salary=person_event['salary'],
                cpf=person_event['cpf']
            )
            # Adiciona o novo evento à sessão
            session.add(new_person)

        # Confirma a transação
        await session.commit()