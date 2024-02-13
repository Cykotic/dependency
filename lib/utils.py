from colorama import Fore
import re
from ps4debug import PS4Debug, PS4DebugException
import functools
import asyncio


class PS4Manager:
    def __init__(self):
        self.connected = False
        self.ps4 = None

    async def get_ip_address(self):
        return input(
            f"{Fore.LIGHTRED_EX}Enter the IP address of your PS4: {Fore.RESET}"
        )

    async def connect(self):
        if self.connected:
            print(f"{Fore.LIGHTRED_EX}You are already connected to the PS4.")
            return

        ip_address = await self.get_ip_address()
        if not self.is_valid_ip(ip_address):
            print(
                f"{Fore.LIGHTRED_EX}Invalid IP address. Please provide a valid IP address."
            )
            return

        try:
            self.ps4 = PS4Debug(ip_address)
            self.connected = True
            print(f"{Fore.LIGHTRED_EX}PS4 console connected successfully.")
            await self.ps4.notify("You are now connected to the PS4 console.")

        except PS4DebugException as e:
            print(
                f"{Fore.LIGHTRED_EX}Error: Failed to connect to the PS4 console at {ip_address}. Reason: {e}"
            )
            print(
                f"{Fore.LIGHTRED_EX}Make sure PS4debug is running on your console and the IP address is correct."
            )
        except Exception as ex:
            print(
                f"{Fore.LIGHTRED_EX}An unexpected error occurred while connecting to the PS4 console: {ex}"
            )

    async def retrieve_and_display_processes(self):
        if not self.connected or self.ps4 is None:
            print(
                f"{Fore.LIGHTRED_EX}Error: Please connect to the PS4 console first using '!connect'."
            )
            return

        try:
            processes = await self.ps4.get_processes()
            if not processes:
                print("No processes running.")
            else:
                for p in processes:
                    print(p.name, p.pid)

                process_name = "eboot.bin"
                pid = next((p.pid for p in processes if p.name == process_name), None)

                if pid is None:
                    print(process_name, "is not running!")
                else:
                    print(f"PID for {process_name}: {pid}")
        except PS4DebugException as e:
            print(
                f"{Fore.LIGHTRED_EX}Error: Failed to retrieve process information. Reason: {e}"
            )

    async def get_process_info(self):
        if not self.connected or self.ps4 is None:
            print(
                f"{Fore.LIGHTRED_EX}Error: Please connect to the PS4 console first using '!connect'."
            )
            return

        pid_input = input("Enter the PID of the process: ")
        if not pid_input.isdigit():
            print(f"{Fore.LIGHTRED_EX}Error: PID must be a numerical value.")
            return

        pid = int(pid_input)

        try:
            process_info = await self.ps4.get_process_info(pid)
            if process_info:
                print(f"Process info for PID {pid}: {process_info}")
        except PS4DebugException as e:
            print(
                f"{Fore.LIGHTRED_EX}Error: Failed to retrieve process information. Reason: {e}"
            )

    async def read_memory(self, pid, address):
        try:
            if self.ps4 is None:
                print(
                    f"{Fore.LIGHTRED_EX}Error: Please connect to the PS4 console first using '!connect'."
                )
                return None

            value = await self.ps4.read_int32(pid=pid, address=address)
            return value
        except Exception as e:
            print(
                f"Error reading memory at address {hex(address)} for process with PID {pid}: {e}"
            )
            return None

    async def write_memory(self):
        try:
            if self.ps4 is None:
                print(
                    f"{Fore.LIGHTRED_EX}Error: Please connect to the PS4 console first using '!connect'."
                )
                return

            pid = int(input("Enter the PID of the process: "))
            address = int(input("Enter the memory address (in hexadecimal): "), 16)
            value = int(input("Enter the value to write: "))
            print(
                f"Writing value {value} to memory address {hex(address)} for process with PID {pid}..."
            )
            write_memory_partial = functools.partial(
                self.ps4.write_int32, pid=pid, address=address
            )
            await write_memory_partial(value=value)
            print("Value written successfully.")
        except ValueError:
            print("Invalid PID, address, or value.")
        except Exception as e:
            print(
                f"Error writing value {value} to memory address {hex(address)} for process with PID {pid}: {e}"
            )

    async def reboot(self):
        if not self.connected:
            print(
                f"{Fore.LIGHTRED_EX}Error: Please connect to the PS4 console first using '!connect'."
            )
            return

        try:
            await self.ps4.reboot()
            print("PS4 rebooting...")
        except PS4DebugException as e:
            print(f"{Fore.LIGHTRED_EX}Error: Failed to reboot the PS4. Reason: {e}")

    async def scan_memory_changes(self):
        try:
            if self.ps4 is None:
                print(
                    f"{Fore.LIGHTRED_EX}Error: Please connect to the PS4 console first using '!connect'."
                )
                return None

            pid = int(input("Enter the PID of the process: "))
            address = int(input("Enter the memory address (in hexadecimal): "), 16)
            value = int(input("Enter the value to monitor for changes: "), 16)

            print(
                f"Monitoring memory changes for value {(value)} in process with PID {pid}..."
            )

            # print(
            #     f"Monitoring memory changes for value {hex(value)} in process with PID {pid}..."
            # )

            previous_value = await self.ps4.read_int32(pid=pid, address=address)
            if previous_value is None:
                print("Unable to read initial memory value.")
                return

            while True:
                current_value = await self.ps4.read_int32(pid=pid, address=address)
                if current_value != previous_value:
                    print(
                        f"Memory value changed: Previous value: {(previous_value)}, Current value: {(current_value)}"
                    )
                    # print(
                    #     f"Memory value changed: Previous value: {hex(previous_value)}, Current value: {hex(current_value)}"
                    # )
                    previous_value = current_value
                await asyncio.sleep(1)

        except ValueError:
            print("Invalid PID, address, or value.")
        except Exception as e:
            print(
                f"Error monitoring memory for value {(value)} in process with PID {pid}: {e}"
            )

    # async def attach_debugger(self):
    #     try:
    #         pid = int(input("Enter the PID of the process: "))
    #         address = int(input("Enter the memory address (in hexadecimal): "), 16)

    #         async with self.ps4.debugger(pid, resume=True) as debugger:

    #             async def breakpoint_hit(event):
    #                 print(f"Breakpoint hit at address {(event.address)}!")
    #                 # Handle breakpoint hit event

    #             await debugger.set_breakpoint(0, True, address, on_hit=breakpoint_hit)
    #             debugger.register_callback(breakpoint_hit)
    #             await asyncio.Event().wait()

    #     except ValueError:
    #         print("Invalid PID or address.")
    #     except Exception as e:
    #         print(f"Error attaching debugger: {e}")

    @staticmethod
    def is_valid_ip(ip):
        # Regular expression to match the IP address format
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        return bool(re.match(ip_pattern, ip))

    @staticmethod
    def display_help():
        print(f"{Fore.LIGHTRED_EX}\nAvailable Commands:{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}!connect{Fore.RESET} - Connect to the PS4 console")
        print(
            f"{Fore.LIGHTRED_EX}!getprocesses{Fore.RESET} - Retrieve a list of processes running on the system"
        )
        print(
            f"{Fore.LIGHTRED_EX}!processinfo{Fore.RESET} - Retrieve detailed information about a specific process"
        )
        print(f"{Fore.LIGHTRED_EX}!reboot{Fore.RESET} - Reboot the console")
        print(
            f"{Fore.LIGHTRED_EX}!scan_memory_changes{Fore.RESET} - Monitor changes in memory values at a specific address"
        )
        print(
            f"{Fore.LIGHTRED_EX}!attach_debugger{Fore.RESET} - Attach debugger to a process and monitor for breakpoints"
        )
        print(
            f"{Fore.LIGHTRED_EX}!crash_game{Fore.RESET} - Crash the game process by writing to a specific memory address"
        )
