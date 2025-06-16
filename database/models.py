#!/usr/bin/env python3
"""
ButterflyBlue Database Models
SQLAlchemy models for all platform data
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Decimal, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    subscription_tier = Column(String, default="free")
    
    # Relationships
    tasks = relationship("Task", back_populates="user")
    campaigns = relationship("Campaign", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    agent_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    input_data = Column(JSON)
    output_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="tasks")

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    campaign_type = Column(String, nullable=False)  # email, social, content, etc.
    status = Column(String, default="draft")  # draft, active, paused, completed
    config = Column(JSON)
    metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    launched_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="campaigns")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    amount = Column(Decimal(10, 2), nullable=False)
    currency = Column(String, default="ZAR")
    gateway = Column(String, nullable=False)  # paystack, paypal
    gateway_payment_id = Column(String)
    status = Column(String, default="pending")  # pending, completed, failed, refunded
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="payments")
    invoice = relationship("Invoice", back_populates="payment", uselist=False)

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    payment_id = Column(String, ForeignKey("payments.id"), nullable=False)
    invoice_number = Column(String, unique=True, nullable=False)
    subtotal = Column(Decimal(10, 2), nullable=False)
    tax_amount = Column(Decimal(10, 2), nullable=False)
    total_amount = Column(Decimal(10, 2), nullable=False)
    invoice_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    payment = relationship("Payment", back_populates="invoice")

class AgentStatus(Base):
    __tablename__ = "agent_status"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # online, offline, busy, error
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    metrics = Column(JSON)
    error_count = Column(Integer, default=0)
    
class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    level = Column(String, nullable=False)  # INFO, WARNING, ERROR, CRITICAL
    agent_name = Column(String)
    message = Column(Text, nullable=False)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database connection and session management
class DatabaseManager:
    def __init__(self, database_url: str = "sqlite:///butterflyblue.db"):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
        
    def close_session(self, session):
        """Close database session"""
        session.close()

# Initialize database manager
db_manager = DatabaseManager()