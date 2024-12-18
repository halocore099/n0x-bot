import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @commands.hybrid_command(name="play", description="Play a song")
    async def play(self, ctx, *, url):
        if not ctx.author.voice:
            return await ctx.send("You need to be in a voice channel!")
            
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
            
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            ctx.voice_client.play(FFmpegPCMAudio(url2, **self.FFMPEG_OPTIONS))
            
        embed = discord.Embed(title="🎵 Now Playing", color=discord.Color.green())
        embed.add_field(name="Song", value=info['title'])
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="pause", description="Pause the current song")
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            embed = discord.Embed(title="⏸️ Paused", color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="resume", description="Resume the current song")
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            embed = discord.Embed(title="▶️ Resumed", color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="queue", description="Show the music queue")
    async def queue(self, ctx):
        if ctx.guild.id not in self.queue:
            return await ctx.send("Queue is empty!")
            
        embed = discord.Embed(title="🎵 Music Queue", color=discord.Color.blue())
        for i, song in enumerate(self.queue[ctx.guild.id], 1):
            embed.add_field(name=f"{i}.", value=song['title'])
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="skip", description="Skip the current song")
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            embed = discord.Embed(title="⏭️ Skipped", color=discord.Color.blue())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
