# cogs/events.py
import discord
from discord.ext import commands
from utils.logroll import log

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        log.info(f'Joined new guild: {guild.name}')
        join_announcement = (f'hey whats up {guild.name}, im moe!')

        if guild.system_channel is not None:
            await guild.system_channel.send(join_announcement)
        else:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(join_announcement)
                    break

async def setup(bot):
    await bot.add_cog(Events(bot))