@bot.command()
@commands.has_permissions(administrator=True)
async def done(ctx, member: discord.Member):
    role_name = "Buyer买家"
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if not role:
        await ctx.send(f"⚠️ Role '{role_name}' not found!")
        return

    await member.add_roles(role)
    await ctx.send(f"已经购买通行证/代送了 {member.mention},\n您已获取 '{role_name}' 称号，请到 https://discord.com/channels/1320960342318387292/1335820101437624414 vouch @DeL .")

    # Check if an image is attached
    if ctx.message.attachments:
        image_url = ctx.message.attachments[0].url  # Get first attachment
        await ctx.send(image_url)

    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def doneds(ctx, member: discord.Member):
    role_name = "Buyer买家"
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if not role:
        await ctx.send(f"⚠️ Role '{role_name}' not found!")
        return

    await member.add_roles(role)
    await ctx.send(f"已经完成代刷了，现在可以登录账号查看了 {member.mention}，\n您已获取 '{role_name}' 称号，请到 https://discord.com/channels/1320960342318387292/1335820101437624414 vouch @DeL .")

    # Check if an image is attached
    if ctx.message.attachments:
        image_url = ctx.message.attachments[0].url  # Get first attachment
        await ctx.send(image_url)

    await ctx.message.delete()
