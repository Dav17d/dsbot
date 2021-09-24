import discord, youtube_dl
from selenium import webdriver
from discord.ext import commands

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def search(self, searchInput):
        driver = webdriver.PhantomJS()
        driver.get(f"https://www.youtube.com/results?search_query={searchInput}&sp=EgIQAQ%253D%253D")
        xpath = driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a")
        link = xpath.get_attribute("href")
        return await link

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def p(self, ctx, url):
        if ctx.author.voice is None:
            return await ctx.send("Зайди в войс")
        if 'youtube' not in url:
            url = search(url)
        if 'list' in url:
            ind = url.find('list')
            url = url[0:(ind-1)]
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
        await ctx.send("хохлы")
        

def setup(client):
    client.add_cog(music(client))
