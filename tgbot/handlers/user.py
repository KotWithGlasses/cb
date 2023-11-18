import json
import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ForceReply
from emoji import emojize

from tgbot.keyboards.inline import i_questions_kb, i_feedbacks_kb, i_more_kb, chanel
from tgbot.keyboards.reply import menu_kb, to_menu, feedback_kb, contacts_kb, info_kb, noting
from tgbot.misc.states import Menu, Feedback

logger = logging.getLogger(__name__)


async def user_start(message: Message, state: FSMContext):
    await message.bot.send_message(chat_id=message.chat.id,
                                   text="Приветствую! \n\nЯ бот, который поможет вам узнать больше о наших курсах профессиональной переподготовки и повышения квалификации. \n\nЕсли у вас есть вопросы или вам нужна дополнительная информация, просто напишите мне. Я всегда готов помочь!",
                                   reply_markup=menu_kb())

    db = message.bot['db']
    try:
        query = '''
            INSERT INTO users (id)
            VALUES ($1);
        '''
        await db.execute(query, message.chat.id)

    except Exception as e:
        pass

    try:
        result = await db.fetch("SELECT id FROM users")
        result = json.loads(result)

        for user in result:
            user = user["id"]
            try:
                user_channel_status = await message.bot.get_chat_member(chat_id="-1002058918144", user_id=user)
                if user_channel_status["status"] == "left":
                    await message.bot.send_message(chat_id=user,
                                                   text="Если вы хотите быть в курсе всех новостей и предложений нашего канала, не забудьте подписаться на нас! Мы регулярно публикуем интересные материалы, советы и актуальную информацию о наших курсах. Присоединяйтесь к нам и станьте частью нашего сообщества!",
                                                   reply_markup=chanel())
            except:
                pass

    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")

    await state.reset_state()


async def menu(message: Message, state: FSMContext):
    await message.bot.send_message(chat_id=message.chat.id, text="Вы вернулись в главное меню", reply_markup=menu_kb())
    await state.reset_state()


async def info(message: Message):
    db = message.bot['db']

    try:
        result = await db.fetch('''
            SELECT DISTINCT "title"
            FROM "courses"
            ORDER BY "title";
        ''')
        result = json.loads(result)

        titles = [record['title'] for record in result]

        await message.answer("У нас есть широкий выбор курсов профессиональной переподготовки и повышения квалификации в различных областях. Наши курсы разработаны опытными специалистами и предлагают актуальные знания и навыки, необходимые для успешной карьеры.", reply_markup=info_kb(titles))
        await message.answer("Выберите направление", reply_markup=info_kb(titles))
    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")

    await Menu.INFO.set()

async def courses_show(message:Message):
    db = message.bot['db']

    try:
        result = await db.fetch('''
                    SELECT DISTINCT "title"
                    FROM "courses"
                    ORDER BY "title";
                ''')
        result = json.loads(result)

        titles = [record['title'] for record in result]
        await message.bot.send_message(chat_id=message.chat.id, text="Список курсов по выбранной категории:", reply_markup=info_kb(titles))

        query2 = '''
            SELECT * FROM "courses"
            WHERE "title" = $1
            ORDER BY "name";
        '''
        result2 = await db.fetch(query2, message.text)
        result2 = json.loads(result2)

        for course in result2:
            text = emojize(f'''Категория: {course["title"]}\n\nНазвание: {course["name"]}\n\n:money_bag:Цена: {course["price"]}\n:watch:Кол-во часов: {course["hours"]}''')
            url = course["link"]
            await message.bot.send_message(chat_id=message.chat.id, text=text, reply_markup=i_more_kb(url))

    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")

async def questions(message: Message):
    await message.answer("Часто задаваемые вопросы:", reply_markup=i_questions_kb())

async def ask_question(message: Message):
    await message.bot.send_message(chat_id=message.chat.id, text="Напишите ваш вопрос", reply_markup=noting())
    await Menu.QUESTIONS.set()

async def asking_q(message: Message, state: FSMContext):
    db = message.bot['db']

    try:
        result = await db.fetch("SELECT MAX(id) FROM questions")
        max = json.loads(result)
        max = max[0]['max'] + 1 if max[0]['max'] is not None else 1

        query = f'''
                    INSERT INTO questions ("id", "question", "user_id", "status")
                    VALUES ($1, $2, $3, $4);
                '''
        await db.execute(query, max, message.text, message.chat.id, True)

        admins = message.bot['config'].tg_bot.admin_ids
        for admin in admins:
            await message.bot.send_message(chat_id=admin, text=emojize(":bell: Новый вопрос от пользователя"))

        await message.bot.send_message(chat_id=message.chat.id, text="Ваш вопрос был передан администорам, ожидайте ответа", reply_markup=menu_kb())
    except Exception as e:
        await message.bot.send_message(chat_id=message.chat.id,
                                       text="Произошла ошибка при отправке вопроса, возможно ваш вопрос слишком длинный",
                                       reply_markup=menu_kb())
        logger.error(f"Error during get_data_handler: {e}")
        await Menu.ADMIN.set()

    await state.reset_state()

async def feedback(message: Message):
    await message.answer("Наши курсы уже помогли многим людям достичь новых высот в своей карьере. Если вы хотите достичь успеха в своей профессии, наши курсы идеально подходят для вас!", reply_markup=feedback_kb())
    await Menu.FEEDBACK.set()


async def look(message: Message):
    await message.answer("Отзывы:", reply_markup=feedback_kb())

    db = message.bot['db']
    try:
        result = await db.fetch("SELECT feedback FROM feedback")
        result = json.loads(result)

        await message.answer(result[0]["feedback"], reply_markup=i_feedbacks_kb(0))
    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")
        await message.answer("Отзывов пока нет", reply_markup=i_feedbacks_kb(0))


async def write(message: Message):
    await message.answer("Напишите ваш отзыв\n", reply_markup=noting())
    await Feedback.ANSWER.set()


async def writing(message: Message, state: FSMContext):
    await message.answer("Спасибо за отзыв!", reply_markup=feedback_kb())

    db = message.bot['db']

    try:
        query = '''
            INSERT INTO feedback (feedback, user_id)
            VALUES ($1, $2);
        '''
        await db.execute(query, message.text, message.chat.id)

    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")

    await Menu.FEEDBACK.set()


async def contacts(message: Message):
    await message.answer("contacts", reply_markup=contacts_kb())
    await Menu.CONTACTS.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start", "menu"], state="*")
    dp.register_message_handler(menu, text=emojize(":house: В меню"), state="*")
    dp.register_message_handler(menu, text=emojize(":no_entry: Отмена"), state="*")

    dp.register_message_handler(info, text=emojize(":information: Информация о курсах"))
    dp.register_message_handler(courses_show, state=Menu.INFO)

    dp.register_message_handler(questions, text=emojize(":white_question_mark: Часто задаваемые вопросы"))

    dp.register_message_handler(ask_question, text=emojize(":red_question_mark: Задать вопрос"))
    dp.register_message_handler(asking_q, state=Menu.QUESTIONS)

    dp.register_message_handler(feedback, text=emojize(":page_facing_up: Отзывы и рекомендации"))
    dp.register_message_handler(look, text=emojize(":eyes: Просмотреть отзывы"), state=Menu.FEEDBACK)
    dp.register_message_handler(write, text=emojize(":pen: Оставить отзыв"), state=Menu.FEEDBACK)
    dp.register_message_handler(writing, state=Feedback.ANSWER)

    dp.register_message_handler(contacts, text=emojize(":telephone_receiver: Контактная информация"))


