import discord
from discord.ext import commands
from sys import argv

class Rules:
    """
    Read da rules.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command()
    async def pirate(self):
        """Hey! You can't steal another trainer's Pokémon!"""
        await self.bot.say("Please refrain from asking for or giving assistance with installing or using illegitimately obtained software.")

    @commands.command()
    async def rules(self):
       """Links to rules website."""
       await self.bot.say("Please check {} for a full list of rules".format(self.bot.welcome_channel.mention))

    @commands.command(hidden=True)
    async def r1(self):
       """Displays rule one."""
       await self.bot.say("```1. Keep all discussion and conduct civil.```")

    @commands.command(hidden=True)
    async def r2(self):
       """Displays rule two."""
       await self.bot.say("```2. Don't link - or ask someone to link - to copyrighted, pirated or illegal content. This includes pirated games, leaked SDKs, and certain two word subreddits that start with a V and a P.```")

    @commands.command(hidden=True)
    async def r3(self):
       """Displays rule three."""
       await self.bot.say("```3. Use each channel for its designated purpose (e.g. #help-and-questions for support, #hacking-general for Vita hacks, #dev for Vita development, #off-topic for random discussion, #psn-ids for sharing PSN IDs)```")

    @commands.command(hidden=True)
    async def r4(self):
       """Displays rule four."""
       await self.bot.say("```4. Brigading another service or server is not acceptable behaviour.```")

    @commands.command(hidden=True)
    async def r5(self):
       """Displays rule five."""
       await self.bot.say("```5. Attempting to stay borderline within the rules is considered breaking the rules. ```")
       
    @commands.command(hidden=True)
    async def r6(self):
       """Displays rule six."""
       await self.bot.say("```6. Pornographic, lewd, or NSFW content is strictly prohibited.```")
       
    @commands.command(hidden=True)
    async def r7(self):
       """Displays rule seven."""
       await self.bot.say("```7. Please keep the #news channel only for link posting, no discussion there.```")


def setup(bot):
    bot.add_cog(Rules(bot))
