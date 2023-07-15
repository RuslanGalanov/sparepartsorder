from pydantic import BaseModel


class Spare(BaseModel):
    ref: str | None
    name: str
    year: str
    amount: int