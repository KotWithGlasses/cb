import json
import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ForceReply

from tgbot.keyboards.inline import i_admin_feedbacks_kb
from tgbot.keyboards.reply import info_kb, noting
from tgbot.misc.states import Menu, Questions
from tgbot.services.callback_datas import feedbacks_callback, courses_callback, questions_callback

logger = logging.getLogger(__name__)

async def q1(call: CallbackQuery):
    await call.answer()

    message = call.message
    await message.bot.send_message(chat_id=message.chat.id, text="Ответ 1")


async def previous(call: CallbackQuery, callback_data: dict):
    message = call.message
    index = int(callback_data['index'])

    db = message.bot['db']

    try:
        result = await db.fetch("SELECT feedback FROM feedback")
        result = json.loads(result)

        if index > 0:
            index -= 1
        else:
            index = len(result)-1

        await message.edit_text(result[index]["feedback"], reply_markup=i_admin_feedbacks_kb(index))
        await call.answer()
    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")
        await call.answer()



async def next(call: CallbackQuery, callback_data: dict):
    message = call.message
    index = int(callback_data['index'])

    db = message.bot['db']

    try:
        result = await db.fetch("SELECT feedback FROM feedback")
        result = json.loads(result)

        if index < len(result)-1:
            index += 1
        else:
            index = 0

        await message.edit_text(result[index]["feedback"], reply_markup=i_admin_feedbacks_kb(index))
        await call.answer()
    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")

        await call.answer()

async def delFeedback(call: CallbackQuery, callback_data: dict):
    message = call.message
    index = int(callback_data['index'])

    db = message.bot['db']

    try:
        result = await db.fetch("SELECT feedback FROM feedback")
        result = json.loads(result)

        query = '''
                    DELETE FROM feedback
                    WHERE feedback = $1;
                '''
        await db.execute(query, result[index]["feedback"])

        await message.bot.send_message(chat_id=message.chat.id, text="Отзыв удалён")
        await call.answer()
    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")
        await call.answer()

async def delCourse(call: CallbackQuery, callback_data: dict):
    message = call.message
    db = message.bot['db']

    try:
        query = '''
                    DELETE FROM courses
                    WHERE id = $1;
                '''
        await db.execute(query, int(callback_data["id"]))

        result = await db.fetch('''
                            SELECT DISTINCT "title"
                            FROM "courses"
                            ORDER BY "title";
                        ''')
        result = json.loads(result)

        titles = [record['title'] for record in result]
        await message.bot.send_message(chat_id=message.chat.id, text="Курс удалён", reply_markup=info_kb(titles))

        await call.answer()
    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")
        await call.answer()

async def q_answer(call: CallbackQuery, callback_data: dict, state: FSMContext):
    message = call.message

    user_id = callback_data["user_id"]
    question_id = callback_data["question_id"]

    await call.answer()
    await message.bot.send_message(chat_id=message.chat.id, text=f"Введите ответ на вопрос №{str(question_id)}", reply_markup=noting())
    await Questions.W_ANSWER.set()
    await state.update_data(user_id=user_id, question_id=question_id)

async def q_del(call: CallbackQuery, callback_data: dict):
    message = call.message
    db = message.bot['db']

    try:
        query = '''
                    DELETE FROM questions
                    WHERE id = $1;
                '''
        await db.execute(query, int(callback_data["question_id"]))

        await message.bot.send_message(chat_id=message.chat.id, text="Вопрос удалён")
        await message.bot.send_message(chat_id=callback_data["user_id"], text="Администратор посчитал ваш вопрос неуместным")

        await call.answer()
    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")
        await call.answer()

def register_admin_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(q1, text="q1")
    dp.register_callback_query_handler(q1, text="q2")

    dp.register_callback_query_handler(previous, feedbacks_callback.filter(direction="previous"), state=Menu.FEEDBACK, is_admin=True)
    dp.register_callback_query_handler(next, feedbacks_callback.filter(direction="next"), state=Menu.FEEDBACK, is_admin=True)
    dp.register_callback_query_handler(delFeedback, feedbacks_callback.filter(direction="del"), state=Menu.FEEDBACK, is_admin=True)
    dp.register_callback_query_handler(delCourse, courses_callback.filter(), state=Menu.INFO, is_admin=True)

    dp.register_callback_query_handler(q_answer, questions_callback.filter(direction="q_answer"), state=Questions.ANSWER, is_admin=True)
    dp.register_callback_query_handler(q_del, questions_callback.filter(direction="del"),
                                       state=Questions.ANSWER, is_admin=True)
