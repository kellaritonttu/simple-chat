import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Header, HTTPException

firebase_admin.initialize_app()


async def get_current_user(authorization: str = Header(...)) -> dict:
    try:
        token = authorization.replace("Bearer ", "")
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")