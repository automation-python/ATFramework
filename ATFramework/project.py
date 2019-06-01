#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import unittest
from ATFramework import *
from ATFramework.runner import HTMLTestRunner
from ATFramework.utils.yamlUtils import *

if Var.ROOT:
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

    suite = []
    Var.datalist = []
    Var.logiclist = []
    pathlsit = []

    LogInfo("******************* Start parsing the scripts file *******************")
    for rt, dirs, files in os.walk(os.path.join(Var.ROOT, "yaml")):
        for f in files:
            scripts_path = os.path.join(rt,f)
            if "yaml" in os.path.splitext(scripts_path)[1]:
                if "data.yaml" in scripts_path:
                    LogInfo(scripts_path)
                pathlsit.append(scripts_path)

    Var.logiclist = getdata(pathlsit)


    LogInfo("******************* Parsing script path *******************")
    if Var.casePath:
        for path in [scripts.strip() for scripts in Var.casePath.strip().split(",")]:
            if path != "":
                for rt,dirs,files in os.walk(os.path.join(Var.ROOT,"yaml")):
                    if path in files:
                        script = os.path.join(rt,path)
                        if os.path.isfile(script):
                            if "data.yaml" in script:
                                LogInfo(script)
                                Var.datalist.append(script)
                                break
                for rt, dirs, files in os.walk(os.path.join(Var.ROOT, "yaml")):
                    if path.split(os.sep)[-1] in rt.split(os.sep):
                        for f in files:
                            script = os.path.join(rt,f)
                            if os.path.isfile(script):
                                if "data.yaml" in script:
                                    LogInfo(script)
                                    Var.datalist.append(script)
    else:
        for rt, dirs, files in os.walk(os.path.join(Var.ROOT, "yaml")):
            for f in files:
                script = os.path.join(rt,f)
                if "yaml" in os.path.splitext(script)[-1]:
                    if "data.yaml" in script:
                        LogInfo(script)
                        Var.datalist.append(script)

    for data in Var.datalist:
        for dataId,value in Var.logiclist.items():
            if data in value["dataPath"]:
                Var.dataId = dataId
                subsuite = unittest.TestLoader().loadTestsFromTestCase(TestScripts)
                suite.append(subsuite)

    try:
        if len(suite):
            suite = unittest.TestSuite(tuple(suite))
            # runner = unittest.TextTestRunner()
            # runner.run(suite)
            html_file = os.path.join(Var.Report, "report.html")
            fp = open(html_file, "wb")
            html_runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                                        title=u"测试",
                                                        description=u"测试")
            html_runner.run(suite)
    except Exception as e:
        raise e


def projectRun():
    pass