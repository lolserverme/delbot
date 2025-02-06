import discord
import os
import math
from discord.ext import commands

# Enable bot intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.members = True  # Enable member-related intents (for role management)

# Set up bot command prefix
bot = commands.Bot(command_prefix="?", intents=intents)

# Price calculation function
def calculate_price(start_level, end_level):
    # Ensure input levels are valid
    if start_level < 1 or end_level > 1000 or start_level >= end_level:
        return "输入的等级范围无效，请检查后重新输入！"

    total_price = 0

    # Price calculation based on level ranges
    if start_level < 300:
        upper_bound = min(300, end_level)
        total_price += (upper_bound - start_level) * 0.06
        start_level = upper_bound

    if start_level < 600:
        upper_bound = min(600, end_level)
        total_price += (upper_bound - start_level) * 0.09
        start_level = upper_bound

    if start_level < 750:
        upper_bound = min(750, end_level)
        total_price += (upper_bound - start_level) * 0.11
        start_level = upper_bound

    if start_level < 900:
        upper_bound = min(900, end_level)
        total_price += (upper_bound - start_level) * 0.13
        start_level = upper_bound

    if start_level < 1000:
        upper_bound = min(1000, end_level)
        total_price += (upper_bound - start_level) * 0.15

    return round(total_price, 2)

# When the bot is ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Example command: "?hello"
@bot.command()
async def hello(ctx):
    await ctx.send("Hello! 👋 I'm DeL's Helper!")

# New Command: "?tng" sends an image file (restricted to admins)
@bot.command()
@commands.has_permissions(administrator=True)  # Restrict to admins
async def tng(ctx):
    image_url = "https://raw.githubusercontent.com/lolserverme/delbot/main/TNG.jpg"  # GitHub-hosted image
    await ctx.send(image_url)
    await ctx.message.delete()

# New Command: "?myr <number>" multiplies the number by 8.5
@bot.command()
async def twd(ctx, number: float):
    result = number * 8.5
    await ctx.send(f"RM{number} x 8.5 = {result}台币")

# Command: "?done @mention" gives a specific role to the mentioned user
@bot.command()
@commands.has_permissions(administrator=True)
async def done(ctx, member: discord.Member, image: discord.Attachment):
    role_name = "Buyer买家"
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"⚠️ Role '{role_name}' not found!")
        return
    await member.add_roles(role)
    await ctx.send(f"已经购买通行证/代送了 {member.mention},\n 您已获取 '{role_name}' 称号，请到 https://discord.com/channels/1320960342318387292/1335820101437624414 vouch @DeL .")
    await ctx.send(f"{image.url}")
    await ctx.message.delete()

# Command: "?doneds @mention" (same as ?done, but for a different use case)
@bot.command()
@commands.has_permissions(administrator=True)
async def doneds(ctx, member: discord.Member, image: discord.Attachment):
    role_name = "Buyer买家"
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"⚠️ Role '{role_name}' not found!")
        return
    await member.add_roles(role)
    await ctx.send(f"已经完成代刷了，现在可以登录账号查看了 {member.mention}，\n您已获取 '{role_name}' 称号，请到 https://discord.com/channels/1320960342318387292/1335820101437624414 vouch @DeL .")
    await ctx.send(f"{image.url}")
    await ctx.message.delete()

# Command: "?cal (start level) - (end level)" calculates leveling price
@bot.command()
async def cal(ctx, start_level: int, end_level: int):
    price_rm = calculate_price(start_level, end_level)
    if isinstance(price_rm, str):
        await ctx.send(price_rm)
    else:
        price_twd = math.ceil(price_rm * 8.5)
        await ctx.send(f"代刷从等级 {start_level} 到等级 {end_level} 的总价格是: RM {price_rm} (台币 {price_twd})")

# New Command: "?id" prints predefined text and deletes the command
@bot.command()
async def id(ctx):
    await ctx.send("""代刷 - DeL
名字/id = 
密码/pass = 
!! 随时准备给验证码哦""")
    await ctx.message.delete()

# New Command: "?req" sends leveling requirements and deletes the command
@bot.command()
async def req(ctx):
    await ctx.send("""====代刷等级需求==== DeL 
1 - 账号必须要拥有2x经验通行证 
2 - lvl1-500 要有rod of the depth(深渊杆) + clever(聪明)附魔 
3 - lvl500-1000 要有nolife + clever(聪明)附魔""")
    await ctx.message.delete()

# Run the bot using the token from Railway secrets
bot.run(os.getenv("DISCORD_TOKEN"))
