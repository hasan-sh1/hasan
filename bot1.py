import discord
import random
from discord.ext import commands
import os
from datetime import datetime
import time as pytime
import re
from discord.ext import commands
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz


# تفعيل الأذونات الأساسية
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

# تعيين البوت
bot = commands.Bot(command_prefix="", case_sensitive=True, intents=intents, reconnect=True)


@bot.event
# عند تشغيل البوت
async def on_ready():
    print(f"login is sacsses {bot.user}")

# رسالة الترحيب
@bot.event
async def on_member_join(member):
    # تحديد قناة الترحيب
    channel = discord.utils.get(member.guild.text_channels, name="👋🏻welcome-الترحيب")

    # تحديد القنوات الأخرى (يمكنك تغيير الأسماء لتناسب السيرفر الخاص بك)
    rules_channel = member.guild.get_channel(
        1309215521803341855
    )  # استبدل بالـ ID الخاص بقناة القوانين
    suggestions_channel = member.guild.get_channel(
        1310680537312137287
    )  # استبدل بالـ ID الخاص بقناة الاقتراحات
    waiting_channel = member.guild.get_channel(
        1310538686848303204
    )  # استبدل بالـ ID الخاص بغرفة الانتظار
    support_channel = member.guild.get_channel(
        1308856361991540756
    )  # استبدل بالـ ID الخاص بقناة الدعم

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
    await channel.send(
        welcome_message_ar, file=discord.File(r".github/workflows/m1.gif")
    )
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

    await channel.send(
        welcome_message_en, file=discord.File(r".github/workflows/m1.gif")
    )


@bot.event
async def on_member_remove(member):
    # الحصول على القناة الافتراضية أو قناة الترحيب
    channel = discord.utils.get(member.guild.text_channels, name="general")

    if channel:
        await channel.send(f"{member} has left the server")
    # else:
    #     print("القناة لم تُعثر عليها.")


@bot.command()
async def ping(ctx):
    await ctx.send(f"your ping: {round(bot.latency * 1000)}ms")




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



# يخرج العضو من الكروب

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    # التحقق من صلاحيات المستخدم
    if not ctx.author.guild_permissions.kick_members:
        await ctx.reply("❌ ليس لديك صلاحية طرد المستخدمين.")
        return

    try:
        # تنفيذ عملية الطرد
        await member.kick(reason=reason)
        await ctx.reply(f"🦶🏻 تم طرد {member.name}#{member.discriminator} بسبب: {reason if reason else 'غير محدد'}.")
    except Exception as e:
        # معالجة أي أخطاء أثناء الطرد
        await ctx.reply("❌ حدث خطأ أثناء محاولة الطرد.")
        print(f"Error in طرد command: {e}")


# أمر عرض قائمة المحظورين
@bot.command()
async def bans(ctx):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.reply("❌ ليس لديك صلاحية عرض قائمة الحظر.")
        return

    # جمع قائمة المحظورين باستخدام async generator
    banned_users = [ban_entry async for ban_entry in ctx.guild.bans()]
    
    if not banned_users:
        await ctx.reply("⚠️ لا توجد قائمة حظر.")
        return

    # عرض قائمة المحظورين
    ban_list = "\n".join([f"{ban_entry.user.name}#{ban_entry.user.discriminator}" for ban_entry in banned_users])
    await ctx.reply(f"📋 قائمة المحظورين:\n{ban_list}")

# أمر فك الحظر عن مستخدم
@bot.command()
async def unban(ctx, *, member: str = None):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.reply("❌ ليس لديك صلاحية إلغاء الحظر.")
        return

    # جمع قائمة المحظورين باستخدام async generator
    banned_users = [ban_entry async for ban_entry in ctx.guild.bans()]
    
    if not member:
        if not banned_users:
            await ctx.reply("⚠️ لا توجد قائمة حظر.")
        else:
            ban_list = "\n".join([f"{ban.user.name}#{ban.user.discriminator}" for ban in banned_users])
            await ctx.reply(f"📋 الرجاء اختيار مستخدم لفك الحظر من القائمة:\n{ban_list}")
        return

    try:
        name, discriminator = member.split("#")
    except ValueError:
        await ctx.reply("❌ الرجاء إدخال المستخدم بصيغة `اسم#رقم`.")
        return

    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == name and user.discriminator == discriminator:
            await ctx.guild.unban(user)
            await ctx.reply(f"✅ تم فك الحظر عن {user.name}#{user.discriminator}.")
            return

    await ctx.reply("⚠️ لم يتم العثور على المستخدم.")

