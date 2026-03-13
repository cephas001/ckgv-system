from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# Replace with your actual PostgreSQL credentials
# Format: postgresql+asyncpg://user:password@localhost/dbname
DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/ckgv_db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session