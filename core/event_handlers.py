from fastapi import FastAPI
from tabulate import tabulate
from sqlalchemy.orm import Session
from sqlalchemy import text

from core.database import engine, Base, SessionLocal
from core.log_config import log_decorator, log


def log_routes(app: FastAPI):
    routes = []
    for route in app.routes:
        route_name = getattr(route, 'name', 'N/A')
        route_path = getattr(route, 'path', 'N/A')
        route_methods = list(getattr(route, 'methods', []))
        routes.append([route_path, route_methods, route_name])
    log("INFO", "API Routes:\n" + tabulate(routes, headers=["Path", "Methods", "Name"], tablefmt="grid"))


def log_tables():
    tables = Base.metadata.tables.keys()
    table_data = [[table] for table in tables]
    log("INFO", "Database Tables:\n" + tabulate(table_data, headers=["Table Name"], tablefmt="grid"))

    # Log fields and data for each table
    db: Session = SessionLocal()
    for table in tables:
        log("INFO", f"Table: {table}")
        columns = Base.metadata.tables[table].columns.keys()
        log("INFO", "Fields:\n" + tabulate([[col] for col in columns], headers=["Field"], tablefmt="grid"))

        # Query all data from the table
        data = db.execute(text(f"SELECT * FROM {table}")).fetchall()
        if data:
            log("INFO", "Data:\n" + tabulate(data, headers=columns, tablefmt="grid"))
        else:
            log("INFO", "Data: No data available")


def create_startup_app_handler(app: FastAPI):
    @app.on_event("startup")
    @log_decorator("INFO")
    async def startup_event():
        log("INFO", "Starting up the application")
        log("INFO", "Creating database tables")
        Base.metadata.create_all(bind=engine)
        # log_tables()
        log_routes(app)


def create_shutdown_app_handler(app: FastAPI):
    @app.on_event("shutdown")
    @log_decorator("INFO")
    async def shutdown_event():
        log("INFO", "Shutting down the application")