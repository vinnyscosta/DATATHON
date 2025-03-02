from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.services.recommendation_service import recommend_articles
from asyncio import Lock
from app.routes.auth import verify_token

router = APIRouter()

# Criando um lock para garantir a execução sequencial
lock = Lock()


# Classe de exemplo (substitua pela sua)
class BasedContentRecomendation:
    def preprocess_data(self):
        print("Preprocessando os dados...")

    def train_model(self):
        print("Treinando o modelo...")

    def save_model(self):
        print("Salvando o modelo...")


@router.post("/execute-model")
async def execute_model(user: str = Depends(verify_token)):
    # Aguarda o lock, garantindo que apenas um processo possa executar ao mesmo tempo  # noqa
    async with lock:
        model = BasedContentRecomendation()
        model.preprocess_data()
        model.train_model()
        model.save_model()
        return {"message": "Model executed successfully!"}


@router.get("/user/{user_id}", response_model=List[Dict[str, Any]])
def get_recommendations(user_id: str, user: str = Depends(verify_token)):
    recommendations = recommend_articles(user_id)

    if recommendations:
        return recommendations

    raise HTTPException(
        status_code=404,
        detail="Nenhuma recomendação encontrada para este usuário"
    )
