import discord
from discord.ext import commands
from discord import app_commands
from bot import MyBot


class Dev(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot

    @app_commands.command(name="tree")
    async def tree(self, interaction: discord.Interaction):
        """Developer command"""
        if interaction.user.id != self.bot.owner_id:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
            return
        try:
            synced = await self.bot.tree.sync()
            print(f"Synced {len(synced)} commands.")
            await interaction.response.send_message("Tree synced !!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred: {e}", ephemeral=True
            )


async def setup(bot: MyBot):
    await bot.add_cog(Dev(bot))
