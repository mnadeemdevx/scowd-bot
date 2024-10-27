import discord
from discord.ext import commands
from discord import app_commands
from utils.captcha import generate_captcha
from bot import MyBot


class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.captcha_dict = {}

    @app_commands.command(
        name="verification-message",
        description="Sends a verification embed!",
    )
    async def send_verification(
        self, interation: discord.Interaction, title: str, description: str
    ):
        embed = discord.Embed(title=title, description=description, color=0xFFFFFF)
        view = VerificationView(self.bot)

        await interation.response.send_message(embed=embed, view=view)


class VerificationView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.primary)
    async def verify_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.handle_verification(interaction)

    async def handle_verification(self, interaction: discord.Interaction):
        user = interaction.user
        captcha_text, captcha_image = generate_captcha()
        interaction.client.captcha_dict[user.id] = captcha_text

        captcha_file = discord.File(captcha_image, filename="captcha.png")
        embed = discord.Embed(
            title="Captcha Verification",
            description="Remember the characters and click **Solve** to enter them.",
            color=0xFFFFFF,
        ).set_image(url="attachment://captcha.png")

        view = CaptchaView(self.bot)
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(
            embed=embed, view=view, file=captcha_file, ephemeral=True
        )


class CaptchaView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="Solve", style=discord.ButtonStyle.gray, emoji="✏️")
    async def solve_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        modal = SolveModalInfo(self.bot)
        modal.add_item(
            discord.ui.TextInput(
                label="TYPE BACK THE CHARACTER BELOW:", placeholder="Captcha value"
            )
        )
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Reload", style=discord.ButtonStyle.gray, emoji="🔄")
    async def reload_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer(ephemeral=True)
        captcha_text, captcha_image = generate_captcha()
        interaction.client.captcha_dict[interaction.user.id] = captcha_text

        captcha_file = discord.File(captcha_image, filename="captcha.png")
        new_embed = discord.Embed(
            title="Captcha Verification",
            description="Remember the characters and click **Solve** to enter them.",
            color=0xFFFFFF,
        ).set_image(url="attachment://captcha.png")

        await interaction.edit_original_response(
            embed=new_embed, attachments=[captcha_file]
        )


class SolveModalInfo(discord.ui.Modal, title="Verify Captcha"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        captcha_value = self.children[0].value
        verified_role = discord.utils.get(guild.roles, name="verified")

        if captcha_value == interaction.client.captcha_dict.get(user.id):
            try:
                if not verified_role:
                    verified_role = await guild.create_role(
                        name="verified", color=discord.Color.green()
                    )
                await user.add_roles(verified_role)
                await interaction.response.defer(thinking=True, ephemeral=True)
                await interaction.followup.send(
                    f":white_check_mark: Thanks! You have obtained the {verified_role.mention} role and you can now access the rest of the channels!!",
                    ephemeral=True,
                )

            except discord.Forbidden:
                await interaction.followup.send(
                    "I don't have permission to assign this role.", ephemeral=True
                )

            except discord.HTTPException:
                await interaction.followup.send(
                    "There was an error assigning the role. Please try again later.",
                    ephemeral=True,
                )
        else:
            await interaction.response.send_message(
                "❌ Invalid captcha, please try again.", ephemeral=True
            )


async def setup(bot: MyBot):
    await bot.add_cog(VerificationCog(bot))
