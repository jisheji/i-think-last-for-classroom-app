import json
import os
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from ui.ui import LoginScreen, HelloScreen, AccountScreen, DeadlinesScreen, Feature3_Screen, Feature4_Screen
from kivy.core.window import Window

Window.size = (360, 800)

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Cyan"
        self.screen_manager = ScreenManager()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        Builder.load_file('ui/kv/login.kv')
        Builder.load_file('ui/kv/hello.kv')
        Builder.load_file('ui/kv/account.kv')
        Builder.load_file('ui/kv/deadlines.kv')
        Builder.load_file('ui/kv/feature3.kv')
        Builder.load_file('ui/kv/feature4.kv')
        
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(HelloScreen(name='hello'))
        self.screen_manager.add_widget(AccountScreen(name='account'))
        self.screen_manager.add_widget(DeadlinesScreen(name='deadlines'))
        self.screen_manager.add_widget(Feature3_Screen(name='feature3'))
        self.screen_manager.add_widget(Feature4_Screen(name='feature4'))

        with open(os.path.join(script_dir, 'data/data.json'), 'r') as f:
            self.data = json.load(f)
        
        return self.screen_manager

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name

if __name__ == '__main__':
    MainApp().run()