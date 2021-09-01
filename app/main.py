from fastapi import FastAPI, Depends, HTTPException

from app.prozorro_sale import views as objects

app = FastAPI()
app.include_router(objects.router)

