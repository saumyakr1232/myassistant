import datetime
from assist.utils.helper import  get_directory


def note(text):
    date = datetime.datetime.now()
    directory = get_directory('notes')
    path = directory / f"{text[:5]}-{date.timestamp()}-note.txt"

    with open(path, "w") as f:
        f.write(text)

    # proc = subprocess.Popen(["gedit", file_name])
    # # proc.wait() #to wait until you close the gedit
    # time.sleep(5)
    # proc.kill()

    return f"Notes saved in {str(directory.absolute())}"


if __name__ == '__main__':
    note("TEsting")
