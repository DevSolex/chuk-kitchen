from pydantic import BaseModel
from typing import Optional, List


class Signup(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    referral_code: Optional[str] = None


class Verify(BaseModel):
    user_id: int
    otp: str


class FoodCreate(BaseModel):
    name: str
    description: str
    price: float


class CartAdd(BaseModel):
    user_id: int
    food_id: int
    quantity: int


class OrderCreate(BaseModel):
    user_id: int