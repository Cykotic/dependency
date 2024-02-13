import os
import asyncio
from colorama import Fore
from lib.commands import handle_input
from lib.utils import PS4Manager

WELCOME_MESSAGES = (
    Fore.LIGHTRED_EX
    + """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠛⢦⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⠀⠱⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠒⠉⠉⠉⠉⠑⠒⠲⠤⢄⣀⡏⠉⠁⠒⠢⢷⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠈⠑⠄⠀⠀⠀⠀⡇⠀
⢀⣠⡤⠖⠚⡏⠉⠉⠁⠉⠉⠉⠁⠀⠠⢄⠀⠎⠁⠀⠰⣀⠀⠀⠄⠈⠙⠆⠈⠂⠀⠀⠀⢸⠀
⠻⣧⡀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠒⠀⣀⡤⠤⠖⡒⠿⠥⣄⡀⠀⢠⠒⠄⠀⠀⠀⢸⠀
⠀⠀⠙⠲⢼⣀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠛⠁⢀⢴⡘⠰⡀⡦⡀⡍⠲⢄⠁⠁⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠈⢉⠗⠀⠀⠀⠀⢀⠞⠁⡄⣠⣧⠎⠘⠁⠀⠣⠁⠱⡏⢆⠈⠳⡀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⣠⠃⠀⢀⡇⠃⠁⠀⠀⠀⠀⠀⠀⠀⠡⠬⣼⡀⠙⡄⠀⠀⠸⡀
⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⢰⡇⠀⠀⢸⢹⠄⠀⠄⠀⠀⠀⠀⠀⠀⢀⣀⠉⢇⠀⣽⡄⠀⠀⡇
⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⣏⢠⠀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡏⢪⢷⣸⠀⣹⣴⠀⠀⡇
⠀⠀⠀⠀⠀⠀⢸⠀⠀⢰⠉⢌⣄⠟⣤⠀⣠⣀⠀⠀⠀⠀⠀⠀⢏⡵⠋⣾⣻⢡⠃⡇⡆⠀⡇
⠀⠀⠀⢀⠀⠀⠀⡆⠀⠘⠀⠀⠪⢴⢸⠙⠊⠉⠓⠀⠀⠀⠀⠀⠘⠯⠞⠁⠹⡹⠐⠀⠁⠀⡇
⠀⠀⡰⠁⠙⢦⡀⠘⡄⠀⠑⠄⣀⢹⢸⡄⠀⠀⠀⠀⠀⠤⠀⠀⠀⠀⠀⣠⡃⡇⡀⠀⠀⢀⠇
⠀⡜⠁⠀⠀⠀⠑⢄⠈⢦⠀⠀⠀⠹⡘⡌⣢⠤⣀⣀⣀⣀⣀⣀⡠⠴⠚⠓⡇⡏⢀⣠⠔⠊⠀
⢰⠁⠀⠀⠀⠀⠀⠈⢢⠀⠑⠒⠒⠒⢣⣩⣀⡞⠉⡽⢄⣀⣵⠛⢭⠑⡖⢲⣳⠉⠁⠀⠀⠀⠀
⡇⠀⠀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⢎⠀⡼⠀⠀⠀⠋⣻⠢⠀⠈⢇⠺⡘⠁⠀⠀⠀⠀⠀⠀
⠉⠉⠉⠑⠒⠢⣄⠀⢀⠜⠀⠀⠀⠀⡌⠀⣇⠀⠀⠀⢸⠝⣆⠀⠀⠸⡀⢱⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⠎⠀⠠⠧⡤⢄⡀⠀⠀⠡⡀⠙⠀⠀⠀⢪⠀⡟⠀⠀⠀⡇⡜⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⠒⠠⠴⢮⣁⠀⡇⠀⠀⢰⠉⢢⣄⡀⠀⢸⠄⡇⠀⠀⡠⠋⢱⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⠎⠀⠑⢤⠎⠁⠀⠀⠙⠫⣍⠁⠀⡽⠒⠋⠀⠀⠀⠑⢆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠑⠒⣼⣀⠠⡪⠭⠩⢔⠄⠑⡎⢀⠀⣀⠤⡀⠀⠀⠈⣧⣀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠊⠉⡠⠐⠛⠂⠤⠀⠀⠙⢄⠅⠀⠀⡠⠇⠓⠒⠓⡙⠀⠀⠑⣄⠀
⠀⠀⠀⠀⠀⠀⠀⢠⠎⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠀⠀⠀⠀⠀⢀⣀⡇⡀⠀⠀⠈⢢
⠀⠀⠀⠀⠀⠀⠀⠸⣀⣠⠤⠬⠮⠶⠒⠒⠤⠤⠤⠴⠢⠬⠥⠀⠄⠍⠍⠉⠀⠀⠀⠄⠠⠀⠈
    """
    + Fore.RESET,
    Fore.LIGHTRED_EX + "\nWelcome to Dependency! ~ Made By Avieah" + Fore.RESET,
    Fore.LIGHTRED_EX + "Type '!help' for available commands.\n" + Fore.RESET,
)


async def display_startup_message():
    # Print the welcome messages
    for message in WELCOME_MESSAGES:
        print(message)


# if the console is clear it still display the message
async def start_prompt():
    try:
        ps4 = PS4Manager()
        while True:
            command = await asyncio.to_thread(
                input, f"{Fore.LIGHTRED_EX}> {Fore.RESET}"
            )
            if command.strip() == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                for message in WELCOME_MESSAGES:  # Print the welcome messages again
                    print(message)
            else:
                await handle_input(command, ps4)
    except asyncio.CancelledError:
        print(f"{Fore.LIGHTRED_EX}Prompt cancelled. Exiting...{Fore.RESET}")
