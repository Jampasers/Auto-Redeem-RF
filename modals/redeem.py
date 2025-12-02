import discord
import os
import sqlite3

class RedeemModal(discord.ui.Modal, title="🎟 Redeem Code"):
    email = discord.ui.TextInput(
        label="Your redfinger email",
        placeholder="awokawok@gmail.com",
        min_length=3,
        max_length=64,
        required=True,
    )
    password = discord.ui.TextInput(
        label="Your redfinger password",
        placeholder="Awokawok",
        min_length=3,
        max_length=64,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        conn = sqlite3.connect("redeem.db")
        cursor = conn.cursor()
        guild = interaction.guild
        category = guild.get_channel(os.getenv("REDEEM_CATEGORY_ID"))

        if category is None or not isinstance(category, discord.CategoryChannel):
            return await interaction.response.send_message("Wrong category ID", ephemeral=True)

        channel = await category.create_text_channel(f'{interaction.user.name}-redeem')
        cursor.execute("""
            INSERT INTO redeems (channel_id, user_id, email, password) VALUES (?,?,?,?)
        """, [channel.id, interaction.user.id, self.email.value, self.password.value])

        await interaction.response.send_message(f'Channel created at {channel.mention}')
        # channel = await interaction.guild.create_text_channel(f'{interaction.user.name}-redeem', category=await discord.utils.get(interaction.guild.categories, ))

    async def on_error(self, error: Exception, interaction: discord.Interaction):
        await interaction.response.send_message(
            "An error occured",
            ephemeral=True
        )
        print(f"[MODAL ERROR] {type(error).__name__}: {error}")
