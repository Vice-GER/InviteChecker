import requests
from colorama import Fore
import json
import time
from os import system


def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return int(config['good'])

def count_lines(inv):
    with open(inv, 'r') as file:
        amount = sum(1 for line in file)
    return int(amount)

def counter(good, bad, checked):
    system(f'title Invite Checker  ^| Checker: Discord ^| Good: {good} ^| Bad: {bad} ^| Checked: {checked}/{amount}')

def checker(goodInvite):
    good = 0
    bad = 0
    checked = 0
    with open('invites.txt', 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            invite = line.strip()  
            response = requests.get(f"https://discord.com/api/invites/{invite}?with_counts=true")
            if response.status_code == 200:
                data = response.json()
                guild_name = data['guild']['name']
                member_count = data['approximate_member_count']
                online = data["approximate_presence_count"]
                boostStats = data["guild"]["premium_subscription_count"]
                with open('used.txt', 'a') as good_file:
                        good_file.write(invite + '\n')
                if member_count >= goodInvite:
                    print(f"{Fore.GREEN}[+] Good Invite | Vanity ➝ {invite} | Name ➝ {guild_name} | Members ➝ {member_count} | Online ➝ {online} | Boosts ➝ {boostStats} {Fore.RESET}")
                    good += 1
                    checked += 1
                    counter(good, bad, checked)
                    with open('good.txt', 'a') as good_file:
                        good_file.write(invite + '\n')
                    with open('invites.txt', 'r') as invites_file:
                        lines = invites_file.readlines()
                    with open('invites.txt', 'w') as invites_file:
                        for line in lines:
                            if line.strip() != invite:
                                invites_file.write(line)
                elif member_count <= goodInvite:
                    print(f"{Fore.MAGENTA}[-] Bad Invite | Vanity ➝  {invite} | Name ➝  {guild_name} | Members ➝  {member_count} | Online ➝  {online} | Boosts ➝  {boostStats} {Fore.RESET}")
                    bad += 1
                    checked += 1
                    counter(good, bad, checked)
                    with open('bad.txt', 'a') as bad_file:
                        bad_file.write(invite + '\n')
                    with open('invites.txt', 'r') as invites_file:
                            lines = invites_file.readlines()
                    with open('invites.txt', 'w') as invites_file:
                        for line in lines:
                            if line.strip() != invite:
                                invites_file.write(line)
                else:
                    print(f"{Fore.LIGHTCYAN_EX}[!] Error Checking Vanity ➝  {invite} {Fore.RESET}")
                    checked += 1
                    with open('invites.txt', 'r') as invites_file:
                            lines = invites_file.readlines()
                    with open('invites.txt', 'w') as invites_file:
                        for line in lines:
                            if line.strip() != invite:
                                invites_file.write(line)
                    continue
            elif response.status_code == 429:
                print(f"{Fore.RED}[!] Ratelimited")

config = load_config()
goodInvite = config

print(f"""{Fore.MAGENTA}
                                            ╦  ╦┬┌─┐┌─┐
                                            ╚╗╔╝││  ├┤ 
                                             ╚╝ ┴└─┘└─┘ 
{Fore.RESET}""")

inv = "invites.txt"
amount = count_lines(inv)

checker(goodInvite)