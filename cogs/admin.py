# moe/cogs/admin.py
# Copyright © 2026 monk <https://github.com/monk-afk>
# SPDX-License-Identifier: MIT
import discord
from discord.ext import commands
from utils.logroll import logging
log = logging.getLogger(__name__)
from utils.nosj import (
    drop_guild_input_tokens,
    drop_user_data,
    reset_file_data,
    save_file_data
)

class Admin(commands.Cog):
    """Admin commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def forgetuser(self, ctx, user: discord.Member):
        """Clear the specified user's conversation."""
        if not user:
            await ctx.send("Forget who? I need a username")
            return
        await drop_user_data(user.id)
        await ctx.send(f"I have no memory of {user.mention}!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def forgetguild(self, ctx):
        """Clear all user conversations."""
        await drop_guild_input_tokens(ctx.guild.id)
        await ctx.send(f"I have no memory of {ctx.guild.name}.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def resetguild(self, ctx):
        """Reset guild chats and settings."""
        await drop_guild(ctx.guild.id)
        await ctx.send(f"Guild {ctx.guild.name} data reset.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setreplychannel(self, ctx):
        """Set moe's designated reply channel."""
        await set_reply_channel(ctx.guild.id, ctx.channel.id)
        await ctx.send(f"Reply channel set to {ctx.channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unsetreplychannel(self, ctx):
        """Unset the reply channel for the guild."""
        await set_reply_channel(ctx.guild.id, None)
        await ctx.send("Reply channel unset.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ignore(self, ctx, user: discord.Member):
        """Add a member to the ignore list."""
        await set_ignore(user.id, True)
        await ctx.send(f"Cold shoulder activated!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dontignore(self, ctx, user: discord.Member):
        """Remove a member from the ignore list."""
        await set_ignore(user.id, False)
        await ctx.send(f"Hi {user.name}!")

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

async def setup(bot):
    await bot.add_cog(Admin(bot))
