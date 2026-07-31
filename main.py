import random
import string
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.clipboard import Clipboard

# --- ЛОГИКА ШИФРАТОРА ---
CHAR_TO_CODE = {
    'А': '100', 'Б': '010', 'В': '001', 'Г': '200', 'Д': '020', 'Е': '002',
    'Ё': '300', 'Ж': '030', 'З': '003', 'И': '400', 'Й': '040', 'К': '004',
    'Л': '500', 'М': '050', 'Н': '005', 'О': '600', 'П': '060', 'Р': '006',
    'С': '700', 'Т': '070', 'У': '007', 'Ф': '800', 'Х': '080', 'Ц': '008',
    'Ч': '900', 'Ш': '090', 'Щ': '009', 'Ъ': '110', 'Ы': '101', 'Ь': '011',
    'Э': '220', 'Ю': '202', 'Я': '022', ' ': '000'
}
CODE_TO_CHAR = {code: char for char, code in CHAR_TO_CODE.items()}
NOISE_CHARS = [c for c in string.ascii_letters if c not in ('o', 'O')]

def getRandomNoise():
    return ''.join(random.choices(NOISE_CHARS, k=random.randint(1, 3)))

def encrypt(text):
    encrypted_chunks = []
    text = text.upper()
    for char in text:
        if char in CHAR_TO_CODE:
            encrypted_chunks.append(CHAR_TO_CODE[char] + getRandomNoise())
        else:
            encrypted_chunks.append(char + getRandomNoise())
    return ''.join(encrypted_chunks)

def decrypt(text):
    clean_text = ''.join(c for c in text if c not in NOISE_CHARS)
    result = []
    i = 0
    while i < len(clean_text):
        three_digits = clean_text[i:i+3]
        if three_digits in CODE_TO_CHAR:
            result.append(CODE_TO_CHAR[three_digits])
            i += 3
        else:
            result.append(clean_text[i])
            i += 1
    return ''.join(result)


# --- ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ---
class CipherApp(App):
    def build(self):
        self.title = "Шифратор"
        
        # Главный вертикальный контейнер
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Поле ввода текста
        # layout.add_widget(Label(text="Исходный текст:", size_hint_y=None, height=30))
        self.input_text = TextInput(multiline=True, hint_text="Введите текст здесь...")
        layout.add_widget(self.input_text)

        # Контейнер для кнопок "Зашифровать" и "Расшифровать"
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        btn_encrypt = Button(text="Зашифровать", background_color=(0.2, 0.6, 1, 1))
        btn_encrypt.bind(on_press=self.on_encrypt)
        
        btn_decrypt = Button(text="Расшифровать", background_color=(0.3, 0.8, 0.4, 1))
        btn_decrypt.bind(on_press=self.on_decrypt)

        btn_layout.add_widget(btn_encrypt)
        btn_layout.add_widget(btn_decrypt)
        layout.add_widget(btn_layout)

        # Поле результата
        layout.add_widget(Label(text="Результат:", size_hint_y=None, height=30))
        self.output_text = TextInput(multiline=True, readonly=True)
        layout.add_widget(self.output_text)

        # Кнопка скопировать результат
        btn_copy = Button(text="Скопировать результат", size_hint_y=None, height=45)
        btn_copy.bind(on_press=self.copy_to_clipboard)
        layout.add_widget(btn_copy)

        return layout

    def on_encrypt(self, instance):
        text = self.input_text.text
        self.output_text.text = encrypt(text)

    def on_decrypt(self, instance):
        text = self.input_text.text
        self.output_text.text = decrypt(text)

    def copy_to_clipboard(self, instance):
        if self.output_text.text:
            Clipboard.copy(self.output_text.text)

if __name__ == '__main__':
    CipherApp().run()