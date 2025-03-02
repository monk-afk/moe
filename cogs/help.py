# cogs/help.py
import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", help="Shows this message")
    async def custom_help(self, ctx, *cog_names):
        if not cog_names:
            embed = discord.Embed(title="Help", description="List of available commands:", color=discord.Color.red())
            embed.set_thumbnail(url=ctx.bot.user.avatar)
            for cog_name, cog in self.bot.cogs.items():
                if cog.get_commands():
                    cog_commands = [f"`{command.name}`: {command.help or 'No description'}" for command in cog.get_commands()]
                    embed.add_field(name=cog_name, value="\n".join(cog_commands), inline=False)
            await ctx.send(embed=embed)
        else:
            for cog_name in cog_names:
                cog = self.bot.get_cog(cog_name)
                if cog:
                    embed = discord.Embed(title=f"Help - {cog_name}", description=cog.__doc__, color=discord.Color.red())
                    embed.set_thumbnail(url=ctx.bot.user.avatar)
                    for command in cog.get_commands():
                        embed.add_field(name=command.name, value=command.help or "No description", inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"No cog named `{cog_name}` found.")

    @commands.command()
    async def source(self, ctx):
        """Link to Source Code."""
        await ctx.send(f"{ctx.bot.user}'s source code: https://github.com/monk-afk/moe")

    @commands.command()
    async def squareone(self, ctx):
        """SquareOne Discord Invite Link."""
        await ctx.send(f"{ctx.bot.user}'s home is at SquareOne: https://discord.gg/pE4Tu3cf23")

async def setup(bot):
    await bot.add_cog(Help(bot))



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