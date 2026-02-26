# Chuks Kitchen Backend API

## Project Overview

This project is a backend implementation of a **Food Ordering & Customer Management System** for **Chuks Kitchen**.

The system allows customers to:

- Register an account
- Verify account via OTP
- Browse available food items
- Add meals to cart
- Place orders
- View order details

The backend is built using:

- **FastAPI**
- **SQLAlchemy ORM**
- **SQLite Database**
- **Uvicorn**

This project focuses on backend system design, API structure, data modeling, and logical flow implementation.

---

# System Architecture

### Architecture Type
Monolithic RESTful API

### Tech Stack
- FastAPI (Application Layer)
- SQLAlchemy (ORM)
- SQLite (Database)
- Uvicorn (Server)

---

# Project Structure

chuks_kitchen/
│
├── app/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── crud.py
│ └── routes.py
│
├── requirements.txt
└── README.md


---

# Data Modeling

## Entities

### 1 User
- id
- email
- phone
- referral_code
- status (unverified / verified)
- otp

### 2 Food
- id
- name
- description
- price
- is_available

### 3 Cart
- id
- user_id

### 4 CartItem
- id
- cart_id
- food_id
- quantity

### 5 Order
- id
- user_id
- total_price
- status
- created_at

### 6 OrderItem
- id
- order_id
- food_id
- quantity
- price_at_order

---

## Key Design Decision

`OrderItem` stores `price_at_order`.

This ensures that if food prices change later, previous orders maintain their original price history.

---

# System Flow Explanation

## 1 User Registration Flow

### POST `/signup`

1. User provides email or phone.
2. System validates input.
3. System checks for duplicate user.
4. OTP is generated.
5. User saved with status = "unverified".

### POST `/verify`

1. User submits OTP.
2. System validates OTP.
3. If correct → status updated to "verified".

---

## 2 Food Flow

### POST `/foods`
- Adds a new food item.

### GET `/foods`
- Returns only foods where `is_available = True`.

---

## 3 Cart Flow

### POST `/cart/add`

1. Check if user has a cart.
2. If not → create cart.
3. Add food item to cart.

Cart and CartItem are separated for proper database normalization and scalability.

---

## 4 Order Flow

### POST `/orders`

1. Retrieve user cart.
2. Validate cart is not empty.
3. Check food availability.
4. Calculate total price.
5. Create Order with status = "Pending".
6. Create OrderItems.
7. Clear cart.
8. Return order ID.

---

### GET `/orders/{id}`

- Fetch order details.
- Returns total price and order status.

---

# API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|------------|
| POST | /signup | Register user |
| POST | /verify | Verify OTP |
| POST | /foods | Add food item |
| GET | /foods | Get available foods |
| POST | /cart/add | Add item to cart |
| POST | /orders | Create order |
| GET | /orders/{id} | Get order details |

---

# Edge Case Handling

### User
- Duplicate email/phone prevented
- Missing credentials rejected
- Invalid OTP rejected

### Cart
- Empty cart cannot be checked out

### Food
- Unavailable food cannot be ordered

### Order
- Non-existent order returns 404

HTTP Status Codes Used:
- 400 → Bad Request
- 404 → Not Found

---

# Scalability Considerations

If the system scales from 100 to 10,000+ users:

### Database
- Migrate from SQLite to PostgreSQL or MySQL
- Add indexing on frequently queried fields

### Performance
- Add pagination to `/foods`
- Introduce caching (Redis)
- Optimize database queries

### Security
- Implement JWT authentication
- Add role-based access control (Admin vs Customer)

### Architecture Upgrade
- Separate into microservices:
  - User Service
  - Order Service
  - Payment Service

---

# How To Run

## 1 Install Dependencies
pip install -r requirements.txt


## 2 Run Server


uvicorn app.main:app --reload


## 3 Open API Documentation
http://127.0.0.1:8000/docs


---

# Assignment Goals Covered

This implementation demonstrates:

- Backend system design
- RESTful API development
- Data modeling and normalization
- Order lifecycle handling
- Edge case management
- Scalability planning

---

# Final Notes

- Authentication system not implemented (as per assignment scope).
- Payment gateway integration not implemented (logic-only assumption).
- Admin role simulated through endpoint usage.
- Designed for clarity, structure, and logical flow.

---

**Backend Developer Deliverable – Chuks Kitchen**