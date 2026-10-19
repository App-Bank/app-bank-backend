from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_schema import UserLogin, TokenResponse
from app.controllers.auth_controller import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login a user",
)
def user_login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        email=credentials.email,
        password=credentials.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return TokenResponse(
        access_token=create_access_token(user),
        token_type="bearer",
    )


# @router.post("/logout")
# def logout(response: Response):
#     response.delete_cookie(
#         key="access_token",
#         path="/",
#         httponly=True,
#         secure=True,
#         samesite="lax",
#     )
#     return {"message": "Logged out"}