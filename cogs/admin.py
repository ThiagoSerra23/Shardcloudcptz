import discord
from discord.ext import commands
from discord.ui import View, Select, Button
from utils.database import upsert_config, get_config

class ChannelConfigView(View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=300)
        self.bot = bot
        self.guild_id = guild_id

    async def update_config(self, interaction, key, value):
        await upsert_config(self.guild_id, **{key: value.id})
        await interaction.response.send_message(f"✅ Configuração atualizada: **{key}** -> {value.mention}", ephemeral=True)
        # Log
        log_cog = self.bot.get_cog("Logs")
        if log_cog:
            await log_cog.log_action(
                interaction.guild,
                "Configuração Alterada",
                f"{interaction.user.mention} definiu **{key}** para {value.mention}",
                discord.Color.gold()
            )

    @discord.ui.channel_select(placeholder="Selecione o Canal de Logs", channel_types=[discord.ChannelType.text], row=0, min_values=1, max_values=1)
    async def select_logs(self, select: Select, interaction: discord.Interaction):
        await self.update_config(interaction, "log_channel_id", select.values[0])

    @discord.ui.channel_select(placeholder="Selecione o Canal de Aprovação", channel_types=[discord.ChannelType.text], row=1, min_values=1, max_values=1)
    async def select_approval(self, select: Select, interaction: discord.Interaction):
        await self.update_config(interaction, "approval_channel_id", select.values[0])

    @discord.ui.channel_select(placeholder="Selecione o Canal de Registro", channel_types=[discord.ChannelType.text], row=2, min_values=1, max_values=1)
    async def select_reg(self, select: Select, interaction: discord.Interaction):
        await self.update_config(interaction, "registration_channel_id", select.values[0])

    @discord.ui.channel_select(placeholder="Selecione Canal de Voz (Bot 24h)", channel_types=[discord.ChannelType.voice], row=3, min_values=1, max_values=1)
    async def select_voice(self, select: Select, interaction: discord.Interaction):
        await self.update_config(interaction, "voice_channel_id", select.values[0])
    
    @discord.ui.channel_select(placeholder="Selecione o Canal do Elenco", channel_types=[discord.ChannelType.text], row=4, min_values=1, max_values=1)
    async def select_cast(self, select: Select, interaction: discord.Interaction):
        await self.update_config(interaction, "cast_channel_id", select.values[0])

class RoleConfigView(View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=300)
        self.bot = bot
        self.guild_id = guild_id

    async def update_config(self, interaction, key, value):
        await upsert_config(self.guild_id, **{key: value.id})
        await interaction.response.send_message(f"✅ Configuração atualizada: **{key}** -> {value.mention}", ephemeral=True)
         # Log
        log_cog = self.bot.get_cog("Logs")
        if log_cog:
            await log_cog.log_action(
                interaction.guild,
                "Configuração Alterada",
                f"{interaction.user.mention} definiu **{key}** para {value.mention}",
                discord.Color.gold()
            )

    @discord.ui.role_select(placeholder="Cargo de Membro Aprovado", row=0, min_values=1, max_values=1)
    async def select_member_role(self, select: Select, interaction: discord.Interaction):
        await self.update_config(interaction, "member_role_id", select.values[0])

    @discord.ui.role_select(placeholder="Cargo do Elenco", row=1, min_values=1, max_values=1)
    async def select_cast_role(self, select: Select, interaction: discord.Interaction):
        await self.update_config(interaction, "cast_role_id", select.values[0])

    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.secondary, row=2)
    async def back_btn(self, button, interaction):
        await interaction.response.edit_message(content="📂 **Painel Principal**", view=MainConfigView(self.bot, self.guild_id))

