import discord
from datetime import datetime


def create_log_embed(before, after, action):

    embed = discord.Embed(timestamp=datetime.now())
    if before.author:
        author_name = before.author.display_name
        author_avatar = before.author.avatar.url if before.author.avatar else None
        embed.set_author(name=author_name, icon_url=author_avatar)
    embed.set_footer(text=before.guild.name)

    if action == "edit":
        embed.description = f"**:pencil2: Message by {before.author.mention} edited in {before.channel.mention}.** [Jump to Message](https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id})"
        embed.add_field(name="Old", value=f"```{before.content}```", inline=False)
        embed.add_field(name="New", value=f"```{after.content}```", inline=False)
    else:
        embed.description = f"**:wastebasket: Message by {before.author.mention} deleted in {before.channel.mention}.**"
        embed.add_field(
            name="Deleted Message", value=f"```{before.content}```", inline=False
        )

    return embed


def create_captcha_embed():
    embed = discord.Embed(
        title="Captcha Verification", description="Solve the captcha below."
    )
    return embed
