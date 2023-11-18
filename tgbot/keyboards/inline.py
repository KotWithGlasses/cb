from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

from tgbot.services.callback_datas import feedbacks_callback, courses_callback, questions_callback


def i_more_kb(url):
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подробнее",
                    url=url
                )
            ]
        ]
    )

    return inline_kb

def chanel():
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подписаться",
                    url="https://t.me/hghghgjhjhjjhjhsddssdsdaa"
                )
            ]
        ]
    )

    return inline_kb

def i_more_admin_kb(url, id):
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подробнее",
                    url=url
                )
            ],
            [
                InlineKeyboardButton(
                    text=emojize(":cross_mark: Удалить курс"),
                    callback_data=courses_callback.new(direction="del", id=id)
                )
            ]
        ]
    )

    return inline_kb

def i_questions_kb():
    inline_kb = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Вопрос 1",
                    callback_data="q1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Вопрос 2",
                    callback_data="q2"
                )
            ]
        ]
    )

    return inline_kb

def i_answer_questions_kb(user_id, question_id):
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=emojize(":pen: Ответить"),
                    callback_data=questions_callback.new(direction="q_answer", user_id=user_id, question_id=question_id)
                )
            ],
            [
                InlineKeyboardButton(
                    text=emojize(":cross_mark: Не отвечать"),
                    callback_data=questions_callback.new(direction="del", user_id=user_id, question_id=question_id)
                )
            ]
        ]
    )

    return  inline_kb


def i_feedbacks_kb(index):
    inline_kb = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=emojize(":left_arrow:"),
                    callback_data=feedbacks_callback.new(direction="previous", index=index)
                ),
                InlineKeyboardButton(
                    text=emojize(":right_arrow:"),
                    callback_data=feedbacks_callback.new(direction="next", index=index)
                )
            ]
        ]
    )

    return inline_kb

def i_admin_feedbacks_kb(index):
    inline_kb = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=emojize(":left_arrow:"),
                    callback_data=feedbacks_callback.new(direction="previous", index=index)
                ),
                InlineKeyboardButton(
                    text=emojize(":right_arrow:"),
                    callback_data=feedbacks_callback.new(direction="next", index=index)
                )
            ],
            [
                InlineKeyboardButton(
                    text=emojize(":cross_mark: Удалить отзыв"),
                    callback_data=feedbacks_callback.new(direction="del", index=index)
                )
            ]
        ]
    )

    return inline_kb
