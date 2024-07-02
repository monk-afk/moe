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
        channel = self.get_channel(self.config.reply_channel)
        if channel:
            await channel.send("I'm back online.")

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command not found.')

def run_bot():
    bot = moeBot(config)
    bot.run(config.discord_token)

if __name__ == '__main__':
    run_bot()