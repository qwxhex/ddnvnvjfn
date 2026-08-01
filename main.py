from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

# --- ФУНКЦИИ ШИФРОВАНИЯ (Здесь логика твоего шифра) ---
def encrypt_text(text):
    return text[::-1]  # Пример: переворот строки (замени на свою функцию, если нужно)

def decrypt_text(text):
    return text[::-1]  # Пример: переворот строки (замени на свою функцию, если нужно)


# --- ЭКРАН 1: ШИФРОВАНИЕ ---
class EncryptScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        layout.add_widget(Label(text="Шифрование", font_size='20sp', size_hint_y=None, height='30dp'))

        self.input_text = TextInput(hint_text="Введите текст для шифрования...", multiline=True)
        layout.add_widget(self.input_text)

        # Ряд кнопок действий (увеличен размер для удобства)
        btn_layout = BoxLayout(size_hint_y=None, height='55dp', spacing=10)
        
        btn_encrypt = Button(text="Зашифровать", font_size='16sp')
        btn_encrypt.bind(on_press=self.do_encrypt)
        
        btn_clear = Button(text="Стереть всё", font_size='16sp')
        btn_clear.bind(on_press=self.clear_all)
        
        btn_layout.add_widget(btn_encrypt)
        btn_layout.add_widget(btn_clear)
        layout.add_widget(btn_layout)

        self.result_text = TextInput(hint_text="Результат...", multiline=True, readonly=True)
        layout.add_widget(self.result_text)

        # Переход на экран дешифрования
        btn_switch = Button(text="Перейти к Дешифрованию ➔", size_hint_y=None, height='55dp', font_size='16sp')
        btn_switch.bind(on_press=lambda x: setattr(self.manager, 'current', 'decrypt'))
        layout.add_widget(btn_switch)

        self.add_widget(layout)

    def do_encrypt(self, instance):
        self.result_text.text = encrypt_text(self.input_text.text)

    def clear_all(self, instance):
        self.input_text.text = ""
        self.result_text.text = ""


# --- ЭКРАН 2: ДЕШИФРОВАНИЕ ---
class DecryptScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        layout.add_widget(Label(text="Дешифрование", font_size='20sp', size_hint_y=None, height='30dp'))

        self.input_text = TextInput(hint_text="Введите зашифрованный текст...", multiline=True)
        layout.add_widget(self.input_text)

        # Ряд кнопок действий
        btn_layout = BoxLayout(size_hint_y=None, height='55dp', spacing=10)
        
        btn_decrypt = Button(text="Расшифровать", font_size='16sp')
        btn_decrypt.bind(on_press=self.do_decrypt)
        
        btn_clear = Button(text="Стереть всё", font_size='16sp')
        btn_clear.bind(on_press=self.clear_all)
        
        btn_layout.add_widget(btn_decrypt)
        btn_layout.add_widget(btn_clear)
        layout.add_widget(btn_layout)

        self.result_text = TextInput(hint_text="Результат...", multiline=True, readonly=True)
        layout.add_widget(self.result_text)

        # Переход на экран шифрования
        btn_switch = Button(text="➔ Перейти к Шифрованию", size_hint_y=None, height='55dp', font_size='16sp')
        btn_switch.bind(on_press=lambda x: setattr(self.manager, 'current', 'encrypt'))
        layout.add_widget(btn_switch)

        self.add_widget(layout)

    def do_decrypt(self, instance):
        self.result_text.text = decrypt_text(self.input_text.text)

    def clear_all(self, instance):
        self.input_text.text = ""
        self.result_text.text = ""


class EggNoFuguApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(EncryptScreen(name='encrypt'))
        sm.add_widget(DecryptScreen(name='decrypt'))
        return sm

if __name__ == '__main__':
    EggNoFuguApp().run()
