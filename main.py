import asyncio
from colorama import init
from lib.user_interface import display_startup_message, start_prompt


async def main():
    await display_startup_message()
    await start_prompt()


if __name__ == "__main__":
    init(autoreset=True)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
