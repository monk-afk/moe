# cogs/tools.py
import discord
from discord.ext import commands
from utils.pgsql import (
    set_reply_channel,
    drop_reply_channel,
    drop_guild_input_ids,
    drop_channel_input_ids
    # drop_user_input_ids
)

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Check the bot's latency."""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    # @commands.command()
    # async def wipe_user_memory(self, ctx):
    #     """Clear your chat memory"""
    #     user_id = ctx.author.id
    #     drop_user_input_ids(user_id)
    #     await ctx.send("I forgot what we were talking about.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def forgetchannel(self, ctx):
        """Clear the focused channel chat memory"""
        channel_id = ctx.channel.id
        drop_channel_input_ids(channel_id)
        await ctx.send(f"I have no memory of {ctx.channel.name}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def forgetguild(self, ctx):
        """Clear all chat memory of this Guild"""
        guild_id = ctx.guild.id
        drop_guild_input_ids(guild_id)
        await ctx.send(f"Cleared all channel data for guild {ctx.guild.name}.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setreplychannel(self, ctx):
        """Set the reply channel for the guild"""
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        set_reply_channel(guild_id, channel_id)
        await ctx.send(f"Reply channel set to {ctx.channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unsetreplychannel(self, ctx):
        """Unset the reply channel for the guild"""
        guild_id = ctx.guild.id
        drop_reply_channel(guild_id)
        await ctx.send("Reply channel unset. I will still reply if you call my name.")

async def setup(bot):
    await bot.add_cog(Tools(bot))




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