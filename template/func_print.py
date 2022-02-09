from import_libs import install_if_nonexistent
install_if_nonexistent('colorama')
from colorama import Fore, Style


def final_message(msg, signature, n):
    green_bar = Style.BRIGHT + Fore.GREEN + '|' + Style.RESET_ALL + Fore.RESET
    for i in msg.split('\n'):
        print(green_bar + ' ' + i + (n - len(i)) * ' ' + ' ' + green_bar)
    print(green_bar + ' ' + n * ' ' + ' ' + green_bar)
    for i in signature.split('\n'):
        line = ' {:>' + str(n) + '} '
        line = line.format(i)
        print(green_bar + line + green_bar)


def division(n):
    print(Style.BRIGHT + Fore.GREEN + '# ' + n * '=' + ' #' + Style.RESET_ALL + Fore.RESET)


def section(n, string):
    print(Style.BRIGHT + Fore.GREEN + '# ' + n * '=' + ' #' + Style.RESET_ALL + Fore.RESET)
    print(Style.BRIGHT + Fore.GREEN + string + Style.RESET_ALL + Fore.RESET)