#!/usr/bin/python3

from getpass import getpass
import requests
import sys
import os

HOST = "https://remotewifi-master.piasco.repl.co/"

def info(msg):
    if msg[0] == '\r':
        print(end='\r')
        msg = msg[1:]
    print(f"[\33[2m+\33[0m] {msg}")

def warn(msg):
    if msg[0] == '\r':
        print(end='\r')
        msg = msg[1:]
    print(f"[\33[93m!\33[0m] {msg}")

def error(msg):
    if msg[0] == '\r':
        print(end='\r')
        msg = msg[1:]
    print(f"/\33[91m!\33[0m\\ {msg}")

def clear():
    if os.name == "nt":
        # berk
        os.system("cls")
    else:
        os.system("clear")

def print_dict(dic: dict):
    if not len(dic.keys()):
        print("\tEmpty")
        return
    key_length = max([len(str(k)) for k in dic.keys()]) + 2
    val_length = max([len(str(v)) for v in dic.values()]) + 2
    print("\t+" + ("-" * key_length) + "+" + ("-" * val_length) + "+")
    for key, value in dic.items():
        print(f"\t|{str(key):^{key_length}}|{str(value):^{val_length}}|")
        print("\t+" + ("-" * key_length) + "+" + ("-" * val_length) + "+")
    print()

def join_link(*args):
    total = ""
    total += args[0]
    terminated_with_slash = total[-1] == '/'
    for arg in args[1:]:
        if terminated_with_slash:
            if arg[0] == '/':
                total += arg[1:]
            else:
                total += arg
        else:
            if arg[0] == '/':
                total += arg
            else:
                total += '/'
                total += arg
        terminated_with_slash = total[-1] == '/'
    return total

def is_ip(ip: str):
    if ip.count('.') != 3:
        return False
    for n in ip.split('.'):
        if not n.isalnum():
            return False
        if int(n) < 0 or int(n) > 255:
            return False
    return True

def is_good_link(link: str):
    if link.count(':') != 1:
        return False
    if not is_ip(link.split(':')[0]):
        return False
    if not link.split(':')[1].isalnum():
        return False
    return True

def connect_to_server(client_ip: str, client_port: int):
    os.system(f"sudo sshuttle --dns -r root@{client_ip}:{client_port} 0/0")

def get_clients_list():
    return requests.get(join_link(HOST, "/api/list")).json()

def banner():
    spaces = (os.get_terminal_size()[0] - 62) // 2
    print(F"""
{' ' * spaces} _____                      _        __          ___ ______ _ 
{' ' * spaces}|  __ \                    | |       \ \        / (_)  ____(_)
{' ' * spaces}| |__) |___ _ __ ___   ___ | |_ ___   \ \  /\  / / _| |__   _ 
{' ' * spaces}|  _  // _ \ '_ ` _ \ / _ \| __/ _ \   \ \/  \/ / | |  __| | |
{' ' * spaces}| | \ \  __/ | | | | | (_) | ||  __/    \  /\  /  | | |    | |
{' ' * spaces}|_|  \_\___|_| |_| |_|\___/ \__\___|     \/  \/   |_|_|    |_|

""")

def main():
    try:
        while 1:
            clear()
            banner()
            info("Retreiving clients list")
            print()
            try:
                liste = get_clients_list()
            except requests.ConnectionError:
                error("Couldn't connect to the server.")
                sys.exit(1)
            for k, v in liste.items():
                print(f"Server \"{k}\" :")
                print_dict(v)
            if not len(liste):
                warn("No servers found. Exiting...")
                sys.exit(0)
            srv = input("[?] Enter the name of the server you want to connect to : ")
            while not srv in liste.keys():
                warn("The name you entered does not exists !")
                srv = input("[?] Enter the name of the server you want to connect to : ")
            link = liste[srv].get("link")
            if not link:
                error("This server does not provide link !")
                input("[?] Press enter to continue, or Ctrl+C to stop the client.")
                continue
            if not is_good_link(link):
                error("The provided link is not correct !")
                input("[?] Press enter to continue, or Ctrl+C to stop the client.")
                continue
            info(f"Connecting to server \"{srv}\"...")
            connect_to_server(link.split(':')[0], link.split(':')[1])
    except KeyboardInterrupt:
        info("\rClosing client...")
        sys.exit(1)

if __name__ == "__main__":
    main()
