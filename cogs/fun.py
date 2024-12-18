import discord
from discord.ext import commands
import random
import aiohttp

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="8ball", description="Ask the magic 8ball a question")
    async def eight_ball(self, ctx, *, question):
        responses = ["It is certain.", "Without a doubt.", "Most likely.", "Ask again later.", 
                    "Cannot predict now.", "Don't count on it.", "My sources say no.", "Outlook not so good."]
        embed = discord.Embed(title="🎱 Magic 8Ball", color=discord.Color.purple())
        embed.add_field(name="Question", value=question)
        embed.add_field(name="Answer", value=random.choice(responses))
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="roll", description="Roll some dice (e.g., 2d6)")
    async def roll(self, ctx, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))
            results = [random.randint(1, limit) for _ in range(rolls)]
            embed = discord.Embed(title="🎲 Dice Roll", color=discord.Color.green())
            embed.add_field(name="Results", value=f"{results}\nTotal: {sum(results)}")
            await ctx.send(embed=embed)
        except ValueError:
            await ctx.send("Format must be NdN (e.g., 2d6)")

    @commands.hybrid_command(name="meme", description="Get a random meme")
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://meme-api.com/gimme') as response:
                data = await response.json()
                embed = discord.Embed(title=data['title'], color=discord.Color.random())
                embed.set_image(url=data['url'])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="joke", description="Get a random joke")
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://official-joke-api.appspot.com/random_joke') as response:
                data = await response.json()
                embed = discord.Embed(title="😄 Random Joke", color=discord.Color.gold())
                embed.add_field(name="Setup", value=data['setup'])
                embed.add_field(name="Punchline", value=data['punchline'])
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="quote", description="Get an inspirational quote")
    async def quote(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.quotable.io/random') as response:
                data = await response.json()
                embed = discord.Embed(title="📜 Quote", color=discord.Color.blue())
                embed.add_field(name=data['author'], value=data['content'])
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
