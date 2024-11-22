import discord
import random
from discord.ext import commands


import os

# intents = discord.Intents.default()  
# bot = commands.Bot(command_prefix="!", intents=intents)

# bot = commands.Bot(command_prefix="!")  





intents = discord.Intents.default()  # تفعيل الأذونات الأساسية
intents.message_content = True 
intents.presences = True
intents.members = True  

#تعيين اول قيمة وتحديد حساسية الاحرف
bot = commands.Bot(command_prefix="", case_sensitive=True, intents=intents)




@bot.event
#عند تشغيل البوت 
async def on_ready():
    print(f"login is success {bot.user}")

@bot.event
async def on_member_join(member):
    print(f"{member} has joined the server")

@bot.event
async def on_member_join(member):
    # الحصول على القناة الافتراضية أو قناة الترحيب
    channel = discord.utils.get(member.guild.text_channels, name="الترحيب")  
    
    if channel:
        # إرسال رسالة ترحيبية
        await channel.send(f"نورت الكروب يا {member.mention}! 🎉")




@bot.event
async def on_member_remove(member):
    print(f"{member} has left the server")

# أمر بسيط يرد على المستخدم
@bot.command()
async def هاي(ctx):
    await ctx.reply("welcome! 😃")

@bot.command()
async def ping(ctx):
    await ctx.send(f"your ping: {round(bot.latency * 1000)}ms")


@bot.command(aliases=["مرحبا","السلام عليكم","السلام عليكم ورحمة الله وبركاته"])
async def السلام(ctx,*,question=None):
    if question is None:
        response=["ارحبببب"," نورت","هلا بيك"]
        await ctx.reply(random.choice(response))
        
    elif question is not None:
         await ctx.reply("وعليكم السلام")



#مسح عدد محدد من الرسائل
@bot.command()
async def clear(ctx,amount=20):
    await ctx.channel.purge(limit=amount)


#اعطاء بان لشخص ما
@bot.command()
async def حظر(ctx,member:discord.Member, *,reason=None):
    if await member.ban(reason=reason):
        await ctx.reply("تم الحظر {}#{}".format(member.name, member.discriminator)) 
    return
    await ctx.reply("لا يوجد مستخدم")

#يخرج العضو من الكروب
@bot.command()
async def طرد(ctx,member:discord.Member, *,reason=None):
    await member.kick(reason=reason)
    await ctx.reply("تم الطرد 🦶🏻{}#{}".format(member.name, member.discriminator)) 


#فك الحظر
@bot.command()
async def الغاء_الحظر(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member.name, member.discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name == user.discriminator) == (member.name, member.discriminator):
            await ctx.guild.unban(user)
            await ctx.reply(f"تم الغاء الحظر {member}")
            return
    await ctx.reply("لا يوجد مستخدم")




@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "hi" in message.content:
        await message.channel.send("welcome !")
    
    # مهم للسماح للأوامر بالعمل
    await bot.process_commands(message)


token = os.getenv("MY_DISCORD_TOKEN")
bot = discord.client()



bot.run(token)

