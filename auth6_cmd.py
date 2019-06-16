#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'WZ'

import auth_lib
import sys

login_url = "https://auth6.tsinghua.edu.cn"


def main():
    par = 'login'
    if len(sys.argv) > 1:
        par = sys.argv[-1]
    else:
        print('default action=login')
    if 'in' in par:
        print('logging in')
        auth_lib.check_result(auth_lib.go_online(login_url))
    else:
        print('logging out')
        auth_lib.check_result(auth_lib.go_offline(login_url))


if __name__ == "__main__":
    main()

