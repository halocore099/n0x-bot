import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = {}

    @commands.hybrid_command(name="ban", description="Ban a member")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(title="Member Banned", color=discord.Color.red())
        embed.add_field(name="User", value=member.name)
        embed.add_field(name="Reason", value=reason or "No reason provided")
        await member.ban(reason=reason)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="kick", description="Kick a member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(title="Member Kicked", color=discord.Color.orange())
        embed.add_field(name="User", value=member.name)
        embed.add_field(name="Reason", value=reason or "No reason provided")
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="mute", description="Mute a member")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: int):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)
        
        await member.add_roles(muted_role)
        embed = discord.Embed(title="Member Muted", color=discord.Color.orange())
        embed.add_field(name="User", value=member.name)
        embed.add_field(name="Duration", value=f"{duration} seconds")
        await ctx.send(embed=embed)
        
        await asyncio.sleep(duration)
        await member.remove_roles(muted_role)

    @commands.hybrid_command(name="warn", description="Warn a member")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member.id not in self.warns:
            self.warns[member.id] = []
        self.warns[member.id].append(reason or "No reason provided")
        
        embed = discord.Embed(title="Member Warned", color=discord.Color.yellow())
        embed.add_field(name="User", value=member.name)
        embed.add_field(name="Reason", value=reason or "No reason provided")
        embed.add_field(name="Warn Count", value=len(self.warns[member.id]))
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="clear", description="Clear messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(title="Messages Cleared", color=discord.Color.green())
        embed.add_field(name="Amount", value=f"{amount} messages")
        await ctx.send(embed=embed, delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
