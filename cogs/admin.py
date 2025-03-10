# cogs/admin.py
import discord
from discord.ext import commands
from utils.logroll import logging
log = logging.getLogger(__name__)
from utils.nosj import (
    drop_guild_input_tokens,
    set_key,
    reset_file_data,
    save_file_data,
    show_file_data
)

class Admin(commands.Cog):
    """Admin commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def forgetuser(self, ctx, user: discord.Member):
        """Clear moe's chat memory of a member."""
        if not user:
            await ctx.send("Forget who? I need a username")
            return
        await set_key(ctx.guild.id, user.id, "input_tokens", [])
        await ctx.send(f"I have no memory of {user.mention}!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def forgetguild(self, ctx):
        """Clear all chat memory of this Guild."""
        await drop_guild_input_tokens(ctx.guild.id)
        await ctx.send(f"I have no memory of {ctx.guild.name}.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def resetguild(self, ctx):
        """Clear all chat memory of this Guild."""
        await drop_guild(ctx.guild.id)
        await ctx.send(f"Guild {ctx.guild.name} data reset.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setreplychannel(self, ctx):
        """Set moe's designated reply channel."""
        await set_key(ctx.guild.id, None, "reply_channel", ctx.channel.id)
        await ctx.send(f"Reply channel set to {ctx.channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unsetreplychannel(self, ctx):
        """Unset the reply channel for the guild."""
        await set_key(ctx.guild.id, None, "reply_channel", None)
        await ctx.send("Reply channel unset.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sayhi(self, ctx, user: discord.User):
        """Add a member to the reply list."""
        if not user:
            await ctx.send("I'm not a mind-reader you know, tell me a name!")
            return
        await set_key(ctx.guild.id, user.id, "reply_to", True)
        await ctx.send(f"Hello {user.name}!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def saybye(self, ctx, user: discord.User):
        """Remove a member from the reply list."""
        if not user:
            await ctx.send("Bye to who?")
            return
        await set_key(ctx.guild.id, user.id, "reply_to", False)
        await ctx.send(f"Bye {user.name}!")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension: str):
        """Reload a module"""
        if not extension:
            await ctx.send("Reload which module? Be specific.")
            return
        try:
            await self.bot.reload_extension(f"cogs.{extension}")
            log.warning(f"cogs.{extension} reloaded by {ctx.author}")
            await ctx.send(f"Reloaded `{extension}` successfully!")
        except Exception as e:
            log.error(f"Failed to reload cogs.{extension}, invoked by {ctx.author}")
            await ctx.send(f"Failed to reload `{extension}`: {e}")

    @commands.command()
    @commands.is_owner()
    async def rebuild(self, ctx):
        """Wipe and rebuild the memory file."""
        log.warning(f"{ctx.author} invoked database rebuild")
        await reset_file_data()
        await ctx.send(f"Rebuild complete!")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shut the bot down"""
        log.info("Shutdown command received")
        await ctx.send("Nooo...")
        await save_file_data()
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def dumpbackend(self, ctx):
        """Dump memory file to logs"""
        try:
            json_data = await show_file_data()
            log.info(f"{json_data}")
            await ctx.send("Dumped backend logs! lol")
        except Exception as e:
            await ctx.send(f"Could not dump! {e}")

async def setup(bot):
    await bot.add_cog(Admin(bot))



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