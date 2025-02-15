import base64, hashlib


async def encode_id(user_id) -> str:
    user_bytes = str(user_id).encode('utf-8')
    hashed = hashlib.md5(user_bytes).digest()
    short_link = base64.urlsafe_b64encode(hashed).decode('utf-8')[:18]  # Ограничение до 10 символов
    return short_link