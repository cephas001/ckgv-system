from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    AdminID = Column(Integer, primary_key=True, index=True)
    Username = Column(String, unique=True, index=True, nullable=False)
    PasswordHash = Column(String, nullable=False)
    Role = Column(String, default="Admin") # E.g., SuperAdmin, Lecturer

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