# أمر حظر مستخدم
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.reply("❌ ليس لديك صلاحية حظر المستخدمين.")
        return

    try:
        await member.ban(reason=reason)
        await ctx.reply(f"✅ تم حظر {member.name}#{member.discriminator} بسبب: {reason if reason else 'غير محدد'}.")
    except Exception as e:
        await ctx.reply("❌ حدث خطأ أثناء محاولة الحظر.")
        print(f"Error in ban command: {e}")





@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    # التحقق من صلاحيات المستخدم
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.reply("❌ ليس لديك صلاحية كتم الأعضاء.")
        return
    
    # التحقق إذا كان العضو ميتًا بالفعل
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        # إذا لم يكن هناك دور "Muted"، نقوم بإنشائه
        mute_role = await ctx.guild.create_role(name="Muted")
        # إضافة صلاحية منع الكتابة للمستخدمين مع الدور "Muted"
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(mute_role, send_messages=False)
        for channel in ctx.guild.voice_channels:
            await channel.set_permissions(mute_role, speak=False)
    
    # إضافة دور "Muted" للعضو
    await member.add_roles(mute_role, reason=reason)
    await ctx.reply(f"✅ تم كتم {member.name}#{member.discriminator} بسبب: {reason if reason else 'غير محدد'}.")

@bot.command()
async def unmute(ctx, member: discord.Member):
    # التحقق من صلاحيات المستخدم
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.reply("❌ ليس لديك صلاحية فك كتم الأعضاء.")
        return
    
    # التحقق من وجود دور "Muted"
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        await ctx.reply("❌ لا يوجد دور كتم في الخادم.")
        return

    # إزالة دور "Muted" من العضو
    await member.remove_roles(mute_role)
    await ctx.reply(f"✅ تم فك كتم {member.name}#{member.discriminator}.")

@bot.command()
async def mutes(ctx):
    # التحقق من صلاحيات المستخدم
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.reply("❌ ليس لديك صلاحية عرض الأعضاء المكتومين.")
        return

    # التحقق من وجود دور "Muted"
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        await ctx.reply("❌ لا يوجد دور كتم في الخادم.")
        return

    # الحصول على الأعضاء المكتومين
    muted_members = [member for member in ctx.guild.members if mute_role in member.roles]
    
    if not muted_members:
        await ctx.reply("❌ لا يوجد أعضاء مكتومين حاليًا.")
        return

    # عرض قائمة الأعضاء المكتومين
    mute_list = "\n".join([f"{member.name}#{member.discriminator}" for member in muted_members])
    await ctx.reply(f"قائمة الأعضاء المكتومين:\n{mute_list}")




# قاموس لتخزين التحذيرات لكل عضو
warns = {}

@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    # التحقق من صلاحيات المستخدم
    if not ctx.author.guild_permissions.kick_members:
        await ctx.reply("❌ ليس لديك صلاحية تحذير الأعضاء.")
        return

    # التحقق من أن العضو موجود في الخادم
    if not isinstance(member, discord.Member):
        await ctx.reply("❌ لم يتم العثور على هذا العضو.")
        return

    # إضافة تحذير جديد للعضو
    if member.id not in warns:
        warns[member.id] = []  # إضافة قائمة فارغة إذا لم يكن لدى العضو تحذيرات سابقة

    warns[member.id].append(reason)

    # إذا وصل العضو إلى 3 تحذيرات، يتم حظره تلقائيًا
    if len(warns[member.id]) >= 3:
        await member.ban(reason="تم حظر العضو بعد تجاوز 3 تحذيرات.")
        await ctx.reply(f"⚠️ {member.name}#{member.discriminator} تم حظره بسبب تجاوز 3 تحذيرات.")
    else:
        await ctx.reply(f"✅ تم تحذير {member.name}#{member.discriminator}. السبب: {reason if reason else 'غير محدد'}.")

@bot.command()
async def unwarn(ctx, member: discord.Member):
    # التحقق من صلاحيات المستخدم
    if not ctx.author.guild_permissions.kick_members:
        await ctx.reply("❌ ليس لديك صلاحية مسح التحذيرات.")
        return

    # التأكد من أن العضو لديه تحذيرات
    if member.id not in warns or not warns[member.id]:
        await ctx.reply(f"❌ {member.name}#{member.discriminator} ليس لديه أي تحذيرات.")
        return

    # إزالة آخر تحذير
    warns[member.id].pop()
    await ctx.reply(f"✅ تم مسح آخر تحذير لـ {member.name}#{member.discriminator}.")

