from typing import Dict

import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings

def generate_custom_jwt(user) -> Dict[str, str] :
    """Генерирует JWT токены (access и refresh) для пользователя."""
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    payload_refresh = {
        "user_id": user.id,
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    refresh = jwt.encode(payload_refresh, settings.SECRET_KEY, algorithm="HS256")

    return { "refresh": refresh, "access": token}
