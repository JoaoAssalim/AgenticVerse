from typing import Annotated
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token")
async def login_for_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}