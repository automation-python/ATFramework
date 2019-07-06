#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ATFramework import *


def register(ages,user,password,code):
    LogInfo("注册账号")
    LogInfo("user:{}".format(user))
    LogInfo("password:{}".format(password))
    LogInfo("code:{}".format(code))
    ages.token = "sdasdlf24034893"
    return ages

def login(ages,user,password):
    LogInfo("登录")
    if "admin" in user and "admin123456" in password:
        LogInfo("登录成功！")
    else:
        LogInfo("登录失败！")
    LogInfo(ages.token)
    return ages


def pay(ages,orderid):
    LogInfo("提交支付")
    LogInfo(orderid)
    return ages

def querypay(ages,orderid,state):
    LogInfo("轮询支付结果")
    LogInfo(orderid)
    return ages