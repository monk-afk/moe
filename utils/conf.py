# conf.py
import os
from py_dotenv import read_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
read_dotenv(dotenv_path)

pgsql_db = os.getenv('PGSQL_DB')

class Config:
    def __init__(self):
        self.discord_token   = os.getenv('AUTH_TOKEN')
        self.discord_prefix  = os.getenv('CMD_PREFIX') + ' '
        self.discord_intents = self.get_discord_intents()
        self.reaction_emojis = self.get_reaction_emojis()

    @staticmethod
    def get_discord_intents():
        return {
            'guilds': True,
            'members': True,
            'messages': True,
            'reactions': True,
            'message_content': True,
        }

    @staticmethod
    def get_reaction_emojis():
        return {
            'upvote': os.getenv('UPVOTE_EMOJI'),
            'downvote': os.getenv('DOWNVOTE_EMOJI'),
            'noyou': os.getenv('NOYOU_EMOJI'),
            'think': os.getenv('THINK_EMOJI'),
            'moeji': os.getenv('MOE_EMOJI'),
            'wow': os.getenv('WOW_EMOJI'),
        }

config = Config()



####################################################################################
# MIT License                                                                      #
#                                                                                  #
# Copyright (c) 2024 monk                                                          #
#                                                                                  #
# Permission is hereby granted, free of charge, to any person obtaining a copy     #
# of this software and associated documentation files (the "Software"), to deal    #
# in the Software without restriction, including without limitation the rights     #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell        #
# copies of the Software, and to permit persons to whom the Software is            #
# furnished to do so, subject to the following conditions:                         #
#                                                                                  #
# The above copyright notice and this permission notice shall be included in all   #
# copies or substantial portions of the Software.                                  #
#                                                                                  #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR       #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,         #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE      #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER           #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,    #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE    #
# SOFTWARE.                                                                        #
####################################################################################