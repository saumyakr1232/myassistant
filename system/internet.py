import requests


def isNetworkConnectionAvail(host='http://google.com'):
    try:
        requests.get(host, timeout=4)
        return True
    except (requests.ConnectionError, requests.Timeout) as e:
        print("No Internet connection")
        print(e)
        return False


if __name__ == '__main__':
    print(isNetworkConnectionAvail())
