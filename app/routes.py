from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from . import models, schemas
import random

router = APIRouter()


# USER SIGNUP
@router.post("/signup")
def signup(data: schemas.Signup, db: Session = Depends(get_db)):
    if not data.email and not data.phone:
        raise HTTPException(status_code=400, detail="Email or phone required")

    existing = db.query(models.User).filter(
        (models.User.email == data.email) |
        (models.User.phone == data.phone)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    otp = str(random.randint(1000, 9999))

    user = models.User(
        email=data.email,
        phone=data.phone,
        referral_code=data.referral_code,
        otp=otp
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created", "otp": otp}


# VERIFY
@router.post("/verify")
def verify(data: schemas.Verify, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == data.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user.status = "verified"
    db.commit()

    return {"message": "Account verified"}


# ADD FOOD
@router.post("/foods")
def add_food(food: schemas.FoodCreate, db: Session = Depends(get_db)):
    new_food = models.Food(**food.dict())
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food


# GET FOODS
@router.get("/foods")
def get_foods(db: Session = Depends(get_db)):
    return db.query(models.Food).filter(models.Food.is_available == True).all()


# ADD TO CART
@router.post("/cart/add")
def add_to_cart(data: schemas.CartAdd, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == data.user_id).first()

    if not cart:
        cart = models.Cart(user_id=data.user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    item = models.CartItem(
        cart_id=cart.id,
        food_id=data.food_id,
        quantity=data.quantity
    )

    db.add(item)
    db.commit()

    return {"message": "Added to cart"}


# CREATE ORDER
@router.post("/orders")
def create_order(data: schemas.OrderCreate, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == data.user_id).first()

    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    order = models.Order(user_id=data.user_id)

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart.items:
        food = db.query(models.Food).filter(models.Food.id == item.food_id).first()

        if not food or not food.is_available:
            raise HTTPException(status_code=400, detail="Food unavailable")

        total += food.price * item.quantity

        order_item = models.OrderItem(
            order_id=order.id,
            food_id=food.id,
            quantity=item.quantity,
            price_at_order=food.price
        )
        db.add(order_item)

    order.total_price = total

    db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).delete()

    db.commit()

    return {"message": "Order created", "order_id": order.id}


# GET ORDER
@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order