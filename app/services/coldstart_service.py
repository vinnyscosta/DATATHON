from app.utils.AWS import DynamoDBClient
from app.models.cold_start import cold_start
from typing import List, Dict


def recommend_top_10() -> List[Dict[str, str]]:
    """ Retorna recomendações de notícias para um usuário específico."""
    recomendations = cold_start.recomend()

    for rec in recomendations:
        rec['news'] = DynamoDBClient.get_news(rec['page'])

    return recomendations
