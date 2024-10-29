from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

class LoginScreen(MDScreen):
    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        print(f"Username: {username}, Password: {password}")
        self.manager.current = 'hello'