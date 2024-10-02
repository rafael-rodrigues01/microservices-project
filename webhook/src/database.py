from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import dotenv
from logging import log

dotenv.load_dotenv()

# URL de conexão com o banco de dados
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

print(type, DATABASE_URL)
log(DATABASE_URL)

# Cria o engine assíncrono para o SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Cria uma sessão assíncrona
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base para declarar os modelos ORM
Base = declarative_base()

# Função para inicializar o banco de dados
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
