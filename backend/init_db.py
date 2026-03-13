import asyncio
from database import engine, Base, AsyncSessionLocal
from models import AdminUser
from passlib.context import CryptContext
from sqlalchemy.future import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init_models():
    # 1. Create the tables in PostgreSQL (Safely ignores if they exist)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 2. Insert a default admin user
    async with AsyncSessionLocal() as session:
        # Check if 'admin' already exists
        result = await session.execute(select(AdminUser).where(AdminUser.Username == "admin"))
        existing_admin = result.scalars().first()
        
        if existing_admin:
            print("Admin user already exists in the database. Ready to go!")
        else:
            # Hash the password "mcpherson2026"
            hashed_pwd = pwd_context.hash("mcpherson2026")
            
            new_admin = AdminUser(
                Username="admin",
                PasswordHash=hashed_pwd,
                Role="SuperAdmin"
            )
            session.add(new_admin)
            await session.commit()
            print("Database initialized and default Admin created successfully!")

if __name__ == "__main__":
    asyncio.run(init_models())