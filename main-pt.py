from os import system
import psutil
import os
from pypresence import Presence
import time
import sys
import discord
import json
import traceback
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.panel import Panel as RichPanel
from rich.progress import Progress
import asyncio
from colorama import Fore, init, Style
import platform
import inquirer
from cloner import Clone

version = '1.4'
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


def get_user_preferences():
    preferences = {}
    preferences['guild_edit'] = True
    preferences['channels_delete'] = True
    preferences['roles_create'] = True
    preferences['categories_create'] = True
    preferences['channels_create'] = True
    preferences['emojis_create'] = False

    def map_boolean_to_string(value):
        return "Sim" if value else "Não"

    panel_title = "Config BETA"
    panel_content = "\n"
    panel_content += f"- Alterar nome e ícone do servidor: {map_boolean_to_string(preferences.get('guild_edit', False))}\n"
    panel_content += f"- Excluir os canais do servidor de destino: {map_boolean_to_string(preferences.get('channels_delete', False))}\n"
    panel_content += f"- Clonar os cargos: {map_boolean_to_string(preferences.get('roles_create', False))}\n"
    panel_content += f"- Clonar as categorias: {map_boolean_to_string(preferences.get('categories_create', False))}\n"
    panel_content += f"- Clonar os canais: {map_boolean_to_string(preferences.get('channels_create', False))}\n"
    panel_content += f"- Clonar os emojis: {map_boolean_to_string(preferences.get('emojis_create', False))}\n"
    console.print(
        RichPanel(panel_content,
                  title=panel_title,
                  style="bold blue",
                  width=70))

    questions = [
        inquirer.List(
            'reconfigure',
            message='Você deseja reconfigurar as configurações padrão?',
            choices=['Sim', 'Não'],
            default='Não')
    ]

    answers = inquirer.prompt(questions)

    reconfigure = answers['reconfigure']
    if reconfigure == 'Sim':
        questions = [
            inquirer.Confirm(
                'guild_edit',
                message='Deseja editar o ícone do servidor e nome?',
                default=False),
            inquirer.Confirm('channels_delete',
                             message='Deseja deletar os canais?',
                             default=False),
            inquirer.Confirm(
                'roles_create',
                message=
                'Deseja clonar os cargos? (NÃO É RECOMENDADO DESATIVAR)',
                default=False),
            inquirer.Confirm('categories_create',
                             message='Deseja clonar as categorias?',
                             default=False),
            inquirer.Confirm('channels_create',
                             message='Deseja clonar os canais?',
                             default=False),
            inquirer.Confirm(
                'emojis_create',
                message=
                'Deseja clonar os Emojis? (É RECOMENDADO ATIVAR ESSA CLONAGEM SOLO(SOZINHA) PARA NÃO OCORRER ERROS)',
                default=False)
        ]

        answers = inquirer.prompt(questions)
        preferences['guild_edit'] = answers['guild_edit']
        preferences['channels_delete'] = answers['channels_delete']
        preferences['roles_create'] = answers['roles_create']
        preferences['categories_create'] = answers['categories_create']
        preferences['channels_create'] = answers['channels_create']
        preferences['emojis_create'] = answers['emojis_create']

    clearall()
    return preferences


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
        table = Table(title="Versões", style="bold magenta", width=85)
        table.add_column("Componente", width=35)
        table.add_column("Versão", style="cyan", width=35)
        table.add_row("Clonador", version)
        table.add_row("Discord.py", discord.__version__)
        table.add_row("Python", versao_python)
        console.print(RichPanel(table))
        console.print(
            RichPanel(f" Autenticação bem-sucedida em {client.user.name}",
                      style="bold green",
                      width=69))
        print(f"\n")
        loading(5)
        clearall()
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))
        preferences = get_user_preferences()

        if not any(preferences.values()):
            preferences = {k: True for k in preferences}

        if preferences['guild_edit']:
            await Clone.guild_edit(guild_to, guild_from)
        if preferences['channels_delete']:
            await Clone.channels_delete(guild_to)
        if preferences['roles_create']:
            await Clone.roles_create(guild_to, guild_from)
        if preferences['categories_create']:
            await Clone.categories_create(guild_to, guild_from)
        if preferences['channels_create']:
            await Clone.channels_create(guild_to, guild_from)
        if preferences['emojis_create']:
            await Clone.emojis_create(guild_to, guild_from)

        end_time = time.time()
        duration = end_time - start_time
        duration_str = time.strftime("%M:%S", time.gmtime(duration))
        print("\n\n")
        print(
            f"{Style.BRIGHT}{Fore.BLUE} O servidor foi clonado com sucesso em {Fore.YELLOW}{duration_str}{Style.RESET_ALL}"
        )
        print(
            f"{Style.BRIGHT}{Fore.BLUE} Visite nosso servidor do Discord: {Fore.YELLOW}https://discord.gg/Qvf5NUtqMg{Style.RESET_ALL}"
        )
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
        print("\n")
        traceback.print_exc()
        panel_text = (
            f"1. ID do servidor incorreto\n"
            f"2. Você não está no servidor inserido\n"
            f"3. Servidor inserido não existe\n"
            f"Mesmo assim não foi resolvido? Entre em contato com o desenvolvedor em [link=https://discord.gg/Qvf5NUtqMg]https://discord.gg/Qvf5NUtqMg[/link]"
        )
        console.print(
            RichPanel(panel_text,
                      title="Possíveis causas e soluções",
                      style="bold red",
                      width=70))
        print(
            Fore.YELLOW +
            "\nO código será reiniciado em 20 segundos. Se você não quiser esperar atualize a página e comece novamente."
        )
        print(Style.RESET_ALL)
        loading(20)
        restart()
        print(Fore.RED + "Reiniciando...")


try:
    client.run(token)
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
