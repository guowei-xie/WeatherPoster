# Weather Poster API

一个基于FastAPI开发的天气海报生成API服务，可以根据城市名称生成包含天气信息的精美海报图片。

## 功能特点

- 支持根据城市名称获取实时天气信息
- 自动生成包含天气数据的精美海报图片
- RESTful API设计，简单易用
- 支持跨域请求
- 可自定义背景图片和字体样式

## 技术栈

- Python 3.13+
- FastAPI - 现代化的Python Web框架
- Uvicorn - ASGI服务器
- Pillow - 图像处理库

## 项目结构

```
├── app/                    # 应用主目录
│   ├── main.py            # 应用入口
│   ├── models/            # 数据模型
│   ├── routers/           # 路由模块
│   └── services/          # 业务逻辑
├── static/                # 静态资源
│   ├── backgrounds/       # 背景图片
│   ├── fonts/            # 字体文件
│   └── icons/            # 图标资源
└── requirements.txt       # 项目依赖
```

## 安装说明

1. 克隆项目

```bash
git clone git@github.com:guowei-xie/WeatherPoster.git
cd WeatherPoster
```

2. 创建虚拟环境并激活

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

服务将在 http://localhost:8000 启动

## API文档

### 生成天气海报

**接口地址**

```
POST /api/v1/weather/poster
```

**请求参数**

请求体为JSON格式，包含以下字段：

```json
{
  "coord": {                 // 坐标信息
    "lon": 116.3972,        // 经度
    "lat": 39.9075         // 纬度
  },
  "weather": [              // 天气信息数组
    {
      "id": 800,           // 天气状况ID
      "main": "Clear",     // 主要天气状况
      "description": "clear sky",  // 天气描述
      "icon": "01d"        // 天气图标代码
    }
  ],
  "main": {                 // 主要天气数据
    "temp": 7.94,          // 温度（摄氏度）
    "feels_like": 7.3,     // 体感温度
    "temp_min": 7.94,      // 最低温度
    "temp_max": 7.94,      // 最高温度
    "pressure": 1016,      // 气压（百帕）
    "humidity": 16         // 湿度（百分比）
  },
  "wind": {                 // 风况信息
    "speed": 1.5,          // 风速（米/秒）
    "deg": 29,             // 风向（度数）
    "gust": 1.69           // 阵风速度
  },
  "sys": {                  // 系统相关信息
    "country": "CN",       // 国家代码
    "sunrise": 1740610279, // 日出时间（Unix时间戳）
    "sunset": 1740650604   // 日落时间（Unix时间戳）
  },
  "name": "Beijing"        // 城市名称
}
```

**响应格式**

成功响应：返回生成的海报图片（image/png格式）

### Python调用示例

```python
import requests
import json

# 天气数据
weather_data = {
    "coord": {"lon": 116.3972, "lat": 39.9075},
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01d"
        }
    ],
    "main": {
        "temp": 7.94,
        "feels_like": 7.3,
        "temp_min": 7.94,
        "temp_max": 7.94,
        "pressure": 1016,
        "humidity": 16
    },
    "wind": {
        "speed": 1.5,
        "deg": 29,
        "gust": 1.69
    },
    "sys": {
        "country": "CN",
        "sunrise": 1740610279,
        "sunset": 1740650604
    },
    "name": "Beijing"
}

# 发送请求
url = "http://localhost:8000/api/v1/weather/poster"
response = requests.post(url, json=weather_data)

# 保存海报图片
if response.status_code == 200:
    with open("weather_poster.png", "wb") as f:
        f.write(response.content)
    print("海报已保存为 weather_poster.png")
else:
    print(f"生成海报失败：{response.status_code}")
```



## 自定义配置

### 背景图片

将自定义背景图片放置在 `static/backgrounds/` 目录下

### 字体文件

将自定义字体文件放置在 `static/fonts/` 目录下

