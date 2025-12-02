import discord
from modals.topup import TopupModal

class TopupButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Topup",
            style=discord.ButtonStyle.primary,
            custom_id="topup_button",
            row=0,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TopupModal)