@bot.command()
async def warnss(ctx, member: discord.Member):
    # التحقق من صلاحيات المستخدم
    if not ctx.author.guild_permissions.kick_members:
        await ctx.reply("❌ ليس لديك صلاحية عرض التحذيرات.")
        return

    # التحقق إذا كان العضو لديه تحذيرات
    if member.id not in warns or not warns[member.id]:
        await ctx.reply(f"❌ {member.name}#{member.discriminator} ليس لديه أي تحذيرات.")
        return

    # عرض عدد التحذيرات
    num_warns = len(warns[member.id])
    await ctx.reply(f"👮‍♂️ {member.name}#{member.discriminator} لديه {num_warns} تحذيرات.")


# قائمة الأدوار المتاحة
available_roles = ["Member", "Friends", "CLAN [M1]", "OWNER"]

# دالة لإضافة دور للعضو
@bot.command()
async def addrole(ctx, member: discord.Member, role_name: str):
    # التحقق من صلاحيات المستخدم
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.reply("❌ ليس لديك صلاحية إضافة الأدوار.")
        return

    # التحقق إذا كان الدور المدخل موجودًا في قائمة الأدوار المتاحة
    if role_name not in available_roles:
        await ctx.reply("❌ هذا الدور غير متاح. الأدوار المتاحة هي: member, friends, clan[M1], owner.")
        return

    # الحصول على الدور من الخادم
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    # التأكد من وجود الدور في الخادم
    if not role:
        await ctx.reply(f"❌ لم يتم العثور على الدور '{role_name}' في هذا الخادم.")
        return

    # إضافة الدور للعضو
    await member.add_roles(role)
    await ctx.reply(f"✅ تم إضافة دور '{role_name}' للعضو {member.name}#{member.discriminator}.")

# دالة لإزالة دور من العضو
@bot.command()
async def unrole(ctx, member: discord.Member, role_name: str):
    # التحقق من صلاحيات المستخدم
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.reply("❌ ليس لديك صلاحية إزالة الأدوار.")
        return

    # التحقق إذا كان الدور المدخل موجودًا في قائمة الأدوار المتاحة
    if role_name not in available_roles:
        await ctx.reply("❌ هذا الدور غير متاح. الأدوار المتاحة هي: member, friends, clan[M1], owner.")
        return

    # الحصول على الدور من الخادم
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    # التأكد من وجود الدور في الخادم
    if not role:
        await ctx.reply(f"❌ لم يتم العثور على الدور '{role_name}' في هذا الخادم.")
        return

    # إزالة الدور من العضو
    await member.remove_roles(role)
    await ctx.reply(f"✅ تم إزالة دور '{role_name}' من العضو {member.name}#{member.discriminator}.")



@bot.command()
async def serverinfo(ctx):
    # جلب السيرفر
    server = ctx.guild

    # جلب التفاصيل الأساسية للسيرفر
    name = server.name
    owner = server.owner
    member_count = server.member_count
    created_at = server.created_at.strftime('%d %B %Y, %H:%M:%S')
    region = server.preferred_locale  # تعديل من server.region إلى server.preferred_locale
    icon = server.icon  # نستخدم icon بدلاً من icon_url للتحقق من وجود الصورة
    verification_level = server.verification_level
    description = server.description if server.description else "لا يوجد وصف."

    # جلب تفاصيل القنوات
    text_channels = len([channel for channel in server.channels if isinstance(channel, discord.TextChannel)])
    voice_channels = len([channel for channel in server.channels if isinstance(channel, discord.VoiceChannel)])

    # جلب تفاصيل الأدوار
    roles = len(server.roles)
    
    # تنسيق المعلومات
    embed = discord.Embed(
        title=f"معلومات السيرفر: {name}",
        color=discord.Color.blue()
    )
    
    if icon:  # إذا كان يوجد صورة
        icon_url = icon.url  # الحصول على رابط الصورة إذا كانت موجودة
        embed.set_thumbnail(url=icon_url)
    else:
        embed.add_field(name="⚠️ الصورة", value="لا توجد صورة للسيرفر.", inline=False)

    embed.add_field(name="👑 المالك", value=owner, inline=False)
    embed.add_field(name="👥 عدد الأعضاء", value=member_count, inline=False)
    embed.add_field(name="📅 تاريخ الإنشاء", value=created_at, inline=False)
    embed.add_field(name="🌍 المنطقة", value=region, inline=False)
    embed.add_field(name="🔐 مستوى التحقق", value=verification_level, inline=False)
    embed.add_field(name="📜 الوصف", value=description, inline=False)
    embed.add_field(name="💬 القنوات النصية", value=text_channels, inline=False)
    embed.add_field(name="🎤 قنوات الصوت", value=voice_channels, inline=False)
    embed.add_field(name="💼 عدد الأدوار", value=roles, inline=False)

    # إرسال المعلومات إلى القناة
    await ctx.reply(embed=embed)


