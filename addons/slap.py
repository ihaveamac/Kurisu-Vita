# slap.py
# Slap a user

import discord
from discord.ext import commands
from sys import argv

class Slap:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def slap(self, ctx):
        author = ctx.message.author
        target = ctx.message.mentions[0]

        if author.user == self.bot.user:
            await self.bot.say("Nice try, " + author.display_name + ".")
        elif author.display_name == target.display_name:
            await self.bot.say("You have slapped yourself. Good job, " + author.display_name + " :ok_hand:")
        else:
            await self.bot.say(target.mention + " has been slapped by " + author.display_name + "!")
        

def setup(bot):
    bot.add_cog(Slap(bot))
