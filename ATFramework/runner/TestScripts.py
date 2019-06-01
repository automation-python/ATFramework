#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ATFramework.runner.TestCase import *
from ATFramework import *

class TestScripts(TestCase):


    def setUp(self):
        map.self = self

    def testCase(self):
        try:
            for func in self.func:
                LogInfo("Step:{}".format(func))
                map = eval(func)
        except Exception as e:
            raise eval()

    def tearDown(self):
        map.__Delattr__()

