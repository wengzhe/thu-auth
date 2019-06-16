#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'WZ'

import auth_lib

login_url = {
            'IPv4': "https://auth4.tsinghua.edu.cn",
            'IPv6': "https://auth6.tsinghua.edu.cn"
            }


def check_online():
    for key in login_url:
        ip_addr = auth_lib.get_data(login_url[key])
        if len(ip_addr):
            print(key, 'is not online!')
            print(auth_lib.go_online(login_url[key], ip_addr[0]))
            return

    print('All Online!')
    return


def main():
    check_online()


if __name__ == "__main__":
    main()

