from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.models.weather_models import WeatherData
from app.services.poster import generate_weather_poster

router = APIRouter()

@router.post("/poster")
async def create_weather_poster(weather_data: WeatherData):
    try:
        poster_bytes = await generate_weather_poster(weather_data)
        return Response(content=poster_bytes, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))