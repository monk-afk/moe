# utils/bot.py
import os
import asyncio
import discord
from discord.ext import commands
from utils.conf import config
from utils.nosj import load_file_data
from utils.logroll import logging
log = logging.getLogger(__name__)

class moeBot(commands.Bot):
    def __init__(self, config):
        intents = discord.Intents.default()
        for intent, value in config.get_discord_intents().items():
            setattr(intents, intent, value)
        super().__init__(command_prefix=config.discord_prefix, intents=intents)
        self.config = config

    async def setup_hook(self):
        await self.load_cogs()

    async def load_cogs(self):
        """Loads all cogs from the cogs folder."""
        cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py"):
                cog_name = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(cog_name)
                    log.info(f"Loaded cog: {cog_name}")
                except Exception as e:
                    log.error(f"Failed to load cog {cog_name}: {e}")
        log.info(f"Bot is ready. Logged in as {self.user.name}")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found.")

async def run_bot():
    log.info("Initializing...")
    bot = moeBot(config)
    bot.remove_command("help")
    await load_file_data()
    async with bot:
        await bot.start(config.discord_token)

if __name__ == "__main__":
    asyncio.run(run_bot())



######################################################################################
##  MIT License                                                                     ##
##                                                                                  ##
##  Copyright © 2024-2025 monk (Discord ID: 699370563235479624)                     ##
##                                                                                  ##
##  Permission is hereby granted, free of charge, to any person obtaining a copy    ##
##  of this software and associated documentation files (the "Software"), to deal   ##
##  in the Software without restriction, including without limitation the rights    ##
##  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       ##
##  copies of the Software, and to permit persons to whom the Software is           ##
##  furnished to do so, subject to the following conditions:                        ##
##                                                                                  ##
##  The above copyright notice and this permission notice shall be included in all  ##
##  copies or substantial portions of the Software.                                 ##
##                                                                                  ##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      ##
##  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        ##
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     ##
##  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          ##
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   ##
##  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE   ##
##  SOFTWARE.                                                                       ##
######################################################################################