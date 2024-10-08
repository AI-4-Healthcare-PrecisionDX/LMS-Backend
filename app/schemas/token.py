from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expire: datetime


class TokenPayload(BaseModel):
    sub: Optional[str] = None
