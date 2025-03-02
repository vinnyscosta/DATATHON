from fastapi import APIRouter, HTTPException, Depends
from utils.AWS import DynamoDBClient
from routes.auth import verify_token

router = APIRouter()


# Rota para buscar noticia
@router.get("/{news_id}", response_model=dict)
def get_user_history(news_id: str, user: str = Depends(verify_token)) -> dict:
    """
    Busca uma noticia.
    """
    history = DynamoDBClient.get_news(news_id)

    if not history:
        raise HTTPException(status_code=404, detail="Histórico não encontrado para o usuário.")  # noqa

    return history
