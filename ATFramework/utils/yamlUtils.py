#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml
import copy
from ATFramework.common.Variable import Var
from ATFramework.common.Loging import *

def getdata(paths):
    '''
    处理脚本
    :param paths:
    :return:
    '''

    datalist = []
    logiclist = []
    data_tag = {}
    logic_tag = {}
    try:
        for path in paths:
            if "data.yaml" in path:
                with open(path,"r") as f :
                    data = yaml.load(f , Loader=yaml.FullLoader)
                    datalist.append(analytical_data(data,path,data_tag))

            if "logic.yaml" in path:
                with open(path, "r") as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)
                    logiclist.append(analytical_logic(data, path, logic_tag))

        remove_repeat_data(data_tag)
        remove_repeat_logic(logic_tag)

        return analytical(datalist,logiclist)

    except Exception as e:
        raise e



def remove_repeat_data(data):
    '''
    去重 dataId
    :param data:
    :return:
    '''
    if "data_tag" in data:
        list = sorted(set(data["data_tag"]), key=data["data_tag"].index)
        str = "\n"
        for mesg in list:
            str = str + "dataId({}) repeat, path: {}\n".format(mesg.split("&#")[0], mesg.split("&#")[1])

        LogError(str)


def remove_repeat_logic(logic):
    '''
    去重 logicId
    :param logic:
    :return:
    '''
    if "logic_tag" in logic:
        list = sorted(set(logic["logic_tag"]), key=logic["logic_tag"].index)
        str = "\n"
        for mesg in list:
            str = str + "logicId({}) repeat, path: {}\n".format(mesg.split("&#")[0], mesg.split("&#")[1])

        LogError(str)

def analytical_data(data,path,data_tag):
    '''
    获取重复的dataId
    :param data:
    :param path:
    :param data_tag:
    :return:
    '''

    if not data["logicId"]:
        LogError("{}:The logicId connot be empty!".format(path))

    if not data["dataId"]:
        LogError("{}:The dataId connot be empty!".format(path))

    data["dataPath"] = path
    if data["dataId"] in data_tag:
        if "data_tag" not in data_tag:
            data_tag["data_tag"] = []
        data_tag["data_tag"].append("{}&#{}".format(data["dataId"],data_tag[data["dataId"]]))
        data_tag["data_tag"].append("{}&#{}".format(data["dataId"], data["dataPath"]))
    else:
        data_tag[data["dataId"]] = data["dataPath"]
    return {data["dataId"]:data}

def analytical_logic(data,path,logic_tag):
    '''
    获取重复的logicId
    :param data:
    :param path:
    :param logic_tag:
    :return:
    '''

    if not data["logicId"]:
        LogError("{}:The logicId connot be empty!".format(path))

    data["logicPath"] = path
    if data["logicId"] in logic_tag:
        if "logic_tag" not in logic_tag:
            logic_tag["logic_tag"] = []
            logic_tag["logic_tag"].append("{}&#{}".format(data["logicId"], logic_tag[data["logicId"]]))
            logic_tag["logic_tag"].append("{}&#{}".format(data["logicId"], data["logicPath"]))
    else:
        logic_tag[data["logicId"]] = data["logicPath"]
    return {data["logicId"]: data}

def analytical(data,logic):
    '''
    关联data logic数据
    :param data:
    :param logic:
    :return:
    '''

    try:
        analytical_list = {}
        for d in data:
            for k,v in d.items():
                logicId = v["logicId"]
                for l in logic:
                    logic_dict = {}
                    if logicId in l:
                        logic_dict = copy.deepcopy(l[logicId])
                        logic_dict["dataId"] = v["dataId"]
                        logic_dict["dataPath"] = v["dataPath"]
                        logic_dict["dataItems"] = v["dataItems"]
                        logic_dict["description_data"] = v["description_data"]
                        list = []
                        for step in logic_dict["steps"]:
                            parameter = {}
                            func = step.split("?")[0]
                            args = step.split("?")[1].split("&")
                            for a in args:
                                if len(a.split("=")) >= 2:
                                    parameter[a.split("=")[0]] = a.split("=")[1]
                                elif len(a.split("=")) >= 1:
                                    parameter[a.split("=")[0]] = ""
                            str = ""
                            for key, value in parameter.items():
                                if str != "":
                                    if key in v["dataItems"]:
                                        str = "{},{}='{}'".format(str,key,v["dataItems"][key])
                                    else:
                                        LogError("{}:{} cannot be empty!".format(l[k]["yamlPath"],key))
                                else:
                                    str = "{}={}".format(key,"map")
                            func_ = "{}({})".format(func,str)
                            list.append(func_)
                            logic_dict["steps"] = list
                        analytical_list[k] = logic_dict
        return analytical_list

    except Exception as e:
        raise e