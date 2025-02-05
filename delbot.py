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
    image_path = "https://raw.githubusercontent.com/lolserverme/delbot/main/TNG.jpg"  # Replace with the name of your uploaded image
    if os.path.exists(image_path):
        await ctx.send(file=discord.File(image_path))
    else:
        pass

    # Delete the command message
    await ctx.message.delete()

# New Command: "?myr <number>" multiplies the number by 8.5
@bot.command()
async def twd(ctx, number: float):
    result = number * 8.5
    await ctx.send(f"RM{number} x 8.5 = {result}台币")

# New Command: "?done @mention" gives a specific role to the mentioned user, sends a confirmation message and an image (restricted to admins)
@bot.command()
@commands.has_permissions(administrator=True)  # Restrict to admins
async def done(ctx, member: discord.Member, image: discord.Attachment):
    # Role name you want to assign to the mentioned user
    role_name = "Buyer买家"  # Replace with the role name you want to assign

    # Get the role object by name
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    # Check if the role exists
    if not role:
        await ctx.send(f"⚠️ Role '{role_name}' not found!")
        return

    # Assign the role to the mentioned user
    await member.add_roles(role)

    # Send confirmation message
    await ctx.send(f"已经购买通行证/代送了 {member.mention},\n 您已获取 '{role_name}' 称号，请到 https://discord.com/channels/1320960342318387292/1335820101437624414 vouch @DeL .")

    # Send the image that was uploaded
    await ctx.send(f"{image.url}")

    # Delete the command message
    await ctx.message.delete()

# New Command: "?doneds @mention" (same behavior as ?done, but for different use)
@bot.command()
@commands.has_permissions(administrator=True)  # Restrict to admins
async def doneds(ctx, member: discord.Member, image: discord.Attachment):
    # Role name you want to assign to the mentioned user (you can change this role name)
    role_name = "Buyer买家"  # Replace with the role name for this use case

    # Get the role object by name
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    # Check if the role exists
    if not role:
        await ctx.send(f"⚠️ Role '{role_name}' not found!")
        return

    # Assign the role to the mentioned user
    await member.add_roles(role)

    # Send confirmation message
    await ctx.send(f"已经完成代刷了，现在可以登录账号查看了 {member.mention}，\n您已获取 '{role_name}' 称号，请到 https://discord.com/channels/1320960342318387292/1335820101437624414 vouch @DeL .")

    # Send the image that was uploaded
    await ctx.send(f"{image.url}")

    # Delete the command message
    await ctx.message.delete()

# New Command: "?cal (start level) - (end level)" calculates the price for leveling and shows both RM and TWD prices
@bot.command()
async def cal(ctx, start_level: int, end_level: int):
    # Calculate price using the function
    price_rm = calculate_price(start_level, end_level)

    # If the result is a string (error message)
    if isinstance(price_rm, str):
        await ctx.send(price_rm)
    else:
        # Calculate TWD price and round to the nearest whole number (after RM calculation)
        price_twd = math.ceil(price_rm * 8.5)
        await ctx.send(f"代刷从等级 {start_level} 到等级 {end_level} 的总价格是: RM {price_rm} (台币 {price_twd})")

# Run the bot using the token from Replit secrets
bot.run(os.getenv("DISCORD_TOKEN"))
