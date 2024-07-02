# conf.py
import os
from py_dotenv import read_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
read_dotenv(dotenv_path)

DATABASE_URL = os.getenv('PGSQL_DB')

class Config:
    def __init__(self):
        self.discord_token = os.getenv('AUTH_TOKEN')
        self.reply_channel = int(os.getenv('REPLY_CHANNEL'))

        self.discord_prefix = 'm1'
        self.discord_intents = self.get_discord_intents()

    @staticmethod
    def get_discord_intents():
        return {
            'guilds': True,
            'members': True,
            'messages': True,
            'reactions': True,
            'presences': True,
            'message_content': True,
        }

config = Config()