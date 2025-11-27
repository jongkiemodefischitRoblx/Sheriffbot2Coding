import discord
from discord.ext import commands
from discord.ui import View, Button
import asyncio

TOKEN = "MTQ0MzQ1Nzk2Njg0OTM5NjkzNw.GGWP-m.WpcQ_TeuHgGxFD7-dFHVR-65CVFukuJWhtouLY"  # Ganti ini dengan token bot kamu

# Pakai intents default (tidak privileged)
intents = discord.Intents.default()
intents.message_content = False  # Nonaktif, jadi anti-toxic tidak jalan
bot = commands.Bot(command_prefix="!", intents=intents)

ticket_count = 0

# ===================================================
# AUTO FIND OR CREATE CATEGORY
# ===================================================
async def get_ticket_category(guild: discord.Guild):
    category = discord.utils.get(guild.categories, name="🎟️ Tickets")
    if category is None:
        category = await guild.create_category("🎟️ Tickets")
    return category

# ===================================================
# CREATE TICKET BUTTON
# ===================================================
class CreateTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket 🎟️", style=discord.ButtonStyle.green)
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        global ticket_count
        ticket_count += 1

        category = await get_ticket_category(interaction.guild)

        ticket_channel = await category.create_text_channel(f"ticket-{ticket_count}")
        await ticket_channel.set_permissions(interaction.user, view_channel=True, send_messages=True)

        await interaction.response.send_message(
            f"Your ticket has been created: **#{ticket_count}**",
            ephemeral=True
        )

        view = CloseTicketView()
        await ticket_channel.send(
            f"**Welcome To Tickets, Let's chat!**\n{interaction.user.mention}",
            view=view
        )

# ===================================================
# CLOSE TICKET
# ===================================================
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket ✅", style=discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Closing ticket in 3...", ephemeral=True)
        await asyncio.sleep(1)
        await interaction.edit_original_response(content="Closing ticket in 2...")
        await asyncio.sleep(1)
        await interaction.edit_original_response(content="Closing ticket in 1...")
        await asyncio.sleep(1)

        await interaction.channel.delete(reason="Ticket closed")

# ===================================================
# SEND PANEL
# ===================================================
@bot.tree.command(name="ticketpanel", description="Send ticket panel")
async def ticketpanel(interaction: discord.Interaction):
    view = CreateTicketView()
    await interaction.response.send_message(
        "**Sheriff Tickets Helps You Contact Staff Without DMs. Safer to Use @SheriffTickets**",
        view=view
    )

# ===================================================
# READY
# ===================================================
@bot.event
async def on_ready():
    print(f"Bot Online as {bot.user}")
    try:
        await bot.tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print(e)

bot.run(TOKEN)
