from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.models import User, UserHistory
from typing import List

router = APIRouter()

# Criar usuário
@router.post("/users")
def create_user(username: str, db: Session = Depends(get_db)):
    new_user = User(username=username)
    db.add(new_user)
    db.commit()
    return {"message": "Usuário cadastrado!", "user_id": new_user.id}

# Buscar usuário
@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"user_id": user.id, "username": user.username}

# Atualizar histórico de leitura
@router.post("/users/{user_id}/history")
def update_user_history(user_id: int, article_id: int, db: Session = Depends(get_db)):
    history_entry = UserHistory(user_id=user_id, article_id=article_id)
    db.add(history_entry)
    db.commit()
    return {"message": "Histórico atualizado!"}

# Buscar histórico de leitura
@router.get("/users/{user_id}/history", response_model=List[int])
def get_user_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(UserHistory).filter(UserHistory.user_id == user_id).all()
    return [entry.article_id for entry in history]
