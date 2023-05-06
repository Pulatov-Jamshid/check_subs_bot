import logging
from aiogram import Bot, Dispatcher, executor, types
import markups as nav
import config as cfg
from db import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')


async def check_sub_channels(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        if await check_sub_channels(cfg.CHANNELS, message.from_user.id):
            if not db.user_exists(message.from_user.id):
                start_command = message.text
                referrer_id = str(start_command[7:])
                if str(referrer_id) != "":
                    if str(referrer_id) != str(message.from_user.id):
                        db.add_user(message.from_user.id, referrer_id)
                        try:
                            await bot.send_message(referrer_id,
                                                   "Sizning ssilkangiz bo'yicha yangi foydalanuvchi ro'yhatdan o'tdi!")
                        except:
                            pass
                    else:
                        db.add_user(message.from_user.id)
                        await bot.send_message(message.from_user.id, "Shaxsiy ssilkadan foydalanish mumkin emas")
                else:
                    db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, "Salom", reply_markup=nav.mainMenu)
        else:
            await bot.send_message(message.from_user.id, cfg.NOT_SUB_MESSAGE, reply_markup=nav.showChannels())


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if await check_sub_channels(cfg.CHANNELS, message.from_user.id):
            if message.text == "ℹProfil":
                await bot.send_message(message.from_user.id,
                                       f"Sizning ID: {message.from_user.id}\nhttps://t.me/{cfg.BOT_NICKNAME}?start={message.from_user.id}\nTaklif qilinganlar soni: {db.get_referrer(message.from_user.id)}")
        else:
            await bot.send_message(message.from_user.id, cfg.NOT_SUB_MESSAGE, reply_markup=nav.showChannels())


@dp.callback_query_handler(text="subchanneldone")
async def subchanneldone(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)

    if await check_sub_channels(cfg.CHANNELS, message.from_user.id):
        await bot.send_message(message.from_user.id, "Salom", reply_markup=nav.mainMenu)
    else:
        await bot.send_message(message.from_user.id, cfg.NOT_SUB_MESSAGE, reply_markup=nav.showChannels())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
