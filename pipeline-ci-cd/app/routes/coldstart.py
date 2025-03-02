from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from services.coldstart_service import recommend_top_10
from routes.auth import verify_token

router = APIRouter()


@router.get("/top_10", response_model=List[Dict[str, Any]])
def get_recommendations(user: str = Depends(verify_token)):
    recommendations = recommend_top_10()

    if recommendations:
        return recommendations

    raise HTTPException(
        status_code=404,
        detail="Nenhuma recomendação encontrada."
    )
