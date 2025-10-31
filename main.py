import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)

LOG_CHANNEL_NAME = os.getenv("LOG_CHANNEL_NAME", "audit-log")


@bot.event
async def on_ready():
    print("I spy with my little eye...")
    for guild in bot.guilds:
        log_channel = discord.utils.get(
            guild.text_channels, name=LOG_CHANNEL_NAME)
        if not log_channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                guild.me: discord.PermissionOverwrite(view_channel=True)
            }
            await guild.create_text_channel(LOG_CHANNEL_NAME, overwrites=overwrites)
    print("Audit log system is ready.")


@bot.event
async def on_message_delete(message):
    if not message.guild or message.author.bot:
        return
    log_channel = discord.utils.get(
        message.guild.text_channels, name=LOG_CHANNEL_NAME)
    if not log_channel:
        return

    embed = discord.Embed(title="Message Deleted",
                          color=discord.Color.red())
    embed.add_field(
        name="Author", value=f"{message.author} ({message.author.id})", inline=False)
    embed.add_field(
        name="Channel", value=message.channel.mention, inline=False)
    embed.add_field(
        name="Content", value=message.content or "*[no text]*", inline=False)

    if message.attachments:
        attachments = "\n".join(a.url for a in message.attachments)
        embed.add_field(name="Attachments", value=attachments, inline=False)

    embed.timestamp = discord.utils.utcnow()
    await log_channel.send(embed=embed)


@bot.event
async def on_message_edit(before, after):
    if not before.guild or before.author.bot or before.content == after.content:
        return
    log_channel = discord.utils.get(
        before.guild.text_channels, name=LOG_CHANNEL_NAME)
    if not log_channel:
        return

    embed = discord.Embed(title="Message Edited",
                          color=discord.Color.orange())
    embed.add_field(
        name="Author", value=f"{before.author} ({before.author.id})", inline=False)
    embed.add_field(name="Channel", value=before.channel.mention, inline=False)
    embed.add_field(
        name="Before", value=before.content or "*[no text]*", inline=False)
    embed.add_field(
        name="After", value=after.content or "*[no text]*", inline=False)
    embed.timestamp = discord.utils.utcnow()

    await log_channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    log_channel = discord.utils.get(
        member.guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        embed = discord.Embed(title="Member Joined",
                              color=discord.Color.green())
        embed.add_field(
            name="User", value=f"{member} ({member.id})", inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    log_channel = discord.utils.get(
        member.guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        embed = discord.Embed(title="Member Left", color=discord.Color.red())
        embed.add_field(
            name="User", value=f"{member} ({member.id})", inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


@bot.event
async def on_member_ban(guild, user):
    log_channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        embed = discord.Embed(title="User Banned",
                              color=discord.Color.dark_red())
        embed.add_field(name="User", value=f"{user} ({user.id})", inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


@bot.event
async def on_member_unban(guild, user):
    log_channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        embed = discord.Embed(title="User Unbanned",
                              color=discord.Color.green())
        embed.add_field(name="User", value=f"{user} ({user.id})", inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


@bot.event
async def on_guild_channel_create(channel):
    log_channel = discord.utils.get(
        channel.guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        embed = discord.Embed(title="Channel Created",
                              color=discord.Color.green())
        embed.add_field(name="Channel", value=f"{channel.name}", inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


@bot.event
async def on_guild_channel_delete(channel):
    log_channel = discord.utils.get(
        channel.guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        embed = discord.Embed(title="Channel Deleted",
                              color=discord.Color.red())
        embed.add_field(name="Name", value=channel.name, inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


@bot.event
async def on_guild_role_create(role):
    log_channel = discord.utils.get(
        role.guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        embed = discord.Embed(title="Role Created",
                              color=discord.Color.green())
        embed.add_field(name="Role", value=role.name, inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


@bot.event
async def on_guild_role_delete(role):
    log_channel = discord.utils.get(
        role.guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        embed = discord.Embed(title="Role Deleted",
                              color=discord.Color.red())
        embed.add_field(name="Role", value=role.name, inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


@bot.event
async def on_guild_emojis_update(guild, before, after):
    log_channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        embed = discord.Embed(title="Emojis Updated",
                              color=discord.Color.blurple())
        embed.add_field(name="Before", value=", ".join(
            e.name for e in before), inline=False)
        embed.add_field(name="After", value=", ".join(
            e.name for e in after), inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


@bot.event
async def on_guild_channel_pins_update(channel, last_pin):
    log_channel = discord.utils.get(
        channel.guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        embed = discord.Embed(title="Pins Updated",
                              color=discord.Color.gold())
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.add_field(name="Last Pin Time",
                        value=str(last_pin), inline=False)
        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)


@bot.event
async def on_member_update(before, after):
    if not before.guild:
        return

    log_channel = discord.utils.get(
        before.guild.text_channels, name=LOG_CHANNEL_NAME)
    if not log_channel:
        return

    before_timeout = before.timed_out_until
    after_timeout = after.timed_out_until

    if before_timeout != after_timeout:
        embed = discord.Embed(title="Member Timeout Updated",
                              color=discord.Color.dark_orange())
        embed.add_field(
            name="User", value=f"{after} ({after.id})", inline=False)

        if after_timeout is None:
            embed.add_field(
                name="Action", value="Timeout removed", inline=False)
        else:
            embed.add_field(name="Action", value="Timed out", inline=False)
            embed.add_field(name="Until", value=str(
                after_timeout), inline=False)

        embed.timestamp = discord.utils.utcnow()
        await log_channel.send(embed=embed)

bot.run(token, log_handler=handler)

