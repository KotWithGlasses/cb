from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize

def noting():
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=emojize(":no_entry: Отмена"))
            ]
        ],
        resize_keyboard=True
    )

    return menu


def menu_kb(is_admin: bool = False):
    if is_admin == False:
        menu = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=emojize(":information: Информация о курсах"))
                ],
                [
                    KeyboardButton(text=emojize(":white_question_mark: Часто задаваемые вопросы"))
                ],
                [
                    KeyboardButton(text=emojize(":red_question_mark: Задать вопрос"))
                ],
                [
                    KeyboardButton(text=emojize(":page_facing_up: Отзывы и рекомендации"))
                ],
                [
                    KeyboardButton(text=emojize(":telephone_receiver: Контактная информация"))
                ]
            ],
            resize_keyboard=True
        )
    else:
        menu = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=emojize(":information: Информация о курсах"))
                ],
                [
                    KeyboardButton(text=emojize(":white_question_mark: Часто задаваемые вопросы"))
                ],
                [
                    KeyboardButton(text=emojize(":red_question_mark: Задать вопрос"))
                ],
                [
                    KeyboardButton(text=emojize(":page_facing_up: Отзывы и рекомендации"))
                ],
                [
                    KeyboardButton(text=emojize(":telephone_receiver: Контактная информация"))
                ],
                [
                    KeyboardButton(text=emojize(":man_office_worker: Меню администратора"))
                ]
            ],
            resize_keyboard=True
        )

    return menu


def admin_kb():
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=emojize(":information: Информация о курсах"))
            ],
            [
                KeyboardButton(text=emojize(":white_question_mark: Часто задаваемые вопросы"))
            ],
            [
                KeyboardButton(text=emojize(":red_question_mark: Задать вопрос"))
            ],
            [
                KeyboardButton(text=emojize(":page_facing_up: Отзывы и рекомендации"))
            ],
            [
                KeyboardButton(text=emojize(":telephone_receiver: Контактная информация"))
            ],
            [
                KeyboardButton(text=emojize(":man_office_worker: Меню администратора"))
            ]
        ],
        resize_keyboard=True
    )

    return menu


def admin_menu_kb():
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=emojize(":light_bulb: Предложить подписаться на канал"))
            ],
            [
                KeyboardButton(text=emojize(":loudspeaker: Разослать сообщение"))
            ],
            [
                KeyboardButton(text=emojize(":plus: Добавить курс"))
            ],
            [
                KeyboardButton(text=emojize(":pen: Ответить на вопросы"))
            ],
            [
                KeyboardButton(text=emojize(":house: В меню"))
            ]
        ],
        resize_keyboard=True
    )

    return menu


def to_menu():
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=emojize(":house: В меню"))
            ]
        ],
        resize_keyboard=True
    )

    return menu

def passing():
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Пропустить")
            ]
        ],
        resize_keyboard=True
    )

    return menu


def info_kb(titles):
    menu = ReplyKeyboardMarkup(resize_keyboard=True)

    menu.add(KeyboardButton(text=emojize(":house: В меню")))
    for title in titles:
        menu.add(KeyboardButton(text=title))

    return menu


def feedback_kb():
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=emojize(":eyes: Просмотреть отзывы"))
            ],
            [
                KeyboardButton(text=emojize(":pen: Оставить отзыв"))
            ],
            [
                KeyboardButton(text=emojize(":house: В меню"))
            ]
        ],
        resize_keyboard=True
    )

    return menu


def contacts_kb():
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=emojize(":house: В меню"))
            ]
        ],
        resize_keyboard=True
    )

    return menu
