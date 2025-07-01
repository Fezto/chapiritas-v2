# app/utils/verifier.py
from itsdangerous import URLSafeTimedSerializer
import os

SECRET = os.getenv("EMAIL_SIGNING_SECRET", "cambia_esta_clave")
SALT   = "email-confirm-salt"
EXPIRE = 60 * 60  # 1 hora

serializer = URLSafeTimedSerializer(SECRET, salt=SALT)

def make_verify_token(user_id: int) -> str:
    return serializer.dumps({"user_id": user_id})

def verify_token(token: str) -> int:
    data = serializer.loads(token, max_age=EXPIRE)
    return data["user_id"]
