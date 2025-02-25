import random
from sqlalchemy.orm import Session
from app.models.models import UserHistory, Article
from typing import List


def recommend_articles(user_id: int, db: Session) -> List[str]:
    user_history = db.query(UserHistory).filter(UserHistory.user_id == user_id).all()  # noqa
    if not user_history:
        return ["Artigo Popular 1", "Artigo Popular 2", "Artigo Popular 3"]
    all_articles = db.query(Article).all()
    recommended = random.sample(all_articles, min(10, len(all_articles)))
    return [article.title for article in recommended]
