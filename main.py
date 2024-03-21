from telegram import *
from telegram.ext import *
from os import environ as env

from dotenv import load_dotenv
load_dotenv()

TOKEN = env['TOKEN']
MANIFEST_URL = env['MANIFEST_URL']


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    text = f'''
Hi, {update.effective_user.name}! This is Notcoin 👋 

Tap on the coin and watch your balance grow.

How much is Notcoin worth? No one knows, probably nothing.

Got any friends? Get them in the game. That way you'll get even more coins together.

Notcoin is what you want it to be. That's all you need to know.'''
    
    keyboard = [
        [
            InlineKeyboardButton(text="🕹️ Let's go", web_app=WebAppInfo(url="https://tondev-1529e.web.app/#/")),
        ],
        [
            InlineKeyboardButton(text="🤙 Join Heonycoin Community", callback_data="community"),
        ],
        [
            InlineKeyboardButton(text="🎓 How to play", callback_data="None"),
        ],
    ]

    await update.message.reply_photo(
        photo='heonycoin_logo.png',
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def hello2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    text = '''🏴‍☠️

You can find good memes in our socials.

Probably nothing else.'''

    keyboard = [
        [
            InlineKeyboardButton(text="Heonycoin Community", callback_data="None"),
        ],
        [
            InlineKeyboardButton(text="Heonycoin on X", callback_data="community"),
        ],
        [
            InlineKeyboardButton(text="❤️‍🔥 Play", callback_data="None"),
        ],
    ]

    await update.effective_message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def good(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=-1002091724209,
        text=update.effective_user.name
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler(command="start", callback=good, filters=filters.Regex("first")))
app.add_handler(CommandHandler("start", hello))
app.add_handler(CallbackQueryHandler(callback=hello2, pattern="community"))

app.run_polling()