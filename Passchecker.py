#!/usr/bin/env python3
"""
PASSCHECKER - Random ASCII banners with colors
Password strength assessor with repeat option (Y/N).
"""

import re
import random
import shutil
import sys
import termios
import tty
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Multiple ASCII banners
BANNERS = [
r"""
  ____   ___   ____  _____ _   _  _____ _    ____ _  __
 |  _ \ / _ \ / ___|| ____| \ | |/ ____| |  / ___| |/ /
 | |_) | | | | |  _ |  _| |  \| | (___ | | | |   | ' / 
 |  __/| |_| | |_| || |___| |\  |\___ \| | | |___| . \ 
 |_|    \___/ \____||_____|_| \_|_____/|_|  \____|_|\_\
""",
r"""
██████╗  █████╗ ███████╗███████╗ ██████╗██╗  ██╗███████╗ ██████╗██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔════╝██╔══██╗
██████╔╝███████║███████╗███████╗██║     █████╔╝ █████╗  ██║     ██████╔╝
██╔═══╝ ██╔══██║╚════██║╚════██║██║     ██╔═██╗ ██╔══╝  ██║     ██╔═══╝ 
██║     ██║  ██║███████║███████║╚██████╗██║  ██╗███████╗╚██████╗██║     
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝     
""",
r"""
 ____   ___   ____   ____  ____ _  __ _____ ____  ____  _____ ____  
|  _ \ / _ \ / ___| / ___||  _ \ |/ /| ____|  _ \|  _ \| ____|  _ \ 
| |_) | | | | |  _  \___ \| | | | ' / |  _| | |_) | | | |  _| | |_) |
|  __/| |_| | |_| |  ___) | |_| | . \ | |___|  __/| |_| | |___|  _ < 
|_|    \___/ \____| |____/|____/|_|\_\|_____|_|   |____/|_____|_| \_\
"""
]

COLORS = [Fore.RED, Fore.GREEN, Fore.CYAN, Fore.YELLOW, Fore.MAGENTA, Fore.LIGHTBLUE_EX]

def show_banner():
    """Print a random banner in random color with centered rainbow subtitle"""
    banner = random.choice(BANNERS)
    banner_color = random.choice(COLORS)

    # Get terminal width
    term_width = shutil.get_terminal_size().columns
    subtitle = "WELCOME TO PASSCHECKER - A Simple Password Strength Tool"

    print(banner_color + banner + Style.RESET_ALL)

    # Print subtitle in rotating colors (letter by letter)
    colored_subtitle = ""
    for i, char in enumerate(subtitle):
        color = random.choice(COLORS)
        colored_subtitle += color + char
    print(colored_subtitle.center(term_width) + Style.RESET_ALL + "\n")

def input_password(prompt="Enter the password to check: "):
    """Password input that shows asterisks instead of hiding input."""
    print(prompt, end="", flush=True)
    password = ""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch == "\n" or ch == "\r":
                print("")
                break
            elif ch == "\x7f":  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                password += ch
                sys.stdout.write("*")
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return password

def analyze_password(pw: str) -> dict:
    """Return a dict with criterion booleans and computed strength."""
    criteria = {
        'length': len(pw) >= 8,
        'upper' : bool(re.search(r'[A-Z]', pw)),
        'lower' : bool(re.search(r'[a-z]', pw)),
        'digit' : bool(re.search(r'\d', pw)),
        'special': bool(re.search(r'[^A-Za-z0-9]', pw)),
    }

    # Strength calculation
    if not criteria['length']:
        strength = 'WEAK'
    else:
        classes_present = sum([criteria['upper'], criteria['lower'], criteria['digit'], criteria['special']])
        if classes_present <= 1:
            strength = 'WEAK'
        elif classes_present <= 3:
            strength = 'MEDIUM'
        else:
            strength = 'STRONG'

    score_points = (1 if criteria['length'] else 0) + sum([criteria['upper'], criteria['lower'], criteria['digit'], criteria['special']])
    score_percent = int((score_points / 5) * 100)

    return {
        'criteria': criteria,
        'strength': strength,
        'score_points': score_points,
        'score_percent': score_percent
    }

def give_feedback(result: dict) -> list:
    """Return actionable suggestions to improve the password."""
    c = result['criteria']
    suggestions = []
    if not c['length']:
        suggestions.append("Make it at least 8 characters long (12+ recommended).")
    if not c['upper']:
        suggestions.append("Add at least one UPPERCASE letter (A-Z).")
    if not c['lower']:
        suggestions.append("Add at least one lowercase letter (a-z).")
    if not c['digit']:
        suggestions.append("Add at least one digit (0-9).")
    if not c['special']:
        suggestions.append("Add at least one special character (e.g. !@#$%^&*).")

    if not suggestions:
        suggestions.append("Good! For stronger security, use a passphrase or 16+ characters.")
    return suggestions

def print_report(result: dict):
    c = result['criteria']

    # Strength color mapping
    strength_colors = {
        "WEAK": Fore.RED,
        "MEDIUM": Fore.YELLOW,
        "STRONG": Fore.GREEN
    }
    strength_colored = strength_colors[result['strength']] + result['strength'] + Style.RESET_ALL

    print("\nPassword Strength Report")
    print("------------------------")
    print(f"Strength : {strength_colored}")
    print(f"Score    : {result['score_points']}/5 ({result['score_percent']}%)")
    print("\nChecks:")
    print(f" - Length >= 8 : {'OK' if c['length'] else 'NO'}")
    print(f" - Contains UPPERCASE letter  : {'YES' if c['upper'] else 'NO'}")
    print(f" - Contains lowercase letter  : {'YES' if c['lower'] else 'NO'}")
    print(f" - Contains digit             : {'YES' if c['digit'] else 'NO'}")
    print(f" - Contains special character : {'YES' if c['special'] else 'NO'}")
    print("\nSuggestions:")
    for s in give_feedback(result):
        print(f" * {s}")
    print()

def main():
    show_banner()
    try:
        while True:
            password = input_password("Enter the password to check: ")
            if not password:
                print("No password entered. Exiting.")
                break

            result = analyze_password(password)
            print_report(result)

            # Ask if user wants another check
            choice = input("Do you want to perform another check? (Y/N): ").strip().lower()
            if choice not in ['y', 'yes']:
                print("\nGoodbye.")
                break
            print()  # blank line before next check
    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled. Goodbye.")

if __name__ == "__main__":
    main()
