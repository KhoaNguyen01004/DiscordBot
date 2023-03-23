import discord
from discord.ext import commands
import asyncio
import API
import os

intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.environ["DISCORD_TOKEN"]


@client.event
async def on_ready():
    print(f'I have logged in as {client.user}')


@client.command(name="hello")
async def hello(ctx):
    async with ctx.channel.typing():
        await asyncio.sleep(0.6)
    await ctx.send('Hello there!')


@client.command()
async def joke(message: discord.Message):
    if message.author == client.user:
        return
    joke = API.Joke().get_joke_json()
    async with message.channel.typing():
        await asyncio.sleep(0.6)
    await message.channel.send(joke["setup"])

    def answer(m: discord.Message):
        return m.author.id == message.author.id and m.channel.id == message.channel.id
    await client.wait_for("message", check=answer)
    async with message.channel.typing():
        await asyncio.sleep(0.6)
    await message.channel.send(joke["punchline"])


@client.command()
async def meme(message: discord.Message):
    meme = API.Meme()
    meme.get_meme_json()
    meme.get_meme()
    async with message.channel.typing():
        await asyncio.sleep(0.6)
    await message.channel.send(file=discord.File("resources/meme.png"))


@client.command()
async def weather_germantown(message: discord.Message):
    weather = API.Weather()
    async with message.channel.typing():
        await asyncio.sleep(0.6)
    data = weather.weather_germantown()
    degree = weather.get_temp(data)
    degree_average = degree["average"]
    degree_feel = degree["feels_like"]
    degree_max = degree["temp_max"]
    degree_min = degree["temp_min"]
    sunrise = weather.get_sun_info(data)["sunrise"]
    sunset = weather.get_sun_info(data)["sunset"]
    description = weather.get_description(data)
    last_update = weather.get_date(data)
    await message.channel.send(f"Temperature (average): {degree_average}°C\n\
                               Temperature (feels like): {degree_feel}°C\n\
                               Temperature (min): {degree_min}°C\n\
                               Temperature (max): {degree_max}°C\n\
                               Sunrise: {sunrise}\n\
                               Sunset: {sunset}\n\
                               Description: {description}\n\
                               Last Update: {last_update}")


client.run(TOKEN)
