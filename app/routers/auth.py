# app/api/routers/auth.py
import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from sqlalchemy.orm import Session
import bcrypt

from app.session import get_session
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.utils.email import send_verification_email
from app.utils.tokens import create_access_token
from app.utils.verifier import make_verify_token, verify_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    session: Session = Depends(get_session)
):
    # 1) Validar email único
    if session.exec(select(User).where(User.email == data.email)).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")

    # 2) Hash de contraseña
    pw_hash = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

    # 3) Crear usuario (email_verified_at vendrá como NULL)
    user = User(
        name=data.name,
        last_name=data.last_name,
        second_last_name=data.second_last_name or "",
        email=data.email,
        password=pw_hash,
        address_id=1,  # Ajusta si necesitas otro default
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # 4) Generar token firmado para verificar email
    token = make_verify_token(user.id)
    base = os.getenv("API_URL", "http://localhost:8000")
    verify_url = f"{base}/auth/verify-email?token={token}"
    resend_url = f"{base}/auth/resend-verification?token={token}"

    # 5) Enviar correo con la plantilla
    await send_verification_email(
        email=user.email,
        verify_url=verify_url,
        resend_url=resend_url
    )

    return {"msg": "Revisa tu correo para verificar tu cuenta"}


@router.get("/verify-email", status_code=status.HTTP_200_OK)
def verify_email(
    token: str = Query(...),
    session: Session = Depends(get_session)
):
    try:
        user_id = verify_token(token)
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token inválido o expirado")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")

    # Marcar email verificado
    user.email_verified_at = datetime.utcnow()
    session.add(user)
    session.commit()

    return {"ok": True, "message": "Correo verificado correctamente!"}


@router.get("/resend-verification", status_code=status.HTTP_200_OK)
async def resend_verification(
    token: str = Query(...),
    session: Session = Depends(get_session)
):
    # Validar token igual que en /verify-email
    try:
        user_id = verify_token(token)
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token inválido o expirado")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")

    # Generar nuevo token y URLs
    new_token = make_verify_token(user.id)
    base = os.getenv("API_URL", "http://localhost:8000")
    new_verify = f"{base}/auth/verify-email?token={new_token}"
    new_resend = f"{base}/auth/resend-verification?token={new_token}"

    await send_verification_email(
        email=user.email,
        verify_url=new_verify,
        resend_url=new_resend
    )

    return {"msg": "Se ha enviado un nuevo enlace de verificación"}


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    session: Session = Depends(get_session)
):
    # 1) Buscar usuario
    user = session.exec(select(User).where(User.email == data.email)).one_or_none()
    if not user or not bcrypt.checkpw(data.password.encode(), user.password.encode()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas")

    # 2) Verificar que el email haya sido confirmado
    if not user.email_verified_at:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Debes verificar tu correo antes de iniciar sesión"
        )

    # 3) Generar JWT de acceso
    access_token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout():
    """
    Como usamos JWT sin estado en el servidor,
    para 'logout' basta con que el cliente borre su token.
    Si implementas refresh-tokens almacenados, aquí podrías
    marcar el token como revocado en base de datos.
    """
    return {"msg": "Has cerrado sesión correctamente"}
