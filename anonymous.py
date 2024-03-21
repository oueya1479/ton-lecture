from telegram import *
from telegram.ext import *
from tonconnect.main import *
from os import environ as env

from dotenv import load_dotenv
load_dotenv()

TOKEN = env['TOKEN']
MANIFEST_URL = env['MANIFEST_URL']

good = '''
YOU ARE GOOD!
🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥⬜️
🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥⬜️
🟥🟥⬜️⬜️⬜️⬜️⬜️🟥🟥⬜️⬜️🟥🟥⬜️🟥🟥⬜️⬜️🟥🟥⬜️🟥🟥⬜️⬜️🟥🟥
🟥🟥⬜️⬜️⬜️⬜️⬜️🟥🟥⬜️⬜️🟥🟥⬜️🟥🟥⬜️⬜️🟥🟥⬜️🟥🟥⬜️⬜️🟥🟥
🟥🟥⬜️⬜️🟥🟥⬜️🟥🟥⬜️⬜️🟥🟥⬜️🟥🟥⬜️⬜️🟥🟥⬜️🟥🟥⬜️⬜️🟥🟥
🟥🟥⬜️⬜️🟥🟥⬜️🟥🟥⬜️⬜️🟥🟥⬜️🟥🟥⬜️⬜️🟥🟥⬜️🟥🟥⬜️⬜️🟥🟥
🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥⬜️
🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥🟥⬜️🟥🟥🟥🟥🟥⬜️
'''

async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.effective_message.text
    if text == "good":
        text = good
    
    if text == "wallet":
        text = await start(update, context)
        return
    
    if text == "send":
        await send_transaction(update, context)
        return

    await context.bot.send_message(
        chat_id=-1002091724209,
        text=text
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters=filters.ALL & ~filters.COMMAND, callback=send_message))
app.add_handler(CallbackQueryHandler(pattern="^connect", callback=connect))
app.add_handler(CallbackQueryHandler(pattern="start", callback=start))
app.run_polling()
