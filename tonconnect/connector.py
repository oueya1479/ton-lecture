from pytonconnect import TonConnect

from tonconnect.config import *
from tonconnect.tc_storage import TcStorage

def get_connector(chat_id: int):
    return TonConnect(MANIFEST_URL, storage=TcStorage(chat_id))