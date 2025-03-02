import pandas as pd
from app.utils.AWS import DynamoDBClient
from app.models.content_based_model import content_bases_model
from typing import List, Dict


def recommend_articles(user_id: str) -> List[Dict[str, str]]:
    """ Retorna recomendações de notícias para um usuário específico."""
    user_history = DynamoDBClient.get_user_history(user_id)
    user_history = pd.DataFrame(user_history)

    if user_history.empty:
        return []

    recomendations = content_bases_model.recomend(user_history)

    recomendations = [
        DynamoDBClient.get_news(rec)
        for rec in recomendations
    ]

    return recomendations
