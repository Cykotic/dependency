from colorama import Fore


async def handle_input(command, ps4):
    if command == "!help":
        ps4.display_help()
    elif command == "!connect":
        await ps4.connect()
    elif command == "!getprocesses":
        await ps4.retrieve_and_display_processes()
    elif command == "!reboot":
        await ps4.reboot()
    elif command == "!processinfo":
        await ps4.get_process_info()
    # elif command == "!read_memory":
    #     await ps4.read_memory()
    # elif command == "!write_memory":
    #     await ps4.write_memory()
    elif command == "!scan_memory_changes":
        await ps4.scan_memory_changes()
    elif command == "!attach_debugger":
        await ps4.attach_debugger()
    # elif command == "!crash_game":
    #     await ps4.crash_game()
    else:
        print(f"{Fore.LIGHTRED_EX}Unknown command: {command}")