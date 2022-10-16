from aiogram import Bot, Dispatcher, executor, types
import os
import db
import keaboardin
import keaboardin as kb


from aiogram.types import user

TOKEN = os.environ['token']
# print(TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = {}


@dp.message_handler(content_types=['contact', 'location'])
async def ph(message: types.Message):
    print('--')
    print(message)


@dp.message_handler()
async def echo(message: types.Message):
    print(message)
    print(message.from_user.id, ' - ', message.from_user.first_name, ' - ', message.text)
    user = {
        'id_telegram': message.from_user.id,
        'username': message.from_user.username,
        'name': message.from_user.first_name
    }
    if len(db.get_user(message.from_user.id)) == 0:
        db.add_user(user)
    users.update({message.from_user.id: message.from_user.first_name})
    # keyboard = kb.keyboard_menu
    if message.text == 'Новини України та зарубіжжя':
        keyboard = kb.inline_keyboard()
    else:
        keyboard = kb.get_kbrd()
        keyboard.add(types.KeyboardButton('Новини України та зарубіжжя'))

    await message.answer(message.text, reply_markup=keyboard)
    # await message.reply(message.text)

    # text = f'Пользователь {message.from_user.first_name} написал {message.text}'
    # for i in users.keys():
    #     if i != message.from_user.id:
    #         await bot.send_message(chat_id=i,
    #                                text=text)


@dp.callback_query_handler()
async def call_echo(callback_q: types.CallbackQuery):
    print(callback_q)
    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(chat_id=callback_q.from_user.id, text=callback_q.data)
if __name__ == '__main__':
    executor.start_polling(dp)
