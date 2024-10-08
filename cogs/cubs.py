import json
from discord.ext import commands
from utility.embedconfig import EmbedClass
from utility.nickname_checker import check_nickname
from utility.cub_dropdown import CUBDropdownView
from utility.fuzzymatch import fuzzmatch

class CUBs(commands.Cog):
    cubs = {}

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embedconf = EmbedClass()

        with open('data/cubs.json') as file:
            self.cubs = json.load(file)

    @commands.Cog.listener()
    async def on_ready(self):
        print('CUBs loaded.')

    @commands.hybrid_command(aliases=['CUB', 'Cub', 'pet'], description="Displays information about a particular CUB.")
    async def cub(self, ctx: commands.Context, *, cub_name) -> None:
        name = fuzzmatch(cub_name)
        if name == "":
            name = cub_name.lower()
        cub_name = check_nickname(name, "cub")

        cub = self.cubs.get(cub_name)
        if cub is None:
            await ctx.send(content=f"{cub_name} is not a valid CUB name. Please try again.")
            return

        view = CUBDropdownView(ctx.author, cub=cub)
        embed = self.embedconf.create_cub_embed(cub, "active")
        view.message = await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(CUBs(bot))
