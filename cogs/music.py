import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'noplaylist': 'True',
            'default_search': 'ytsearch',
            'quiet': True
        }
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    async def search_song(self, query):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                return {'source': info['formats'][0]['url'], 'title': info['title']}
            except:
                return None

    @commands.hybrid_command(name="play", description="Play a song by name or URL")
    async def play(self, ctx, *, query):
        if not ctx.author.voice:
            return await ctx.send("You need to be in a voice channel!")
            
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

        async with ctx.typing():
            if not query.startswith('http'):
                # Search for the song
                result = await self.search_song(query)
                if result is None:
                    return await ctx.send("Could not find the song!")
                url = result['source']
                title = result['title']
            else:
                # Direct URL
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(query, download=False)
                    url = info['formats'][0]['url']
                    title = info['title']

            if ctx.guild.id not in self.queue:
                self.queue[ctx.guild.id] = []

            if ctx.voice_client.is_playing():
                # Add to queue
                self.queue[ctx.guild.id].append({'source': url, 'title': title})
                embed = discord.Embed(title="🎵 Added to Queue", description=title, color=discord.Color.green())
                return await ctx.send(embed=embed)

            # Play immediately
            ctx.voice_client.play(FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), 
                                after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
            
            embed = discord.Embed(title="🎵 Now Playing", description=title, color=discord.Color.green())
            await ctx.send(embed=embed)

    async def play_next(self, ctx):
        if ctx.guild.id in self.queue and self.queue[ctx.guild.id]:
            next_song = self.queue[ctx.guild.id].pop(0)
            ctx.voice_client.play(FFmpegPCMAudio(next_song['source'], **self.FFMPEG_OPTIONS),
                                after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
            
            embed = discord.Embed(title="🎵 Now Playing", description=next_song['title'], color=discord.Color.green())
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

    @commands.hybrid_command(name="search", description="Search for a song")
    async def search(self, ctx, *, query):
        async with ctx.typing():
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                try:
                    info = ydl.extract_info(f"ytsearch5:{query}", download=False)
                    embed = discord.Embed(title="🔎 Search Results", color=discord.Color.blue())
                    for i, entry in enumerate(info['entries'][:5], 1):
                        embed.add_field(name=f"{i}. {entry['title']}", 
                                      value=f"Duration: {int(entry['duration'])//60}:{int(entry['duration'])%60:02d}", 
                                      inline=False)
                    await ctx.send(embed=embed)
                except:
                    await ctx.send("An error occurred while searching.")

    @commands.hybrid_command(name="leave", description="Disconnect the bot from voice")
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            if ctx.guild.id in self.queue:
                self.queue[ctx.guild.id].clear()
            embed = discord.Embed(title="👋 Disconnected", color=discord.Color.red())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
