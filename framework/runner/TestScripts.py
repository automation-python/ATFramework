#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from framework.runner.TestCase import *
from framework import *
from framework import LogInfo,Step,ages

class TestScripts(TestCase):


    def setUp(self):
        pass

    def testCase(self):
        try:
            LogInfo(self.steps)
            for func in self.steps:
                if self.dataItems.Skip:
                    self.skipTest('Skip')
                Step(func)
                eval(func)
        except Exception as e:
            raise e

    def tearDown(self):
        ages.__Delattr__()


