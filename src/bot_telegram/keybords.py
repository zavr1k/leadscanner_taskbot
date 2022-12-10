from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from schemas import Task


def get_task_keyboard(tasks: list[Task]) -> InlineKeyboardMarkup:
    """Create inlinekeyboard with user's tasks"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    for task in tasks:
        button = InlineKeyboardButton(
            text=task.title, callback_data=str(task.id))
        keyboard.add(button)
    return keyboard


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
add_button = KeyboardButton(text='/add')
list_button = KeyboardButton(text='/list')
main_keyboard.add(add_button, list_button)
