import discord
import random
from discord.ext import commands


import os

intents = discord.Intents.default()  # تفعيل الأذونات الأساسية
intents.message_content = True 
intents.presences = True
intents.members = True  

#تعيين اول قيمة وتحديد حساسية الاحرف
bot = commands.Bot(command_prefix="", case_sensitive=True, intents=intents)


@bot.event
# عند تشغيل البوت
async def on_ready():
    print(f"login is sacsses {bot.user}")

@bot.event
async def on_member_join(member):
    # الحصول على القناة الافتراضية أو قناة الترحيب
    channel = discord.utils.get(member.guild.text_channels, name="general")

    if channel:
        # قائمة رسائل الترحيب
        responses = ["welcome 🤩", "نورت الكروب 🎉", "💕هلا بيك"]
        # اختيار رسالة عشوائية
        random_response = random.choice(responses)
        # إرسال رسالة الترحيب
        await channel.send(f"{random_response}, {member.mention}")


@bot.event
async def on_member_remove(member):
    # الحصول على القناة الافتراضية أو قناة الترحيب
    channel = discord.utils.get(member.guild.text_channels, name="general")

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

    elif question is not None:
        await ctx.reply("وعليكم السلام")


@bot.command()
async def clear(ctx, amount=50):
    # التحقق إذا كان المستخدم لديه أذونات "Administrator" أو "Manage Messages"
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount)  # مسح الرسائل
        await ctx.send(
            f"تم مسح {amount} رسالة.", delete_after=5
        )  # إرسال رسالة بعد المسح وتختفي بعد 5 ثواني
    else:
        await ctx.send(
            "لا تملك الأذونات اللازمة لاستخدام هذا الأمر. فقط الأدمن يمكنه ذلك.",
            delete_after=5,
        )


# اعطاء بان لشخص ما
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if await member.ban(reason=reason):
        await ctx.reply("تم الحظر {}#{}".format(member.name, member.discriminator))
    else:
        await ctx.reply("لا يوجد مستخدم")


# يخرج العضو من الكروب
@bot.command()
async def طرد(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.reply("تم الطرد 🦶🏻{}#{}".format(member.name, member.discriminator))


# فك الحظر
@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member.name, member.discriminator = member.split("#")

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
        await message.reply("welcome !")
    if "كيف الحال" in message.content:
        await message.reply("الحمد لله وأنت؟")
    if "كيفك" in message.content:
        await message.reply("الحمد لله وأنت؟")
    if "اخبارك" in message.content:
        await message.reply("كلشي تمام ")
    if "ادمن" in message.content:
        # الحصول على المستخدم باستخدام ID
        developer_id = "1218995514994065440"  # استبدل هذا بمعرف المطور
        developer = await message.guild.fetch_member(developer_id)

        if developer:
            await message.reply(f"{developer.mention} هو الادمن الخاص بنا!")
        else:
            await message.reply("لا يمكن العثور على المطور في هذا السيرفر.")

    if "باي" in message.content:
        await message.reply(" الله معك👋🏻 ")

    if "مطور" in message.content:
        # الحصول على المستخدم باستخدام ID
        developer_id = "916733482057760789"  # استبدل هذا بمعرف المطور
        developer = await message.guild.fetch_member(developer_id)

        if developer:
            await message.reply(f"{developer.mention} هو المطور الخاص بنا!")
        else:
            await message.reply("لا يمكن العثور على المطور في هذا السيرفر.")

    # مهم للسماح للأوامر بالعمل
    await bot.process_commands(message)


# التعامل مع CommandNotFound لمنع ظهور الأخطاء
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        # تجاهل CommandNotFound بدون طباعة الخطأ
        pass
    else:
        # التعامل مع الأخطاء الأخرى
        raise error

    


token = os.getenv("DISCORD_TOKEN_1")



bot.run(token)

