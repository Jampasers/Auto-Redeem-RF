import discord
import os
import sqlite3
from functions.generate_qris import generate_qr_image
from functions.saweria import saweria_qris

class RedeemModal(discord.ui.Modal, title="🎟 Redeem Code"):
    amount = discord.ui.TextInput(
        label="Amount",
        placeholder="Minimal 2000",
        min_length=3,
        max_length=64,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        interaction.response.defer(ephemeral=True)
        amount = self.amount.value
        if not isinstance(amount, (int, float)): 
            return await interaction.response.edit_message("Amount must be a number")

        qris_data = saweria_qris(interaction.user.id, f"Ini Ada {amount}", amount)

        if qris_data:
            file_path = generate_qr_image(qris_data["data"]["qr_string"], "qris.png")

            file = discord.File(file_path, filename="qris.png")

            embed = discord.Embed(
                title="QRIS Bayar",
                description=f"Jumlah: Rp {amount:,}\nScan untuk membayar.",
                color=discord.Color.random()
            )

            interaction.user.send(embed=embed, file=file)
            interaction.response.edit_message("QRIS send trough your dm.")

    async def on_error(self, error: Exception, interaction: discord.Interaction):
        await interaction.response.edit_message(
            "An error occured",
            ephemeral=True
        )
        print(f"[MODAL ERROR] {type(error).__name__}: {error}")
