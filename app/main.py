from fastapi import FastAPI

from app.prozorro_sale import views as objects

app = FastAPI()
app.include_router(objects.router)
