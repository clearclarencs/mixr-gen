import discord, io
from discord.ext import commands 
from main import gen

client = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@client.event
async def on_ready():
    print("Started")

@client.command(name='mixr', help='Generates free drink')
async def go(ctx):
    with io.BytesIO() as image_binary:
        email = gen(use_card=True, card=ctx.message.content.replace("!mixr", "").strip()).save(image_binary, 'PNG')
        await ctx.send(email)
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

client.run("Njc2Nzk5MDUyMTYzMTg2Njg5.GLlT6o.WJfWn4U9DYPtQwJ8SKpRLMyCiAe321JCBtkWOU")