import customtkinter as ctk
from datetime import datetime
from weather_api import get_current_weather, get_forecast

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLORS = {
    "bg_main":    "#0d1117",
    "bg_card":    "#161b22",
    "bg_detail":  "#21262d",
    "bg_input":   "#1c2128",
    "accent":     "#58a6ff",
    "accent2":    "#3fb950",
    "text_main":  "#e6edf3",
    "text_muted": "#8b949e",
    "border":     "#30363d",
    "danger":     "#f85149",
    "warning":    "#d29922",
    "success":    "#3fb950",
}

WEATHER_GRADIENTS = {
    "Clear":        "#FF8C00",
    "Clouds":       "#708090",
    "Rain":         "#4682B4",
    "Drizzle":      "#5F9EA0",
    "Thunderstorm": "#483D8B",
    "Snow":         "#87CEEB",
    "Mist":         "#A9A9A9",
    "default":      "#58a6ff",
}

WEATHER_ICONS = {
    "Clear":        "☀️",
    "Clouds":       "☁️",
    "Rain":         "🌧️",
    "Drizzle":      "🌦️",
    "Thunderstorm": "⛈️",
    "Snow":         "❄️",
    "Mist":         "🌫️",
    "default":      "🌡️",
}


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("780x820")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_main"])
        self._build_ui()

    def _build_ui(self):

        # ── Верхняя панель ──
        self._build_topbar()

        # ── Поиск ──
        self._build_search()

        # ── Карточка текущей погоды ──
        self._build_weather_card()

        # ── Прогноз на 5 дней ──
        self._build_forecast_section()

        # ── Статус бар ──
        self._build_statusbar()

        # Обновляем часы каждую минуту
        self._tick()

    def _build_topbar(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=24, pady=(18, 0))

        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left,
            text="⛅",
            font=ctk.CTkFont(size=30),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            left,
            text="WeatherApp",
            font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
            text_color=COLORS["text_main"],
        ).pack(side="left")

        # Дата и время — справа
        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.pack(side="right")

        self.time_label = ctk.CTkLabel(
            right,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_muted"],
        )
        self.time_label.pack()

        ctk.CTkFrame(
            self,
            height=1,
            fg_color=COLORS["border"]
        ).pack(fill="x", padx=24, pady=(12, 0))

    # ──────────────────────────────────────────
    def _build_search(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=24, pady=16)

        self.entry = ctk.CTkEntry(
            frame,
            placeholder_text="  🔍  Введите город...  (например: Moscow, Tokyo, Paris)",
            font=ctk.CTkFont(size=14),
            height=48,
            corner_radius=12,
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_main"],
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self._search())

        self.btn = ctk.CTkButton(
            frame,
            text="Найти",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=48,
            width=110,
            corner_radius=12,
            fg_color=COLORS["accent"],
            hover_color="#1f6feb",
            text_color="#ffffff",
            command=self._search,
        )
        self.btn.pack(side="right")

    # ──────────────────────────────────────────
    def _build_weather_card(self):
        self.card = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_card"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        self.card.pack(fill="x", padx=24, pady=(0, 12))

        self.placeholder = ctk.CTkLabel(
            self.card,
            text="🌍  Введите название города чтобы увидеть погоду",
            font=ctk.CTkFont(size=14),
            text_color=COLORS["text_muted"],
        )
        self.placeholder.pack(pady=45)

    # ──────────────────────────────────────────
    def _build_forecast_section(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(0, 8))

        ctk.CTkLabel(
            header,
            text="📅  Прогноз на 5 дней",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLORS["text_main"],
        ).pack(side="left")

        self.forecast_row = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.forecast_row.pack(fill="x", padx=24)

    # ──────────────────────────────────────────
    def _build_statusbar(self):
        self.status = ctk.CTkLabel(
            self,
            text="Готов к работе",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"],
        )
        self.status.pack(pady=10)

    def _search(self):
        city = self.entry.get().strip()
        if not city:
            self._set_status("⚠️  Введите название города", COLORS["warning"])
            return

        self.btn.configure(text="⏳", state="disabled")
        self._set_status(f"Загружаем погоду для «{city}»...", COLORS["accent"])
        self.after(80, lambda: self._load(city))

    def _load(self, city: str):
        weather  = get_current_weather(city)
        forecast = get_forecast(city)

        if not weather or "error" in weather:
            msg = weather.get("error", "Неизвестная ошибка") if weather else "Ошибка"
            self._set_status(f"❌  {msg}", COLORS["danger"])
            self.btn.configure(text="Найти", state="normal")
            return

        self._render_weather(weather)
        self._render_forecast(forecast)

        self._set_status(
            f"✅  Обновлено в {datetime.now().strftime('%H:%M:%S')}  •  {weather['city']}, {weather['country']}",
            COLORS["success"]
        )
        self.btn.configure(text="Найти", state="normal")

    def _render_weather(self, w: dict):
        for wgt in self.card.winfo_children():
            wgt.destroy()

        accent = WEATHER_GRADIENTS.get(w["weather_main"], WEATHER_GRADIENTS["default"])
        self.card.configure(border_color=accent)

        top = ctk.CTkFrame(self.card, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(20, 10))

        left = ctk.CTkFrame(top, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left,
            text=w["icon"],
            font=ctk.CTkFont(size=80),
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text=w["description"],
            font=ctk.CTkFont(size=14),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", pady=(2, 0))

        # Правая — город + температура
        right = ctk.CTkFrame(top, fg_color="transparent")
        right.pack(side="right", anchor="ne")

        ctk.CTkLabel(
            right,
            text=f"{w['city']}, {w['country']}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["text_main"],
        ).pack(anchor="e")

        ctk.CTkLabel(
            right,
            text=f"{w['temp']}°C",
            font=ctk.CTkFont(size=68, weight="bold"),
            text_color=accent,
        ).pack(anchor="e")

        ctk.CTkLabel(
            right,
            text=f"Ощущается как {w['feels_like']}°C",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_muted"],
        ).pack(anchor="e")

        ctk.CTkLabel(
            right,
            text=f"🔺 {w['temp_max']}°   🔻 {w['temp_min']}°",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_main"],
        ).pack(anchor="e", pady=(4, 0))

        ctk.CTkFrame(
            self.card,
            height=1,
            fg_color=COLORS["border"]
        ).pack(fill="x", padx=20, pady=(8, 12))

        details_data = [
            ("💧", "Влажность",   f"{w['humidity']}%"),
            ("🌬️", "Ветер",       f"{w['wind_speed']} м/с {w['wind_dir']}"),
            ("🔵", "Давление",    f"{w['pressure']} гПа"),
            ("👁️", "Видимость",   f"{w['visibility']} км"),
        ]

        grid = ctk.CTkFrame(self.card, fg_color="transparent")
        grid.pack(fill="x", padx=20, pady=(0, 20))

        for i, (emoji, label, value) in enumerate(details_data):
            cell = ctk.CTkFrame(
                grid,
                fg_color=COLORS["bg_detail"],
                corner_radius=12,
            )
            cell.grid(row=0, column=i, padx=5, sticky="nsew")
            grid.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(
                cell,
                text=emoji,
                font=ctk.CTkFont(size=22),
            ).pack(pady=(12, 2))

            ctk.CTkLabel(
                cell,
                text=label,
                font=ctk.CTkFont(size=11),
                text_color=COLORS["text_muted"],
            ).pack()

            ctk.CTkLabel(
                cell,
                text=value,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=COLORS["text_main"],
            ).pack(pady=(2, 12))

    def _render_forecast(self, forecast: list):
        for wgt in self.forecast_row.winfo_children():
            wgt.destroy()

        if not forecast:
            ctk.CTkLabel(
                self.forecast_row,
                text="Прогноз недоступен",
                text_color=COLORS["text_muted"]
            ).pack(pady=15)
            return

        DAYS_RU = {
            "Monday": "Понедельник", "Tuesday": "Вторник",
            "Wednesday": "Среда",    "Thursday": "Четверг",
            "Friday": "Пятница",     "Saturday": "Суббота",
            "Sunday": "Воскресенье",
        }
        DAYS_SHORT = {
            "Monday": "Пн", "Tuesday": "Вт", "Wednesday": "Ср",
            "Thursday": "Чт", "Friday": "Пт", "Saturday": "Сб", "Sunday": "Вс",
        }

        for i, day in enumerate(forecast):
            date_obj  = datetime.strptime(day["date"], "%Y-%m-%d")
            day_en    = date_obj.strftime("%A")
            day_short = DAYS_SHORT.get(day_en, day_en[:2])
            date_str  = date_obj.strftime("%d.%m")
            accent    = WEATHER_GRADIENTS.get(
                            day.get("weather_main", ""), WEATHER_GRADIENTS["default"])

            card = ctk.CTkFrame(
                self.forecast_row,
                fg_color=COLORS["bg_card"],
                corner_radius=14,
                border_width=1,
                border_color=COLORS["border"],
            )
            card.grid(row=0, column=i, padx=5, pady=4, sticky="nsew")
            self.forecast_row.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(
                card,
                text=day_short,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=COLORS["text_main"],
            ).pack(pady=(14, 0))

            ctk.CTkLabel(
                card,
                text=date_str,
                font=ctk.CTkFont(size=11),
                text_color=COLORS["text_muted"],
            ).pack()

            ctk.CTkFrame(
                card, height=1,
                fg_color=COLORS["border"]
            ).pack(fill="x", padx=10, pady=6)

            ctk.CTkLabel(
                card,
                text=day["icon"],
                font=ctk.CTkFont(size=32),
            ).pack()

            ctk.CTkLabel(
                card,
                text=f"{day['temp_max']}°",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color=accent,
            ).pack(pady=(4, 0))

            ctk.CTkLabel(
                card,
                text=f"{day['temp_min']}°",
                font=ctk.CTkFont(size=13),
                text_color=COLORS["text_muted"],
            ).pack()

            ctk.CTkFrame(
                card, height=1,
                fg_color=COLORS["border"]
            ).pack(fill="x", padx=10, pady=6)

            ctk.CTkLabel(
                card,
                text=f"💧 {day['humidity']}%",
                font=ctk.CTkFont(size=11),
                text_color=COLORS["text_muted"],
            ).pack()

            ctk.CTkLabel(
                card,
                text=f"🌬️ {day['wind_speed']} м/с",
                font=ctk.CTkFont(size=11),
                text_color=COLORS["text_muted"],
            ).pack(pady=(2, 12))

    def _set_status(self, text: str, color: str = ""):
        self.status.configure(
            text=text,
            text_color=color or COLORS["text_muted"]
        )

    def _tick(self):
        now = datetime.now().strftime("🗓  %d %B %Y   🕐  %H:%M")
        self.time_label.configure(text=now)
        self.after(60_000, self._tick)