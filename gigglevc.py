#!/usr/bin/env python

import discord

import gigdb
import gigguild
from settings import bot_token

intents = discord.Intents.none()
intents.guilds = True
intents.members = True
intents.voice_states = True
client = discord.Client(intents=intents)

@client.event
async def on_guild_channel_create(channel):
    if isinstance(channel, discord.VoiceChannel):
        # Create roles if they do not exist
        if not discord.utils.get(channel.guild.roles, name=channel.name + " Owner"):
            await channel.guild.create_role(name=channel.name + " Owner")
        if not discord.utils.get(channel.guild.roles, name=channel.name + " Mod"):
            await channel.guild.create_role(name=channel.name + " Mod")

@client.event
async def on_voice_state_update(member, before, after):
    guild = member.guild

    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
        # make sure this is the right log entry
        if entry.target.id == member.id:
            # Check if the action was a mute
            if entry.before.mute is False and entry.after.mute is True:
                print(f"{entry.user.id} muted {entry.target.id}")
            # Check if the action was an unmute
            if entry.before.mute is True and entry.after.mute is False:
                print(f"{entry.user.id} unmuted {entry.target.id}")

@client.event
async def on_voice_state_update_not(member, before, after):
    if before.mute and not after.mute:
        gigdb.delete_mute_member(member.guild.id, member.id)
        if member.guild.id in gigguild.guilds:
            channel = member.guild.get_channel(gigguild.guilds[member.guild.id].mod_log_channel_id)
            if channel:
                await channel.send(embed=discord.Embed(description=f"{member.mention} has been unmuted", color=0x00ff00))

    if after.mute:
        gigdb.add_mute_member(member.guild.id, member.id, member.name)
        if member.guild.id in gigguild.guilds:
            channel = member.guild.get_channel(gigguild.guilds[member.guild.id].mod_log_channel_id)
            if channel:
                await channel.send(embed=discord.Embed(description=f"{member.mention} has been muted", color=0x00ff00))

    if before.channel == after.channel:
        return

    if before.channel:
        role = discord.utils.get(member.guild.roles, name=f"{before.channel.name} Ping")
        if role:
            await member.remove_roles(role)

    if after.channel:
        role = discord.utils.get(member.guild.roles, name=f"{after.channel.name} Ping")
        if not role:
            role_name = f"{after.channel.name} Ping"
            role = await member.guild.create_role(name=role_name)
        await member.add_roles(role)

if __name__ == "__main__":
    client.run(bot_token)
