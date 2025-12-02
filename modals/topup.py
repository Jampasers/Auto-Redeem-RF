import discord
import os
import sqlite3

class RedeemModal(discord.ui.Modal, title="🎟 Redeem Code"):
    amount = discord.ui.TextInput(
        label="Amount",
        placeholder="Minimal 2000",
        min_length=3,
        max_length=64,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        amount = self.amount.value
        if not isinstance(amount, (int, float)): 
            return await interaction.response.send_message("Amount must be a number", ephemeral=True)

    async def on_error(self, error: Exception, interaction: discord.Interaction):
        await interaction.response.send_message(
            "An error occured",
            ephemeral=True
        )
        print(f"[MODAL ERROR] {type(error).__name__}: {error}")
