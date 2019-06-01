#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ATFramework import *

def register(map,user,password,code):
    LogInfo("注册账号")
    LogInfo("user:{}".format(user))
    LogInfo("password:{}".format(password))
    LogInfo("code:{}".format(code))
    map.token = "sdasdlf24034893"
    return map

def login(map,user,password):
    LogInfo("登录")
    if "admin" in user and "admin123456" in password:
        LogInfo("登录成功！")
    else:
        LogInfo("登录失败！")
    LogInfo(map.token)
    return map


def pay(map,orderid):
    LogInfo("提交支付")
    LogInfo(orderid)
    return map

def querypay(map,orderid,state):
    LogInfo("轮询支付结果")
    LogInfo(orderid)
    map.self.assertEqual(state,"200")
    return map