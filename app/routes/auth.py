from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt
# from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# Configuração do JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define autenticação com Bearer Token
security = HTTPBearer()

router = APIRouter()

# Função para criar um token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Endpoint para gerar um token de login
@router.post("/auth/login")
def login():
    access_token = create_access_token({"sub": "user_id_123"})  # Simulação de usuário autenticado
    return {"access_token": access_token, "token_type": "Bearer"}

# Middleware para verificar token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # Obtém o token Bearer do cabeçalho
    # try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")  # Retorna o usuário autenticado
    # except ExpiredSignatureError:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    # except InvalidTokenError:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

# Rota protegida usando o token JWT
@router.get("/user/me")
def get_current_user(user: str = Depends(verify_token)):
    return {"user": user}
