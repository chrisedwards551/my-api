from datetime import datetime

from pydantic import BaseModel


class RefreshTokenCreate(BaseModel):
    token: str
    expires_at: datetime


class RefreshTokenResponse(BaseModel):
    id: int
    user_id: int
    token: str
    expires_at: datetime
    revoked: bool

    class Config:
        from_attributes = True