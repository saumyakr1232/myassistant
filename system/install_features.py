try:
    from sys import platform
    from termcolor import cprint
    import os
except:
    pass


# pip3 install SpeechRecognition

def install_command_system():
    x = platform.lower()
    pt = '-' * 17 + "Installing voice command system" + '-' * 17
    cprint(pt, 'magenta')
    print()
    s = """ Packages are need to install,\n\n\t1)SpeechRecognition\n\t2)Py_Audio\n\n If you face any problem, install them manually.\n"""
    cprint(s, 'yellow')
    if 'linux' in x:
        cprint("System : Linux", 'green')
        os.system('pip3 install SpeechRecognition')
        os.system('sudo apt-get install python3-pyaudio')
    elif 'darwin' in x:
        cprint("System : Mac Os", 'green')
        os.system('pip3 install SpeechRecognition')
        os.system('brew install portaudio')
        os.system('python3 -m pip install pyaudio')
        os.system('python3 -m pip install numpy')

    elif 'win' in x:
        cprint("System : Windows", 'green')
        os.system('pip install SpeechRecognition')
        os.system('python -m pip install pyaudio')
        os.system('python -m pip install numpy')
    else:
        cprint("Can't determine the system. Sorry sir.", 'red')

    print()
    cprint('-' * len(pt), 'magenta')


# pip install pyttsx3

def install_speaking_system():
    x = platform.lower()
    pt = '-' * 17 + "Installing speaking system" + '-' * 17
    cprint(pt, 'magenta')
    print()
    s = """ Packages are need to install,\n\n\t1)pyttsx3\n\n\t2)espeak/gespeaker\n\n If you face any problem, install them manually.\n"""
    cprint(s, 'yellow')

    if 'linux' in x:
        cprint("System : Linux", 'green')
        os.system('pip3 install pyttsx3')
        cprint('\nWhich linux distribution are you using ? ', 'cyan')
        cprint('\n 1)debian-based\n 2)Arch-based\n 3)Other')
        cprint('\nEnter the index number : ', 'cyan', end='')
        index = int(input())
        if index == 2:
            cprint(' Installing Gespeaker ...', 'green')
            os.system('yay -S gespeaker')
        elif index == 1:
            cprint(' Installing espeak ...', 'green')
            os.system('sudo apt-get install espeak')
        else:
            cprint(" If your voice reply don't work you need install espeak/gespeaker manually", 'red')

    elif 'darwin' in x:
        cprint("System : Mac Os", 'green')
        os.system('pip3 install pyttsx3')
    elif 'win' in x:
        cprint("System : Windows", 'green')
        os.system('pip install pypiwin32')
    else:
        cprint("Can't determine the system. Sorry sir.", 'red')

    print()
    cprint('-' * len(pt), 'magenta')


def speed_up():
    pt = '-' * 17 + "Speeding up system" + '-' * 17
    cprint(pt, 'magenta')
    print()
    s = """ Packages are need to install,\n\n\t1)python-Levenshtein-wheels\n\t2)python-Levenshtein\n\n If you face any problem, install them manually.\n"""
    cprint(s, 'yellow')

    os.system("pip3 install python-Levenshtein-wheels")
    os.system("pip3 install python-Levenshtein")

    print()
    cprint('-' * len(pt), 'magenta')


if __name__ == "__main__":
    speed_up()
