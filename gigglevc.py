#!/usr/bin/env python

import discord

import gigdb
import gigguild
from settings import bot_token

intents = discord.Intents.none()
intents.guilds = True
intents.voice_states = True
client = discord.Client(intents=intents)

@client.event
async def on_guild_channel_create(channel):
    if isinstance(channel, discord.VoiceChannel):
        await channel.guild.create_role(name=channel.name + " Owner")
        await channel.guild.create_role(name=channel.name + " Mod")

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
    gigguild.load_guilds()
    client.run(bot_token)
