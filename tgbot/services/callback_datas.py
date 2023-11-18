from aiogram.utils.callback_data import CallbackData

feedbacks_callback = CallbackData("feedback", "direction", "index")
courses_callback = CallbackData("courses", "direction", "id")
questions_callback = CallbackData("courses", "direction", "user_id", "question_id")