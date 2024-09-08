from fastapi import FastAPI

from core.log_config import log_decorator, log


def create_startup_event(app: FastAPI):
    @app.on_event("startup")
    @log_decorator("INFO")
    async def startup_event():
        log("INFO", "Starting up the application")


def create_shutdown_event(app: FastAPI):
    @app.on_event("shutdown")
    @log_decorator("INFO")
    async def shutdown_event():
        log("INFO", "Shutting down the application")
