from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import re

class KeyboardMixin:
    """
    Объект клавиатуры.
    Умеет генерировать заданную разметку и отслеживать последнюю нажатую кнопку
    """
    def __init__(self):
        self.keyboard_dict = {}
        self.buttons_in_row = 2 # Количество кнопок в ряду

    def generate_keyboard_markup(self):
        """
        Собираем разметку и запоминаем нажатые кнопки
        """
        keyboard = list()
        rows = list()
        buttons_list = list()
        for button, data in self.keyboard_dict.items():
            buttons_list.append(InlineKeyboardButton(button, callback_data=data))

        i = 0
        for i in range(len(buttons_list)):
            rows.append(buttons_list[i])
            i += 1
            if i % self.buttons_in_row == 0:
                keyboard.append(rows[:i])
                rows = []

        last_row_button_num = len(self.keyboard_dict.keys()) % self.buttons_in_row
        if last_row_button_num != 0:
            keyboard.append(buttons_list[-last_row_button_num:])

        markup = InlineKeyboardMarkup(keyboard)

        return markup

    def get_pressed_button(self, callback_data):
        """ Добавляет символ "•" к последней нажатой кнопке Inline клавиаутры """
        for k, v in self.keyboard_dict.items():
            self.keyboard_dict[k] = re.sub("•", "", v)

        new_button = "•" + self.keyboard_dict[callback_data] + "•"
        self.keyboard_dict[callback_data] = new_button