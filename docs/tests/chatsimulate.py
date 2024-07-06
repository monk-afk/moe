# cogs/chatsimulation.py
import discord
from discord.ext import commands
import asyncio

class ChatSimulate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.processing_channel = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        channel_id = message.channel.id
        if channel_id in self.processing_channel:
            return

        typing_task = asyncio.create_task(self.send_typing(message.channel))
        self.processing_channel[channel_id] = typing_task

        try:
            await asyncio.sleep(2)  # simulate message processing
            await message.channel.send(f"Processed message: {message.content}")

        finally:
            typing_task.cancel()
            del self.processing_channel[channel_id]

    async def send_typing(self, channel):
        try:
            while True:
                await channel.typing()
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass

async def setup(bot):
    await bot.add_cog(ChatSimulate(bot))



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