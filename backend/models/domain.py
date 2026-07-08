from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy import Column, Integer, String
from core.database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    # Notice the first argument is explicitly the lowercase string for Postgres
    AdminID = Column("adminid", Integer, primary_key=True, index=True)
    Username = Column("username", String, unique=True, index=True)
    PasswordHash = Column("passwordhash", String)
    Role = Column("role", String)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    LogID = Column(Integer, primary_key=True, index=True)
    AdminID = Column(Integer, ForeignKey("admin_users.AdminID"))
    ActionType = Column(String, nullable=False) # E.g., "UPLOAD_PDF", "UPDATE_GRAPH"
    Timestamp = Column(DateTime(timezone=True), server_default=func.now())

class SystemConfig(Base):
    __tablename__ = "system_config"

    ConfigID = Column(Integer, primary_key=True, index=True)
    Model_Version = Column(String, default="en_core_web_md")
    Last_Updated = Column(DateTime(timezone=True), onupdate=func.now())