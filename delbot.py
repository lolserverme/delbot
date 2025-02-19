import discord
import os
import math
import asyncio
from discord.ext import commands

# Enable bot intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.members = True  # Enable member-related intents (for role management)

# Set up bot command prefix
bot = commands.Bot(command_prefix="?", intents=intents)

# Price calculation function
def calculate_price(start_level, end_level):
    if start_level < 1 or end_level > 1000 or start_level >= end_level:
        return "\u8f93\u5165\u7684\u7b49\u7ea7\u8303\u56f4\u65e0\u6548，\u8bf7\u68c0\u67e5\u540e\u91cd\u65b0\u8f93\u5165！"
    
    total_price = 0
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

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! 👋 I'm DeL's Helper!")

@bot.command()
@commands.has_permissions(administrator=True)
async def tng(ctx):
    image_url = "https://raw.githubusercontent.com/lolserverme/delbot/main/TNG.jpg"
    await ctx.send(image_url)
    await ctx.message.delete()

@bot.command()
async def twd(ctx, number: float):
    result = number * 8.5
    await ctx.send(f"RM{number} x 8.5 = {result}台币")

@bot.command()
async def cal(ctx, start_level: int, end_level: int):
    price_rm = calculate_price(start_level, end_level)
    if isinstance(price_rm, str):
        await ctx.send(price_rm)
    else:
        price_twd = math.ceil(price_rm * 8.5)
        await ctx.send(f"代刷从等级 {start_level} 到等级 {end_level} 的总价格是: RM {price_rm} (台币 {price_twd})")

@bot.command()
@commands.has_permissions(administrator=True)  # Only admins can access this command
async def id(ctx):
    await ctx.send("""代刷 - DeL
名字/id = 
密码/pass = 
!! 随时准备给验证码哦""")
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)  # Only admins can access this command
async def req(ctx):
    await ctx.send("""====代刷等级需求==== DeL 
1 - 账号必须要拥有2x经验通行证 
2 - lvl1-500 要有rod of the depth(深渊杆) + clever(聪明)附魔 
3 - lvl500-1000 要有nolife + clever(聪明)附魔""")
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(manage_channels=True)
@commands.cooldown(1, 10, commands.BucketType.channel)  # 1 use per 10 seconds per channel
async def paid(ctx, amount: str, *, text: str = ""):
    try:
        amount = amount.replace(",", "").strip()  # Remove commas and extra spaces
        amount = float(amount)  # Convert to float
        
        await asyncio.sleep(1)  # Small delay to avoid immediate rate limit
        formatted_amount = int(amount) if amount.is_integer() else amount
        new_name = f"paid - {formatted_amount} {text}".strip()
        
        await ctx.channel.edit(name=new_name)
        await ctx.send(f"✅ 频道名称已更改为: {new_name}")
    
    except ValueError:
        await ctx.send("⚠️ 请输入有效的数字作为金额！")
    except discord.Forbidden:
        await ctx.send("⚠️ 我没有权限更改频道名称！")
    except discord.HTTPException:
        await ctx.send("⚠️ 发生错误，无法更改频道名称！")
    
    await ctx.message.delete()
# Load or initialize balances
def load_balances():
    try:
        with open("balances.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_balances():
    with open("balances.json", "w") as f:
        json.dump(balances, f, indent=4)

balances = load_balances()

# Command to add balance
@bot.command()
@commands.has_permissions(administrator=True)
async def add(ctx, amount: float, member: discord.Member):
    user_id = str(member.id)
    
    if user_id not in balances:
        balances[user_id] = 0
    
    balances[user_id] += amount
    save_balances()
    await ctx.send(f"✅ {member.mention} 的余额增加了 RM {amount}. 当前余额: RM {balances[user_id]}")

# Command to check balance
@bot.command()
async def balance(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    user_id = str(member.id)
    balance = balances.get(user_id, 0)
    await ctx.send(f"💰 {member.mention} 的当前余额: RM {balance}")

# Command to deduct balance
@bot.command()
@commands.has_permissions(administrator=True)
async def deduct(ctx, amount: float, member: discord.Member):
    user_id = str(member.id)
    
    if user_id not in balances or balances[user_id] < amount:
        await ctx.send(f"⚠️ {member.mention} 的余额不足！")
        return
    
    balances[user_id] -= amount
    save_balances()
    await ctx.send(f"✅ {member.mention} 的余额减少了 RM {amount}. 当前余额: RM {balances[user_id]}")
    
# New Command: "?done @mention"
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

    # Process and send the image that was uploaded
    image_file = await image.to_file()
    await ctx.send(file=image_file)

    # Delete the command message
    await ctx.message.delete()

# New Command: "?doneds @mention" (same behavior as ?done)
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

    # Process and send the image that was uploaded
    image_file = await image.to_file()
    await ctx.send(file=image_file)

    # Delete the command message
    await ctx.message.delete()

bot.run(os.getenv("DISCORD_TOKEN"))
