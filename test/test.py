from kivymd.uix.navigationdrawer.navigationdrawer import MDScrollView
from kivymd.uix.screen import MDScreen
from datetime import datetime
from kivy.metrics import dp
from calendar import monthrange, day_name
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.pickers import MDDatePicker, MDTimePicker


# Builder.load_file('DSEBApp/kv/hello.kv')

class HelloScreen(MDScreen):
    def __init__(self, **kwargs):
        self.app = kwargs.pop('app', None)
        super(HelloScreen, self).__init__(**kwargs)
        self.dialog = None
        
    def on_enter(self, *args):
        super().on_enter(*args)
        self.update_greeting()
        self.populate_calendar_bar()
        Clock.schedule_once(self.center_today)

    def update_greeting(self):
        current_time = datetime.now().time()
        username = self.manager.get_screen('login').ids.username.text

        if current_time < datetime.strptime('12:00:00', '%H:%M:%S').time():
            greeting = "Good Morning"
        elif current_time < datetime.strptime('18:00:00', '%H:%M:%S').time():
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"

        self.ids.greeting_label.text = f"{greeting},\n{username}!"

    def populate_calendar_bar(self):
        scroll_view = ScrollView(do_scroll_x=True, do_scroll_y=False, bar_width=0)
        layout = GridLayout(cols=365, size_hint_x=None)
        layout.bind(minimum_width=layout.setter('width'))
        now = datetime.now()
        days_in_month = monthrange(now.year, now.month)[1]

        screen_width = self.ids.calendar_scroll.width
        day_width = screen_width / 9
        total_calendar_width = days_in_month * day_width

        offset = (screen_width / 2) - (now.day * day_width) + (day_width / 2)
        if offset < 0:
            offset = 0

        temp_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), padding=[dp(10), dp(20), dp(10), dp(10)])  # Adjust padding

        for day in range(1, days_in_month + 1):
            date = datetime(now.year, now.month, day)
            day_label = MDLabel(
                text=str(day),
                halign='center',
                theme_text_color='Primary',
                size_hint=(None, None),
                size=(day_width, day_width),
                font_style='H6',
                font_size='14.5sp'  # Adjust font size for day
            )

            weekday_label = MDLabel(
                text=day_name[date.weekday()][:3],  # Get the abbreviated weekday name
                halign='center',
                theme_text_color='Secondary',
                size_hint=(None, None),
                size=(day_width, dp(20)),
                font_style='Caption',
                font_size='12sp'  # Adjust font size for weekday
            )

            day_box = MDBoxLayout(orientation='vertical', size_hint=(None, None), size=(day_width, day_width + dp(10)))
            day_box.add_widget(day_label)
            day_box.add_widget(weekday_label)

            if day == now.day:
                with day_box.canvas.before:
                    Color(1, 69/255.0, 76/255.0, 1)  # Red color
                    self.rect = RoundedRectangle(size=(day_box.width + dp(20), day_box.height + dp(20)), pos=(day_box.x - dp(10), day_box.y - dp(10)), radius=[(10, 10), (10, 10), (10, 10), (10, 10)])
                    day_box.bind(size=self.update_rect, pos=self.update_rect)

            temp_layout.add_widget(day_box)

        self.ids.calendar_bar.width = total_calendar_width
        self.ids.calendar_bar.add_widget(temp_layout)
        self.ids.calendar_scroll.content_width = total_calendar_width

    def center_today(self, *args):
        now = datetime.now()
        screen_width = self.ids.calendar_scroll.width
        day_width = screen_width / 7  # Adjust day width to fit 7 days on screen
        total_calendar_width = self.ids.calendar_bar.width

        # Calculate offset to center the current day
        offset = (screen_width / 2) - (now.day * day_width) + (day_width / 2)
        if offset < 0:
            offset = 0

        self.ids.calendar_scroll.scroll_x = offset / total_calendar_width  # Set initial scroll position

    def update_rect(self, instance, value):
        self.rect.pos = (instance.x - dp(5), instance.y - dp(5))
        self.rect.size = (instance.width + dp(10), instance.height + dp(10))

    def show_add_schedule_dialog(self):
        # Set up the dialog content
        layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None,
            height="250dp"  # Adjust the height of the dialog box
        )

        # Add MDTextField elements to the layout
        self.schedule_title = MDTextField(
            hint_text="Enter schedule title",
            size_hint_y=None,
            height="40dp"
        )
        self.schedule_description = MDTextField(
            hint_text="Enter schedule description",
            size_hint_y=None,
            height="40dp"
        )
        self.schedule_date = MDTextField(
            hint_text="Select schedule date",
            size_hint_y=None,
            height="40dp",
            readonly=True,
        )
        self.schedule_date.bind(on_focus=self.show_date_picker)

        self.schedule_time = MDTextField(
            hint_text="Select schedule time",
            size_hint_y=None,
            height="40dp",
            readonly=True,
        )
        self.schedule_time.bind(on_focus=self.show_time_picker)

        # Add the text fields to the layout
        layout.add_widget(self.schedule_title)
        layout.add_widget(self.schedule_description)
        layout.add_widget(self.schedule_date)
        layout.add_widget(self.schedule_time)

        # Create the dialog
        self.dialog = MDDialog(
            title="Add Schedule",
            type="custom",
            content_cls=layout,  # Add the layout as the dialog content
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="ADD",
                    on_release=self.add_schedule
                )
            ]
        )

        # Open the dialog
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def add_schedule(self, *args):
        title = self.dialog.content_cls.children[3].text
        description = self.dialog.content_cls.children[2].text
        date = self.dialog.content_cls.children[1].text
        time = self.dialog.content_cls.children[0].text
        self.ids.schedule_box.add_widget(MDLabel(text=f"{date} {time} - {title}: {description}", halign='left'))
        self.dialog.dismiss()
    
    def show_date_picker(self, instance, value):
        if instance.focus:  # Only show if the field is focused
            instance.focus = False  # Prevent the keyboard from showing
            date_dialog = MDDatePicker()
            date_dialog.bind(on_save=self.on_date_selected)
            date_dialog.open()

    # Callback for date picker
    def on_date_selected(self, instance, value, date_range):
        self.dialog.content_cls.children[0].text = str(value)

    # Method to show the time picker
    def show_time_picker(self, instance, value):
        if instance.focus:  # Only show if the field is focused
            instance.focus = False
            time_dialog = MDTimePicker()
            time_dialog.bind(time=self.on_time_selected)
            time_dialog.open()

    # Callback for time picker
    def on_time_selected(self, instance, time):
        self.schedule_time.text = str(time)  # Set the selected time in the text field 
        