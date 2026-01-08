import discord
from discord.ext import commands
from discord.ui import Modal, InputText, View, Button
from utils.database import get_config
import datetime

class RegistrationModal(Modal):
    def __init__(self, bot):
        super().__init__(title="Registro de Membro")
        self.bot = bot
        
        self.add_item(InputText(
            label="Quem te indicou?", 
            placeholder="Nome de quem te convidou para o servidor",
            required=True,
            min_length=2,
            max_length=100
        ))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        guild = interaction.guild
        config = await get_config(guild.id)
        
        if not config or not config["approval_channel_id"]:
            return await interaction.followup.send("❌ Sistema de aprovação não configurado. Contate um administrador.", ephemeral=True)
            
        approval_channel = guild.get_channel(config["approval_channel_id"])
        if not approval_channel:
             return await interaction.followup.send("❌ Canal de aprovação não encontrado. Contate um administrador.", ephemeral=True)

        # Data collection
        indicacao = self.children[0].value
        
        embed = discord.Embed(
            title="📋 Novo Registro Pendente",
            description=f"Usuário: {interaction.user.mention} (`{interaction.user.id}`)",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="🤝 Indicado por", value=indicacao, inline=False)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        # We need to import ApprovalView dynamically to avoid circular imports? 
        # Or better, define it in a shared utils or handle it here if it's simple.
        # Ideally, the ApprovalView should be in cogs/approval.py. 
        # But we need to attach it here. 
        # To keep it clean, let's create the view in the approval cog but since we can't import easily across cogs without reloading,
        # we can make the View validation loose or simply import the class from a separate views file.
        # For simplicity, I will assume the Approval Cog will handle the listening of persistent views 
        # if I add a custom_id, OR I can just import it inside the callback if needed.
        # Actually, best practice is to have the view here or in a ui module. 
        # Let's put a custom ID on the buttons and let the Approval Cog Listen to them.
        
        # BUT, standard practice: Send the view with the message.
        from cogs.approval import ApprovalView # Local import to avoid circular dependency at module level
        
        await approval_channel.send(embed=embed, view=ApprovalView(self.bot, interaction.user.id))
        
        await interaction.followup.send("✅ Registro enviado para análise! Aguarde aprovação.", ephemeral=True)
        
        # Log
        log_cog = self.bot.get_cog("Logs")
        if log_cog:
            await log_cog.log_action(
                guild,
                "Registro Iniciado",
                f"Usuário {interaction.user.mention} enviou registro.\nIndicação: {indicacao}",
                discord.Color.blue()
            )

class RegistrationView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Solicitar", style=discord.ButtonStyle.success, emoji="📝", custom_id="reg_start_btn")
    async def start_reg(self, button, interaction):
        await interaction.response.send_modal(RegistrationModal(self.bot))

class Registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Re-register the view for persistence
        self.bot.add_view(RegistrationView(self.bot))

    @commands.command(name="setup_registro")
    @commands.has_permissions(administrator=True)
    async def setup_registro(self, ctx):
        from utils.database import get_registration_config
        
        config = await get_registration_config(ctx.guild.id)
        if not config:
            config = {
                "panel_title": "Chupetaz",
                "panel_description": "Bem-vindo ao Chupetaz!\nPara acessar nosso servidor, basta realizar o registro e aguardar a liberação da equipe.\n\nSomos uma família focada em PvP, portanto já deixamos claro: é preciso ter habilidade para entrar.\n\nMostre seu potencial e venha fazer parte do time!",
                "panel_image": None,
                "panel_footer": "discord.gg/chupetaz"
            }
        
        embed = discord.Embed(
            title=config["panel_title"],
            description=config["panel_description"],
            color=discord.Color.blue()
        )
        
        if config["panel_image"]:
            embed.set_image(url=config["panel_image"])
            
        if config["panel_footer"]:
            embed.set_footer(text=config["panel_footer"])
        
        await ctx.send(embed=embed, view=RegistrationView(self.bot))
        try:
            await ctx.message.delete()
        except:
            pass

def setup(bot):
    bot.add_cog(Registration(bot))
