# moe/cogs/tools.py
# Copyright © 2026 monk (https://github.com/monk-afk)
# SPDX-License-Identifier: MIT
import discord
from discord.ext import commands
from utils.dialogpt import dialogpt
from utils.nosj import (
  get_input_tokens,
  set_key
)
from datetime import datetime

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tokenizer = dialogpt.load_tokenizer()

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
    async def dayone(self, ctx):
        """Show SquareOne days online."""
        # dayone = "2023-05-28 20:01:34" CEST (19:01:34 UCT)
        onedays = f"{(datetime.now() - datetime(2023, 5, 28, 20, 1, 34)).total_seconds() / 86400:.5f}"
        await ctx.send(f"SquareOne is {onedays} days old.")

    @commands.command()
    @commands.has_permissions(send_messages=True)
    async def forgetme(self, ctx):
        """Erase your chat history from møe's memory"""
        try:
            await set_key(ctx.guild.id, ctx.author.id, "input_tokens", [])
            await ctx.send(f"I have no memory of {ctx.author.mention}!")
        except Exception as e:
            await log.warning(f"Could forget user: {e}")

async def setup(bot):
    await bot.add_cog(Tools(bot))
