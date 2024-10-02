from pydantic import BaseModel
from datetime import date
from sqlalchemy import Column, Integer, String, Date, Numeric
from database import Base

class Person(BaseModel):
    """
    Modelo de dados que representa um evento relacionado a uma pessoa.

    Attributes:
        name (str): Nome da pessoa.
        email (str): Email da pessoa.
        gender (str): Gênero da pessoa.
        birth_date (date): Data de nascimento da pessoa.
        address (str): Endereço da pessoa.
        salary (float): Salário da pessoa.
        cpf (str): CPF da pessoa.
    """
    name: str
    email: str
    gender: str
    birth_date: date
    address: str
    salary: float
    cpf: str

class WebhookRequest(BaseModel):
    """
    Modelo de dados que representa uma requisição de webhook.

    Attributes:
        body (str): Corpo da requisição, geralmente em formato JSON.
        event (str): Tipo de evento que disparou a requisição de webhook.
    """
    body: str
    event: str

class FictionalPerson(BaseModel):
    """
    Modelo de dados que representa um evento relacionado a uma pessoa.

    Attributes:
        name (str): Nome da pessoa.
        email (str): Email da pessoa.
        gender (str): Gênero da pessoa.
        birth_date (date): Data de nascimento da pessoa.
        address (str): Endereço da pessoa.
        salary (float): Salário da pessoa.
        cpf (str): CPF da pessoa.
    """
    person_id: int
    name: str
    email: str
    gender: str
    birth_date: date
    address: str
    salary: float
    cpf: str

class FictionalAccount(BaseModel):
    account_id: int
    status_id: int
    due_day: int
    person_id: int
    balance: float
    avaliable_balance: float

class FictionalCard(BaseModel):
    card_id: int
    card_number: float
    account_id: int 
    status_id: int
    limit: float
    expiration_date: str

class PersonEvent(Base):
    __tablename__ = "person_events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    birth_date = Column(Date, nullable=False)
    address = Column(String(255), nullable=False)
    salary = Column(Numeric, nullable=False)
    cpf = Column(String(11), nullable=False)