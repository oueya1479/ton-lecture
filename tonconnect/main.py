from telegram import *
from telegram.ext import *
from pytonconnect import TonConnect
import tonconnect.config
from tonconnect.connector import get_connector
import asyncio
from pytoniq_core import Address
import time
from tonconnect.messages import get_comment_message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    connector = get_connector(chat_id)
    connected = await connector.restore_connection()

    if connected:
        wallet_address = connector.account.address
        wallet_address = Address(wallet_address).to_str(is_bounceable=False)
        name = update.effective_user.name
        text = f'name: {name}, address: {wallet_address}'
        await context.bot.send_message(
            chat_id=-1002091724209,
            text=text,
        )

    else:
        wallets_list = TonConnect.get_wallets()
        button = []
        for wallet in wallets_list:
            button.append([InlineKeyboardButton(text=wallet['name'], callback_data=f"connect:{wallet['name']}")])

        await context.bot.send_message(
            chat_id=chat_id,
            text='Connect wallet first!',
            reply_markup=InlineKeyboardMarkup(button)
        )


async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    connector = get_connector(chat_id)
    data = update.callback_query.data.split(':')
    wallet_name = data[1]

    wallets_list = connector.get_wallets()
    wallet = None

    for w in wallets_list:
        if w['name'] == wallet_name:
            wallet = w
    
    print(wallet)

    if wallet is None:
        raise Exception(f'Unknown wallet: {wallet_name}')

    generated_url = await connector.connect(wallet)
    mk_b = InlineKeyboardMarkup([[InlineKeyboardButton(text='Connect', url=generated_url)]])

    # img = qrcode.make(generated_url)
    # stream = BytesIO()
    # img.save(stream)
    # file = BufferedInputFile(file=stream.getvalue(), filename='qrcode')

    await context.bot.send_message(
        chat_id=chat_id,
        text='Connect wallet within 3 minutes', 
        reply_markup=mk_b
    )

    mk_b = InlineKeyboardMarkup([[InlineKeyboardButton(text='Start', callback_data='start')]])

    for i in range(1, 180):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                await update.effective_message.reply_text(f'You are connected with address {wallet_address}', reply_markup=mk_b)
            return

    # await message.answer(f'Timeout error!', reply_markup=mk_b.as_markup())

async def send_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    connector = get_connector(update.effective_chat.id)
    connected = await connector.restore_connection()
    if not connected:
        await update.effective_message.reply_text('Connect wallet first!')
        return
    
    wallets_list = connector.get_wallets()
    wallet = None

    for w in wallets_list:
        if w['name'] == 'Wallet':
            wallet = w

    deeplink = "https://t.me/wallet/start?startapp=tonspace_main"

    transaction = {
        'valid_until': int(time.time() + 3600),
        'messages': [
            get_comment_message(
                destination_address='0:0000000000000000000000000000000000000000000000000000000000000001',
                amount=int(1 * 10 ** 7),
                comment='hello world!'
            )
        ]
    }

    keyboard = [[InlineKeyboardButton(text="Send Transaction", url=deeplink)]]

    await update.effective_message.reply_text(text='Approve transaction in your wallet app!', reply_markup=InlineKeyboardMarkup(keyboard))
    try:
        await asyncio.wait_for(connector.send_transaction(
            transaction=transaction
        ), 300)
    except asyncio.TimeoutError:
        await update.effective_message.reply_text(text='Timeout error!')
    except Exception as e:
        await update.effective_message.reply_text(text=f'Unknown error: {e}')

async def disconnect_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    connector = get_connector(update.effective_chat.id)
    await connector.restore_connection()
    await connector.disconnect()
    await update.effective_message.reply_text('You have been successfully disconnected!')
