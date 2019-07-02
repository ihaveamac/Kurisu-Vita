import asyncio
import discord
import json
import re
from discord.ext import commands
from subprocess import call
from string import printable
from sys import argv

class Events:
    """
    Special event handling.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    # don't add spaces or dashes to words
    piracy_tools = [
        'freeshop',
        'fr3eshop',
        'fr33shop',
        'fre3shop',
        'ciangel',
        'ciaangel',
        'tikdevil',
        'tikshop',
        'fr335h0p',
        'fr€€shop',
        'fr€€sh0p',
        'fr3esh0p',
        'fr//shop',
        'fr//sh0p',
        'free$hop',
        'fr$$hop',
        'friishop',
        'fr££shop',
        'fr£€shop',
        'fr£shop',
        'fr£eshop',
        'fre£shop',
        'fr€£shop',
        'threeshop',
        'thr33shop',
        'thr££shop',
        'thr£eshop',
        'thr33shop',
        'fr33sh0p',
        'freshop',
        'fresh0p',
        'fr$shop',
        'pkgi',
        'pkgj',
        'pkjl',
        'pckgj',
        'pckgl',
        'pckgi',
        'rvitapiracy',
        'r/vitapiracy',
        'npsbrowser',
        'nopaybrowser',
        'npbrowser',
        'npsstore',
        'npstore',
        'nopaystore',
        'npsshop',
        'npshop',
        'nopayshop'
        'yespaystation',
        'nopaystation',
        'titlekeys',
    ]

    # I hate naming variables sometimes
    user_antispam = {}
    channel_antispam = {}

    async def add_restriction(self, member, rst):
        with open("data/restrictions.json", "r") as f:
            rsts = json.load(f)
        if member.id not in rsts:
            rsts[member.id] = []
        if rst not in rsts[member.id]:
            rsts[member.id].append(rst)
        with open("data/restrictions.json", "w") as f:
            json.dump(rsts, f)

    async def scan_message(self, message):
        embed = discord.Embed()
        embed.description = message.content
        if message.author.id in self.bot.watching:
            await self.bot.send_message(self.bot.messagelogs_channel, "**Watch log**: {} in {}".format(message.author.mention, message.channel.mention), embed=embed)
        is_help_channel = message.channel.name[0:5] == "help-"
        msg = ''.join(char for char in message.content.lower() if char in printable)
        msg_no_separators = re.sub('[ -]', '', msg)
        contains_invite_link = "discordapp.com/invite" in msg or "discord.gg" in msg or "join.skype.com" in msg
        contains_piracy_site_mention = any(x in msg for x in ('3dsiso', '3dschaos'))
        contains_piracy_url_mention = any(x in msg for x in ('3ds.titlekeys', 'wiiu.titlekeys', 'titlekeys.com'))
        contains_piracy_tool_mention = any(x in msg_no_separators for x in self.piracy_tools)
        contains_piracy_site_mention_indirect = any(x in msg for x in ('iso site', 'chaos site'))
        # lazy attachment check, i've got to find a better way of doing this
        for f in message.attachments:
            if f["filename"][-4:] == ".exe" or f["filename"][-4:] == ".scr" or f["filename"][-4:] == ".com":
                embed2 = discord.Embed(description="Size: {}\nDownload: [{}]({})".format(f["size"], f["filename"], f["url"]))
                await self.bot.send_message(self.bot.modlogs_channel, "📎 **Attachment**: {} uploaded to {}".format(message.author.mention, message.channel.mention), embed=embed2)
        if contains_invite_link:
            await self.bot.send_message(self.bot.messagelogs_channel, "✉️ **Invite posted**: {} posted an invite link in {}\n------------------\n{}".format(message.author.mention, message.channel.mention, message.content))
        if contains_piracy_tool_mention:
            try:
                await self.bot.delete_message(message)
            except discord.errors.NotFound:
                pass
            try:
                await self.bot.send_message(message.author, "Please read {}. You cannot mention tools used for piracy, therefore your message was automatically deleted.".format(self.bot.welcome_channel.mention), embed=embed)
            except discord.errors.Forbidden:
                pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            await self.bot.send_message(self.bot.messagelogs_channel, "**Bad tool**: {} mentioned a piracy tool in {} (message deleted)".format(message.author.mention, message.channel.mention), embed=embed)
        if contains_piracy_site_mention or contains_piracy_url_mention:
            try:
                await self.bot.delete_message(message)
            except discord.errors.NotFound:
                pass
            try:
                await self.bot.send_message(message.author, "Please read {}. You cannot mention sites used for piracy directly, therefore your message was automatically deleted.".format(self.bot.welcome_channel.mention), embed=embed)
            except discord.errors.Forbidden:
                pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            await self.bot.send_message(self.bot.messagelogs_channel, "**Bad site**: {} mentioned a piracy site directly in {} (message deleted)".format(message.author.mention, message.channel.mention), embed=embed)
        elif contains_piracy_site_mention_indirect:
            if is_help_channel:
                try:
                    await self.bot.delete_message(message)
                except discord.errors.NotFound:
                    pass
                try:
                    await self.bot.send_message(message.author, "Please read {}. You cannot mention sites used for piracy in the help-and-questions channels directly or indirectly, therefore your message was automatically deleted.".format(self.bot.welcome_channel.mention), embed=embed)
                except discord.errors.Forbidden:
                    pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            await self.bot.send_message(self.bot.messagelogs_channel, "**Bad site**: {} mentioned a piracy site indirectly in {}{}".format(message.author.mention, message.channel.mention, " (message deleted)" if is_help_channel else ""), embed=embed)

    async def keyword_search(self, message):
        if "wiiu" in message.channel.name and "download" in message.content and "update" in message.content and "manag" in message.content:  # intentional typo in manage
            embed = discord.Embed(description="A failed update in Download Management does not mean there is an update and the system is trying to download it. This means your blocking method (DNS etc.) is working and the system can't check for an update.", color=discord.Color(0x009AC7))
            await self.bot.send_message(message.channel, message.author.mention, embed=embed)

    async def user_spam_check(self, message):
        if message.author.id not in self.user_antispam:
            self.user_antispam[message.author.id] = []
        self.user_antispam[message.author.id].append(message)
        if len(self.user_antispam[message.author.id]) == 6:  # it can trigger it multiple times if I use >. it can't skip to a number so this should work
            await self.bot.add_roles(message.author, self.bot.muted_role)
            await self.add_restriction(message.author, "Muted")
            msg_user = "You were automatically muted for sending too many messages in a short period of time!\n\nIf you believe this was done in error, send a direct message to one of the staff in {}.".format(self.bot.welcome_channel.mention)
            try:
                await self.bot.send_message(message.author, msg_user)
            except discord.errors.Forbidden:
                pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            log_msg = "🔇 **Auto-muted**: {} muted for spamming | {}#{}\n🗓 __Creation__: {}\n🏷 __User ID__: {}".format(message.author.mention, message.author.name, message.author.discriminator, message.author.created_at, message.author.id)
            embed = discord.Embed(title="Deleted messages", color=discord.Color.gold())
            msgs_to_delete = self.user_antispam[message.author.id][:]  # clone list so nothing is removed while going through it
            for msg in msgs_to_delete:
                embed.add_field(name="#"+msg.channel.name, value=msg.content)
            await self.bot.send_message(self.bot.modlogs_channel, log_msg, embed=embed)
            await self.bot.send_message(self.bot.mods_channel, log_msg + "\nSee {} for a list of deleted messages.".format(self.bot.modlogs_channel.mention))
            for msg in msgs_to_delete:
                try:
                    await self.bot.delete_message(msg)
                except discord.errors.NotFound:
                    pass  # don't fail if the message doesn't exist
        await asyncio.sleep(3)
        self.user_antispam[message.author.id].remove(message)
        try:
            if len(self.user_antispam[message.author.id]) == 0:
                self.user_antispam.pop(message.author.id)
        except KeyError:
            pass  # if the array doesn't exist, don't raise an error

    async def channel_spam_check(self, message):
        if message.channel.id not in self.channel_antispam:
            self.channel_antispam[message.channel.id] = []
        self.channel_antispam[message.channel.id].append(message)
        if len(self.channel_antispam[message.channel.id]) == 25:  # it can trigger it multiple times if I use >. it can't skip to a number so this should work
            overwrites_everyone = message.channel.overwrites_for(self.bot.everyone_role)
            overwrites_everyone.send_messages = False
            await self.bot.edit_channel_permissions(message.channel, self.bot.everyone_role, overwrites_everyone)
            msg_channel = "This channel has been automatically locked for spam. Please wait while staff review the situation."
            embed = discord.Embed(title="Deleted messages", color=discord.Color.gold())
            msgs_to_delete = self.user_antispam[message.author.id][:]  # clone list so nothing is removed while going through it
            for msg in msgs_to_delete:
                embed.add_field(name="@"+self.bot.escape_name(msg.author), value=msg.content)
            await self.bot.send_message(message.channel, msg_channel)
            log_msg = "🔒 **Auto-locked**: {} locked for spam".format(message.channel.mention)
            await self.bot.send_message(self.bot.modlogs_channel, log_msg, embed=embed)
            await self.bot.send_message(self.bot.mods_channel, log_msg + " @here\nSee {} for a list of deleted messages.".format(self.bot.modlogs_channel.mention))
            msgs_to_delete = self.channel_antispam[message.channel.id][:]  # clone list so nothing is removed while going through it
            for msg in msgs_to_delete:
                try:
                    await self.bot.delete_message(msg)
                except discord.errors.NotFound:
                    pass  # don't fail if the message doesn't exist
        await asyncio.sleep(5)
        self.channel_antispam[message.channel.id].remove(message)
        try:
            if len(self.channel_antispam[message.channel.id]) == 0:
                self.channel_antispam.pop(message.channel.id)
        except KeyError:
            pass  # if the array doesn't exist, don't raise an error

    async def on_message(self, message):
        if message.channel.is_private:
            return
        if message.author.name == "GitHub" and message.author.discriminator == "0000":
            await self.bot.send_message(self.bot.helpers_channel, "Automatically pulling changes!")
            call(['git', 'pull'])
            await self.bot.close()
            return
        await self.bot.wait_until_all_ready()
        if message.author == self.bot.server.me or self.bot.staff_role in message.author.roles or message.channel == self.bot.helpers_channel:  # don't process messages by the bot or staff or in the helpers channel
            return
        await self.scan_message(message)
        await self.keyword_search(message)
        self.bot.loop.create_task(self.user_spam_check(message))
        self.bot.loop.create_task(self.channel_spam_check(message))

    async def on_message_edit(self, message_before, message_after):
        await self.bot.wait_until_all_ready()
        if message_after.author == self.bot.server.me or self.bot.staff_role in message_after.author.roles or message_after.channel == self.bot.helpers_channel:  # don't process messages by the bot or staff or in the helpers channel
            return
        await self.scan_message(message_after)

def setup(bot):
    bot.add_cog(Events(bot))
