from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Weather Poster API",
    description="Generate weather poster images based on weather data",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# 导入路由
from app.routers import weather

# 注册路由
app.include_router(weather.router, prefix="/api/v1/weather", tags=["weather"])

@app.get("/")
async def root():
    return {"message": "Welcome to Weather Poster API"}