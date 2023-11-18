from aiogram.dispatcher.filters.state import StatesGroup, State


class Menu(StatesGroup):
    INFO = State()
    QUESTIONS = State()
    FEEDBACK = State()
    CONTACTS = State()
    ADMIN = State()

class Feedback(StatesGroup):
    ANSWER = State()

class Send(StatesGroup):
    ANSWER = State()

class Questions(StatesGroup):
    ANSWER = State()
    W_ANSWER = State()

class CourseReg(StatesGroup):
    TITLE = State()
    NAME = State()
    LINK = State()
    PRICE = State()
    HOURS = State()
    END = State()