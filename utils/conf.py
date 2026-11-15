# moe/utils/conf.py
# Copyright © 2026 monk <https://github.com/monk-afk>
# SPDX-License-Identifier: MIT
import os
from py_dotenv import read_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.isfile(dotenv_path):
    read_dotenv(dotenv_path)

class Config:
    def __init__(self):
        self.discord_token   = os.getenv("AUTH_TOKEN")
        self.discord_prefix  = os.getenv("CMD_PREFIX") + " "
        self.discord_intents = self.get_discord_intents()
        self.reaction_emojis = self.get_reaction_emojis()
        self.storage_key     = os.getenv("STORAGE_KEY")

    @staticmethod
    def get_discord_intents():
        return {
            "guilds": True,
            "members": True,
            "messages": True,
            "reactions": True,
            "message_content": True,
        }

    @staticmethod
    def get_reaction_emojis():
        return {
            "upvote": os.getenv("UPVOTE_EMOJI"),
            "downvote": os.getenv("DOWNVOTE_EMOJI"),
            "noyou": os.getenv("NOYOU_EMOJI"),
            "think": os.getenv("THINK_EMOJI"),
            "moeji": os.getenv("MOE_EMOJI"),
            "wow": os.getenv("WOW_EMOJI"),
        }

config = Config()
