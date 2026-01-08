import discord
from discord.ext import commands
from datetime import datetime
from utils.database import get_config

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_action(self, guild, title, description, color=discord.Color.blue(), fields=None, thumbnail=None):
        config = await get_config(guild.id)
        if not config or not config["log_channel_id"]:
            return

        channel = guild.get_channel(config["log_channel_id"])
        if not channel:
            return

        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.now()
        )
        
        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
        
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
            
        embed.set_footer(text=f"Log System • {guild.name}", icon_url=guild.icon.url if guild.icon else None)

        try:
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Failed to send log: {e}")

def setup(bot):
    bot.add_cog(Logs(bot))
