#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ATFramework import *
import requests
import json
import time


@keywords
def register(ages,userName,password,authCode):

    Step("注册")
    url = 'http://47.110.43.11/kasa/user/register'
    body = {
        "userName":userName,
        "password":password,
        "authCode":authCode
    }
    Step('请求参数：{}'.format(body))
    response = requests.post(url=url,data=body)
    if response.ok:
        result = json.loads(response.text)
        Step('返回参数：{}'.format(result))
        assert result['code'] == 200
    time.sleep(2)
    return ages

@keywords
def login(ages,userName,password,token):

    Step("登录")
    url = 'http://47.110.43.11/kasa/user/login'
    headers = {"token":token}
    body = {
        "userName":userName,
        "password":password
    }
    Step('请求参数：{}'.format(body))
    response = requests.post(url=url,data=body,headers=headers)
    if response.ok:
        result = json.loads(response.text)
        Step('返回参数：{}'.format(result))
        assert result['code'] == 200
    time.sleep(2)
    return ages


@keywords
def error(ages):
    Step('失败')
    a = 'test'
    time.sleep(2)
    return  a + 1


if __name__ == "__main__":
    pass