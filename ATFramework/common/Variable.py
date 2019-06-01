#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import config

class Variable(object):
    def __getattr__(self, item):
        try:
            return object.__getattribute__(item)
        except:
            attrvalue = None
            try:
                attrvalue = config.config[item]
            except:
                pass
            return attrvalue
    def __setattr__(self, key, value):
       object.__setattr__(self,key,value)

Var = Variable()