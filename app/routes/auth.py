from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

# Configuração do JWT
SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define autenticação com Bearer Token
security = HTTPBearer()

router = APIRouter()


# Função para criar o token
def create_access_token(expires_delta: timedelta = None):
    to_encode = {
        "exp": datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)),  # noqa
        "sub": "generic_user"
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Rota para gerar o token
@router.post("/get-token")
def generate_token():
    access_token = create_access_token()
    return {"access_token": access_token, "token_type": "Bearer"}


# Função para verificar o token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):  # noqa
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
