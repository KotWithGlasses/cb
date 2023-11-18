import json
import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ForceReply
from emoji import emojize

from tgbot.keyboards.inline import i_admin_feedbacks_kb, i_more_admin_kb, i_answer_questions_kb, chanel
from tgbot.keyboards.reply import admin_kb, admin_menu_kb, feedback_kb, info_kb, passing, to_menu, menu_kb, noting
from tgbot.misc.states import Menu, Send, CourseReg, Questions

# from tgbot.services.parser import coursesLinks

logger = logging.getLogger(__name__)


async def admin_start(message: Message, state: FSMContext):
    await message.bot.send_message(chat_id=message.chat.id,
                                   text="Приветствую! \n\nЯ бот, который поможет вам узнать больше о наших курсах профессиональной переподготовки и повышения квалификации. \n\nЕсли у вас есть вопросы или вам нужна дополнительная информация, просто напишите мне. Я всегда готов помочь!",
                                   reply_markup=admin_kb())

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


async def admin_menu(message: Message):
    await message.bot.send_message(chat_id=message.chat.id, text="Вы вошли в меню администратора",
                                   reply_markup=admin_menu_kb())

    await Menu.ADMIN.set()


async def admin_back(message: Message, state: FSMContext):
    await message.bot.send_message(chat_id=message.chat.id, text="Вы вернулись в главное меню", reply_markup=admin_kb())

    await state.reset_state()


async def send_invite(message: Message):
    db = message.bot['db']

    try:
        result = await db.fetch("SELECT id FROM users")
        result = json.loads(result)

        for user in result:
            user = user["id"]
            try:
                user_channel_status = await message.bot.get_chat_member(chat_id="-1002058918144", user_id=user)
                if user_channel_status["status"] == "left":
                    await message.bot.send_message(chat_id=user, text="Если вы хотите быть в курсе всех новостей и предложений нашего канала, не забудьте подписаться на нас! Мы регулярно публикуем интересные материалы, советы и актуальную информацию о наших курсах. Присоединяйтесь к нам и станьте частью нашего сообщества!", reply_markup=chanel())
            except:
                pass

    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")

    await message.bot.send_message(chat_id=message.chat.id, text="Приглашения отправлены не подписанным пользователям",
                                   reply_markup=admin_kb())


async def send_msg(message: Message):
    await message.bot.send_message(chat_id=message.chat.id, text="Введите сообщение, которое хотите разослать",
                                   reply_markup=noting())

    await Send.ANSWER.set()

async def msg(message: Message, state: FSMContext):
    db = message.bot['db']
    try:
        result = await db.fetch("SELECT id FROM users")
        result = json.loads(result)

        for user in result:
            user = user["id"]
            try:
                await message.bot.send_message(chat_id=user, text=message.text)
            except:
                pass

    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")

    await message.bot.send_message(chat_id=message.chat.id, text="Сообщение отправлено",
                                   reply_markup=admin_kb())

    await state.reset_state()


async def answer_questions(message: Message):
    db = message.bot['db']

    try:
        result = await db.fetch('''
                        SELECT *
                        FROM "questions"
                        WHERE "status" = true;
                    ''')
        result = json.loads(result)

        await message.bot.send_message(chat_id=message.chat.id, text="Список вопросов:", reply_markup=to_menu())
        if result == []:
            await message.bot.send_message(chat_id=message.chat.id, text="Вопросов пока нет", reply_markup=to_menu())
        for question in result:
            text = emojize(f'''Вопрос №{str(question["id"])}: \n\n{question["question"]}''')

            await message.bot.send_message(chat_id=message.chat.id, text=text, reply_markup=i_answer_questions_kb(question["user_id"], question["id"]))

    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")

    await Questions.ANSWER.set()

