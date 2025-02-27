from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, JSONResponse
from app.models.weather_models import WeatherData
from app.services.poster import generate_weather_poster
from uuid import uuid4
import os

router = APIRouter()

# 创建临时文件夹用于存储生成的海报
TEMP_DIR = "static/temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/poster")
async def create_weather_poster(weather_data: WeatherData):
    try:
        # 生成海报图片
        poster_bytes = await generate_weather_poster(weather_data)
        
        # 生成唯一的文件名
        filename = f"{uuid4()}.png"
        file_path = os.path.join(TEMP_DIR, filename)
        
        # 保存图片到临时文件
        with open(file_path, "wb") as f:
            f.write(poster_bytes)
        
        # 构建下载链接
        download_url = f"/static/temp/{filename}"
        
        return JSONResponse({
            "status": "success",
            "message": "海报生成成功",
            "data": {
                "download_url": download_url
            }
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))