@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    # إذا لم يتم تحديد العضو، سيتم استخدام الذي أرسل الأمر
    if member is None:
        member = ctx.author

    # جلب التفاصيل الأساسية للعضو
    name = member.name
    discriminator = member.discriminator
    joined_at = member.joined_at.strftime('%d %B %Y, %H:%M:%S')
    created_at = member.created_at.strftime('%d %B %Y, %H:%M:%S')
    roles = [role.name for role in member.roles if role.name != "@everyone"]  # استبعاد دور الجميع
    nickname = member.nick if member.nick else "لا يوجد لقب"
    status = str(member.status).capitalize()
    game = member.activity.name if member.activity else "لا يلعب حالياً"

    # التحقق من وجود صورة للعضو
    avatar = member.avatar
    if avatar:
        avatar_url = avatar.url
    else:
        avatar_url = None

    # إعداد الـ embed
    embed = discord.Embed(
        title=f"معلومات العضو: {name}#{discriminator}",
        color=discord.Color.green()
    )
    
    # إضافة صورة إن وجدت
    if avatar_url:
        embed.set_thumbnail(url=avatar_url)
    else:
        embed.add_field(name="⚠️ الصورة", value="لا توجد صورة للعضو.", inline=False)

    # إضافة الحقول الأخرى
    embed.add_field(name="🔤 الاسم الكامل", value=f"{name}#{discriminator}", inline=False)
    embed.add_field(name="🎮 الحالة", value=status, inline=False)
    embed.add_field(name="🕹️ اللعب الحالي", value=game, inline=False)
    embed.add_field(name="📅 تاريخ الانضمام إلى السيرفر", value=joined_at, inline=False)
    embed.add_field(name="📅 تاريخ إنشاء الحساب", value=created_at, inline=False)
    embed.add_field(name="📝 اللقب", value=nickname, inline=False)
    embed.add_field(name="💼 الأدوار", value=", ".join(roles) if roles else "لا أدوار", inline=False)

    # إرسال المعلومات إلى القناة
    await ctx.reply(embed=embed)

 

@bot.command()
@commands.has_permissions(administrator=True)  # الصلاحيات للأدمن فقط
async def antispam(ctx, status: str):
    """لتفعيل أو إيقاف ميزة الـ Antispam"""
    global antispam_enabled

    if status.lower() == "on":
        antispam_enabled = True
        await ctx.send("✅ تم تفعيل نظام منع الرسائل المكررة!")
    elif status.lower() == "off":
        antispam_enabled = False
        await ctx.send("✅ تم إيقاف نظام منع الرسائل المكررة!")
    else:
        await ctx.send("❌ الرجاء كتابة `on` لتفعيل أو `off` لإيقاف.")





@bot.command()
@commands.has_permissions(administrator=True)  # صلاحيات الأدمن فقط
async def antilink(ctx, status: str):
    global antilink_enabled
    if status.lower() == "on":
        antilink_enabled = True
        await ctx.reply("✅ تم تفعيل منع الروابط.")
    elif status.lower() == "off":
        antilink_enabled = False
        await ctx.reply("✅ تم تعطيل منع الروابط.")
    else:
        await ctx.reply("❌ يرجى استخدام الأمر بالشكل الصحيح: antilink [on/off]")

