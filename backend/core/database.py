from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch the database URL securely
DATABASE_URL = os.getenv("DATABASE_URL")

# Safety check to ensure the URL was successfully loaded
if not DATABASE_URL:
    raise ValueError("CRITICAL: DATABASE_URL environment variable is not set.")

# Initialize the async engine using the secured URL
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session