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

bot = commands.Bot(intents=intents, reconnect=True)


@bot.event
# عند تشغيل البوت
async def on_ready():
    print(f"login is sacsses {bot.user}")


@bot.event
async def on_member_join(member):
    # تحديد قناة الترحيب
    channel = discord.utils.get(member.guild.text_channels, name="👋🏻welcome-الترحيب")

    # تحديد القنوات الأخرى (يمكنك تغيير الأسماء لتناسب السيرفر الخاص بك)
    rules_channel = member.guild.get_channel(1309215521803341855)  # استبدل بالـ ID الخاص بقناة القوانين
    suggestions_channel = member.guild.get_channel(1310680537312137287)  # استبدل بالـ ID الخاص بقناة الاقتراحات
    waiting_channel = member.guild.get_channel(1310538686848303204)  # استبدل بالـ ID الخاص بغرفة الانتظار
    support_channel = member.guild.get_channel(1308856361991540756)  # استبدل بالـ ID الخاص بقناة الدعم

    if channel:
        # الحصول على عدد الأعضاء الحالي في السيرفر
        member_count = len(member.guild.members)

        # رسالة الترحيب
        # رسالة الترحيب باللغة العربية
    welcome_message_ar = f"""{member.mention}
مرحبًا بك في عائلة M1 🎉
أنت العضو رقم {member_count}
لقد أصبحت الآن جزءًا من واحدة من أقوى الكلانات وأكثرها تعاونًا.
{member.guild.name} نؤمن بالعمل الجماعي، الاحترام المتبادل، وروح التحدي التي تقودنا دائمًا إلى القمة.

❤️ نصائح مهمة ❤️
    • تأكد من قراءة قوانين الكلان والالتزام بها لضمان تجربة ممتعة للجميع: {rules_channel.mention if rules_channel  else "رابط القوانين غير متوفر"}
    • شاركنا أفكارك، مهاراتك، وطاقتك الإيجابية لتحقيق النجاح معًا: {suggestions_channel.mention if suggestions_channel else "رابط غرفة الاقتراحات غير متوفر"}
    • إذا كنت بحاجة إلى مساعدة أو لديك استفسارات، لا تتردد في التواصل مع أي من القادة أو الأعضاء: {waiting_channel.mention if waiting_channel else "رابط غرفة الانتظار غير متوفر"}
    
لدعم كلان [M1]: {support_channel.mention if support_channel else "رابط قناة الدعم غير متوفر"}
معًا، نحن أقوى 💪 دعونا نثبت أن M1 دائمًا في القمة 😎
"""
    await channel.send(welcome_message_ar, file=discord.File(r".github/workflows/m1.gif"))
# رسالة الترحيب باللغة الإنجليزية
    # الحصول على القنوات بالـ ID


# رسالة الترحيب باللغة الإنجليزية
    welcome_message_en = f"""{member.mention}
Welcome to the M1 Family 🎉
You are member number {member_count}
You have now joined one of the strongest and most collaborative clans.
Here at {member.guild.name}, we believe in teamwork, mutual respect, and the spirit of challenge that always leads us to the top.

❤️ Important Tips ❤️
    • Make sure to read the clan rules and follow them to ensure a fun experience for everyone: {rules_channel.mention if rules_channel else "Rules channel not available"}
    • Share your ideas, skills, and positive energy to achieve success together: {suggestions_channel.mention if suggestions_channel else "Suggestions channel not available"}
    • If you need help or have questions, don't hesitate to contact any of the leaders or members: {waiting_channel.mention if waiting_channel else "Waiting room not available"}
    
To support the M1 Clan: {support_channel.mention if support_channel else "Support channel not available"}
Together, we are stronger 💪 Let's prove that M1 is always at the top 😎
"""

# إرسال الرسالة
    # await channel.send(welcome_message_en)


# إرسال الرسالتين مع صورة متحركة لكل واحدة
    
    await channel.send(welcome_message_en, file=discord.File(r".github/workflows/m1.gif"))



@bot.event
async def on_member_remove(member):
    # الحصول على القناة الافتراضية أو قناة الترحيب
    channel = discord.utils.get(member.guild.text_channels, name="general")

    if channel:
        # إرسال رسالة ترحيبية
        await channel.send(f"{member} has left the server")
    # else:
    #     print("القناة لم تُعثر عليها.")


# أمر بسيط يرد على المستخدم
@bot.command()
async def هاي(ctx):
    await ctx.reply("هايات😃")


@bot.command()
async def hi(ctx):
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
        
        
    if "باي" in message.content:
        await message.reply(" الله معك👋🏻 ")

        
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(word in message.content for word in ["كيف الحال", "كيفك", "اخبارك"]):
        await message.reply("الحمد لله وأنت؟")

    if "ادمن" in message.content:
        developer_id = "1218995514994065440"
        developer = await message.guild.fetch_member(developer_id)
        if developer:
            await message.reply(f"{developer.mention} هو الادمن الخاص بنا!")
        else:
            await message.reply("لا يمكن العثور على الادمن في هذا السيرفر.")

    
    if "مطور" in message.content:
        developer_id = "916733482057760789"
        developer = await message.guild.fetch_member(developer_id)
        if developer:
            await message.reply(f"{developer.mention} هو المطور الخاص بنا!")
        else:
            await message.reply("لا يمكن العثور على المطور في هذا السيرفر.")
            # مهم للسماح للأوامر بالعمل
    await bot.process_commands(message)
    
# الردود العشوائية
def get_random_response(responses):
    return random.choice(responses)

@bot.event
async def on_error(event, *args, **kwargs):
    with open("error.log", "a") as f:
        f.write(f"Error in {event}: {args}, {kwargs}\n")

@bot.event
async def on_disconnect():
    print("Disconnected from Discord.")

@bot.event
async def on_resumed():
    print("Successfully resumed the session.")





    


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