async def getAnswer(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    question_id = data.get("question_id")

    db = message.bot['db']
    answer_text = "Ответ на ваш вопрос:\n\n"+message.text
    try:
        await message.bot.send_message(chat_id=user_id, text=answer_text)
        await message.bot.send_message(chat_id=message.chat.id, text=f"Ответ на вопрос №{str(question_id)} отправлен", reply_markup=to_menu())

        query = '''
                            DELETE FROM questions
                            WHERE id = $1;
                        '''
        await db.execute(query, int(question_id))
    except Exception as e:
        await message.bot.send_message(chat_id=message.chat.id, text=f"Не удалось отправить ответ", reply_markup=to_menu())
    await state.reset_state(with_data=True)

    await Questions.ANSWER.set()
async def courses_show(message: Message):
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
            text = emojize(
                f'''Категория: {course["title"]}\n\nНазвание: {course["name"]}\n\n:money_bag:Цена: {course["price"]}\n:watch:Кол-во часов: {course["hours"]}''')
            url = course["link"]
            await message.bot.send_message(chat_id=message.chat.id, text=text, reply_markup=i_more_admin_kb(url, str(course["id"])))

    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")

async def look(message: Message):
    await message.answer("Отзывы:", reply_markup=feedback_kb())

    db = message.bot['db']
    try:
        result = await db.fetch("SELECT feedback FROM feedback")
        result = json.loads(result)

        await message.answer(result[0]["feedback"], reply_markup=i_admin_feedbacks_kb(0))
    except Exception as e:
        logger.error(f"Error during get_data_handler: {e}")
        await message.answer("Отзывов пока нет", reply_markup=i_admin_feedbacks_kb(0))

class CourseData:
    def __init__(self):
        self.title = None
        self.name = None
        self.price = None
        self.priceNum = None
        self.hours = None
        self.hoursNum = None
        self.link = None

async def addCourse(message: Message, state: FSMContext):
    current_state = await state.get_state()

    previous_course_data = await state.get_data()
    course_data = CourseData()

    for key, value in previous_course_data.items():
        setattr(course_data, key, value)

    if current_state == "Menu:ADMIN":
        await message.bot.send_message(chat_id=message.chat.id, text="Введите категорию", reply_markup=noting())
        await CourseReg.TITLE.set()

    elif current_state == "CourseReg:TITLE":
        course_data.title = message.text
        await message.bot.send_message(chat_id=message.chat.id, text="Введите название", reply_markup=noting())
        await CourseReg.NAME.set()

    elif current_state == "CourseReg:NAME":
        course_data.name = message.text
        await message.bot.send_message(chat_id=message.chat.id, text="Пришлите ссылку на курс", reply_markup=noting())
        await CourseReg.LINK.set()

    elif current_state == "CourseReg:LINK":
        course_data.link = message.text
        await message.bot.send_message(chat_id=message.chat.id, text="Введите цену целым числом (пример: 4500)", reply_markup=passing())
        await CourseReg.PRICE.set()

    elif current_state == "CourseReg:PRICE":
        if message.text == "Пропустить":
            course_data.price = "Цена не указана"

            await message.bot.send_message(chat_id=message.chat.id, text="Введите кол-во часов числом",
                                           reply_markup=passing())
            await CourseReg.HOURS.set()
        else:
            try:
                course_data.priceNum = int(message.text)

                formatted_number = '{:,}'.format(int(message.text)).replace(',', ' ')
                course_data.price = f"{formatted_number},00 ₽"

                await message.bot.send_message(chat_id=message.chat.id, text="Введите кол-во часов числом", reply_markup=passing())
                await CourseReg.HOURS.set()
            except Exception as e:
                print(e)
                await message.bot.send_message(chat_id=message.chat.id, text="Ошибка при добавлении курса", reply_markup=admin_menu_kb())
                await Menu.ADMIN.set()

    elif current_state == "CourseReg:HOURS":
        if message.text == "Пропустить":
            course_data.hours = "Кол-во часов не указано"
        try:
            course_data.hoursNum = int(message.text)
            course_data.hours = message.text + " часов"
        except Exception as e:
            await message.bot.send_message(chat_id=message.chat.id, text="Ошибка при добавлении курса",
                                           reply_markup=admin_menu_kb())
            await Menu.ADMIN.set()

        course = course_data.__dict__
        db = message.bot['db']

        try:
            result = await db.fetch("SELECT MAX(id) FROM courses")
            max = json.loads(result)
            max = max[0]['max'] + 1 if max[0]['max'] is not None else 1
            query = f'''
                INSERT INTO courses ("id", "hours", "hoursNum", "link", "name", "price", "priceNum", "title")
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
            '''
            await db.execute(query, max, course["hours"], course["hoursNum"], course["link"], course["name"], course["price"], course["priceNum"], course["title"])
            await message.bot.send_message(chat_id=message.chat.id, text="Курс добавлен",
                                           reply_markup=admin_menu_kb())
        except Exception as e:
            await message.bot.send_message(chat_id=message.chat.id, text="Ошибка при добавлении курса",
                                           reply_markup=admin_menu_kb())
            logger.error(f"Error during get_data_handler: {e}")
            await Menu.ADMIN.set()

        await Menu.ADMIN.set()

    else:
        print("Неожиданное состояние:", current_state)
        # Обрабатываем неожиданное состояние
        await message.bot.send_message(chat_id=message.chat.id, text="Неожиданное состояние!")

    # Сохраняем текущие значения в состояние
    await state.update_data(**course_data.__dict__)

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

        await message.bot.send_message(chat_id=message.chat.id, text="Ваш вопрос был передан администорам, ожидайте ответа", reply_markup=admin_menu_kb())
    except Exception as e:
        await message.bot.send_message(chat_id=message.chat.id,
                                       text="Произошла ошибка при отправке вопроса, возможно ваш вопрос слишком длинный",
                                       reply_markup=admin_menu_kb())
        logger.error(f"Error during get_data_handler: {e}")
        await Menu.ADMIN.set()

    await state.reset_state()
# async def parse(message: Message):
#     try:
#         db = message.bot['db']
#         count = 1
#
#         # query = '''
#         #     DELETE FROM feedback
#         # '''
#         # query2 = '''
#         #     DELETE FROM courses
#         # '''
#         # query3 = '''
#         #     DELETE FROM users
#         # '''
#         # await db.execute(query)
#         # await db.execute(query2)
#         # await db.execute(query3)
#
#         for course in coursesLinks:
#
#             query = f'''
#                 INSERT INTO courses ("id", "hours", "hoursNum", "link", "name", "price", "priceNum", "title")
#                 VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
#             '''
#             await db.execute(query, count, course["hours"], course["hoursNum"], course["link"], course["name"], course["price"], course["priceNum"], course["title"])
#             count += 1
#
#     except Exception as e:
#         logger.error(f"Error during get_data_handler: {e}")

def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start", "menu"], state="*", is_admin=True)
    # dp.register_message_handler(parse, commands=["parse"])

    dp.register_message_handler(admin_menu, text=emojize(":man_office_worker: Меню администратора"), state="*", is_admin=True)
    dp.register_message_handler(admin_back, text=emojize(":house: В меню"), state="*", is_admin=True)
    dp.register_message_handler(admin_back, text=emojize(":no_entry: Отмена"), state="*", is_admin=True)

    dp.register_message_handler(send_invite, text=emojize(":light_bulb: Предложить подписаться на канал"), state=Menu.ADMIN, is_admin=True)
    dp.register_message_handler(send_msg, text=emojize(":loudspeaker: Разослать сообщение"), state=Menu.ADMIN, is_admin=True)
    dp.register_message_handler(msg, state=Send.ANSWER, is_admin=True)
    dp.register_message_handler(addCourse, text=emojize(":plus: Добавить курс"), state=Menu.ADMIN, is_admin=True)
    dp.register_message_handler(addCourse, state=CourseReg.states, is_admin=True)
    dp.register_message_handler(answer_questions, state=Menu.ADMIN, is_admin=True)
    dp.register_message_handler(getAnswer, state=Questions.W_ANSWER, is_admin=True)

    dp.register_message_handler(courses_show, state=Menu.INFO, is_admin=True)

    dp.register_message_handler(look, text=emojize(":eyes: Просмотреть отзывы"), state=Menu.FEEDBACK, is_admin=True)

    dp.register_message_handler(asking_q, state=Menu.QUESTIONS, is_admin=True)