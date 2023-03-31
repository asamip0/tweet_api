from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime


class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tweet = Column(String, unique=True, index=True)
    created_on = Column(DateTime)
    modified_on = Column(DateTime)
