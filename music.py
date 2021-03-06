import os
import discord, youtube_dl
from selenium import webdriver
from discord.ext import commands

def load_driver():
	CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
	chrome_bin = os.environ.get("GOOGLE_CHROME_BIN’, “chromedriver")
	options = webdriver.ChromeOptions()
	options.binary_location = chrome_bin
	options.add_argument(" — disable-gpu")
	options.add_argument(" — no-sandbox")
	options.add_argument(" — headless")
	driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
	return driver

def search(self, searchInput):
    driver = load_driver()
    driver.get(f"https://www.youtube.com/results?search_query={searchInput}&sp=EgIQAQ%253D%253D")
    xpath = driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a")
    link = xpath.get_attribute("href")
    driver.close()
    return link

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def p(self, ctx, *, userInput):
        if ctx.author.voice is None:
            return await ctx.send("Зайди в войс")
        
        if 'youtu' not in userInput:
            url = search(self, userInput)
        elif 'list' in userInput:
            ind = userInput.find('list')
            url = userInput[0:(ind-1)]
        else:
            url = userInput

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
        await ctx.send("Запускаю")
        

def setup(client):
    client.add_cog(music(client))
