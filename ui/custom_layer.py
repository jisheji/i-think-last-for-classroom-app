# custom_layer.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class SomeLayer(BoxLayout):
    def __init__(self, **kwargs):
        super(SomeLayer, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='This is a custom layer!'))
