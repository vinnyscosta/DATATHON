import os
import pandas as pd
import logging
from typing import List
from app.utils.AWS import S3Client


# Configurar logging para exibir no terminal
logging.basicConfig(
    level=logging.INFO,  # Define o nível mínimo de log
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato da mensagem
    handlers=[logging.StreamHandler()]  # Exibir logs no terminal
)


class ColdStart:
    def __init__(
        self,
        bucket_name: str = "datathon-base",
        model_s3_path: str = "models/recomendations.csv"
    ):
        self.bucket_name = bucket_name
        self.model_s3_path = model_s3_path
        self.df_news = None
        self.model_dir = "local_model"

        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

    def download_recomendacoes(self, file_name="recomendations.csv") -> bool:
        """Baixa o modelo coldstart do S3."""
        logging.info(f"Baixando modelo coldstart do S3: {file_name}...")

        file_path = os.path.join(self.model_dir, file_name)

        if not S3Client.get_file_s3(self.bucket_name, self.model_s3_path, file_path):  # noqa
            logging.error("Erro ao baixar modelo coldstart do S3! O arquivo não foi encontrado ou houve falha no download.")  # noqa
            return False

        return True

    def load_recomendacoes(self, file_name="recomendations.csv") -> None:
        """Carrega notícias com mais interações."""
        if self.download_recomendacoes(file_name):
            file_path = os.path.join(self.model_dir, file_name)
            self.df_news = pd.read_csv(file_path)
            logging.info("Recomendações carregadas com sucesso.")
        else:
            logging.error("Falha ao carregar recomendações.")

    def recomend(self) -> List[dict]:
        """Retorna a lista de recomendações no formato de dicionário."""
        if self.df_news is None:
            logging.warning("Nenhuma recomendação carregada. Execute load_recomendacoes.")  # noqa
            return []

        return self.df_news.to_dict(orient="records")


# Carregamento de top 10 noticias
cold_start = ColdStart("datathon-base-458807800524")
cold_start.load_recomendacoes()
