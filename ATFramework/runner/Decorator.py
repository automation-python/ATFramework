#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ATFramework import *

def keywords(func,*args,**kwds):
    def wrapper(*args,**kwds):
        result = None
        try:
            if len(args) or len(kwds):
                result = func(*args,**kwds)
            else:
                result = func()

        except Exception as e:

            # 获得异常的详细信息
            message = traceback.format_exc()
            LogError(message,False)
            raise e


        return result
    return wrapper