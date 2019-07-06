#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ATFramework import *

class TestCase(unittest.TestCase):

    def __getattr__(self, item):
        try:
            return  self.__getattribute__(item)
        except:
            attrvalue = None
            self.__setattr__(item,attrvalue)
            return attrvalue

    def __init__(self,methodName='runTest'):
        super(TestCase,self).__init__(methodName)

        if Var.dataId:
            for dataId,data in Var.dataCombo_list.items():
                if Var.dataId == dataId:
                    for key,value in data.items():
                        setattr(self,key,value)

    def run(self,result=None):
        '''

        :param result:
        :return:
        '''
        try:
            LogInfo('\n')
            LogInfo("******************* TestCase {} Start *******************".format(self.description_data))
            unittest.TestCase.run(self, result)
        except Exception as e:
            raise e
