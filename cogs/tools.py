# cogs/tools.py
import discord
from discord.ext import commands

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Check the bot's latency."""
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

async def setup(bot):
    await bot.add_cog(Tools(bot))