# Datathon - Grupo 19

## 📌 Descrição
API para recomendação de notícias utilizando FastAPI. O projeto implementa diferentes modelos de recomendação, incluindo **Cold Start** e **Content-Based Filtering**.

## 👥 Integrantes
- **Luiz Carlos dos Santos** - luizcarloos@gmail.com / RM356280  
- **Igor Bruno de Jesus da Silva** - igor.bruno2012@gmail.com / RM356420  
- **Vinicius Gomes Costa** - vinicius00.vc@gmail.com / RM355817  
- **Elzo dos Santos Sousa** - elzo.santos.sousa@gmail.com / RM356007  
- **Fabiano Emiliano** - fab.emiliano@gmail.com / RM354635  

## 🚀 Tecnologias Utilizadas
- **Python 3.11**
- **FastAPI**
- **Uvicorn**
- **Docker**
- **GitHub Actions** (CI/CD)
- **AWS**

## 📂 Estrutura do Projeto
```
|   .env
|   .env.example
|   .gitignore
|   docker-compose.yml
|   Dockerfile
|   README.md
|   requirements.txt
|   
+---.github
|   \---workflows
|           main.yml
|           
+---app
|   |   main.py
|   |
|   +---models
|   |   |   cold_start.py
|   |   |   content_based_model.py
|   |
|   +---routes
|   |   |   auth.py
|   |   |   coldstart.py
|   |   |   health.py
|   |   |   news.py
|   |   |   recommendations.py
|   |   |   users.py
|   |
|   +---services
|   |   |   coldstart_service.py
|   |   |   recommendation_service.py
|   |
|   +---utils
|   |   |   AWS.py
|   |
+---notebooks_kaggle
|   |   mlet-postech-fiap-datathon-g19-coldstart.ipynb
|   |   mlet-postech-fiap-datathon-g19-history.ipynb
|   |   mlet-postech-fiap-datathon-g19-update_s3.ipynb
|
```

## 🛠️ Como Rodar o Projeto

### 📌 Requisitos
- Docker e Docker Compose instalados
- Python 3.11 instalado (caso queira rodar localmente)

### 🔥 Rodando com Docker
```bash
docker-compose up -d --build
```
A API ficará disponível em `http://localhost:8010/docs`.

### 🏗️ Rodando Localmente
1. Clone o repositório:
```bash
git clone https://github.com/vinnyscosta/DATATHON.git
cd DATATHON
```
2. Crie um ambiente virtual e ative:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Execute o servidor FastAPI:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload
```
Acesse a documentação interativa em `http://localhost:8010/docs`.

## 🔄 CI/CD com GitHub Actions
Este projeto utiliza **GitHub Actions** para automação do deploy. O fluxo está definido em `.github/workflows/main.yml` e funciona da seguinte forma:

1. Ao fazer **push** na branch `main`, o código é enviado via FTP para o servidor remoto.
2. O servidor acessa a pasta do projeto, derruba os containers existentes e recria com as novas alterações.

### 🔄 Pipeline de Deploy
O arquivo `main.yml` realiza as seguintes etapas:
- **Checkout do código** do repositório
- **Deploy via FTP** para o servidor
- **Atualização dos containers Docker** remotamente via SSH


# 📌 **Resumo Atualizado das Rotas da API**  

A API agora permite **gerenciar interações de usuários, buscar notícias e buscar recomendações** de modelos prontos.  

---

## **🔹 Rota de Health Check**  
📌 **Checagem da API**  
- `GET /health` → **Verifica status da API**  
---

## **🔹 Rotas de Authenticação**  
📌 **Authenticação da API**  
- `POST /auth/get-token` → **Cria token para uso da API** 

---

## **🔹 Rotas de Usuários**  
📌 **Gerenciamento de usuários e histórico de navegação**  
- `POST /users/add-interection/` → **Adiciona nova interação de usuário**  
- `GET /users/user-history/{user_id}` → **Consultar historico de acessos do usuário**

---

## **🔹 Rotas de Notícias**  
📌 **Gerenciamento das notícias disponíveis**  
- `GET /news/{news_id}` → **Buscar uma notícia pelo ID**.

---

## **🔹 Rotas de Recomendações**  
📌 **Buscar previsões do modelo treinado**  
- `GET /recommendations/user/{user_id}` → **Obter recomendações personalizadas para um usuário baseado no histórico dele**.  
- `POST /recommendations/execute-model` → **Executa criação de novo modelo de recomendação por histórico**.

---

## **🔹 Rotas de Cold Start**  
📌 **Buscar recomendações de notícias populares**  
- `GET /cold_start/top_10` → **Obter recomendações baseado nas interações recentes**.

---

## **🔹 Rota Básico**  
📌 **Rota de entrada**  
- `GET /` → **Entrada da API**



