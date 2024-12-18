import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Check bot latency")
    async def ping(self, ctx):
        embed = discord.Embed(title="🏓 Pong!", color=discord.Color.green())
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="serverinfo", description="Show server information")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"{guild.name} Info", color=discord.Color.blue())
        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="userinfo", description="Show user information")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name}'s Info", color=member.color)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Roles", value=len(member.roles))
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
