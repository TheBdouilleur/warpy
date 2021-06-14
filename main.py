import sys
import time
import subprocess
import webbrowser
import pystray
from PIL import Image, ImageDraw

SU_PASSWORD = 'bob'


class CommandError(Exception):
    pass


def create_ui():
    warp_checkbox = pystray.MenuItem(
        'Warpified', on_clicked, checked=lambda item: state)
    warpplus_checkbox = pystray.MenuItem(
        'Get Warp+ data', on_clicked, checked=lambda item: warpplus_state) 
    quit_button = pystray.MenuItem('Quit warpy', on_clicked)
    help_button = pystray.MenuItem('Get help', on_clicked)
    menu = pystray.Menu(
        warp_checkbox,
        warpplus_checkbox,
        quit_button,
        help_button
    )

    icon = pystray.Icon('Warpy', load_image('icon.png'), menu=menu)
    return icon


def load_image(path):
    image = Image.open(path)
    return image


def on_clicked(icon, item):
    print(f"[+] '{item.text}' button pressed")
    if item.text == "Quit warpy":
        print("[-] Quitting...")
        ui.stop()
        sys.exit(0)
    elif item.text == "Warpified":
        global state
        command = f'sudo -S wg-quick {"down" if state else "up"} wgcf-profile'.split()
        try:
            print(f"[*] Running command {command}")
            print(f'[*] Providing sudo with password "{SU_PASSWORD}"')
            process = subprocess.run(command, input=bytes(
                f'{SU_PASSWORD}\n', 'utf-8'), capture_output=True)
            if process.returncode != 0:
                raise(CommandError(
                    f"Command returned code {process.returncode} and message {process.stderr}"))
        except Exception as e:
            print("[!] An error occured while running command:")
            print(f"[!] {type(e)}\n{str(e)}")
        else:
            print(
                f"[*] Successfully {'activated' if not state else 'deactivated'} Warp")
            state = not item.checked
            print(f"[*] Toggling check")
    elif item.text == "Get Warp+ data":
        print(f"")
        extract_warpplus_data()
    elif item.text == "Get help":
        webbrowser.open("https://github.com/TheBdouilleur/warpy/issues")
        print("[*] Opened issue page on default web browser.")

def extract_warpplus_data():
    pass

process = subprocess.run(['wgcf', 'trace'], capture_output=True)
state = b"warp=on" in process.stdout
warpplus_state = False
print("[+] Starting...")
print(f"[*] Warp is {'on' if state else 'off'}")
ui = create_ui()
try:
    ui.run()
except KeyboardInterrupt:
    print("[!] Aborted by user.")
    ui.stop()
    sys.exit("aborted")
except Exception as e:
    print("[!] An error occured while running mainloop:")
    print(f"[!] {type(e)}\n{str(e)}")

