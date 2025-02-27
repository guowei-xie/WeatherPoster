from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path
from app.models.weather_models import WeatherData

# 定义资源路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR / "static"
FONTS_DIR = STATIC_DIR / "fonts"
BACKGROUNDS_DIR = STATIC_DIR / "backgrounds"
ICONS_DIR = STATIC_DIR / "icons"

# 确保目录存在
STATIC_DIR.mkdir(exist_ok=True)
FONTS_DIR.mkdir(exist_ok=True)
BACKGROUNDS_DIR.mkdir(exist_ok=True)
ICONS_DIR.mkdir(exist_ok=True)

async def generate_weather_poster(weather_data: WeatherData) -> bytes:
    """生成天气海报

    Args:
        weather_data: 天气数据

    Returns:
        bytes: PNG格式的图片字节数据
    """
    # 使用背景图片创建9:16比例的图片
    width, height = 540, 960  # 9:16比例
    background_path = str(BACKGROUNDS_DIR / "default.png")
    try:
        # 打开并调整背景图片大小
        background = Image.open(background_path)
        background = background.resize((width, height), Image.Resampling.LANCZOS)
        image = background
    except Exception:
        # 如果无法加载背景图片，使用纯白色背景
        image = Image.new('RGB', (width, height), color='white')
    
    draw = ImageDraw.Draw(image)

    # 使用中文字体
    try:
        font_path = str(FONTS_DIR / "微软雅黑粗体.ttf")  # 使用微软雅黑粗体
        title_font = ImageFont.truetype(font_path, 80)  # 调整城市名称字体大小
        large_font = ImageFont.truetype(font_path, 60)  # 调整温度显示字体大小
        medium_font = ImageFont.truetype(font_path, 40)  # 调整天气描述字体大小
        normal_font = ImageFont.truetype(font_path, 32)  # 调整普通信息字体大小
    except Exception as e:
        print(f"加载字体失败: {e}")
        title_font = ImageFont.load_default()
        large_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()

    # 绘制半透明背景
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 80))  # 调整透明度
    image.paste(overlay, (0, 0), overlay)

    # 设置文字样式
    text_color = 'white'
    shadow_color = (0, 0, 0, 160)  # 使用半透明黑色作为阴影
    shadow_offset = 3  # 增加阴影偏移量

    # 绘制城市名称（增强阴影效果）
    draw.text((width/2 + shadow_offset, height*0.2 + shadow_offset), weather_data.name, 
             font=title_font, fill=shadow_color, anchor="mm")
    draw.text((width/2, height*0.2), weather_data.name, 
             font=title_font, fill=text_color, anchor="mm")

    # 绘制温度（水平布局）
    temp_text = f"{weather_data.main.temp}°C"
    draw.text((width*0.3 + shadow_offset, height*0.4 + shadow_offset), temp_text, 
             font=large_font, fill=shadow_color, anchor="mm")
    draw.text((width*0.3, height*0.4), temp_text, 
             font=large_font, fill=text_color, anchor="mm")

    # 绘制天气描述（水平布局）
    weather_desc = weather_data.weather[0].description
    draw.text((width*0.7 + shadow_offset, height*0.4 + shadow_offset), weather_desc, 
             font=medium_font, fill=shadow_color, anchor="mm")
    draw.text((width*0.7, height*0.4), weather_desc, 
             font=medium_font, fill=text_color, anchor="mm")

    # 调整其他天气信息的布局（更紧凑的布局）
    info_y = height*0.5  # 调整信息区块起始位置
    info_spacing = height*0.08  # 调整行间距

    # 为每个信息块添加半透明背景
    info_block_height = 60  # 调整信息块高度以适应更小的字体
    info_block_padding = 40
    info_block_color = (0, 0, 0, 40)

    # 体感温度
    info_block = Image.new('RGBA', (width-80, info_block_height), info_block_color)
    image.paste(info_block, (40, int(info_y-info_block_padding)), info_block)
    feels_like_text = f"体感温度: {weather_data.main.feels_like}°C"
    draw.text((width/2 + shadow_offset, info_y + shadow_offset), feels_like_text, 
             font=normal_font, fill=shadow_color, anchor="mm")
    draw.text((width/2, info_y), feels_like_text, 
             font=normal_font, fill=text_color, anchor="mm")

    # 湿度
    image.paste(info_block, (40, int(info_y+info_spacing-info_block_padding)), info_block)
    humidity_text = f"湿度: {weather_data.main.humidity}%"
    draw.text((width/2 + shadow_offset, info_y + info_spacing + shadow_offset), humidity_text, 
             font=normal_font, fill=shadow_color, anchor="mm")
    draw.text((width/2, info_y + info_spacing), humidity_text, 
             font=normal_font, fill=text_color, anchor="mm")

    # 风速
    image.paste(info_block, (40, int(info_y+2*info_spacing-info_block_padding)), info_block)
    wind_text = f"风速: {weather_data.wind.speed} m/s"
    draw.text((width/2 + shadow_offset, info_y + 2 * info_spacing + shadow_offset), wind_text, 
             font=normal_font, fill=shadow_color, anchor="mm")
    draw.text((width/2, info_y + 2 * info_spacing), wind_text, 
             font=normal_font, fill=text_color, anchor="mm")

    # 转换为字节流
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img_byte_arr.getvalue()