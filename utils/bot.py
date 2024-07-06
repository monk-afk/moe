# bot.py
import os
import discord
from discord.ext import commands
from utils.conf import config

class moeBot(commands.Bot):
    def __init__(self, config):
        intents = discord.Intents.default()
        for intent, value in config.get_discord_intents().items():
            setattr(intents, intent, value)
        super().__init__(command_prefix=config.discord_prefix, intents=intents)
        self.config = config

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.load_cogs()

    async def load_cogs(self):
        cogs_dir = os.path.join(os.path.dirname(__file__), '..', 'cogs')
        for filename in os.listdir(cogs_dir):
            if filename.endswith('.py'):
                cog_name = f'cogs.{filename[:-3]}'
                try:
                    await self.load_extension(cog_name)
                    print(f'Loaded cog: {cog_name}')
                except Exception as e:
                    print(f'Failed to load cog {cog_name}: {str(e)}')
        print(f'Bot is ready. Logged in as {self.user.name}')

    # async def on_message(self, message):
    #     if message.author.bot:
    #         return
    #     await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command not found.')

def run_bot():
    bot = moeBot(config)
    bot.run(config.discord_token)

if __name__ == '__main__':
    run_bot()




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