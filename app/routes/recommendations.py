from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.recommendation_service import recommend_articles
from app.models.database import get_db
from app.routes.auth import get_current_user
from typing import List

router = APIRouter()

@router.get("/recommendations/{user_id}", response_model=List[str])
def get_recommendations(user_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return recommend_articles(user_id, db)