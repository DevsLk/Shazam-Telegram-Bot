"""
    Shazam Telegram Bot
    Copyright (C) 2021 @PredatorHackerzZ
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import logging
import ffmpeg
import asyncio
import json
import requests
from ShazamAPI import Shazam
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from vars import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    "Shazam",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


START_TEXT = """Hello {}
I am Shazam Music Search bot. \
Send me audio file for search result.
> `I can search in inline too. [Coming Soon]`
Made by @TheTeleRoid"""

JOIN_BUTTON = [
    InlineKeyboardButton(
        text='⭕ Updates Channel ⭕',
        url='https://telegram.me/TeleRoidGroup'
    )
]


@bot.on_message(filters.private & filters.command("start"))
async def start(_, message):
    await message.reply_text(
        text=START_TEXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([JOIN_BUTTON]),
        disable_web_page_preview=True,
        quote=True
    )

@bot.on_message(filters.private & filters.audio)
async def shazam(_, message):
    user_id = message.from_user.id
    DL = "./{user_id}"
    m = await message.reply_text("**Shazam Processing**")
    a = await bot.download_media(message, DL)
    try:
       mp3_file_content_to_recognize = open(a, 'rb').read()
       shazam = Shazam(mp3_file_content_to_recognize)
       recognize_generator = shazam.recognizeSong()
       output = next(recognize_generator)
       cj = json.dumps(output)
    except:
       return await m.edit("**Error**")

    key = 'XBH4IgeIY2D40O6RAjn4r8vMav7xy6IN'
    text = cj
    t_title = "Shazam By JE"

    login_data = {
       'api_dev_key': key,
       'api_user_name': 'JasonYako',
       'api_user_password': 'Lel@takataka9'
        }
    data = {
       'api_option': 'paste',
       'api_dev_key':key,
       'api_paste_code':text,
       'api_paste_name':t_title,
       'api_paste_expire_date': 'N',
       'api_user_key': None,
       'api_paste_format': None,
        }

    login = requests.post("https://pastebin.com/api/api_login.php", data=login_data)

    r = requests.post("https://pastebin.com/api/api_post.php", data=data)

    txt = "**Shazam Done ✨\n\nBy ~ @TheTeleRoid**"
    await m.edit(txt, reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton(
                                     "Results 📃", url=f"{r.text}")]]))
    os.remove(a)

        
bot.start()
idle()    
