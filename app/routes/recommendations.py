from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.services.recommendation_service import recommend_articles

router = APIRouter()


@router.get("/recommendations/{user_id}", response_model=List[Dict[str, Any]])
def get_recommendations(user_id: str):
    recommendations = recommend_articles(user_id)

    if not recommendations:
        raise HTTPException(status_code=404, detail="Nenhuma recomendação encontrada para este usuário")

    return recommendations
