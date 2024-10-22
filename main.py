from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
import json
import re

# شاشة تسجيل الدخول
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.username_input = TextInput(hint_text='Username', size_hint=(1, 0.2))
        self.password_input = TextInput(hint_text='Password', password=True, size_hint=(1, 0.2))

        login_button = Button(text='Login', size_hint=(1, 0.2))
        login_button.bind(on_press=self.login)

        register_button = Button(text='Register', size_hint=(1, 0.2))
        register_button.bind(on_press=self.go_to_register)

        google_login_button = Button(text='Login with Google', size_hint=(1, 0.2))
        google_login_button.bind(on_press=self.login_with_google)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(register_button)
        layout.add_widget(google_login_button)
        self.add_widget(layout)

    def login(self, instance):
        data = json.dumps({'username': self.username_input.text, 'password': self.password_input.text})
        headers = {'Content-type': 'application/json'}
        UrlRequest('http://localhost:5000/login', req_body=data, req_headers=headers, on_success=self.on_success)

    def login_with_google(self, instance):
        # هنا يمكنك إضافة منطق تسجيل الدخول عبر Google
        pass

    def on_success(self, request, result):
        if 'status' in result and result['status'] == 'success':
            self.manager.current = 'chat'  # هنا يجب أن تكون شاشة المحادثة أو الشاشة التالية

    def go_to_register(self, instance):
        self.manager.current = 'register'

# شاشة التسجيل
class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.username_input = TextInput(hint_text='Username', size_hint=(1, 0.2))
        self.password_input = TextInput(hint_text='Password', password=True, size_hint=(1, 0.2))
        self.email_input = TextInput(hint_text='Email', size_hint=(1, 0.2))
        self.phone_input = TextInput(hint_text='Phone Number', size_hint=(1, 0.2))

        register_button = Button(text='Register', size_hint=(1, 0.2))
        register_button.bind(on_press=self.register)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.phone_input)
        layout.add_widget(register_button)
        self.add_widget(layout)

    def register(self, instance):
        email = self.email_input.text
        phone = self.phone_input.text
        if not self.validate_email(email):
            self.email_input.text = ""
            self.email_input.hint_text = "Invalid email! Please try again."
            return

        data = json.dumps({
            'username': self.username_input.text,
            'password': self.password_input.text,
            'email': email,
            'phone': phone
        })
        headers = {'Content-type': 'application/json'}
        UrlRequest('http://localhost:5000/register', req_body=data, req_headers=headers, on_success=self.on_success)

    def validate_email(self, email):
        # تحقق من صيغة البريد الإلكتروني باستخدام تعبير منتظم
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(regex, email) is not None

    def on_success(self, request, result):
        if 'status' in result and result['status'] == 'success':
            self.manager.current = 'login'  # العودة إلى شاشة تسجيل الدخول بعد التسجيل الناجح
        else:
            self.email_input.hint_text = "Registration failed. Please try again."

# التطبيق الأساسي
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        return sm

if __name__ == "__main__":
    MyApp().run()
