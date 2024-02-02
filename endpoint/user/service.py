from datetime import datetime, timedelta

from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from endpoint.user.repository import get_user, create_user, update_user, delete_user
from data.db.models import User

from config import CREDENTIAL_SECRET_KEY, CREDENTIAL_ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def register_user(
    username: str, email: str, password1: str, password2: str
) -> None:
    """
    """

    if password1 != password2:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")

    try:
        await create_user(
            {
                "username": username,
                "email": email,
                "password": pwd_context.hash(password1),
            }
        )

    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23505:
            raise HTTPException(
                status_code=400, detail="Existing Username or Email."
            ) from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e


async def get_user_by_username(username: str) -> User:
    """
    """
    try:
        user = await get_user(username)
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="User ID Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e
    return user


async def verify_user(username, password) -> str:
    """
    """
    user = await get_user_by_username(username)

    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(
        payload, CREDENTIAL_SECRET_KEY, algorithm=CREDENTIAL_ALGORITHM
    )

    return access_token


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    현재 로그인한 유저의 정보를 jwt 토큰을 바탕으로 불러옵니다.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, CREDENTIAL_SECRET_KEY, algorithms=[CREDENTIAL_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    user = await get_user_by_username(username)
    if user is None:
        raise credentials_exception

    return user


async def update_current_user(
    username_original: str, username_to_update: str, email_to_update: str
) -> None:
    """
    현재 존재하는 유저의 정보를 수정할 때의 구체적인 동작을 정의합니다.
    """
    try:
        await update_user(
            username=username_original,
            user_req={"username": username_to_update, "email": email_to_update},
        )
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23505:
            raise HTTPException(
                status_code=400, detail="Existing Username or Email."
            ) from e
        if code == 23503:
            raise HTTPException(status_code=400, detail="User ID Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e


async def delete_current_user(username: str) -> None:
    """
    현재 존재하는 유저를 삭제할 때의 구체적인 동작을 정의합니다.
    """
    try:
        user = await get_user_by_username(username)
        await delete_user(username)
    except IntegrityError as e:
        code: int = int(e.orig.pgcode)
        if code == 23503:
            raise HTTPException(status_code=400, detail="User ID Not Found.") from e
        raise HTTPException(
            status_code=500, detail=f"Unknown Error. {e.orig.pgcode}: {e.orig}"
        ) from e