class MainConfigView(View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=300)
        self.bot = bot
        self.guild_id = guild_id

    @discord.ui.button(label="Configurar Canais", style=discord.ButtonStyle.primary, emoji="📺")
    async def config_channels(self, button, interaction):
        await interaction.response.edit_message(content="📺 **Configuração de Canais**\nSelecione os canais correspondentes abaixo:", view=ChannelConfigView(self.bot, self.guild_id))

    @discord.ui.button(label="Configurar Cargos", style=discord.ButtonStyle.primary, emoji="👔")
    async def config_roles(self, button, interaction):
        val = "⚠️ Discord.py 2.0+ required for Role Select" # Placeholder check implied by environment
        await interaction.response.edit_message(content="👔 **Configuração de Cargos**\nSelecione os cargos correspondentes abaixo:", view=RoleConfigView(self.bot, self.guild_id))

    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger, emoji="✖️")
    async def close(self, button, interaction):
        await interaction.message.delete()

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="chupetinha")
    @commands.has_permissions(administrator=True)
    async def chupetinha(self, ctx):
        """Abre o painel geral de configuração."""
        embed = discord.Embed(
            title="⚙️ Painel de Controle - Chupetinha",
            description="Bem-vindo ao sistema de configuração centralizada.\nUtilize os botões abaixo para gerenciar todo o servidor.",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text="Configuração Avançada e Simplificada")
        
        await ctx.send(embed=embed, view=MainConfigView(self.bot, ctx.guild.id))

    @commands.command(name="config_registro")
    @commands.has_permissions(administrator=True)
    async def config_registro(self, ctx):
        """Configurar painel de registro."""
        from utils.database import get_registration_config
        
        config = await get_registration_config(ctx.guild.id)
        if not config:
            config = {
                "panel_title": "Chupetaz",
                "panel_description": "Bem-vindo ao Chupetaz!",
                "panel_image": None,
                "panel_footer": "discord.gg/chupetaz"
            }
        
        embed = discord.Embed(
            title="⚙️ Configuração do Painel de Registro",
            description="**Configurações atuais:**",
            color=discord.Color.blue()
        )
        embed.add_field(name="Título", value=config["panel_title"], inline=False)
        embed.add_field(name="Descrição", value=config["panel_description"][:100] + "..." if len(config["panel_description"]) > 100 else config["panel_description"], inline=False)
        embed.add_field(name="Imagem", value=config["panel_image"] or "Nenhuma", inline=False)
        embed.add_field(name="Rodapé", value=config["panel_footer"], inline=False)
        
        # Create View with Edit Button
        view = View(timeout=300)
        
        async def edit_callback(interaction: discord.Interaction):
            from utils.database import upsert_registration_config
            from discord.ui import Modal, InputText
            
            current = await get_registration_config(interaction.guild.id)
            if not current:
                current = config
            
            class ConfigModal(Modal):
                def __init__(self):
                    super().__init__(title="Editar Painel de Registro")
                    
                    self.add_item(InputText(
                        label="Título",
                        placeholder="Ex: Chupetaz",
                        value=current["panel_title"],
                        max_length=256
                    ))
                    self.add_item(InputText(
                        label="Descrição",
                        placeholder="Texto explicativo do painel",
                        value=current["panel_description"],
                        style=discord.InputTextStyle.long,
                        max_length=4000
                    ))
                    self.add_item(InputText(
                        label="URL da Imagem (opcional)",
                        placeholder="https://...",
                        value=current["panel_image"] or "",
                        required=False,
                        max_length=512
                    ))
                    self.add_item(InputText(
                        label="Rodapé",
                        placeholder="Ex: discord.gg/chupetaz",
                        value=current["panel_footer"] or "",
                        max_length=256
                    ))
                
                async def callback(self, interaction: discord.Interaction):
                    await upsert_registration_config(
                        interaction.guild.id,
                        panel_title=self.children[0].value,
                        panel_description=self.children[1].value,
                        panel_image=self.children[2].value or None,
                        panel_footer=self.children[3].value
                    )
                    await interaction.response.send_message("✅ Configuração atualizada com sucesso!", ephemeral=True)
            
            await interaction.response.send_modal(ConfigModal())
        
        edit_button = Button(label="Editar", style=discord.ButtonStyle.primary, emoji="✏️")
        edit_button.callback = edit_callback
        view.add_item(edit_button)
        
        await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Admin(bot))
