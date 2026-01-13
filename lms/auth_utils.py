import jwt
from datetime import datetime, timedelta
from django.conf import settings

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 1

def create_jwt(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)
