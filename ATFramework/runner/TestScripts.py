#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import copy
from ATFramework.runner.TestCase import *
from ATFramework import *
from ATFramework.common.Ages import ages

class TestScripts(TestCase):


    def setUp(self):
        pass

    def testCase(self):
        try:
            LogInfo(self.steps)
            for func in self.steps:
                if 'Skip' in self.dataItems:
                    if self.dataItems['Skip']:
                        self.skipTest('Skip')
                Step(func)
                eval(func)
        except Exception as e:
            raise e

    def tearDown(self):
        ages.__Delattr__()


