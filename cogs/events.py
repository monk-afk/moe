# cogs/events.py
import discord
from discord.ext import commands
from utils.logroll import log
from utils.pgsql import drop_guild_input_ids, drop_reply_channel

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        log.info(f'Joined new guild: {guild.name}')
        join_announcement = (f'hey {guild.name}, im moe! use `m1 help` for my command list')

        if guild.system_channel is not None:
            await guild.system_channel.send(join_announcement)
        else:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(join_announcement)
                    break

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guild_id = guild.id
        drop_guild_input_ids(guild_id)
        drop_reply_channel(guild_id)
        log.info(f'Removed from guild: {guild.name}')

    # @commands.Cog.listener()
    # async def on_member_join(self, member):  # Add self as the first parameter
    #     log.info(f'Member joined: {member.name}')
    #     channel = discord.utils.get(member.guild.channels, name='general')
    #     if channel:
    #         await channel.send(f'Welcome to the server, {member.mention}!')
    #         log.info(f'Sent welcome message to {member.mention}')

async def setup(bot):
    await bot.add_cog(Events(bot))




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