from collections import Counter,defaultdict
import datetime
import os
import random
import discord
from discord.ext import commands,tasks
from dotenv import load_dotenv
from SpamFilter import AntiSpam
from database.firebase_methods import *
from level.levelling import historyChecker
from discord import File
from easy_pil import Editor, Canvas, load_image_async, Font

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)
dictionary_check = True
timer_check = True
content_check = True
history_check = True
CHANNEL_ID = 1265436602545606728

@bot.event
async def on_ready():
    #task başlat
    checker.start()
    print("Pixie Bot Başlatıldı!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Merhaba,Pixie Bot Hazır")

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.errors.CheckFailure):
        await ctx.send("Bu komut için kayıt görev bulunamadı!")

@bot.event
async def on_error(event,*args,**kwargs):
    with open("err.log","a") as f:
        raise
    
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Merhaba {member.name}, Pixie sunucusuna hoşgeldin!")
    
@bot.command(name="roll_dice")
async def roll(ctx,number_dice,number_sides):
    dice = [
        str(random.choice(range(1,int(number_sides)+1)))
        for _ in range(int(number_dice))
    ]
    await ctx.send(', '.join(dice))
    
@bot.command(name="create_channel")
@commands.has_role("admin")
async def create_channel(ctx,channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels,name=channel_name)
    if not existing_channel:
        print("kanal oluşturuldu")
        await guild.create_text_channel(channel_name)
        
        
    
@bot.command(name='rank')
async def rank(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    #await spamFilter(ctx)
    user_data = get_data(member.id,0)
    next_level_xp = (user_data["level"] + 1) * 100
    current_level_xp = user_data["level"] * 100
    xp_need = next_level_xp - current_level_xp
    xp = user_data["xp"]
    percentage = (xp_need / 100) * xp
    print(percentage)
        
    ## Rank card
    background = Editor("assets/bg.png")

    profile = await load_image_async(str(member.display_avatar))
    profile = Editor(profile).resize((150, 150)).circle_image()
    square = Canvas((500, 500), "#06FFBF")
    square = Editor(square)
    square.rotate(30, expand=True)
    background.paste(square.image, (600, -250))
    background.paste(profile.image, (30, 30))
    background.rectangle(
        (200, 180), width=630, height=40, fill="#484b4e", radius=20
    )
    background.bar(
        (200, 180),
        max_width=630,
        height=40,
        percentage=percentage,
        fill="#00fa81",
        radius=20,
    )
    poppins = Font.poppins(size=30)
    background.text((200, 20),"Level Sorgulandı", font=poppins,color="white")
    background.text((200, 60),str(member.display_name), font=poppins,color="white")
    background.rectangle((200, 100), width=350, height=2, fill="#17F3F6")
    background.text(
        (200, 130),
        f"Level : {user_data['level']}"
        + f" XP : {xp} / {int((user_data['level'] + 1) * 100)}",
        font=poppins,
        color="white",
    )

    file = File(fp=background.image_bytes, filename="card.png")
    await ctx.send(file=file)

@bot.command(name="99")
async def nine_nine(ctx):
    br_99_quotes = [

        "I\m the human form of the 💯 emoji",
        "Bingot!",
        (
            "Cool. Cool cool cool cool cool cool cool, "
            "no doubt no doubt no doubt no doubt."
            
        )
        
    ]
    response = random.choice(br_99_quotes)
    await ctx.send(response)
    
    
@tasks.loop(seconds=10)
async def checker():
    await historyChecker(bot,CHANNEL_ID)

bot.run(str(TOKEN))
    
    