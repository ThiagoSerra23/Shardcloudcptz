import discord
from discord.ext import commands, tasks
from utils.database import get_config

class VoiceControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_voice_connection.start()

    def cog_unload(self):
        self.check_voice_connection.cancel()

    @tasks.loop(minutes=1)
    async def check_voice_connection(self):
        """Periodically ensures the bot is connected."""
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            await self.join_voice(guild)

    async def join_voice(self, guild):
        config = await get_config(guild.id)
        
        channel_id = None
        if config:
            channel_id = config.get("voice_channel_id")
            
        # Fallback ID integration
        if not channel_id:
             # Check if the fallback ID exists in this guild
             fallback_id = 1443971232440782938
             fallback_channel = guild.get_channel(fallback_id)
             if fallback_channel:
                 channel_id = fallback_id

        if not channel_id:
            return

        channel = guild.get_channel(channel_id)
        if not channel or not isinstance(channel, discord.VoiceChannel):
            return

        # Check if already connected
        if guild.voice_client:
            if guild.voice_client.channel.id == channel.id:
                return # Already here
            else:
                try:
                    await guild.voice_client.move_to(channel)
                except Exception:
                    pass
        else:
            try:
                vc = await channel.connect()
                # Apply self-deafen/mute after connection
                await vc.guild.change_voice_state(channel=channel, self_deaf=True, self_mute=True)
                print(f"🔊 Joined voice channel: {channel.name} in {guild.name}")
            except Exception as e:
                # Ignore list index errors (minor connection issue)
                if "list index out of range" not in str(e):
                    print(f"❌ Failed to join voice: {e}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Determine if the bot was disconnected
        if member.id == self.bot.user.id and not after.channel:
            # Reconnect
            await self.join_voice(member.guild)

    @commands.group(name="botcall", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def botcall(self, ctx):
        await ctx.send("Use `!botcall entrar` para forçar a entrada do bot.")

    @botcall.command(name="entrar")
    @commands.has_permissions(administrator=True)
    async def join_cmd(self, ctx):
        await self.join_voice(ctx.guild)
        await ctx.send("✅ Tentando conectar ao canal configurado...")

def setup(bot):
    bot.add_cog(VoiceControl(bot))
