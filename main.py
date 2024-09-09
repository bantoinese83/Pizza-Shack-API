from fastapi import FastAPI
from starlette.responses import RedirectResponse

from api import menu, orders, product, users, recommendations
from core.event_handlers import create_startup_app_handler, create_shutdown_app_handler
from core.middleware_config import add_cors_middleware, add_logging_middleware, add_timing_middleware, \
    add_custom_header_middleware, ProfilingMiddleware

# Create the FastAPI application
app: FastAPI = FastAPI(
    title="Pizza-Shack API",
    description="API for Pizza Shack, a pizza delivery service. This API allows users to browse the menu, "
                "place orders, manage products, and handle user accounts. It includes endpoints for creating, "
                "reading, updating, and deleting resources. The API is designed to be RESTful and provides detailed "
                "responses for each operation. It also includes middleware for logging, CORS, and custom headers to "
                "enhance security and performance.",
    version="0.1"
)


# Add middlewares
def add_middlewares(application: FastAPI) -> None:
    add_cors_middleware(application)
    add_logging_middleware(application)
    add_timing_middleware(application)
    add_custom_header_middleware(application)
    application.add_middleware(ProfilingMiddleware)


add_middlewares(app)


# Add event handlers
def add_event_handlers(application: FastAPI) -> None:
    create_startup_app_handler(application)
    create_shutdown_app_handler(application)


add_event_handlers(app)


# Include routers
def include_routers(application: FastAPI) -> None:
    application.include_router(menu.router, prefix="/api", tags=["menu"])
    application.include_router(orders.router, prefix="/api", tags=["orders"])
    application.include_router(product.router, prefix="/api", tags=["products"])
    application.include_router(users.router, prefix="/api", tags=["users"])
    application.include_router(recommendations.router, prefix="/api", tags=["recommendations"])


include_routers(app)


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
