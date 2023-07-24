import subprocess
import os
from pathlib import Path
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install
import colorama
from colorama import Fore, init, Style

colorama.init
install()

console = Console()


def clear_screen():
    os.system('clear')
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


def main():
    clear_screen()
    language = questionary.select("Escolha uma linguagem:",
                                  choices=["pt", "en"]).ask()
    if not is_python_installed():
        clear_screen()
        console.print(
            Panel(f"O Python não está instalado em seu sistema.",
                  title="[bold red]Erro[/bold red]"))
        return
    elif not is_main_script_present(language):
        clear_screen()
        console.print(
            Panel(f"Arquivo main-{language}.py não encontrado.",
                  title="[bold red]Erro[/bold red]"))
        return
    elif not confirm_execution(language):
        clear_screen()
        console.print(
            Panel("Operação cancelada.",
                  title="[bold yellow]Aviso[/bold yellow]"))
        return
    try:
        subprocess.run([get_python_interpreter(), f"main-{language}.py"])
    except subprocess.CalledProcessError as e:
        clear_screen()
        console.print(
            Panel(f"Erro ao executar o subprocesso: {e}",
                  title="[bold red]Erro[/bold red]"))


def is_python_installed():
    try:
        subprocess.check_output(["python", "--version"])
        return True
    except subprocess.CalledProcessError:
        return False


def is_main_script_present(language):
    return Path(f"main-{language}.py").is_file()


def confirm_execution(language):
    messages = {
        "pt":
        "Você está prestes a executar o script main-pt.py. Deseja continuar?",
        "en":
        "You are about to execute the main-en.py script. Do you want to continue?"
    }
    clear_screen()
    confirmation = questionary.confirm(messages[language]).ask()
    return confirmation


def get_python_interpreter():
    if is_python3_installed():
        return "python3"
    else:
        return "python"


def is_python3_installed():
    try:
        subprocess.check_output(["python3", "--version"])
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    main()