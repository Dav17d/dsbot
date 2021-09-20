import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def p(self, ctx, url):
        if ctx.author.voice is None:
            return await ctx.send("Зайди в войс, даун")
        if 'list' in url:
            return await ctx.send("Кидай ссылку на видос, сука, а не на плейлист!")        
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format':'bestaudio'}
        vc = ctx.voice_client   
        print(url)
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download = False)
        url2 = info['formats'][0]['url']

        source = discord.FFmpegPCMAudio(source = url2, **FFMPEG_OPTIONS)
        vc.play(source)
        await ctx.send("ПОДПИСЫВАЙТЕСЬ НА КАНАЛ https://www.youtube.com/channel/UCw8Ecp0fPBRJBNiKGT0FmJg")
        

def setup(client):
    client.add_cog(music(client))
