import os
import pandas as pd
import numpy as np
import nltk
import pickle
import logging
import shutil
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from typing import List
from app.utils.AWS import S3Client, DynamoDBClient

# Configurar logging para exibir no terminal
logging.basicConfig(
    level=logging.INFO,  # Define o nível mínimo de log
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato da mensagem
    handlers=[logging.StreamHandler()]  # Exibir logs no terminal
)

# Baixar as stopwords do NLTK
nltk.download('stopwords')
stop_words = stopwords.words('portuguese')


def compress_similarity_matrix(cosine_sim, k=50):
    """Retorna apenas os k vizinhos mais similares para cada notícia."""
    compressed_sim = {}
    for i, row in enumerate(cosine_sim):
        top_k_indices = np.argsort(row)[-k:]  # Pega os índices dos K mais similares
        compressed_sim[i] = {idx: row[idx] for idx in top_k_indices}

    return compressed_sim


class BasedContentRecomendation:
    def __init__(
        self,
        bucket_name: str = "datathon-base",
        s3_path: str = "base_original/noticias/",
        model_s3_path: str = "models/content_based_model.pkl",
        dias_a_manter: int = 45
    ):
        self.s3_path = s3_path
        self.model_s3_path = model_s3_path
        self.dias_a_manter = dias_a_manter
        self.bucket_name = bucket_name
        self.df_news = None
        self.cosine_sim = None
        self.news_id_to_index = None
        self.index_to_news_id = None
        self.vectorizer = TfidfVectorizer(stop_words=stop_words)
        self.temp_dir = "temp_news"
        self.model_dir = "model"

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

    def _download_files_from_s3(self) -> None:
        """Baixa os arquivos da pasta no S3 para a pasta local `temp_news/`."""
        if not self.bucket_name:
            print("Nenhum bucket S3 configurado. Pulando download.")
            return

        print(f"Baixando arquivos do S3: {self.s3_path}")
        file_list = S3Client.list_files_s3(self.bucket_name, self.s3_path)

        if not file_list:
            print("Nenhum arquivo encontrado no S3!")
            return

        for file_info in file_list:
            file_key = file_info['Key']
            file_name = os.path.basename(file_key)
            save_path = os.path.join(self.temp_dir, file_name)
            S3Client.get_file_s3(self.bucket_name, file_key, save_path)

        print("Download concluído!")

    def _concat_dfs(self) -> pd.DataFrame:
        """Concatena os arquivos CSV baixados em um único DataFrame."""
        df_full = pd.DataFrame()
        for dirname, _, filenames in os.walk(self.temp_dir):
            for filename in filenames:
                logging.info(f'Reading {os.path.join(dirname, filename)}')
                df_auxiliar = pd.read_csv(os.path.join(dirname, filename), low_memory=False)  # noqa
                df_full = pd.concat([df_full, df_auxiliar], ignore_index=True)
        return df_full

    def preprocess_data(self) -> None:
        """Realiza o pré-processamento dos dados."""
        logging.info("Starting data preprocessing.")
        self._download_files_from_s3()
        self.df_news = self._concat_dfs()
        self.df_news = self.df_news[['page', 'url', 'issued', 'title', 'caption', 'body']]  # noqa
        self.df_news.drop_duplicates(inplace=True)
        self.df_news['issued'] = pd.to_datetime(self.df_news['issued'])

        data_limite = self.df_news['issued'].max() - pd.Timedelta(days=self.dias_a_manter)  # noqa
        self.df_news = self.df_news[self.df_news['issued'] >= data_limite]
        print("Data Minima para recomendação: ", data_limite)
        logging.info(f"Notícias recentes: {self.df_news.shape[0]}")

        self.df_news['news_content'] = self.df_news['title'] + ' ' + self.df_news['caption'] + ' ' + self.df_news['body']  # noqa
        logging.info("Data preprocessing completed.")

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def train_model(self) -> None:
        """Treina o modelo de recomendação."""
        logging.info("Training model.")
        tfidf_matrix = self.vectorizer.fit_transform(self.df_news['news_content'])  # noqa
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        self.news_id_to_index = {news_id: idx for idx, news_id in enumerate(self.df_news['page'])}  # noqa
        self.index_to_news_id = list(self.df_news['page'])

        logging.info("Model training completed.")

    def get_similarity(self, i, j):
        """Retorna a similaridade entre duas notícias usando os k vizinhos mais próximos."""  # noqa
        if i == j:
            return 1.0  # Similaridade de uma notícia com ela mesma
        if i in self.compressed_sim and j in self.compressed_sim[i]:
            return self.compressed_sim[i][j]
        if j in self.compressed_sim and i in self.compressed_sim[j]:
            return self.compressed_sim[j][i]
        return 0.0  # Similaridade 0 se as notícias não forem vizinhas

    def save_model(self, file_name="content_based_model.pkl") -> None:
        """Salva o modelo localmente e faz upload para o S3."""
        logging.info(f"Salvando modelo localmente em {file_name}...")
        with open(os.path.join(self.model_dir, file_name), 'wb') as f:
            pickle.dump({
                'cosine_sim': compress_similarity_matrix(self.cosine_sim),  # noqa
                'news_id_to_index': self.news_id_to_index,
                'index_to_news_id': self.index_to_news_id,
                'dias_mantidos': self.dias_a_manter,
            }, f)

        if self.bucket_name:
            logging.info(f"Enviando modelo para S3: {self.model_s3_path}...")
            S3Client.upload_file_s3(
                self.bucket_name,
                os.path.join(self.model_dir, file_name),
                self.model_s3_path
            )
            logging.info("Modelo enviado com sucesso ao S3!")

    def download_model(self, file_name="content_based_model.pkl") -> None:
        """Baixa o modelo do S3."""
        logging.info(f"Baixando modelo do S3: {file_name}...")

        # Verificar se o arquivo foi baixado com sucesso
        if not S3Client.get_file_s3(
            self.bucket_name,
            self.model_s3_path,
            (os.path.join(self.model_dir, file_name)),
        ):
            logging.error((
                "Erro ao baixar modelo do S3! "
                "O arquivo não foi encontrado ou houve falha no download."
            ))
            return False

        return True

    def load_model(self, file_name="content_based_model.pkl") -> None:
        """Baixa o modelo do S3 e carrega na memória."""
        self.download_model(file_name)
        logging.info("Carregando modelo...")

        try:
            with open(os.path.join(self.model_dir, file_name), 'rb') as f:
                data = pickle.load(f)
        except Exception as e:
            logging.error(f"Erro ao carregar o modelo: {e}")
            return None

        self.dias_a_manter = data.get('dias_mantidos')
        self.cosine_sim = data.get('cosine_sim')
        self.news_id_to_index = data.get('news_id_to_index')
        self.index_to_news_id = data.get('index_to_news_id')
        self.model_dir = "model"

        if self.cosine_sim is None or self.news_id_to_index is None or self.index_to_news_id is None:  # noqa
            logging.error("Dados essenciais não encontrados no modelo carregado.")  # noqa
            return None

        # Verificação adicional dos dados carregados
        print(f"dias mantidos no modelo: {type(self.dias_a_manter)}")
        print(f"cosine_sim: {type(self.cosine_sim)}")
        print(f"news_id_to_index: {type(self.news_id_to_index)}")
        print(f"index_to_news_id: {type(self.index_to_news_id)}")

        logging.info("Modelo carregado com sucesso!")

    def recomend(self, user_history, num_recommendations=10) -> List[str]:
        """
        Realiza a recomendação de notícias para um usuário.
        Retorna uma lista de IDs das notícias recomendadas.
        """
        recommended_news_ids = set()

        for news_id in user_history['history']:
            # Verifica se o ID está no mapa de notícias
            if news_id in self.news_id_to_index:
                # Obter o índice da notícia
                news_index = self.news_id_to_index[news_id]

                # Obter os k vizinhos mais similares
                similar_news = self.cosine_sim.get(news_index, {}).items()

                # Ordena as notícias pela similaridade
                sorted_similar_news = sorted(similar_news, key=lambda x: x[1], reverse=True)[:num_recommendations]  # noqa

                # Converter índices de volta para news_id
                recommended_news_ids.update(
                    self.index_to_news_id[i]
                    for i, _ in sorted_similar_news
                )

        return list(recommended_news_ids)[:num_recommendations]


# Carregamento de modelo já criado
content_bases_model = BasedContentRecomendation("datathon-base-458807800524")
content_bases_model.load_model()


if __name__ == '__main__':
    # Criação de um novo modelo
    model = BasedContentRecomendation()
    model.preprocess_data()
    model.train_model()
    model.save_model()

    # Carregamento de modelo já criado
    model = BasedContentRecomendation()
    model.load_model()

    # Recomendação para um usuário
    user_id = "1505326617b9465f6e13eb1d0d9782bff2af61822a7bc780fa058e95851d15ee"  # noqa
    user_history = DynamoDBClient.get_user_history(user_id)
    user_history = pd.DataFrame(user_history)
    user_history = user_history[['userId', 'history']]
    model.recomend(user_history)
