from settings._first_load_ import check_if_first_time
from Main import main
from settings.setting import read_bot
from system.path import getpath
from termcolor import cprint
import sys, os


def get_args(lt, lim):
    get = ''
    for i in range(1, lim):
        get += str(lt[i]) + ' '
    return get.strip()


def all_args(lt):
    ok = False
    arg = ''
    for w in lt:
        if ok:
            arg += w + ' '
        if w == '-arg':
            ok = True
    return arg.strip()


def make_path(arg_list, length):
    path = ''
    flag = False
    for i in range(1, length):
        if arg_list[i] == '-arg':
            break;
        if flag:
            path += ' '
        path += arg_list[i]
        flag = True
    return path


if __name__ == '__main__':
    check_if_first_time()
    try:
        length = len(sys.argv)
        arg_list = list(sys.argv)
        if '-arg' in arg_list:
            original_path = getpath(__file__)
            p = str(sys.argv)
            file_path = make_path(arg_list, length)
            arg = all_args(arg_list)
            # print(arg, file_path)
            main(arg, original_path)
        else:
            arg = get_args(arg_list, len(arg_list))
            main(arg, original_path=os.getcwd())
            # print(arg)

    except Exception as e:
        main(original_path=os.getcwd())
