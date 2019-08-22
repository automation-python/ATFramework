#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import traceback
import unittest
from framework import Var , LogInfo

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
            for dataId,data in Var.linkedData_list.items():
                if Var.dataId == dataId:
                    for key,value in data.items():
                        setattr(self,key,value)

    def run(self,result=None):
        '''

        :param result:
        :return:
        '''
        try:

            Var.CaseMessage = ""
            Var.CaseStepIndex = 0
            Var.SnapshotIndex = 0

            LogInfo('\n')
            LogInfo("******************* TestCase {} Start *******************".format(self.description_data))
            unittest.TestCase.run(self, result)
            LogInfo("********************Total: %s, Pass: %s, Failed: %s, Error: %s, Skipped: %s ********************" % (
                result.testsRun,len(result.successes),len(result.failures),len(result.errors),len(result.skipped)))
        except Exception as e:
            raise e
