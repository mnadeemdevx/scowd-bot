import discord
from discord.ext import commands
from datetime import datetime
from utils.embed import create_log_embed
from bot import MyBot


class LoggingCog(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.LOGGING_CHANNELS = {
            1069495495568916480: 1296823358129705093,
            1106614144427368558: 1296796473022746634,
        }

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.guild or before.author.bot:
            return
        await self.log_message(before.guild.id, create_log_embed(before, after, "edit"))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild or message.author.bot:
            return
        await self.log_message(
            message.guild.id, create_log_embed(message, None, "delete")
        )

    async def log_message(self, guild_id, embed):
        logging_channel_id = self.LOGGING_CHANNELS.get(guild_id)
        if logging_channel_id:
            logging_channel = self.bot.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(embed=embed)


async def setup(bot: MyBot):
    await bot.add_cog(LoggingCog(bot))
