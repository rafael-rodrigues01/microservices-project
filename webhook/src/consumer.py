import sys
import pika
import asyncio
from src.database import init_db, insert_person_event
from models import PersonEvent


# Função para processar as mensagens
async def process_message(ch, method, properties, body):
    """
    Processa a mensagem recebida do RabbitMQ e insere no banco de dados PostgreSQL usando SQLAlchemy.

    Args:
        ch: Canal RabbitMQ.
        method: Método de entrega.
        properties: Propriedades da mensagem.
        body: Corpo da mensagem.
    """
    try:
        # Converte o corpo da mensagem para um dicionário Python
        person_event = eval(body.decode())  # Deserializa a mensagem

        # Insere os dados no banco de dados usando SQLAlchemy
        await insert_person_event(person_event)

        print(f"Evento de pessoa inserido no banco de dados: {person_event}")

    except Exception as e:
        print(f"Erro ao processar a mensagem: {str(e)}")

    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma a mensagem no RabbitMQ

# Função para configurar o consumidor RabbitMQ
def start_consuming():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")  # Host do RabbitMQ conforme especificado no docker-compose
    )
    channel = connection.channel()

    # Declare o nome da fila (deve ser o mesmo usado ao enviar mensagens)
    channel.queue_declare(queue="person_events", durable=True)

    # Configura o consumo da fila e vincula à função de processamento
    channel.basic_consume(queue="person_events", on_message_callback=lambda ch, method, properties, body: asyncio.run(process_message(ch, method, properties, body)))

    print("Aguardando mensagens...")

    # Inicia o consumo
    channel.start_consuming()

if __name__ == "__main__":
    start_consuming()
