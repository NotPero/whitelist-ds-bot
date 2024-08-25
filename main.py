import discord
from discord.ext import commands
import json
import random
import asyncio
from datetime import datetime

with open('config.json') as config_file:
    config = json.load(config_file)

with open('locales.json') as locales_file:
    locales = json.load(locales_file)

with open('questions.json') as questions_file:
    questions = json.load(questions_file)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

def get_locale_message(locale, key, **kwargs):
    message = locales.get(locale, {}).get(key, "")
    if kwargs:
        return message.format(**kwargs)
    return message


@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')
    await bot.tree.sync()

@bot.tree.command(name=config["COMMAND"], description="Start the whitelist process")
async def whitelist(interaction: discord.Interaction):
    guild = interaction.guild
    user = interaction.user

    locale = config.get("LANGUAGE", "en")


    if guild is None:
        await interaction.response.send_message(get_locale_message(locale, "error_general"), ephemeral=True)
        return


    user_roles = [role.id for role in user.roles]
    if any(role_id in user_roles for role_id in config["ROLE_ID"]):
        await interaction.response.send_message(get_locale_message(locale, "already_whitelisted"), ephemeral=True)
        return


    await interaction.response.send_message(get_locale_message(locale, "check_dm"), ephemeral=True)

    log_channel = guild.get_channel(config["LOG_CHANNEL_ID"])
    if log_channel:
        embed = discord.Embed(
            title=get_locale_message(locale, "whitelist_attempt"),
            description=get_locale_message(locale, "log_attempt", user=user.mention),
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        await log_channel.send(embed=embed)

    if len(questions) < config["NUM_QUESTIONS"]:
        await interaction.followup.send(get_locale_message(locale, "not_enough_questions"), ephemeral=True)
        return

    selected_questions = random.sample(questions, config["NUM_QUESTIONS"])
    correct_answers = 0

    def check(m):
        return m.author == user and isinstance(m.channel, discord.DMChannel)

    try:
        for q in selected_questions:
            embed = discord.Embed(title=get_locale_message(locale, "whitelist_question"), description=q["question"], color=0x00ff00)

            options_text = ""
            for i, option in enumerate(q["options"]):
                options_text += f"{i + 1}) {option}\n"

            embed.add_field(name=get_locale_message(locale, "options"), value=options_text, inline=False)
            await user.send(embed=embed)

            try:
                response = await bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await user.send(get_locale_message(locale, "time_expired"))
                return

            try:
                tokens = response.content.replace(',', ' ').split()
                selected_indices = [int(x) - 1 for x in tokens if x.isdigit()]
            except ValueError:
                selected_indices = []


            if set(selected_indices) == set(q["correct"]):
                correct_answers += 1


        percentage = (correct_answers / config["NUM_QUESTIONS"]) * 100
        pass_threshold_fraction = config.get("PASS_THRESHOLD", 0.8)

        if (correct_answers / config["NUM_QUESTIONS"]) >= pass_threshold_fraction:
            roles = []
            for role_id in config["ROLE_ID"]:
                role = guild.get_role(role_id)
                if role:
                    roles.append(role)
            if roles:
                await user.add_roles(*roles)
            await user.send(get_locale_message(locale, "success_message", percentage=percentage))
            
            if log_channel:
                embed = discord.Embed(
                    title=get_locale_message(locale, "whitelist_passed"),
                    description=get_locale_message(locale, "log_passed", user=user.mention, percentage=percentage),
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                await log_channel.send(embed=embed)

        else:
            await user.send(get_locale_message(locale, "failure_message", percentage=percentage))

            if log_channel:
                embed = discord.Embed(
                    title=get_locale_message(locale, "whitelist_failed"),
                    description=get_locale_message(locale, "log_failed", user=user.mention, percentage=percentage),
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                await log_channel.send(embed=embed)

    except discord.Forbidden:
        await interaction.followup.send(get_locale_message(locale, "error_dm"), ephemeral=True)
    except Exception as e:
        await user.send(get_locale_message(locale, "error_general"))
        print(f'Errore: {e}')


@bot.tree.command(name=config["givewhitelist"]["COMMAND"], description="Give whitelist role to a user")
async def givewhitelist(interaction: discord.Interaction, utente: discord.Member):
    guild = interaction.guild
    user = interaction.user


    locale = config.get("LANGUAGE", "en")


    user_roles = [role.id for role in user.roles]
    allowed_roles = config["givewhitelist"]["ALLOWED_ROLES"]

    if not any(role_id in user_roles for role_id in allowed_roles):
        await interaction.response.send_message(get_locale_message(locale, "givewhitelist_not_allowed"), ephemeral=True)
        return


    roles = []
    for role_id in config["ROLE_ID"]:
        role = guild.get_role(role_id)
        if role:
            roles.append(role)
    if roles:
        await utente.add_roles(*roles)
        await interaction.response.send_message(get_locale_message(locale, "givewhitelist_success", giver=user.mention, receiver=utente.mention), ephemeral=True)


        log_channel = guild.get_channel(config["LOG_CHANNEL_ID"])
        if log_channel:
            embed = discord.Embed(
                title="Give Whitelist",
                description=get_locale_message(locale, "givewhitelist_success", giver=user.mention, receiver=utente.mention),
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            await log_channel.send(embed=embed)

bot.run(config['TOKEN'])
