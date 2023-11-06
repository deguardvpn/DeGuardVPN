import os
import base64
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from config import API_KEYS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication


def encode_token(api_token):
    try:
        return base64.b64decode(api_token).decode()
    except:
        return False


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    api_key = encode_token(api_key)

    if api_key:
        if api_key not in API_KEYS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Forbidden")
        else:
            return True

    return False
