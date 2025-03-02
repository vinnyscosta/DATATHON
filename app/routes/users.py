from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.utils.AWS import DynamoDBClient  # Certifique-se de que o DynamoDBClient está importado corretamente

router = APIRouter()


# Pydantic model para validação dos dados recebidos na requisição
class InteractionRequest(BaseModel):
    user_id: str
    history: str
    user_type: str
    number_of_clicks: int
    page_visits: int
    scroll_percentage: float
    time_on_page: int


# Rota para cadastrar uma nova interação
@router.post("/add-interaction/")
def add_interaction(request: InteractionRequest):
    """
    Cadastra uma nova interação do usuário no DynamoDB.
    """
    success = DynamoDBClient.add_user_interaction(
        user_id=request.user_id,
        history=request.history,
        user_type=request.user_type,
        number_of_clicks=request.number_of_clicks,
        page_visits=request.page_visits,
        scroll_percentage=request.scroll_percentage,
        time_on_page=request.time_on_page,
    )

    if success:
        return {"message": "Interação salva com sucesso!"}
    else:
        raise HTTPException(status_code=500, detail="Erro ao salvar interação.")


# Rota para buscar o histórico de interações de um usuário
@router.get("/user-history/{user_id}", response_model=List[dict])
def get_user_history(user_id: str) -> List[dict]:
    """
    Busca o histórico de interações de um usuário.
    """
    history = DynamoDBClient.get_user_history(user_id)

    if not history:
        raise HTTPException(status_code=404, detail="Histórico não encontrado para o usuário.")

    return history
