from fastapi import FastAPI
from routers.base import base_router
from routers.seg_route import seg_router
from controllers.seg_controller import load_model
from contextlib import asynccontextmanager
from util.config import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model(config.model_path)
    yield
    del app.state.model


app = FastAPI(title="Diabetic Foot Ulcer Segmentation API",
              description="U-Net semantic segmentation for diabetic foot ulcer detection.", 
              lifespan=lifespan)

app.include_router(base_router)
app.include_router(seg_router)