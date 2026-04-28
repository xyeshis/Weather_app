 WeatherDesk (Python Desktop Weather App)
 https://t.me/ai_agent_angel
<img width="740" height="813" alt="image" src="https://github.com/user-attachments/assets/cd0079d0-5f18-4677-a72c-45132917b1b8" />

Desktop-приложение для просмотра текущей погоды и прогноза по городу. Интерфейс на CustomTkinter, данные берутся из OpenWeatherMap API.

 Возможности
- Поиск погоды по названию города
- Текущая погода: температура, ощущается, влажность, давление, ветер, видимость (если доступно)
- Прогноз на несколько дней
- Обработка ошибок: нет сети, неверный API-ключ (401), город не найден (404), лимиты (429)

 Технологии
- Python 3.11+
- CustomTkinter (GUI)
- requests (HTTP)

 Структура проекта
weather_app/ main.py ui.py weather_api.py assets/ app.ico requirements.txt .env.example


 Требования
- Windows 10/11 (для сборки .exe)
- Python 3.11+ (рекомендуется)
- Доступ в интернет

 Установка и запуск (из исходников)
1. Клонируйте репозиторий или скачайте архив.
2. Создайте виртуальное окружение и установите зависимости:

Windows (PowerShell):
```
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
Укажите API-ключ OpenWeatherMap (см. раздел ниже).

```
python main.py
```
Настройка API-ключа OpenWeatherMap
Приложение использует API-ключ OpenWeatherMap.

Рекомендуемый вариант: хранить ключ в переменных окружения или в .env (если вы используете python-dotenv).

Пример .env.example:


```
OPENWEATHER_API_KEY=your_key_here
Варианты подключения ключа:

Через переменную окружения OPENWEATHER_API_KEY
Через файл .env рядом с проектом (если в коде подключён python-dotenv)
В крайнем случае — напрямую в weather_api.py (не рекомендуется для публичных репозиториев)
Примечание: новый ключ OpenWeatherMap иногда активируется не сразу.
