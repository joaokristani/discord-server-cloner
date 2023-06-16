from os import system
import psutil
import os
from pypresence import Presence
import time
import sys
import discord
import subprocess
import json
import traceback
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.panel import Panel as RichPanel
from rich.text import Text
from rich.progress import Progress
import asyncio
from colorama import Fore, init, Style
import platform
import inquirer
from cloner import Clone

version = '0.3'
clones = {'Clones_teste_feitos': 0}
versao_python = sys.version.split()[0]

console = Console()


def clearall():
    system('clear')
    print(f"""{Style.BRIGHT}{Fore.RED}
 ▄▄▄██▀▀▀▒█████   ▄▄▄       ▒█████   ██ ▄█▀ ██▀███   ██▓  ██████ ▄▄▄█████▓ ▄▄▄       ███▄    █  ██▓
   ▒██  ▒██▒  ██▒▒████▄    ▒██▒  ██▒ ██▄█▒ ▓██ ▒ ██▒▓██▒▒██    ▒ ▓  ██▒ ▓▒▒████▄     ██ ▀█   █ ▓██▒
   ░██  ▒██░  ██▒▒██  ▀█▄  ▒██░  ██▒▓███▄░ ▓██ ░▄█ ▒▒██▒░ ▓██▄   ▒ ▓██░ ▒░▒██  ▀█▄  ▓██  ▀█ ██▒▒██▒
▓██▄██▓ ▒██   ██░░██▄▄▄▄██ ▒██   ██░▓██ █▄ ▒██▀▀█▄  ░██░  ▒   ██▒░ ▓██▓ ░ ░██▄▄▄▄██ ▓██▒  ▐▌██▒░██░
 ▓███▒  ░ ████▓▒░ ▓█   ▓██▒░ ████▓▒░▒██▒ █▄░██▓ ▒██▒░██░▒██████▒▒  ▒██▒ ░  ▓█   ▓██▒▒██░   ▓██░░██░
 ▒▓▒▒░  ░ ▒░▒░▒░  ▒▒   ▓▒█░░ ▒░▒░▒░ ▒ ▒▒ ▓▒░ ▒▓ ░▒▓░░▓  ▒ ▒▓▒ ▒ ░  ▒ ░░    ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░▓  
 ▒ ░▒░    ░ ▒ ▒░   ▒   ▒▒ ░  ░ ▒ ▒░ ░ ░▒ ▒░  ░▒ ░ ▒░ ▒ ░░ ░▒  ░ ░    ░      ▒   ▒▒ ░░ ░░   ░ ▒░ ▒ ░
 ░ ░ ░  ░ ░ ░ ▒    ░   ▒   ░ ░ ░ ▒  ░ ░░ ░   ░░   ░  ▒ ░░  ░  ░    ░        ░   ▒      ░   ░ ░  ▒ ░
 ░   ░      ░ ░        ░  ░    ░ ░  ░  ░      ░      ░        ░                 ░  ░         ░  ░  
{Style.RESET_ALL}{Fore.MAGENTA}{Fore.RESET}""")


client = discord.Client()
if os == "Windows":
    system("cls")
else:
    print(chr(27) + "[2J")
    clearall()
while True:
    token = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Enter your token to proceed{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    guild_s = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Enter the ID of the server you wish to replicate{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    guild = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Enter the ID of the destination server to paste the copied server{Style.RESET_ALL}{Fore.RESET}\n>'
    )
    clearall()
    print(f'{Style.BRIGHT}{Fore.GREEN}The entered values are:')
    token_length = len(token)
    hidden_token = "*" * token_length
    print(
        f'{Style.BRIGHT}{Fore.GREEN}Your token: {Fore.YELLOW}{hidden_token}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}Server ID to replicate: {Fore.YELLOW}{guild_s}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}ID of the server you want to paste the copied server: {Fore.YELLOW}{guild}{Style.RESET_ALL}{Fore.RESET}'
    )
    confirm = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Are the values correct? {Fore.YELLOW}(Y/N){Style.RESET_ALL}{Fore.RESET}\n >'
    )
    if confirm.upper() == 'Y':
        if not guild_s.isnumeric():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}The server ID to replicate should only contain numbers.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not guild.isnumeric():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}The destination server ID should only contain numbers.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not token.strip() or not guild_s.strip() or not guild.strip():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}One or more fields are blank.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if len(token.strip()) < 3 or len(guild_s.strip()) < 3 or len(
                guild.strip()) < 3:
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}One or more fields have less than 3 characters.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        break

    elif confirm.upper() == 'N':
        clearall()
