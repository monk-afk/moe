# cogs/tools.py
import discord
from discord.ext import commands
from utils.dialogpt import dialogpt
from utils.nosj import (
  get_input_tokens,
  set_key
)

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
    async def forgetme(self, ctx):
        """Erase your chat history from møe's memory"""
        try:
            await set_key(ctx.guild.id, ctx.author.id, "input_tokens", [])
            await ctx.send(f"I have no memory of {ctx.author.mention}!")
        except Exception as e:
            await log.warning(f"Could forget user: {e}")

    @commands.command()
    @commands.has_permissions(send_messages=True)
    async def chatlogs(self, ctx):
        """Show your chat history with møe from this Guild"""
        try:
            chat_history = await get_input_tokens(ctx.guild.id, ctx.author.id)
            chat_history = self.tokenizer.decode(chat_history, skip_special_tokens=False).split("<|endoftext|>")
            chat_history = "\n".join(message.strip() for message in chat_history if message.strip())
            await ctx.send(f"{ctx.author}'s chat history: \n```{chat_history}```")
        except Exception as e:
            await ctx.send(f"I've never spoken to {ctx.author}!")
            await log.warning(f"Could not get user history: {e}")

async def setup(bot):
    await bot.add_cog(Tools(bot))



######################################################################################
##  MIT License                                                                     ##
##                                                                                  ##
##  Copyright © 2024-2025 monk                                                      ##
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