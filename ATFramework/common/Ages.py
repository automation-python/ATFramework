#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Ages(object):
    def __getattr__(self, item):
        try:
            return object.__getattribute__(item)
        except:
            attrvalue = None
            return attrvalue
    def __setattr__(self, key, value):
       object.__setattr__(self,key,value)

    def __Delattr__(self):
        try:
            for attr in self.__dir__():
                if "__" not in attr:
                    delattr(self, attr)
        except Exception as e:
            print(e)
ages = Ages()