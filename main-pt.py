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
console = Console()


def loading(seconds):
    with Progress() as progress:
        task = progress.add_task("", total=seconds)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)


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
{Style.RESET_ALL}{Fore.RESET}""")


versao_python = sys.version.split()[0]


def restart():
    python = sys.executable
    os.execv(python, [python] + sys.argv)


client = discord.Client()
if os == "Windows":
    system("cls")
else:
    print(chr(27) + "[2J")
    clearall()
while True:
    token = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Insira o seu token para prosseguir{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    guild_s = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Insira o ID do servidor que você deseja replicar{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    guild = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Insira o ID do servidor de destino para colar o servidor copiado{Style.RESET_ALL}{Fore.RESET}\n>'
    )
    clearall()
    print(f'{Style.BRIGHT}{Fore.GREEN}Os valores inseridos são:')
    token_length = len(token)
    hidden_token = "*" * token_length
    print(
        f'{Style.BRIGHT}{Fore.GREEN}Seu token: {Fore.YELLOW}{hidden_token}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}ID do Servidor para replicar: {Fore.YELLOW}{guild_s}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}ID do Servidor que você deseja colar o servidor copiado: {Fore.YELLOW}{guild}{Style.RESET_ALL}{Fore.RESET}'
    )
    confirm = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Os valores estão corretos? {Fore.YELLOW}(Y/N){Style.RESET_ALL}{Fore.RESET}\n >'
    )
    if confirm.upper() == 'Y':
        if not guild_s.isnumeric():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}O ID do servidor para replicar deve conter apenas números.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not guild.isnumeric():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}O ID do servidor de destino deve conter apenas números.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not token.strip() or not guild_s.strip() or not guild.strip():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}Um ou mais campos estão em branco.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if len(token.strip()) < 3 or len(guild_s.strip()) < 3 or len(
                guild.strip()) < 3:
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}Um ou mais campos têm menos de 3 caracteres.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        break
    elif confirm.upper() == 'N':
        clearall()
    else:
        clearall()
        print(
            f'{Style.BRIGHT}{Fore.RED}Opção inválida. Por favor, insira Y ou N.{Style.RESET_ALL}{Fore.RESET}'
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
        table = Table(title="Versões", style="bold magenta", width=40)
        table.add_column("Componente")
        table.add_column("Versão", style="cyan")
        table.add_row("Clonador", version)
        table.add_row("Discord.py", discord.__version__)
        table.add_row("Python", versao_python)
        console.print(RichPanel(table))
        console.print(
            RichPanel(f" Autenticação bem-sucedida",
                      style="bold green",
                      width=47))
        console.print(
            RichPanel(
                f" Olá, {client.user.name}! A clonagem começará em breve...",
                style="bold blue",
                width=47))
        print(f"\n")
        loading(20)
        clearall()
        questions = [
            inquirer.List(
                'clone_emojis',
                message="\033[35mDeseja clonar emojis?\033[0m",
                choices=['\033[32mSim\033[0m', '\033[31mNão\033[0m'],
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
        if answers['clone_emojis'] == '\033[32mSim\033[0m':
            print(
                f"{Style.BRIGHT}{Fore.YELLOW}Clonagem de emojis em andamento. Isso pode levar alguns instantes."
            )
            loading(13)
            await Clone.emojis_create(guild_to, guild_from)

        print(
            f"{Style.BRIGHT}{Fore.BLUE}O servidor foi clonado com sucesso em {Fore.YELLOW}{duration_str}{Style.RESET_ALL}"
        )
        print(
            f"{Style.BRIGHT}{Fore.BLUE}Visite nosso servidor do Discord: {Fore.YELLOW}https://discord.gg/Qvf5NUtqMg{Style.RESET_ALL}"
        )
        with open('saves.json', 'r') as f:
            clones = json.load(f)
        clones['Clones_teste_feitos'] += 1
        with open('saves.json', 'w') as f:
            json.dump(clones, f)
        print(
            f"{Style.BRIGHT}{Fore.BLUE}Finalizando processo e encerrando a sessão na conta {Fore.YELLOW}{client.user}"
        )
        await asyncio.sleep(30)
        await client.close()  #fecha o codigo

    except discord.LoginFailure:
        print(
            "Não foi possível autenticar na conta. Verifique se o token está correto."
        )
    except discord.Forbidden:
        print(
            "Não foi possível realizar a clonagem devido a permissões insuficientes."
        )
    except discord.NotFound:
        print(
            "Não foi possível encontrar algum dos elementos da cópia (canais, categorias, etc.)."
        )
    except discord.HTTPException:
        print(
            "Houve um erro de comunicação com a API do Discord. Em 20 segundos, o código continuará a partir do ponto em que parou."
        )
        loading(20)

        await Clone.emojis_create(guild_to, guild_from)
    except asyncio.TimeoutError:
        print(f"Ocorreu um erro: TimeOut")
    except Exception as e:

        print(Fore.RED + " Ocorreu um erro:", e)
        traceback.print_exc()
        print(Fore.YELLOW + " Possíveis causas e soluções:")
        print(Fore.YELLOW + " 1. ID do servidor incorreto")
        print(Fore.YELLOW + " 2. Você não está no servidor inserido")
        print(Fore.YELLOW + " 3. Servidor inserido não existe")
        print(
            Fore.RED +
            "Mesmo assim não foi resolvido? entre em contato com o desenvolvedor em https://discord.gg/Qvf5NUtqMg"
        )
        print(
            Fore.YELLOW +
            "\n\nO código será reiniciado em 20 segundos. Se você não quiser esperar atualize a página e comece novamente."
        )
        print(Style.RESET_ALL)
        loading(20)
        restart()
        print(Fore.RED + "Reiniciando...")


try:
    client.run(token, bot=False)
except discord.LoginFailure:
    print(Fore.RED + "O token inserido é inválido")
    print(
        Fore.YELLOW +
        "\n\nO código será reiniciado em 10 segundos. Se você não quiser esperar atualize a página e comece novamente."
    )
    print(Style.RESET_ALL)
    loading(10)
    restart()
    clearall()
    print(Fore.RED + "Reiniciando...")