# قائمة الردود العشوائية
responses = {
    "هاي": ["هايات😃", "هلااا 😊", "أهلاً وسهلاً! 👋"],
    "بوت": ["🙂خير", "كيف يمكنني مساعدتك؟ 🤖", " شبيك عيني😮‍💨"],
    "مرحبا": ["ارحبببب", "✨نورت", "هلا بيك"],
    "السلام عليكم": ["وعليكم السلام", "وعليكم السلام حياك الله"],
    "السلام عليكم ورحمة الله وبركاته": ["وعليكم السلام ورحمة الله وبركاته"],
    "كيف الحال": " بخير وأنت؟ ",
    "كيفك": "الحمد لله وأنت؟",
    "اخبارك": "كلشي تمام",
    "باي": "الله معك👋🏻",
    "كفو": "كفو منك🫡",
    "مين عمك": "ميسي😉",
    "سلام":"سلالم",
    "شباب":"اني بوت😫",
    "صديقي ":"عيوني😗",
    "فديتك":"فداك راسي🤭",
    "احبك":"حبك برص🤐",
    "hi": ["hi 👋🏻", "Hello! 😊", "Hey! How's it going?"],
    "how are you":"very good😄",
    "what ":"nothing😐",
    "thank you":"welcome🥰",
    
}

# معرّفات المطورين والإداريين
developer_ids = {
    "ادمن": "1218995514994065440",  # معرف الإدمن
    "مطور": "916733482057760789",  # معرف المطور
}

# قائمة الكلمات المحظورة
banned_words = ["حمار", "حيوان", "كلب"]  # ضع الكلمات المحظورة هنا
antispam_enabled = True
antilink_enabled = False

# تخزين التحذيرات
warns = {}
# تخزين أوقات الرسائل السابقة
last_message_time = {}

@bot.event
async def on_message(message):
    global antispam_enabled, antilink_enabled

    if message.author == bot.user:
        return  # لا ترد على رسائل البوت نفسه

    # **التحقق إذا كانت الرسالة تحتوي على كلمة محظورة**
    for word in banned_words:
        if word in message.content:
            await message.delete()  # حذف الرسالة التي تحتوي على الكلمة المحظورة
            await message.channel.send(f"❌ تم حذف رسالة تحتوي على كلمة محظورة من {message.author.name}.")
            
            # إعطاء التحذير للعضو
            if message.author.id not in warns:
                warns[message.author.id] = []
            
            warns[message.author.id].append(f"استخدام كلمة محظورة.")
            
            # إذا وصل العضو إلى 3 تحذيرات، يتم حظره تلقائيًا
            if len(warns[message.author.id]) >= 3:
                await message.author.ban(reason="تم حظر العضو بسبب تجاوز 3 تحذيرات.")
                await message.channel.send(f"⚠️ {message.author.name}#{message.author.discriminator} تم حظره بسبب تجاوز 3 تحذيرات.")
            else:
                await message.channel.send(f"✅ تم تحذير {message.author.name}#{message.author.discriminator} بسبب استخدام كلمة محظورة.")
            return  # الخروج لتجنب المزيد من الفحص

    # **التحقق إذا كانت ميزة حظر الروابط مفعلة**
    if antilink_enabled and not message.author.guild_permissions.administrator:
        if re.search(r"(https?://\S+)", message.content):
            await message.delete()  # حذف الرسالة
            await message.channel.send(f"❌ {message.author.mention} الروابط ممنوعة في هذا السيرفر.")
            return

    # **التحقق من الرسائل المكررة**
    if antispam_enabled:
        current_time = pytime.time()
        member_id = message.author.id

        # التحقق مما إذا كان العضو قد أرسل رسالة في وقت قريب
        if member_id in last_message_time:
            time_difference = current_time - last_message_time[member_id]

            # إذا كان الفرق الزمني أقل من 5 ثوانٍ، يتم حذف الرسالة
            if time_difference < 3:
                await message.delete()  # حذف الرسالة
                await message.author.send("تم إيقاف رسالتك لأنها مكررة. الرجاء التوقف عن إرسال نفس الرسالة.")
                return  # الخروج لتجنب المزيد من الفحص

        # تحديث وقت الرسالة الأخيرة
        last_message_time[member_id] = current_time

    # **الردود العشوائية على الرسائل**
    if message.content.lower() in responses:
        response = responses[message.content.lower()]

        if isinstance(response, list):  # إذا كانت الردود عشوائية (قائمة)
            reply = random.choice(response)
        else:  # إذا كانت الردود نصية ثابتة
            reply = response

        await message.reply(reply)

    # التحقق من الكلمات المخصصة للرد على المعرّفات
    for key, developer_id in developer_ids.items():
        if key in message.content:
            try:
                developer = await message.guild.fetch_member(developer_id)
                if developer:
                    await message.reply(f"{developer.mention} هو {key} الخاص بنا!")
                else:
                    await message.reply(f"لا يمكن العثور على {key} في هذا السيرفر.")
            except Exception as e:
                await message.reply(f"حدث خطأ أثناء البحث عن {key}: {str(e)}")
            break  # إيقاف التكرار بعد الرد على الكلمة المناسبة

    await bot.process_commands(message)  # السماح للأوامر بالعمل


