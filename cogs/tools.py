# moe/cogs/tools.py
# Copyright © 2026 monk <https://github.com/monk-afk>
# SPDX-License-Identifier: MIT
import discord
from discord.ext import commands
from utils.nosj import drop_user_data
from datetime import datetime

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(send_messages=True)
    async def ping(self, ctx):
        """Check the bot's latency."""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    @commands.has_permissions(send_messages=True)
    async def time(self, ctx):
        """Get the current time."""
        timenow = datetime.now()
        timefmt = timenow.strftime("%B %d, %Y at %H:%M")
        timeunix = timenow.strftime("%s")
        await ctx.send(f"Server time: {timefmt}\nLocal time: <t:{timeunix}:f>")

    @commands.command()
    @commands.has_permissions(send_messages=True)
    async def forgetme(self, ctx):
        """Erase all your chat history from møe's memory"""
        try:
            await drop_user_data(ctx.author.id)
            await ctx.send(f"I have no memory of {ctx.author.mention}!")

async def setup(bot):
    await bot.add_cog(Tools(bot))
