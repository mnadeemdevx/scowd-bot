import discord
from datetime import datetime


def create_log_embed(before, after, action):

    embed = discord.Embed(color=0xFFFFFF, timestamp=datetime.now())
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


def create_custom_embed():
    embed = discord.Embed(
        title="Title",
        description="Description",
        color=0xFFFFFF,
    )
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/853174868551532564/860462053063393280/embed_image.png?ex=671f62bc&is=671e113c&hm=3300b3cdb691362c13ebc441ea32fb71af28aad9bca49dc1355f5bb786dbf3c4&"
    )
    embed.set_footer(
        text="Footer Message",
        icon_url="https://cdn.discordapp.com/attachments/853174868551532564/860464565338898472/embed_thumbnail.png?ex=671f6513&is=671e1393&hm=440f2884c11cebdfbcb7201d478e4b1040fffb9686ef5855a9cc45f853f2834e&",
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/853174868551532564/860464565338898472/embed_thumbnail.png?ex=671f6513&is=671e1393&hm=440f2884c11cebdfbcb7201d478e4b1040fffb9686ef5855a9cc45f853f2834e&"
    )

    return embed
