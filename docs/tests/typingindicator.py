# cogs/typingindicator.py
import discord
from discord.ext import commands
import asyncio
import random

class TypingIndicator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testtype(self, ctx):
        """Test Typing Indicator in Multiple Channels."""
        messages = [f"Message {i}" for i in range(10)]
        tasks = [asyncio.create_task(self.process_message(ctx, message, i)) for i, message in enumerate(messages)]
        await asyncio.gather(*tasks)

    async def send_typing(self, ctx):
        while True:
            print(f"{ctx.channel}: Typing...")
            await asyncio.sleep(5)

    async def process_message(self, ctx, message, task_id):
        typing_task = asyncio.create_task(self.send_typing(ctx))
        try:
            delay = random.uniform(0.5, 3.0)
            print(f"Processing {message} with task ID {task_id}, will take {delay:.2f} seconds.")
            await asyncio.sleep(delay)
            response = f"Processed {message} with task ID {task_id}."
            print(response)
        finally:
            typing_task.cancel()

async def setup(bot):
    await bot.add_cog(TypingIndicator(bot))


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