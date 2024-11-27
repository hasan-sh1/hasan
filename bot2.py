import discord
from discord.ext import commands, tasks
import asyncio
import os
import logging

# إعداد مستوى تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# إعداد البوت
intents = discord.Intents.default()
intents.message_content = True  # تفعيل Message Content Intent
intents.presences = True  # تفعيل Presence Intent
intents.members = True  # تفعيل Server Members Intent
bot = commands.Bot(command_prefix="", intents=intents)

# قائمة الأذكار
azkar = [
    "سبحان الله \n الحمد لله \n لا اله إلا الله \n الله أكبر",  
    "لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير",
    "اللهم صلِّ وسلم على نبينا محمد",
    "اللَّهُمَّ إِنِّي أَسأَلُك الهُدَى، والتُّقَى، والعَفَاف، والغِنَى",
    "استغفر الله العظيم وأتوب إليه",
    "اللهم اجعلنا ممن عفوت ورضيت عنهم وغفرت لهم واستجبت دعائهم وكتبت لهم الجنة.",
    "وَاصْبِرْ لِحُكْمِ رَبِّكَ فَإِنَّكَ بِأَعْيُنِنَا✨",
    "سبحانك اللهم وبحمدك",
    "فَصَبرٌ جَميْلٌ",
    "اللهم صلِّ وسلم على نبينا محمد",
    "سبحان الله وبحمده، سبحان الله العظيم",
]

# المتغيرات
current_index = 0
channel_id = 1311111776510672906
interval = 1  
is_active = True  

# مهمة الأذكار
@tasks.loop(seconds=interval * 60)
async def send_azkar():
    global current_index, channel_id
    if not is_active or channel_id is None:
        return
    try:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(azkar[current_index], allowed_mentions=discord.AllowedMentions.none())
            current_index = (current_index + 1) % len(azkar)
    except Exception as e:
        print(f"Error in send_azkar: {e}")


@bot.event
async def on_ready():
    try:
        print(f'Logged in as {bot.user}')
        if channel_id:
            send_azkar.start()
    except Exception as e:
        print(f"Error in on_ready: {e}")


# أمر لتحديد القناة التي سترسل فيها الأذكار
@bot.command()
async def set_channel(ctx):
    global channel_id
    channel_id = ctx.channel.id  # حفظ ID القناة
    await ctx.send(f"تم تعيين قناة الأذكار: {ctx.channel.name}")

# أمر لتغيير المؤقت
@bot.command()
async def مؤقت(ctx, time: int):
    global interval, send_azkar
    if ctx.author.guild_permissions.administrator:  # التحقق من صلاحيات المستخدم
        interval = time  # ضبط المؤقت بالدقائق
        if send_azkar.is_running():
            send_azkar.change_interval(seconds=interval * 60)  # تغيير التكرار بالثواني
        await ctx.send(f"تم ضبط مؤقت إرسال الأذكار إلى {interval} دقيقة.")
    else:
        await ctx.send("عذرًا، يجب أن تكون إداريًا لتغيير المؤقت.")

# أمر لتشغيل الأذكار
@bot.command()
@commands.has_permissions(administrator=True)  # التحقق من أن المستخدم إداري
async def تشغيل(ctx):
    global is_active
    if not is_active:
        is_active = True
        await ctx.send("تم تفعيل إرسال الأذكار.")
    else:
        await ctx.send("الأذكار مفعلة بالفعل.")

# أمر لإيقاف الأذكار
@bot.command()
@commands.has_permissions(administrator=True)  # التحقق من أن المستخدم إداري
async def توقف(ctx):
    global is_active
    if is_active:
        is_active = False
        await ctx.send("تم إيقاف إرسال الأذكار.")
    else:
        await ctx.send("الأذكار متوقفة بالفعل.")

# أمر لعرض الأوامر المتاحة
@bot.command()
async def أوامر(ctx):
    commands_list = [
        "!تشغيل - لتفعيل إرسال الأذكار",
        "!توقف - لإيقاف إرسال الأذكار",
        "!مؤقت <الوقت> - لضبط وقت إرسال الأذكار بالدقائق",
        "!set_channel - لتحديد القناة التي ستُرسل فيها الأذكار"
    ]
    await ctx.send("\n".join(commands_list))

# معالجة الأخطاء في أوامر الصلاحيات
@مؤقت.error
@تشغيل.error
@توقف.error
async def missing_permissions_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("عذرًا، يجب أن تكون إداريًا لتنفيذ هذا الأمر.")

# تشغيل البوت
token = os.getenv("DISCORD_TOKEN_2")
bot.run(token)
