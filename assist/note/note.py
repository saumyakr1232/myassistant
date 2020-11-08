import datetime
import subprocess


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    proc = subprocess.Popen(["gedit", file_name])
    # proc.wait() #to wait until you close the gedit


if __name__ == '__main__':
    note("alternate")
