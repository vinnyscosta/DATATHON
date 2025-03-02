from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    auth,
    health,
    recommendations,
    users,
    news,
    coldstart
)

app = FastAPI(
    title="Datathon - Grupo 19",
    description=(
        "API para recomendação de notícias.\n\n"
        "**Integrantes:**\n\n"
        "- Luiz Carlos dos Santos - luizcarloos@gmail.com / RM356280\n"
        "- Igor Bruno de Jesus da Silva - igor.bruno2012@gmail.com / RM356420\n"  # noqa
        "- Vinicus Gomes Costa - vinicius00.vc@gmail.com / RM355817\n"
        "- Elzo dos Santos Sousa - elzo.santos.sousa@gmail.com / RM356007\n"
        "- Fabiano Emiliano - fab.emiliano@gmail.com / RM354635\n"
    ),
    version="1.0.0",
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticação"]
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["Usuários"]
)

app.include_router(
    news.router,
    prefix="/news",
    tags=["Notícias"]
)

app.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["Recomendações"]
)

app.include_router(
    coldstart.router,
    prefix="/cold_start",
    tags=["Cold Start"]
)


@app.get("/")
def root():
    return {"message": "API rodando! Acesse /docs para ver a documentação."}