else:
    clearall()
    print(
        f'{Style.BRIGHT}{Fore.RED}Invalid option. Please enter Y or N.{Style.RESET_ALL}{Fore.RESET}'
    )
input_guild_id = guild_s
output_guild_id = guild
token = token
clearall()


@client.event
async def on_ready():
    try:
        start_time = time.time()
        global clones
        table = Table(title="Versions", style="bold magenta")
        table.add_column("Component")
        table.add_column("Version")
        table.add_row("Cloner", str(version), style="cyan")
        table.add_row("Discord.py", str(discord.__version__), style="cyan")
        table.add_row("Python", str(versao_python), style="cyan")
        console.print(RichPanel(table))
        console.print(
            RichPanel(f" Successful authentication",
                      style="bold green",
                      width=47))
        console.print(
            RichPanel(
                f" Hello, {client.user.name}! Cloning will start momentarily...",
                style="bold blue",
                width=47))
        print(f"\n")
        questions = [
            inquirer.List(
                'clone_emojis',
                message="\033[35mDo you want to clone emojis?\033[0m",
                choices=['\033[32mYes\033[0m', '\033[31mNo\033[0m'],
            ),
        ]
        answers = inquirer.prompt(questions)
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))
        await Clone.guild_edit(guild_to, guild_from)
        await Clone.channels_delete(guild_to)
        await Clone.roles_create(guild_to, guild_from)
        await Clone.categories_create(guild_to, guild_from)
        await Clone.channels_create(guild_to, guild_from)
        end_time = time.time()
        duration = end_time - start_time
        duration_str = time.strftime("%M:%S", time.gmtime(duration))
        if answers['clone_emojis'] == '\033[32mYes\033[0m':
            print(
                f"{Style.BRIGHT}{Fore.YELLOW}Cloning emojis in progress. This may take a few moments."
            )
            await asyncio.sleep(13)
            await Clone.emojis_create(guild_to, guild_from)
            print(
                f"{Style.BRIGHT}{Fore.BLUE}The server was successfully cloned in {Fore.YELLOW}{duration_str}{Style.RESET_ALL}"
            )
            print(
                f"{Style.BRIGHT}{Fore.BLUE}Visit our Discord server: {Fore.YELLOW}https://discord.gg/Qvf5NUtqMg{Style.RESET_ALL}"
            )
            clones['Clones_teste_feitos'] += 1
            with open('saves.json', 'w') as f:
                json.dump(clones, f)
            print(
                f"{Style.BRIGHT}{Fore.BLUE}Finalizing process and ending session on account {Fore.YELLOW}{client.user}"
            )
            await client.close()  # closes the code
    except discord.LoginFailure:
        print(
            "Could not authenticate to the account. Check if the token is correct."
        )
    except discord.Forbidden:
        print("Could not clone due to insufficient permissions.")
    except discord.HTTPException:
        print(
            "An error occurred in communicating with the Discord API. In 20 seconds, the code will resume from where it left off."
        )
        await asyncio.sleep(20)
        await Clone.emojis_create(guild_to, guild_from)

    except discord.NotFound:
        print(
            "Could not find one of the copy elements (channels, categories, etc.)."
        )
    except Exception as e:
        print(Fore.RED + "An error occurred:", e)


try:
    client.run(token, bot=False)
except discord.LoginFailure:
    print(Fore.RED + "The inserted token is invalid")
    print(
        Fore.YELLOW +
        "\n\nThe code will be restarted in 10 seconds. If you don't want to wait, refresh the page and start again."
    )
    print(Style.RESET_ALL)
    time.sleep(10)
    subprocess.Popen(["python", __file__])
    print(Fore.RED + "Restarting...")
