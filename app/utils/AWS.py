import os
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN', None)
AWS_REGION = os.environ.get('AWS_REGION', None)


class S3Client:
    AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
    AWS_SESSION_TOKEN = AWS_SESSION_TOKEN
    AWS_REGION = AWS_REGION

    @classmethod
    def get_s3_client(cls):
        return boto3.client(
            "s3",
            aws_access_key_id=cls.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=cls.AWS_SECRET_ACCESS_KEY,
            # aws_session_token=cls.AWS_SESSION_TOKEN,
            region_name=cls.AWS_REGION,
        )

    @classmethod
    def get_file_s3(
        cls,
        bucket_name: str,
        file_path: str,
        save_path: str
    ) -> bool:
        """Baixa um arquivo do S3 e salva no caminho especificado"""
        s3 = cls.get_s3_client()

        try:
            # Obtém o arquivo do S3
            response = s3.get_object(Bucket=bucket_name, Key=file_path)

            # Lê o conteúdo do arquivo em bytes
            file_content = response['Body'].read()

            # Salva o conteúdo em um arquivo no local especificado
            with open(save_path, 'wb') as f:
                f.write(file_content)

            print(f"Arquivo '{file_path}' baixado com sucesso em '{save_path}'!")  # noqa
            return True
        except Exception as e:
            print(f"Erro ao baixar arquivo: {e}")
            return False

    @classmethod
    def list_files_s3(cls, bucket_name, s3_directory):
        """Lista os arquivos de um diretório no S3"""
        s3 = cls.get_s3_client()
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_directory)
        return response.get('Contents', [])

    @classmethod
    def upload_file_s3(cls, bucket_name: str, file_path: str, s3_path: str):
        """Faz upload de um arquivo para o S3."""
        s3 = cls.get_s3_client()
        try:
            s3.upload_file(file_path, bucket_name, s3_path)
            print(f"Arquivo '{file_path}' enviado para '{s3_path}' no S3!")
            return True
        except Exception as e:
            print(f"Erro ao fazer upload do arquivo: {e}")
            return False


class DynamoDBClient:

    @classmethod
    def get_dynamo_client(cls):
        return boto3.resource(
            "dynamodb",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            # aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_REGION,
        )

    @classmethod
    def get_news(cls, news_id: str) -> Optional[Dict[str, Any]]:
        """Busca uma notícia no DynamoDB"""
        dynamodb = cls.get_dynamo_client()
        table = dynamodb.Table("noticias_datathon")

        response = table.query(
            KeyConditionExpression="page = :page_value",
            ExpressionAttributeValues={":page_value": news_id}
        )

        items = response.get("Items", [])

        if items:
            print(f"Encontrados {len(items)} registros para page={news_id}")
            for item in items:
                print(item)
        else:
            print("Nenhum registro encontrado!")

    @classmethod
    def get_user_history(cls, user_id: str) -> List[Dict[str, Any]]:
        """Busca histórico de um usuário"""
        dynamodb = cls.get_dynamo_client()
        table = dynamodb.Table("interacoes-datathon")

        try:
            response = table.query(KeyConditionExpression=Key("userId").eq(user_id))  # noqa
            return response.get("Items", [])  # Retorna lista caso não exista interações  # noqa
        except Exception as e:
            print(f"Erro ao buscar histórico do usuário '{user_id}': {e}")
            return []

    @classmethod
    def add_user_interaction(
        cls,
        user_id: str,
        history: str,
        user_type: str,
        number_of_clicks: int,
        page_visits: int,
        scroll_percentage: float,
        time_on_page: int,
    ) -> bool:
        """Salva uma nova interação no DynamoDB"""

        dynamodb = cls.get_dynamo_client()
        table = dynamodb.Table("interacoes-datathon")

        timestamp_now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

        # Verifica se já existe interação para manter o `timestampHistory_new`
        existing_history = cls.get_user_history(user_id)
        timestamp_new = existing_history[0]["timestampHistory_new"] if existing_history else timestamp_now  # noqa

        item = {
            "userId": user_id,
            "history": history,
            "historySize": 1,
            "numberOfClicksHistory": number_of_clicks,
            "pageVisitsCountHistory": page_visits,
            "scrollPercentageHistory": scroll_percentage,
            "timeOnPageHistory": time_on_page,
            "timestampHistory": timestamp_now,
            "timestampHistory_new": timestamp_new,
            "userType": user_type,
        }

        try:
            table.put_item(Item=item)
            print(f"Interação salva com sucesso para o usuário {user_id}")
            return True
        except Exception as e:
            print(f"Erro ao salvar interação: {e}")
            return False


# 🔹 Exemplo de uso:
if __name__ == "__main__":
    user_id = "f98d1132f60d46883ce49583257104d15ce723b3bbda2147c1e31ac76f0bf069"  # noqa
    history = DynamoDBClient.get_user_history(user_id)
    print(f"🔹 Histórico do usuário: {history}")

    news_id = "41c4680b-c375-4850-ad51-87ebb14e5843"
    news = DynamoDBClient.get_news(news_id)
    print(f"🔹 Notícia encontrada: {news}")

    DynamoDBClient.add_user_interaction(
        user_id, news_id, "teste", 5, 3, 0.5, 120,
    )

    bucket_name = "datathon-base"
    files = S3Client.list_files_s3(bucket_name, 'base_original/interacoes')
    for file in files:
        filename = file['Key'].split('/')[-1]
        print("Baixando file: %s" % filename)
        S3Client.get_file_s3(bucket_name, file['Key'], filename)
