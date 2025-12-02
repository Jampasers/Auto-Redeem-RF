from discord.ext import commands
import os

class Redeem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="redeem", description="Show auto redeem panel", guild_only=True,guild_ids=os.getenv("GUILD_ID").split(","))
    @commands.has_any_role(1445321100555718707)
    async def redeem(self, ctx: commands.Context):
        print("Sek")
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Redeem(bot))