from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class UserHistory(Base):
    __tablename__ = "user_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)