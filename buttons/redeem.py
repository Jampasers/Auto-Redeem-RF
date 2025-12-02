import discord
from modals.redeem import RedeemModal

class RedeemButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Redeem",
            style=discord.ButtonStyle.primary,
            custom_id="redeem_button",
            row=0,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RedeemModal)
