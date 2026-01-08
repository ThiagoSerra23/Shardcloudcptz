import discord
from discord.ext import commands, tasks
from discord import SlashCommandGroup, Option
from utils.database import get_config, upsert_config
import datetime

class Cast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_cast_embed.start()

    def cog_unload(self):
        self.update_cast_embed.cancel()

    @tasks.loop(seconds=20)
    async def update_cast_embed(self):
        await self.bot.wait_until_ready()
        
        # Iterate over all guilds the bot config has (simplification: just connected guilds)
        for guild in self.bot.guilds:
            config = await get_config(guild.id)
            if not config:
                continue
                
            channel_id = config.get("cast_channel_id")
            message_id = config.get("cast_message_id")
            role_id = config.get("cast_role_id")
            
            if not channel_id or not role_id:
                continue
                
            channel = guild.get_channel(channel_id)
            if not channel:
                continue
                
            role = guild.get_role(role_id)
            if not role:
                continue
                
            # Build the list
            members = role.members
            members.sort(key=lambda m: m.display_name)
            
            # Create list of mentions
            member_mentions = [m.mention for m in members]
            
            # ====== EDITE AQUI PARA MUDAR O ESPAÇAMENTO ======
            # Para adicionar espaço entre as menções, mude o "\n" abaixo:
            # "\n" = sem espaço extra (padrão)
            # "\n\n" = 1 linha de espaço
            # "\n\n\n" = 2 linhas de espaço
            separator = "\n\n"  # <-- MUDE ESTE VALOR AQUI!
            # =================================================
            
            # Create Description (simple list of mentions)
            if member_mentions:
                desc_lines = separator.join(member_mentions)
            else:
                desc_lines = "Nenhum membro no elenco."

            embed = discord.Embed(
                title=f"Elenco Chupetaz",
                description=desc_lines,
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now()
            )
            if config.get("panel_footer"):
                embed.set_footer(text=config["panel_footer"])
            else:
                embed.set_footer(text="discord.gg/chupetaz")

            # Edit or Send
            if message_id:
                try:
                    msg = await channel.fetch_message(message_id)
                    await msg.edit(embed=embed)
                    continue
                except discord.NotFound:
                    pass # Message deleted, send new one
            
            # Send new message
            try:
                msg = await channel.send(embed=embed)
                await upsert_config(guild.id, cast_message_id=msg.id)
            except Exception as e:
                print(f"Failed to update cast in {guild.name}: {e}")

    @commands.command(name="setup_elenco")
    @commands.has_permissions(administrator=True)
    async def setup_elenco(self, ctx):
        # Trigger the loop manually or let it run
        # Calling loop logic once to instant create
        # We need to make sure config is set
        config = await get_config(ctx.guild.id)
        if not config or not config["cast_channel_id"] or not config["cast_role_id"]:
            return await ctx.send("❌ Configure o canal e o cargo do elenco primeiro em `!config`.")
            
        await ctx.send("✅ Sistema de elenco iniciado. Aguarde a atualização automática (Max 20s).")
        # Note: The loop runs automatically, so it will pick up eventually.

def setup(bot):
    bot.add_cog(Cast(bot))