last_message_time = {}


# دالة جلب الوقت بناءً على اسم المدينة أو الدولة
def get_time_by_city_or_country(location_name):
        # استخدام User-Agent خاص لتجنب الحظر
    geolocator = Nominatim(user_agent="mybot")  
    location = geolocator.geocode(location_name)
    
    
    if location:
        # الحصول على إحداثيات المدينة أو الدولة
        latitude = location.latitude
        longitude = location.longitude
        
        # تحديد المنطقة الزمنية باستخدام TimezoneFinder
        timezone_finder = TimezoneFinder()
        result = timezone_finder.timezone_at(lng=longitude, lat=latitude)
        
        if result:
            # تحديد المنطقة الزمنية باستخدام pytz
            timezone = pytz.timezone(result)
            time_in_timezone = datetime.now(timezone)
            
            # إرجاع الوقت
            return time_in_timezone.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return "لم يتم العثور على المنطقة الزمنية."
    else:
        return "لم يتم العثور على المدينة أو الدولة."

# # أمر البوت لإظهار الوقت في المدينة أو الدولة
@bot.command()
async def time(ctx, *, location_name: str):
    """جلب الوقت في المدينة أو الدولة المدخلة"""
    time_in_location = get_time_by_city_or_country(location_name)
    await ctx.send(f"الوقت في {location_name} هو: {time_in_location}")


@bot.command()
@commands.has_permissions(administrator=True)  # تقييد الأمر للإداريين فقط
async def الأوامر(ctx):
    """عرض جميع الأوامر مع شرح بسيط"""
    commands_info = """
    ================ ***قائمة الأوامر*** ================

    =========== **إدارة الدردشة** ===========
    1. `antispam [on/off]`: لتفعيل أو إيقاف ميزة منع الرسائل المكررة.
    2. `antilink [on/off]`: لتفعيل أو إيقاف ميزة منع الروابط.
    3. `clear [number]`: لحذف عدد من الرسائل.
    3. `الكلمات`: لعرض كلمات الردود التلقائي .

    =========== **إدارة الرتب** ===========
    4. `addrole [@user] [role]`: لإعطاء رتبة للعضو.
    5. `unrole [@user] [role]`: لإلغاء الرتبة للعضو.

    =========== **الحظر والطرد** ===========
    6. `ban [@user]`: لحظر عضو.
    7. `unban [@user]`: لإلغاء حظر عضو.
    8. `bans`: لعرض قائمة الأعضاء المحظورين.
    9. `kick [@user]`: لطرد عضو.

    =========== **التحذيرات والكتم** ===========
    10. `warn [@user] [reason]`: لتحذير عضو مع السبب.
    11. `unwarn [@user]`: لإزالة تحذير للعضو.
    12. `warnss [@user]`: لعرض عدد التحذيرات للعضو.
    13. `mute [@user]`: لكتم عضو.
    14. `unmute [@user]`: لإلغاء كتم عضو.
    15. `mutes`: لعرض قائمة الأعضاء المكتومين.

    =========== **معلومات** ===========
    16. `serverinfo`: لعرض معلومات السيرفر.
    17. `userinfo [@user]`: لعرض معلومات العضو.
    17. `time [country or city]`: لعرض الوقت والتاريخ  .
    """
    await ctx.send(commands_info)

@bot.command()
async def الكلمات(ctx):
    """يعرض الكلمات التي يمكن للـ bot الرد عليها"""
    # استخراج الكلمات التي يملك البوت ردود عليها
    response_keys = list(responses.keys())
    
    # تحويل القائمة إلى نص مع فصل الكلمات بفواصل
    response_text = "**== \n ==**".join(response_keys)
    
    # إرسال الرسالة
    await ctx.send(f"الكلمات التي يمكنني الرد عليها هي: {response_text}")

@الأوامر.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("عذرًا، ليس لديك صلاحيات كافية لاستخدام هذا الأمر. يجب أن تكون إداريًا.")
    


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

