import discord
from discord.ext import commands
from sys import argv

class Assistance:
    """
    Commands that will mostly be used in #help-and-questions.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def simple_embed(self, text, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = text
        await self.bot.say("", embed=embed)

    @commands.command(pass_context=True, name="sr", hidden=True)
    async def staffreq(self, ctx, *, msg_request=""):
        """Request staff, with optional additional text. Staff only."""
        author = ctx.message.author
        if (self.bot.helpers_role not in author.roles) and (self.bot.staff_role not in author.roles) and (self.bot.verified_role not in author.roles) and (self.bot.trusted_role not in author.roles):
            msg = "{0} You cannot used this command at this time. Please ask individual staff members if you need help.".format(author.mention)
            await self.bot.say(msg)
            return
        await self.bot.delete_message(ctx.message)
        # await self.bot.say("Request sent.")
        msg = "❗️ **Assistance requested**: {0} by {1} | {2}#{3} @here".format(ctx.message.channel.mention, author.mention, author.name, ctx.message.author.discriminator)
        if msg_request != "":
            # msg += "\n✏️ __Additional text__: " + msg_request
            embed = discord.Embed(color=discord.Color.gold())
            embed.description = msg_request
        await self.bot.send_message(self.bot.mods_channel, msg, embed=(embed if msg_request != "" else None))
        await self.bot.send_message(author, "✅ Online staff has been notified of your request in {0}.".format(ctx.message.channel.mention), embed=(embed if msg_request != "" else None))

    @commands.command(pass_context=True)
    async def guide(self, ctx, *, console="auto"):
        """Links to Plailect's or FlimFlam69's guide."""
        console == console.lower()
        if console == "vita" or (console == "auto" and "wiiu" not in ctx.message.channel.name):
            embed = discord.Embed(title="Guide", color=discord.Color(0xCE181E))
            embed.set_author(name="Yifan Lu", url="https://henkaku.xyz/")
            embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/698944593715310592/wTDlD5rA_400x400.png")
            embed.url = "https://vita.hacks.guide/"
            embed.description = "Plailect's guide for hacking your PS Vita or PSTV."
            await self.bot.say("", embed=embed)


    @commands.command()
    async def update(self):
        """Explains to not update"""
        await self.simple_embed("Updating to the latest system firmware may potentially cause your console to become unhackable in the future. Spoofing the latest firmware in HENkaku Settings is recommended to avoid accidental updates.")


    @commands.command()
    async def downgrade(self):
        """Downgrade help"""
        await self.simple_embed("You can downgrade as long as your system is currently hacked. However, you can't downgrade past the firmware your console came on from the factory.", title="Can I downgrade?")

    @commands.command()
    async def question(self):
        """Tells user to be descriptive"""
        await self.simple_embed("> Reminder: if you would like someone to help you, please be as descriptive as possible, of your situation, things you have done, as little as they may seem, aswell as assisting materials. Asking to ask wont expedite your process, and may delay assistance.")


def setup(bot):
    bot.add_cog(Assistance(bot))
