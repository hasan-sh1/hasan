import discord
from discord.ext import commands, tasks
import asyncio
import os
import logging
from datetime import datetime

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

# تذكيرات مخصصة بأوقات محددة
scheduled_messages = {
    (3,45):"اللهم إني أسألك الهدى والتقى والعفاف والغنى ",
    (7,0): " الساعة 7 صباحًا أذكار الصباح:\n سُبْحَانَ اللهِ وبِحَمْدِهِ (مئة مرة أو أكثر). \n• سبحان الله العظيم وبحمده؛ مئة مرّة. \n• اللهمَّ إني أسألُك علمًا نافعًا ورزقًا طيبًا وعملًا متقبلًا. \n• اللهمَّ بك أصبحنا وبك أمسينا وبك نحيا وبك نموتُ وإليك النُّشورُ. \n• حَسْبِيَ اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ ۖ عَلَيْهِ تَوَكَّلْتُ ۖ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ(سبع مرات). \n• لا إلهَ إلَّا اللهُ وحدَه لا شريك له له المُلكُ وله الحمدُ وهو على كلِّ شيءٍ قديرٌ. \n• بسمِ اللَّهِ الَّذي لا يضرُّ معَ اسمِهِ شيءٌ ، في الأرضِ ، ولا في السَّماءِ ، وَهوَ السَّميعُ العليمُ (ثلاث مرات). \n• سُبْحَان الله عَدَدَ خَلْقِهِ، سبحان الله رِضَا نفسه، سبحان الله زِنَةَ عَرْشِهِ، سبحان الله مِدَادَ كلماته ثلاث مرّات. \n• يا حيُّ يا قيومُ برحمتك أستغيثُ ، و أَصلِحْ لي شأني كلَّه ، و لا تَكِلْني إلى نفسي طرفَةَ عَينٍ أبدًا. \n• اللهمّ عافِني في بدني، اللهمّ عافني في سمعي، اللهمّ عافني في بصري، لا إله إلّا أنت ( ثلاث مرّات). \n• لا إلَه إلَّا اللهُ وحدَه لا شَريكَ له، له المُلكُ وله الحمدُ يُحيِي ويُميتُ وهو على كلِّ شيءٍ قديرٌ (عشر مرات). \n• سبحان الله العظيم وبحمده؛ مئة مرّة. \n• رضيتُ باللهِ ربًّا وبالإسلامِ دينًا وبمحمَّدٍ صلَّى اللهُ عليه وسلَّم نبيًّا. \n• سبحان اللهِ والحمدُ للهِ ولا إلهَ إلَّا اللهُ واللهُ أكبرُ ولا حولَ ولا قوَّةَ إلَّا باللهِ العليِّ العظيمِ(مئة مرّةٍ أو أكثر).",
    
    (12,0): " الساعة 12 ظهرًا:\n لا إله إلا الله وحده لا شريك له.",
    (16,0): " الساعة 4 عصرًا:\n اللهم صلِّ وسلم على نبينا محمد.",
    (21,0): " الساعة 9 مساءً أذكار المساء:\n اللهم بك أمسينا، وبك أصبحنا، وبك نحيا، وبك نموت، وإليك المصير. رواه أصحاب السنن عدا النسائي. \n* لا إله إلا الله وحده، لا شريك له، له الملك، وله الحمد، وهو على كل شيء قدير. رواه البزار والطبراني في . \n* يا حي يا قيوم برحمتك أستغيث، أصلح لي شأني كله، ولا تكلني إلى نفسي طرفة عين أبدا. رواه البزار. \n* اللهم أنت ربي، لا إله إلا أنت، خلقتني وأنا عبدك, وأنا على عهدك ووعدك ما استطعت، أعوذ بك من شر ما صنعت، أبوء لك بنعمتك علي، وأبوء بذنبي، فاغفر لي، فإنه لا يغفر الذنوب إلا أنت. رواه البخاري. \n* اللهم فاطر السموات والأرض، عالم الغيب والشهادة، رب كل شيء ومليكه، أشهد أن لا إله إلا أنت, أعوذ بك من شر نفسي، ومن شر الشيطان وشركه، وأن أقترف على نفسي سوءا، أو أجره إلى مسلم. رواه الترمذي. \n*أمسينا وأمسى الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له، اللهم إني أسألك من خير ما في هذه الليلة، وخير ما بعدها، اللهم إني أعوذ بك من شر هذه الليلة وشر ما بعدها، اللهم إني أعوذ بك من الكسل وسوء الكبر، وأعوذ بك من عذاب في النار وعذاب في القبر. رواه مسلم."
}

# المتغيرات
current_index = 0
channel_id = 1311111776510672906
interval = 60  # مؤقت الأذكار العشوائية بالدقائق
is_active = True  # لتفعيل أو إيقاف المهام

# مهمة الأذكار العشوائية
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

# مهمة التذكيرات المخصصة
@tasks.loop(seconds=40)
async def send_scheduled_messages():
    if not is_active or channel_id is None:
        return

    now = datetime.now()
    current_time = (now.hour, now.minute)  # الحصول على الوقت الحالي كساعتين ودقيقتين
    if current_time in scheduled_messages:  # التحقق من وجود الوقت الحالي في التذكيرات
        try:
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(scheduled_messages[current_time], allowed_mentions=discord.AllowedMentions.none())
        except Exception as e:
            print(f"Error in send_scheduled_messages: {e}")


@bot.event
async def on_ready():
    try:
        print(f'Logged in as {bot.user}')
        if channel_id:
            send_azkar.start()  # بدء مهمة الرسائل العشوائية
            send_scheduled_messages.start()  # بدء مهمة التذكيرات المخصصة
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
