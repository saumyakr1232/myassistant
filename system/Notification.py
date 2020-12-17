from plyer import notification


# fixme : problem on linux

def notifyMe(title, message, icon):
    notification.notify(
        title=title,
        message=message,
        app_icon=icon,
        timeout=5
    )


# ph5ec3f51f6901f


def main():
    message = "sir there is a political debate is going on in \'Backchod University\' group "
    icon_path = r"F:\covid-19\head.ico"
    title = "Unexpected"
    notifyMe(title, message, icon_path)


if __name__ == '__main__':
    main()
