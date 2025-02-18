from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN_CHAT_IDS = os.getenv('ADMIN_CHAT_IDS')
CHANNEL_ID = os.getenv('CHANNEL_ID')
MINIAPP_URL = os.getenv('MINIAPP_URL')
SUPPORT_CHAT_ID = os.getenv('SUPPORT_CHAT_ID')