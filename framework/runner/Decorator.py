#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from framework import *

def keywords(func,*args,**kwds):
    def wrapper(*args,**kwds):
        result = None
        try:
            if len(args) or len(kwds):
                result = func(*args,**kwds)
            else:
                result = func()
        except Exception as e:
            raise e
        return result
    return wrapper