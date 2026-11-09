# moe/cogs/events.py
# Copyright © 2026 monk <https://github.com/monk-afk>
# SPDX-License-Identifier: MIT
import discord
from discord.ext import commands
from utils.logroll import logging
log = logging.getLogger(__name__)
from utils.nosj import (
  drop_guild,
  drop_user_data
)

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
        await drop_guild(guild.id)
        log.info(f'Removed from guild: {guild.name}')

    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload):
        user = getattr(payload, "user", None)
        user_id = getattr(user, "id", None) or getattr(payload, "user_id", None)

        if payload.guild_id is None or user_id is None:
            log.warning(f'[on_raw_member_remove] incomplete payload: guild_id={payload.guild_id}, user_id={user_id}')
            return

        await drop_user_data(user_id, payload.guild_id)

async def setup(bot):
    await bot.add_cog(Events(bot))
