from collections import defaultdict
import random
from SpamFilter import AntiSpam
from discord import File,Member
import discord
from discord.ext import commands
from easy_pil import Editor,Canvas,load_image_async,Font
from database.firebase_methods import *

user_message_count = defaultdict(int)
last_message_id = None #son alınan mesaj id

async def historyChecker(bot,CHANNEL_ID):
    global last_message_id
    channel_id = CHANNEL_ID
    channel = bot.get_channel(channel_id)
    
    if channel:
        messages = []
        if last_message_id:
            async for message in channel.history(after=discord.Object(id=last_message_id)):
                messages.append(message)
                
        else:
            async for message in channel.history(limit=1000):
                messages.append(message)
                
        if messages:
            last_message_id = messages[0].id
            
        new_message_count = defaultdict(int)
        
        for message in messages:
            user_id = message.author.id
            new_message_count[user_id]+=1
            user_message_count[user_id]+=1
            
        for user_id,count in new_message_count.items():
            total_count = user_message_count[user_id]
            print(total_count)
            if total_count % 10 == 0:
                user = bot.get_user(user_id)
                if user:
                    #level arttırma fonksiyonu çalışsın
                    if not user.avatar:
                        await updateUserRank(user.display_name,user_id,user.default_avatar,total_count,channel)
                        
                    else:
                        await updateUserRank(user.display_name,user_id,user.avatar,total_count,channel)
                    print(f'{user.display_name} (ID: {user_id}) kullanıcı {total_count} mesaj attı')
                    
    else:
        print(f"Kanal Bulunamadı: {channel_id}")


async def updateUserRank(name,user_id,avatar,total_message,ctx):
    user_data = get_data(user_id,total_message)
    next_level_xp = (user_data["level"] + 1) * 100
    current_level_xp = user_data["level"] * 100
    xp_need = next_level_xp - current_level_xp
    new_level = int((user_data["xp"] + 5)/100)
    if new_level > user_data["level"]:
        new_level = new_level
    else:
        new_level = user_data["level"]
    xp = user_data["xp"]
    percentage = (xp_need / 100) * xp
    print(percentage)
    response = add_data(user_id,new_level,str(name),xp+5)
    
    #rank card
    background =Editor("assets/bg.png")
    profile = await load_image_async(str(avatar))
    profile = Editor(profile).resize((150,150)).circle_image()
    square = Canvas((500,500),"#06FFBF")
    square = Editor(square)
    square.rotate(30,expand=True)
    background.paste(square.image,(600,-250))
    background.paste(profile.image,(30,30))
    background.rectangle((200,180),width=630,height=40,fill="#484b4e",radius=20)
    background.bar(
        (200,180),
        max_width=630,
        height=40,
        percentage = percentage,
        fill="#00fa81",
        radius=20,
    )
    
    poppins = Font.poppins(size=30)
    background.text((200,40),str(name),font=poppins,color="white")
    background.rectangle((200,100),width=350,height=2,fill="#17F3F6")
    background.text(
        (200,130),
        f"Level : {new_level}"
        + f" XP : {xp+5} / {int((user_data['level']+1)*100)}",
        font=poppins,
        color="white"
    )
    file = File(fp=background.image_bytes,filename="rankcard.png")
    await ctx.send(file=file)
