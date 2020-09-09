import mechanize

if __name__ == '__main__':
    url = "https://lms.galgotiasuniversity.edu.in/login/index.php"

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]

    sign_in = br.open(url)

    br.select_form(id="login")

    br["username"] = "18SCSE1010138"
    br["password"] = "Watermelo@1232"

    logged_in = br.submit()

    response1 = br.open("https://lms.galgotiasuniversity.edu.in/course/view.php?id=43356")

    logincheck = logged_in.read()

    print(logincheck)
    print(type(logincheck))

    print(response1.read())

    with open("result.html", 'w') as f:
        f.write(str(logincheck))
# ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           # 'Windows NT 5.2; .NET CLR 1.1.4322)')