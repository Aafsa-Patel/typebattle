from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(50),unique=True,nullable=False,index=True)
    email=Column(String(100),unique=True,nullable=False,index=True)
    password_hash=Column(String(255),nullable=False)
    created_at=Column(DateTime,server_default=func.now())

class PracticeResult(Base):
    __tablename__='practice_results'
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey('users.id'),nullable=False,index=True)
    passage=Column(Text,nullable=False)
    wpm=Column(Float,nullable=False)
    accuracy=Column(Float,nullable=False)
    errors=Column(Integer,nullable=False)
    time_taken=Column(Integer,nullable=False)
    created_at=Column(DateTime,server_default=func.now())

class BattleResult(Base):
    __tablename__='battle_results'
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey('users.id'),nullable=False,index=True)
    mode=Column(String(20),nullable=False)
    wpm=Column(Float,nullable=False,default=0)
    accuracy=Column(Float,nullable=False,default=0)
    score=Column(Integer,nullable=False,default=0)
    won=Column(Boolean,nullable=False,default=False)
    time_taken=Column(Integer,nullable=False,default=0)
    created_at=Column(DateTime,server_default=func.now())
