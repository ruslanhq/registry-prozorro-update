from fastapi import FastAPI

from app.prozorro_sale.views import router_obj, router_auc

app = FastAPI()
app.include_router(router_obj)
app.include_router(router_auc)
