from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserResponseModel(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    default_payment_method_id: Optional[str] = None
    promo_credit_granted: Optional[datetime]
    is_verified: bool