#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: Cedar
# @Date  : 2020/6/4
# @Desc  :


import socket
import socks
import requests

socks.set_default_proxy(socks.HTTP, "192.168.1.55", 4411)
socket.socket = socks.socksocket
print(requests.get('http://ifconfig.me/ip').text)

