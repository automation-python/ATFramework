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
            for dataId,value in Var.logiclist.items():
                if Var.dataId in dataId:
                    setattr(self,"logicId",value["logicId"])
                    setattr(self,"dataId", value["dataId"])
                    setattr(self,"description_data", value["description_data"])
                    setattr(self,"description_logic", value["description_logic"])
                    setattr(self,"dataPath", value["dataPath"])
                    setattr(self,"logicPath", value["logicPath"])
                    setattr(self,"func", value["steps"])

    def run(self,result=None):
        '''

        :param result:
        :return:
        '''
        try:
            LogInfo("******************* TestCase {} Start *******************".format(self.description_data))
            unittest.TestCase.run(self, result)
        except Exception as e:
            raise e
