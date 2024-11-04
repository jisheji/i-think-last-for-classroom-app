from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
import requests
from kivy.lang import Builder
from kivy.core.window import Window
from datetime import datetime

class Feature3_Screen(MDScreen):
    api_key = "fb5d71ff9a5e07ceca86d42c2d23e1be"

    def on_enter(self):
        # Fetch weather when screen is entered
        location = "Ha Noi"
        self.get_weather(location)
        self.get_current_date()
        print("Weather info should be updated now.")

    def get_location(self):
        try:
            response = requests.get("http://ip-api.com/json/")
            data = response.json()
            if response.status_code == 200 and data['status'] == 'success':
                return f"{data['city']},{data['regionName']},{data['country']}"
            else:
                print("Could not get location")
                return None
        except requests.ConnectionError:
            print("No Internet Connection")
            return None

    def get_weather(self, location):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            if response.status_code != 200:
                print("City Not Found or API Error")
                return

            data = response.json()
            if data["cod"] != "404":
                temperature = round(data["main"]["temp"])
                humidity = data["main"]["humidity"]
                weather = data["weather"][0]["description"]
                weather_id = int(data["weather"][0]["id"])
                wind_speed = round(data["wind"]["speed"] * 18 / 5)
                location = f"{data['name']}, {data['sys']['country']}"

                print(f"Location: {location}")
                print(f"Weather: {weather}, Temp: {temperature}, Humidity: {humidity}, Wind: {wind_speed}")

                self.ids.temperature.text = f"[b]{temperature}°C[/b]"
                self.ids.weather.text = weather.capitalize()
                self.ids.humidity.text = f"{humidity}%"
                self.ids.wind_speed.text = f"{wind_speed} km/h"
                self.ids.location.text = location

                weather_image_path = ""
                if weather_id == 800:
                    weather_image_path = "weather_icons/sunny.png"
                elif 200 <= weather_id <= 232:
                    weather_image_path = "weather_icons/stormy.png"
                elif 300 <= weather_id <= 321 or 500 <= weather_id <= 531:
                    weather_image_path = "weather_icons/rainy.png"
                elif 600 <= weather_id <= 622:
                    weather_image_path = "weather_icons/snowy.png"
                elif 701 <= weather_id <= 781:
                    weather_image_path = "weather_icons/foggy.png"
                elif 801 <= weather_id <= 804:
                    weather_image_path = "weather_icons/cloudy.png"
                elif "cloud" in weather:
                    weather_image_path = "weather_icons/cloudy.png"
                else:
                    weather_image_path = "weather_icons/sunny.png"

                print(f"Setting weather image to: {weather_image_path}")
                self.ids.weather_image.source = weather_image_path
            else:
                print("City Not Found")
        except requests.ConnectionError:
            print("No Internet Connection")

    def search_weather(self):
        city_name = self.root.ids.city_name.text.strip()
        if city_name:
            self.get_weather(city_name)
    def get_current_date(self):
        now = datetime.now()
        self.ids.date_label.text = now.strftime("%Y/%m/%d")
