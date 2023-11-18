import json
import logging

from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline import i_feedbacks_kb
from tgbot.misc.states import Menu
from tgbot.services.callback_datas import feedbacks_callback

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

        await message.edit_text(result[index]["feedback"], reply_markup=i_feedbacks_kb(index))
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

        await message.edit_text(result[index]["feedback"], reply_markup=i_feedbacks_kb(index))
        await call.answer()
    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")
        await call.answer()



def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(q1, text="q1")

    dp.register_callback_query_handler(previous, feedbacks_callback.filter(direction="previous"), state=Menu.FEEDBACK)
    dp.register_callback_query_handler(next, feedbacks_callback.filter(direction="next"), state=Menu.FEEDBACK)
