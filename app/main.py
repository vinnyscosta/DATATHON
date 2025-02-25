from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from app.routes import recommendations, auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(auth.router)
app.include_router(recommendations.router)


# Teste uma rota simples
@app.get("/")
def root():
    return {"message": "API is running"}


# Configuração de templates
templates = Jinja2Templates(directory="app/templates")
