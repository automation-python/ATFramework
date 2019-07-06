#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import unittest
from ATFramework import *
from ATFramework.runner import HTMLTestRunner
from ATFramework.utils.yamlUtils import *
from ATFramework import xmlrunner

if Var.ROOT:
    Var.Total = 0
    Var.Pass = 0
    Var.Failed = 0
    Var.Error = 0
    Var.reprot_time = time.strftime('%Y%d%H%M%S',time.localtime(time.time()))
    Var.Report = os.path.join(Var.ROOT,"Report",Var.reprot_time)

    LogInfo("Report:{}".format(Var.Report))
    if not os.path.exists(Var.Report):
        os.makedirs(Var.Report)

    LogInfo(Loging(logging.INFO))


def projectInit():
    '''
    解析脚本
    :return:
    '''

    Var.datalist = []
    Var.logiclist = []
    Var.dataCombo_list
    pathlsit = []

    LogInfo("******************* Start parsing the scripts file *******************")
    for rt, dirs, files in os.walk(os.path.join(Var.ROOT, "yaml")):
        for f in files:
            scripts_path = os.path.join(rt,f)
            if "yaml" in os.path.splitext(scripts_path)[1]:
                if "data.yaml" in scripts_path:
                    LogInfo(scripts_path)
                pathlsit.append(scripts_path)

    Var.dataCombo_list = getdata(pathlsit)


    LogInfo("******************* Parsing script path *******************")
    if Var.casePath:
        for path in [scripts.strip() for scripts in Var.casePath.strip().split(",")]:
            isExists = False
            if path != "":
                for rt,dirs,files in os.walk(os.path.join(Var.ROOT,"yaml")):
                    if path in files:
                        script = os.path.join(rt,path)
                        if os.path.isfile(script):
                            if "data.yaml" in script:
                                if script not in Var.datalist:
                                    LogInfo(script)
                                    Var.datalist.append(script)
                                    isExists = True
                            if "logic.yaml" in script:
                                if script not in Var.logiclist:
                                    LogInfo(script)
                                    Var.logiclist.append(script)
                                    isExists = True
                for rt, dirs, files in os.walk(os.path.join(Var.ROOT, "yaml")):
                    if path.split(os.sep)[-1] in rt.split(os.sep):
                        for f in files:
                            script = os.path.join(rt,f)
                            if os.path.isfile(script):
                                if "data.yaml" in script:
                                    if script not in Var.datalist:
                                        LogInfo(script)
                                        Var.datalist.append(script)
                                        isExists = True
            if not isExists:
                LogError("{}: does not exist!".format(path),False)
    else:
        for rt, dirs, files in os.walk(os.path.join(Var.ROOT, "yaml")):
            for f in files:
                script = os.path.join(rt,f)
                if "yaml" in os.path.splitext(script)[-1]:
                    if "data.yaml" in script:
                        LogInfo(script)
                        Var.datalist.append(script)


def projectRun():
    '''
    组织用例
    :return:
    '''

    try:

        suite = []
        list = []
        for data_path in Var.datalist:
            for dataId, value in Var.dataCombo_list.items():
                if data_path in value["dataPath"]:
                    if dataId not in list:
                        list.append(dataId)

        for logic_path in Var.logiclist:
            for dataId, value in Var.dataCombo_list.items():
                if logic_path in value["logicPath"]:
                    if dataId not in list:
                        list.append(dataId)

        for dataId in list:
            Var.dataId = dataId
            subsuite = unittest.TestLoader().loadTestsFromTestCase(TestScripts)
            suite.append(subsuite)


        if len(suite):
            suite = unittest.TestSuite(tuple(suite))
            runner = xmlrunner.XMLTestRunner(verbosity=1)
            runner.run(suite)


    except Exception as e:
        raise e