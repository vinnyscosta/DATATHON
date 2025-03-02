from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from app.routes import recommendations

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
# app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
# app.include_router(users.router, prefix="/users", tags=["Usuários"])
# app.include_router(articles.router, prefix="/api", tags=["Notícias"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recomendações"])


@app.get("/")
def root():
    return {"message": "API rodando!"}


# Configuração de templates
templates = Jinja2Templates(directory="app/templates")
