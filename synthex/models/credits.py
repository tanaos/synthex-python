from pydantic import BaseModel


class CreditModel(BaseModel):
    amount: int
    currency: str