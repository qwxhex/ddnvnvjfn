import string
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.clipboard import Clipboard  # Модуль для работы с буфером обмена

ENGLISH_LETTERS = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'

# --- 1. ТАБЛИЦА СИМВОЛОВ И ЦИФРОВЫХ КОДОВ ---
CHAR_TO_CODE = {
    'а': '100', 'б': '010', 'в': '001', 'г': '200', 'д': '020',
    'е': '002', 'ё': '300', 'ж': '030', 'з': '003', 'и': '400',
    'й': '040', 'к': '004', 'л': '500', 'м': '050', 'н': '005',
    'о': '600', 'п': '060', 'р': '006', 'с': '700', 'т': '070',
    'у': '007', 'ф': '800', 'х': '080', 'ц': '008', 'ч': '900',
    'ш': '090', 'щ': '009', 'ъ': '110', 'ы': '101', 'ь': '011',
    'э': '220', 'ю': '202', 'я': '022', ' ': '000',
    '0': '330', '1': '303', '2': '033', '3': '440', '4': '404',
    '5': '044', '6': '550', '7': '505', '8': '055', '9': '660', 
    '.': '606', ',': '606', '-': '066', '[': '770', ']': '707',
    '{': '077', '}': '880', '(': '808', ')': '088', ''': '990',
    '*': '909', '"': '099', '~': '666', '!': '111', '?': '222',
    ':': '333', ';': '444', '_': '555', '/': '777'
}

CODE_TO_CHAR = {v: k for k, v in CHAR_TO_CODE.items()}


# --- 2. ЛОГИКА ШИФРОВАНИЯ ---
def encrypt_text(text):
    if not text:
        return ""
    
    digits_sequence = []
    for char in text.lower():
        code = CHAR_TO_CODE.get(char, '000')
        digits_sequence.append(code)
    
    full_digits = "".join(digits_sequence)

    result = []
    i = 0
    n = len(full_digits)
    
    while i < n:
        chunk_size = random.choice([1, 2])
        chunk = full_digits[i:i + chunk_size]
        result.append(chunk)
        i += chunk_size
        
        letter_count = random.choice([1, 2])
        random_letters = "".join(random.choice(ENGLISH_LETTERS) for _ in range(letter_count))
        result.append(random_letters)
        
    return "".join(result)


# --- 3. ЛОГИКА ДЕШИФРОВАНИЯ ---
def decrypt_text(text):
    if not text:
        return ""
    
    only_digits = "".join([char for char in text if char.isdigit()])
    
    decrypted_chars = []
    step = 3
    
    for i in range(0, len(only_digits), step):
        code = only_digits[i:i + step]
        char = CODE_TO_CHAR.get(code, '?')
        decrypted_chars.append(char)
        
    return "".join(decrypted_chars)


# --- ЦВЕТОВАЯ ПАЛИТРА (RGBA) ---
COLOR_BLUE = [0.2, 0.5, 0.9, 1]     # Синий (Зашифровать, Копировать, Переход)
COLOR_GREEN = [0.2, 0.7, 0.3, 1]    # Зеленый (Расшифровать)
COLOR_RED = [0.85, 0.2, 0.2, 1]     # Красный (Стереть всё)


# --- ЭКРАН 1: ШИФРОВАНИЕ ---
class EncryptScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        layout.add_widget(Label(text="Шифрование", font_size='20sp', size_hint_y=None, height='30dp'))

        self.input_text = TextInput(hint_text="Введите текст для шифрования...", multiline=True)
        layout.add_widget(self.input_text)

        # Панель управления (Зашифровать + Стереть)
        btn_layout = BoxLayout(size_hint_y=None, height='50dp', spacing=10)
        
        btn_encrypt = Button(
            text="Зашифровать", 
            font_size='16sp', 
            background_color=COLOR_BLUE, 
            background_normal=''
        )
        btn_encrypt.bind(on_press=self.do_encrypt)
        
        btn_clear = Button(
            text="Стереть всё", 
            font_size='16sp', 
            background_color=COLOR_RED, 
            background_normal=''
        )
        btn_clear.bind(on_press=self.clear_all)
        
        btn_layout.add_widget(btn_encrypt)
        btn_layout.add_widget(btn_clear)
        layout.add_widget(btn_layout)

        # Поле вывода результата
        self.result_text = TextInput(hint_text="Зашифрованный цифровой код...", multiline=True, readonly=True)
        layout.add_widget(self.result_text)

        # Кнопка копирования результата (Синяя)
        btn_copy = Button(
            text="Копировать результат", 
            size_hint_y=None, 
            height='45dp', 
            font_size='15sp',
            background_color=COLOR_BLUE,
            background_normal=''
        )
        btn_copy.bind(on_press=self.copy_result)
        layout.add_widget(btn_copy)

        # Переход на экран дешифрования (Синяя)
        btn_switch = Button(
            text="Перейти к Дешифрованию ➔", 
            size_hint_y=None, 
            height='50dp', 
            font_size='16sp',
            background_color=COLOR_BLUE,
            background_normal=''
        )
        btn_switch.bind(on_press=lambda x: setattr(self.manager, 'current', 'decrypt'))
        layout.add_widget(btn_switch)

        self.add_widget(layout)

    def do_encrypt(self, instance):
        self.result_text.text = encrypt_text(self.input_text.text)

    def clear_all(self, instance):
        self.input_text.text = ""
        self.result_text.text = ""

    def copy_result(self, instance):
        if self.result_text.text:
            Clipboard.copy(self.result_text.text)


# --- ЭКРАН 2: ДЕШИФРОВАНИЕ ---
class DecryptScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        layout.add_widget(Label(text="Дешифрование", font_size='20sp', size_hint_y=None, height='30dp'))

        self.input_text = TextInput(hint_text="Введите шифр...", multiline=True)
        layout.add_widget(self.input_text)

        # Панель управления (Расшифровать + Стереть)
        btn_layout = BoxLayout(size_hint_y=None, height='50dp', spacing=10)
        
        btn_decrypt = Button(
            text="Расшифровать", 
            font_size='16sp', 
            background_color=COLOR_GREEN, 
            background_normal=''
        )
        btn_decrypt.bind(on_press=self.do_decrypt)
        
        btn_clear = Button(
            text="Стереть всё", 
            font_size='16sp', 
            background_color=COLOR_RED, 
            background_normal=''
        )
        btn_clear.bind(on_press=self.clear_all)
        
        btn_layout.add_widget(btn_decrypt)
        btn_layout.add_widget(btn_clear)
        layout.add_widget(btn_layout)

        # Поле вывода результата
        self.result_text = TextInput(hint_text="Расшифрованный текст...", multiline=True, readonly=True)
        layout.add_widget(self.result_text)

        # Кнопка копирования результата (Синяя)
        btn_copy = Button(
            text="Копировать результат", 
            size_hint_y=None, 
            height='45dp', 
            font_size='15sp',
            background_color=COLOR_BLUE,
            background_normal=''
        )
        btn_copy.bind(on_press=self.copy_result)
        layout.add_widget(btn_copy)

        # Переход на экран шифрования (Синяя)
        btn_switch = Button(
            text="➔ Перейти к Шифрованию", 
            size_hint_y=None, 
            height='50dp', 
            font_size='16sp',
            background_color=COLOR_BLUE,
            background_normal=''
        )
        btn_switch.bind(on_press=lambda x: setattr(self.manager, 'current', 'encrypt'))
        layout.add_widget(btn_switch)

        self.add_widget(layout)

    def do_decrypt(self, instance):
        self.result_text.text = decrypt_text(self.input_text.text)

    def clear_all(self, instance):
        self.input_text.text = ""
        self.result_text.text = ""

    def copy_result(self, instance):
        if self.result_text.text:
            Clipboard.copy(self.result_text.text)


class EggNoFuguApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(EncryptScreen(name='encrypt'))
        sm.add_widget(DecryptScreen(name='decrypt'))
        return sm

if __name__ == '__main__':
    EggNoFuguApp().run()
