import requests

API_KEY = "bb215875d0af6a5be75e6e402df78af7"
BASE_URL = "https://api.openweathermap.org/data/2.5"

WEATHER_ICONS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️",
}

WIND_DIRECTION = {
    "N": "⬆️ С",
    "NE": "↗️ СВ",
    "E": "➡️ В",
    "SE": "↘️ ЮВ",
    "S": "⬇️ Ю",
    "SW": "↙️ ЮЗ",
    "W": "⬅️ З",
    "NW": "↖️ СЗ",
}

def get_wind_direction(degrees):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degrees / 45) % 8
    return WIND_DIRECTION[directions[index]]

def get_current_weather(city: str) -> dict | None:
    try:
        url = f"{BASE_URL}/weather"
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "ru"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        weather_main = data["weather"][0]["main"]

        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "temp_min": round(data["main"]["temp_min"]),
            "temp_max": round(data["main"]["temp_max"]),
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": round(data["wind"]["speed"]),
            "wind_dir": get_wind_direction(data["wind"].get("deg", 0)),
            "description": data["weather"][0]["description"].capitalize(),
            "visibility": data.get("visibility", 0) // 1000,
            "icon": WEATHER_ICONS.get(weather_main, "🌡️"),
            "weather_main": weather_main,
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": "Город не найден! Проверьте название."}
        return {"error": f"Ошибка сервера: {e.response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Нет подключения к интернету!"}
    except requests.exceptions.Timeout:
        return {"error": "Превышено время ожидания!"}

def get_forecast(city: str) -> list | None:
    try:
        url = f"{BASE_URL}/forecast"
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "ru",
            "cnt": 40
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        daily = {}
        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]
            time = item["dt_txt"].split(" ")[1]

            if time == "12:00:00" and date not in daily:
                weather_main = item["weather"][0]["main"]
                daily[date] = {
                    "date": date,
                    "temp_max": round(item["main"]["temp_max"]),
                    "temp_min": round(item["main"]["temp_min"]),
                    "description": item["weather"][0]["description"].capitalize(),
                    "icon": WEATHER_ICONS.get(weather_main, "🌡️"),
                    "humidity": item["main"]["humidity"],
                    "wind_speed": round(item["wind"]["speed"]),
                }

        return list(daily.values())[:5]

    except Exception:
        return []