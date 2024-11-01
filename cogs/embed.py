import discord
from discord import app_commands
from discord.ext import commands
from discord import Color
from bot import MyBot


class EmbedCog(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.reset_embed_data()

    def reset_embed_data(self):
        """Reset the embed data to default values."""
        self.embed_data = {
            "title": "Title",
            "description": "Description",
            "color": 0xFFFFFF,
            "footer_message": "Footer Message",
            "image": "https://cdn.discordapp.com/attachments/853174868551532564/860462053063393280/embed_image.png?ex=671f62bc&is=671e113c&hm=3300b3cdb691362c13ebc441ea32fb71af28aad9bca49dc1355f5bb786dbf3c4&",
            "thumbnail": "https://cdn.discordapp.com/attachments/853174868551532564/860464565338898472/embed_thumbnail.png?ex=671f6513&is=671e1393&hm=440f2884c11cebdfbcb7201d478e4b1040fffb9686ef5855a9cc45f853f2834e&",
            "footer": "https://cdn.discordapp.com/attachments/853174868551532564/860464565338898472/embed_thumbnail.png?ex=671f6513&is=671e1393&hm=440f2884c11cebdfbcb7201d478e4b1040fffb9686ef5855a9cc45f853f2834e&",
        }

    @app_commands.command(
        name="embed", description="Generate and send embed to specific channel."
    )
    async def create_embed(
        self, interaction: discord.Interaction, channel: discord.channel.TextChannel
    ):
        try:
            embed = discord.Embed(
                title=self.embed_data["title"],
                description=self.embed_data["description"],
                color=self.embed_data["color"],
            )
            embed.set_image(
                url=self.embed_data["image"],
            )
            embed.set_footer(
                text=self.embed_data["footer_message"],
                icon_url=self.embed_data["footer"],
            )
            embed.set_thumbnail(
                url=self.embed_data["thumbnail"],
            )
            await interaction.response.defer(thinking=True)
            dropdown = EmbedDropDown(self.bot, self.embed_data)
            view = EmbedDropDownView(self.bot, dropdown, channel, embed)
            message = await interaction.followup.send(
                embed=embed, view=view, ephemeral=True
            )

            def check(m):
                return m.channel == interaction.channel and m.author != self.bot.user

            await self.bot.wait_for("message", check=check)
            for item in view.children:
                item.disabled = True
            await message.edit(view=view)

        except Exception as e:
            await interaction.followup.send(e, ephemeral=True)


class EmbedDropDown(discord.ui.Select):
    def __init__(self, bot, embed_data):
        options = [
            discord.SelectOption(
                label="Edit Message (Title, Description, Footer)",
                emoji="<:plus:1300160705168801832>",
                description="Edit your embed title, description, and footer",
                value=0,
            ),
            discord.SelectOption(
                label="Edit Thumbnail Image",
                emoji="🖼️",
                description="Small image on the right side of embed",
                value=1,
            ),
            discord.SelectOption(
                label="Edit Main Image",
                emoji="🖼️",
                description="Edit your embed image",
                value=2,
            ),
            discord.SelectOption(
                label="Edit Footer Icon",
                emoji="🖌️",
                description="Small icon near footer message",
                value=3,
            ),
            discord.SelectOption(
                label="Edit Embed Color",
                emoji="⚪",
                description="Change the color of the embed",
                value=4,
            ),
        ]
        super().__init__(
            placeholder="Select an option to design the message", options=options
        )
        self.bot = bot
        self.embed_data = embed_data

    async def callback(self, interaction: discord.Interaction):

        selected_value = int(self.values[0])
        title = ""
        if selected_value == 0:
            title = "Set Embed Message"
        elif selected_value == 1:
            title = "Edit Thumbnail Image"
        elif selected_value == 2:
            title = "Edit Main Image"
        elif selected_value == 3:
            title = "Edit Footer Icon"
        elif selected_value == 4:
            title = "Set Embed Color"

        modal = EmbedModal(
            bot=self.bot,
            embed_data=self.embed_data,
            option_value=selected_value,
            title=title,
            view=self.view,
        )
        await interaction.response.send_modal(modal)


class EmbedDropDownView(discord.ui.View):
    def __init__(
        self,
        bot: MyBot,
        dropdown: discord.ui.Select,
        channel: discord.TextChannel,
        embed: discord.Embed,
    ):
        super().__init__(timeout=60.0)
        self.bot = bot
        self.add_item(dropdown)
        self.channel = channel
        self.embed = embed

        # Add buttons
        self.add_item(SendButton(channel))
        self.add_item(CancelButton())


class SendButton(discord.ui.Button):
    def __init__(self, channel):
        super().__init__(
            label=f"Send to #{channel.name}",
            style=discord.ButtonStyle.green,
        )
        self.channel = channel

    async def callback(self, interaction: discord.Interaction):
        message = await self.channel.send(embed=self.view.embed)
        jump_url = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        await interaction.response.send_message(
            f"<:green_tick:1300171482491781280> | Embed was sent to {self.channel.mention} ([Jump URL]({jump_url}))",
            ephemeral=True,
        )

        # Reset embed data to default values after sending
        self.view.bot.get_cog("EmbedCog").reset_embed_data()

        for item in self.view.children:
            item.disabled = True
        await interaction.message.edit(view=self.view)


class CancelButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Cancel", style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        # Notify user of cancellation
        await interaction.response.send_message(
            "<:red_tick:1300171587944976426> | Embed sending cancelled.", ephemeral=True
        )
        # Disable all components after canceling
        for item in self.view.children:
            item.disabled = True
        await interaction.message.edit(view=self.view)


class EmbedModal(discord.ui.Modal):
    def __init__(self, bot, embed_data, option_value, title, view):
        super().__init__(title=title)
        self.bot = bot
        self.embed_data = embed_data
        self.option_value = option_value
        self.view = view

        if self.option_value == 0:
            self.add_item(
                discord.ui.TextInput(
                    label="Title",
                    placeholder="Enter text for title of embed here...",
                    default=self.embed_data["title"],
                    required=False,
                )
            )
            self.add_item(
                discord.ui.TextInput(
                    label="Description",
                    placeholder="Enter text for description of embed here...",
                    default=self.embed_data["description"],
                    required=False,
                    max_length=4000,
                    style=discord.TextStyle.paragraph,
                )
            )
            self.add_item(
                discord.ui.TextInput(
                    label="Footer Text",
                    placeholder="Enter text for footer of embed here...",
                    default=self.embed_data["footer_message"],
                    required=False,
                )
            )
        elif self.option_value == 1:
            self.add_item(
                discord.ui.TextInput(
                    label="Enter Imgae Url (Optional)",
                    placeholder="Leave empty to remove image...",
                    default=self.embed_data["thumbnail"],
                    required=False,
                )
            )
        elif self.option_value == 2:
            self.add_item(
                discord.ui.TextInput(
                    label="Enter Imgae Url (Optional)",
                    placeholder="Leave empty to remove image...",
                    default=self.embed_data["image"],
                    required=False,
                )
            )
        elif self.option_value == 3:
            self.add_item(
                discord.ui.TextInput(
                    label="Enter Imgae Url (Optional)",
                    placeholder="Leave empty to remove image...",
                    default=self.embed_data["footer"],
                    required=False,
                )
            )
        elif self.option_value == 4:
            self.add_item(
                discord.ui.TextInput(
                    label="Embed Color",
                    placeholder="Examples: red, green, blue, #ffffff etc.",
                    required=False,
                )
            )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            # Update the embed_data based on user input
            if self.option_value == 0:
                self.embed_data["title"] = self.children[0].value
                self.embed_data["description"] = self.children[1].value
                self.embed_data["footer_message"] = self.children[2].value
            elif self.option_value == 1:
                self.embed_data["thumbnail"] = self.children[0].value
            elif self.option_value == 2:
                self.embed_data["image"] = self.children[0].value
            elif self.option_value == 3:
                self.embed_data["footer"] = self.children[0].value
            elif self.option_value == 4:
                color_value = self.children[0].value
                # try:
                #     if color_value.count("#"):
                #         self.embed_data["color"] = color_value
                #     else:
                #         # Try to convert the color value to a hex integer
                #         self.embed_data["color"] = int(color_value.lstrip("#"), 16)
                # except ValueError:
                #     await interaction.followup.send(
                #         "Invalid color format.", ephemeral=True
                #     )
                #     return
                try:
                    color_value = self.children[0].value.strip()  # Get the color input

                    # Check if the color is a name recognized by discord.Color
                    if hasattr(Color, color_value.lower()):
                        self.embed_data["color"] = getattr(
                            Color, color_value.lower()
                        )().value
                    else:
                        # If not, attempt to parse it as a hex color
                        self.embed_data["color"] = int(color_value.lstrip("#"), 16)

                except ValueError:
                    await interaction.followup.send(
                        "Invalid color format. Please use a valid color name or hex code.",
                        ephemeral=True,
                    )
                    return

            # Update the embed with the new data
            embed = discord.Embed(
                title=self.embed_data["title"],
                description=self.embed_data["description"],
                color=self.embed_data["color"],
            )
            embed.set_image(url=self.embed_data["image"])
            embed.set_footer(
                text=self.embed_data["footer_message"],
                icon_url=self.embed_data["footer"],
            )
            embed.set_thumbnail(url=self.embed_data["thumbnail"])

            self.view.embed = embed
            # Edit the message with the updated embed
            await interaction.message.edit(embed=embed)

        except Exception as e:
            await interaction.followup.send(e, ephemeral=True)


async def setup(bot: MyBot):
    await bot.add_cog(EmbedCog(bot))
