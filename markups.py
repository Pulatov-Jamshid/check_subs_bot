from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import CHANNELS

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
btnProfile = KeyboardButton('ℹProfil')
mainMenu.add(btnProfile)

def showChannels():
    keyboard = InlineKeyboardMarkup(row_width=1)

    for channel in CHANNELS:
        btn = InlineKeyboardButton(text=channel[0], url=channel[2])
        keyboard.insert(btn)

    btnDoneSub = InlineKeyboardButton(text='Obuna bo\'ldim', callback_data="subchanneldone")
    keyboard.insert(btnDoneSub)
    return keyboard

