# cogs/react.py
import discord
import re
from discord.ext import commands
from utils.conf import config
import asyncio

reaction_emojis = config.get_reaction_emojis()
reaction_patterns = {
    r".*\b[Uu]pvote[sd]?\b.*": config.reaction_emojis['upvote'],
    r".*\b[Gg]ood\b.*": config.reaction_emojis['upvote'],
    r".*\b[Dd]ownvote[sd]?\b.*": config.reaction_emojis['downvote'],
    r".*\b[Bb]ad\b.*": config.reaction_emojis['downvote'],
    r".*\b[Nn]o\s*[yo]?u\b.*": config.reaction_emojis['noyou'],
    r".*\b([Mm][Ee])\1+\b.*": config.reaction_emojis['moeji'],
    r".*\b[Tt]hinks?[ing]?\b.*": config.reaction_emojis['think'],
    r".*\b[Ww][OoWw]*\b.*": config.reaction_emojis['wow'],
}

class React(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return

        if message.content.startswith(self.bot.command_prefix):
            return

        if message.guild is None:
            return

        for pattern, emoji_id in reaction_patterns.items():
            if re.search(pattern, message.content):
                if emoji_id in self.emojis:
                    emoji = self.emojis[emoji_id]
                else:
                    try:
                        emoji = await self.bot.fetch_application_emoji(emoji_id)
                        self.emojis[emoji_id] = emoji
                    except Exception as e:
                        print(f"Error fetching emoji: {e}")
                        continue
                try:
                    await asyncio.sleep(2)
                    await message.add_reaction(emoji)
                except Exception as e:
                    print(f"Error adding reaction: {e}")

async def setup(bot):
    await bot.add_cog(React(bot))



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