from fastapi import FastAPI
from starlette.responses import RedirectResponse

from api import menu, orders, product, users
from core.middleware_config import add_cors_middleware, add_logging_middleware, add_timing_middleware, \
    add_custom_header_middleware

app = FastAPI(title="Pizza-Shack API",
              description="API for Pizza Shack, a pizza delivery service. This API allows users to browse the menu, "
                          "place orders, manage products, and handle user accounts. It includes endpoints for "
                          "creating, reading, updating, and deleting resources. The API is designed to be RESTful and "
                          "provides detailed responses for each operation. It also includes middleware for logging, "
                          "CORS, and custom headers to enhance security and performance.",
              version="0.1")

# Add middlewares
add_cors_middleware(app)
add_logging_middleware(app)
add_timing_middleware(app)
add_custom_header_middleware(app)

app.include_router(menu.router, prefix="/api", tags=["menu"])
app.include_router(orders.router, prefix="/api", tags=["orders"])
app.include_router(product.router, prefix="/api", tags=["products"])
app.include_router(users.router, prefix="/api", tags=["users"])


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")