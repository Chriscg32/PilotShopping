from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    subscription_tier = Column(String, default="starter")
    api_key = Column(String, unique=True)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    campaigns = relationship("Campaign", back_populates="user")
    tasks = relationship("Task", back_populates="user")
    usage_metrics = relationship("UsageMetric", back_populates="user")

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # marketing, development, etc.
    status = Column(String, default="active")
    configuration = Column(JSON)
    results = Column(JSON)
    created_at = Column(DateTime, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="campaigns")
    tasks = relationship("Task", back_populates="campaign")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    campaign_id = Column(String, ForeignKey("campaigns.id"))
    agent_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    status = Column(String, default="pending")
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(String)
    processing_time = Column(Integer)  # milliseconds
    created_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="tasks")
    campaign = relationship("Campaign", back_populates="tasks")

class UsageMetric(Base):
    __tablename__ = "usage_metrics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    metric_type = Column(String, nullable=False)  # api_calls, ai_requests, etc.
    value = Column(Integer, nullable=False)
    period = Column(String, nullable=False)  # daily, monthly
    date = Column(DateTime, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="usage_metrics")