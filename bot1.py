import discord
import random
from discord.ext import commands
import os

# تفعيل الأذونات الأساسية
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

# تعيين البوت
bot = commands.Bot(command_prefix="", case_sensitive=True, intents=intents)


# عند تشغيل البوت
@bot.event
async def on_ready():
    print(f"login is success {bot.user}")


# عند انضمام عضو جديد
@bot.event
async def on_member_join(member):
    # الحصول على القناة الافتراضية أو قناة الترحيب
    channel = member.guild.system_channel
    if channel:
        # قائمة رسائل الترحيب
        responses = ["welcome 🤩", "نورت الكروب 🎉", "💕هلا بيك"]
        # اختيار رسالة عشوائية
        random_response = random.choice(responses)
        # إرسال رسالة الترحيب
        await channel.send(f"{random_response}, {member.mention}")


# عند مغادرة عضو
@bot.event
async def on_member_remove(member):
    # الحصول على القناة الافتراضية أو قناة الترحيب
    channel = member.guild.system_channel
    if channel:
        # إرسال رسالة عند مغادرة العضو
        await channel.send(f"{member} has left the server")
    else:
        print(f"{member} has left the server")


# أمر بسيط يرد على المستخدم
@bot.command()
async def هاي(ctx):
    await ctx.reply("هايات😃")


@bot.command()
async def hello(ctx):
    await ctx.reply("hi 👋🏻")


@bot.command()
async def بوت(ctx):
    await ctx.reply("🙂خير")


@bot.command()
async def ping(ctx):
    await ctx.send(f"your ping: {round(bot.latency * 1000)}ms")


@bot.command(aliases=["مرحبا", "السلام عليكم", "السلام عليكم ورحمة الله وبركاته"])
async def السلام(ctx, *, question=None):
    if question is None:
        response = ["ارحبببب", " نورت", "هلا بيك"]
        await ctx.reply(random.choice(response))
    else:
        await ctx.reply("وعليكم السلام")


# مسح الرسائل
@bot.command()
async def clear(ctx, amount=50):
    # التحقق إذا كان المستخدم لديه أذونات "Administrator" أو "Manage Messages"
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount)  # مسح الرسائل
        await ctx.send(f"تم مسح {amount} رسالة.", delete_after=5)  # إرسال رسالة بعد المسح وتختفي بعد 5 ثواني
    else:
        await ctx.send("لا تملك الأذونات اللازمة لاستخدام هذا الأمر. فقط الأدمن يمكنه ذلك.", delete_after=5)


# حظر المستخدم
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.reply(f"تم الحظر {member.name}#{member.discriminator}")


# طرد المستخدم
@bot.command()
async def طرد(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.reply(f"تم الطرد 🦶🏻 {member.name}#{member.discriminator}")


# فك الحظر
@bot.command()
async def unban(ctx, *, member):
    if "#" not in member:
        await ctx.reply("يرجى إدخال اسم المستخدم بالتنسيق الصحيح: username#1234")
        return

    banned_users = await ctx.guild.bans()
    name, discriminator = member.split("#")
    
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == name and user.discriminator == discriminator:
            await ctx.guild.unban(user)
            await ctx.reply(f"تم الغاء الحظر {member}")
            return
    await ctx.reply("لا يوجد مستخدم بهذا الاسم")


# الردود العشوائية
def get_random_response(responses):
    return random.choice(responses)


# التعامل مع الرسائل
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(word in message.content for word in ["كيف الحال", "كيفك", "اخبارك"]):
        await message.reply("الحمد لله وأنت؟")

    if "hi" in message.content:
        await message.reply("welcome!")

    if "ادمن" in message.content:
        developer_id = "1218995514994065440"
        developer = await message.guild.fetch_member(developer_id)
        if developer:
            await message.reply(f"{developer.mention} هو الادمن الخاص بنا!")
        else:
            await message.reply("لا يمكن العثور على المطور في هذا السيرفر.")

    if "باي" in message.content:
        await message.reply("الله معك👋🏻")

    if "مطور" in message.content:
        developer_id = "916733482057760789"
        developer = await message.guild.fetch_member(developer_id)
        if developer:
            await message.reply(f"{developer.mention} هو المطور الخاص بنا!")
        else:
            await message.reply("لا يمكن العثور على المطور في هذا السيرفر.")
    
    # السماح بتنفيذ الأوامر
    await bot.process_commands(message)


# التعامل مع الأخطاء
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        pass  # تجاهل CommandNotFound
    else:
        raise error


# تشغيل البوت
token = os.getenv("DISCORD_TOKEN_1")
bot.run(token)
