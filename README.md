# 🍕 Pizza-Shack API

## 📄 Description
Pizza-Shack API is a RESTful API for Pizza Shack, a pizza delivery service. This API allows users to browse the menu, place orders, manage products, and handle user accounts. It includes endpoints for creating, reading, updating, and deleting resources. The API is designed to provide detailed responses for each operation and includes middleware for logging, CORS, and custom headers to enhance security and performance.

## 🛠️ Tech Stack
- **Programming Language**: Python
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Middleware**: Starlette
- **Logging**: Loguru
- **Spinner**: Halo
- **Deployment**: Choreo

## 📚 Libraries
- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Starlette**: A lightweight ASGI framework/toolkit, which is ideal for building high-performance asyncio services.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Loguru**: A library which aims to bring enjoyable logging in Python.
- **Halo**: A beautiful terminal spinner for Python.
- **Uvicorn**: A lightning-fast ASGI server implementation, using `uvloop` and `httptools`.

## 🛠️ Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/bantoinese83/pizza-shack-api.git
    cd pizzashack-api
    ```
2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## 🚀 Usage
1. Run the application:
    ```sh
    uvicorn main:app --reload
    ```
2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the Swagger UI documentation.

## 📋 Endpoints
### 🍽️ Menu
- **GET** `/api/menu`: Fetch all menu items
- **POST** `/api/menu`: Add a new menu item
- **GET** `/api/menu/{item_id}`: Fetch menu item by ID
- **PUT** `/api/menu/{item_id}`: Update menu item by ID
- **DELETE** `/api/menu/{item_id}`: Delete menu item by ID
- **GET** `/api/menu/name/{name}`: Fetch menu items by name
- **GET** `/api/menu/price/`: Fetch menu items by price range

### 📦 Orders
- **GET** `/api/orders`: Fetch all orders
- **POST** `/api/orders/`: Create a new order
- **GET** `/api/orders/{order_id}`: Fetch order by ID
- **PUT** `/api/orders/{order_id}`: Update order by ID
- **DELETE** `/api/orders/{order_id}`: Delete order by ID
- **GET** `/api/users/{user_id}/orders`: Fetch orders by user ID

### 🛒 Products
- **POST** `/api/products/`: Create a new product
- **GET** `/api/products/`: Fetch all products
- **GET** `/api/products/{product_id}`: Fetch product by ID
- **PUT** `/api/products/{product_id}`: Update product by ID
- **DELETE** `/api/products/{product_id}`: Delete product by ID

### 👤 Users
- **POST** `/api/users/`: Create a new user
- **GET** `/api/users/`: Fetch all users
- **GET** `/api/users/{user_id}`: Fetch user by ID
- **PUT** `/api/users/{user_id}`: Update user by ID
- **DELETE** `/api/users/{user_id}`: Delete user by ID

### 🔍 Recommendations
- **GET** `/api/recommendations`: Get product recommendations based on past orders
- **GET** `/api/recommendations/user/{user_id}`: Get product recommendations for a specific user
- **GET** `/api/recommendations/product/{product_id}`: Get product recommendations based on a specific product
- **GET** `/api/recommendations/category/{category}`: Get product recommendations based on a specific category

## 📜 License
This project is licensed under the MIT License.