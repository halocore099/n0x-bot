import discord
from discord.ext import commands
from datetime import datetime

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.hybrid_command(name="commands", description="Shows all commands")  # Changed from "help" to "commands"
    async def show_commands(self, ctx):  # Changed function name too
        embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())
        
        # Add command categories
        embed.add_field(name="🛠️ Utility", value="`ping`, `serverinfo`, `userinfo`, `avatar`", inline=False)
        embed.add_field(name="🎮 Fun", value="`8ball`, `roll`, `meme`, `joke`, `quote`", inline=False)
        embed.add_field(name="🛡️ Moderation", value="`ban`, `kick`, `mute`, `warn`, `clear`", inline=False)
        embed.add_field(name="🎵 Music", value="`play`, `pause`, `resume`, `queue`, `skip`", inline=False)
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="info", description="Shows bot information")
    async def info(self, ctx):
        uptime = datetime.now() - self.start_time
        embed = discord.Embed(title="Bot Information", color=discord.Color.blue())
        embed.add_field(name="Developer", value="Your Name")
        embed.add_field(name="Version", value="1.0.0")
        embed.add_field(name="Uptime", value=str(uptime).split('.')[0])
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Users", value=len(self.bot.users))
        embed.set_footer(text="Made with discord.py")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommands(bot))
