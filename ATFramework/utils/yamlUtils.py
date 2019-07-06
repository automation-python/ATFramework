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

        analytical_logic_isExists(datalist,logiclist)
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
        string = "\n"
        for mesg in list:
            string = string + "{}: dataId({}) cannot be repeated!\n".format(mesg.split("&#")[1], mesg.split("&#")[0])

        LogError(string)

def remove_repeat_logic(logic):
    '''
    去重 logicId
    :param logic:
    :return:
    '''
    if "logic_tag" in logic:
        list = sorted(set(logic["logic_tag"]), key=logic["logic_tag"].index)
        string = "\n"
        for mesg in list:
            string = string + "{}: logicId({}) cannot be repeated!\n".format(mesg.split("&#")[1], mesg.split("&#")[0])

        LogError(string)

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

def analytical_logic_isExists(datalist,logiclist):
    '''
    check if thd logicId exists!
    :param data:
    :param logic:
    :return:
    '''
    l_list = []
    for logic in logiclist:
        for key in logic:
            l_list.append(key)

    for data in datalist:
        for key,value in data.items():
            if value["logicId"] not in l_list:
                LogError('{}:logicId({}) does not exist!'.format(value["dataPath"], value["logicId"]))

def analytical(data,logic):
    '''
    关联data logic数据
    :param data:
    :param logic:
    :return:
    '''

    try:
        analytical_list = {}
        for comboData  in dataCombo(data,logic):
            steps = []
            for step in comboData["steps"]:
                func = step.split("?")[0]
                args = step.split("?")[1].split("&")
                for a in args:
                    if "ages" not in a:
                        alist = a.split("=")
                        if len(alist)==2:
                            if alist[1] in comboData['dataItems'].keys():
                                a_value = comboData['dataItems'][alist[1]]
                                if isinstance(a_value,str):
                                    step = step.replace("={}".format(alist[1]) ,"='{}'".format(a_value))
                                else:
                                    step = step.replace("={}".format(alist[1]), "={}".format(a_value))
                            else:
                                LogError('{}: {} cannot be empty!'.format(comboData["logicPath"], a),False)
                        else:
                            LogError('{}: {} invalid syntax!'.format(comboData["logicPath"],step))
                step = step.replace("?", "(").replace("&", ",") + ")"
                steps.append(step)
            comboData["steps"] = steps
            analytical_list[comboData["dataId"]] = comboData

        return analytical_list


    except Exception as e:
        raise e

def dataCombo(data,logic):
    '''
    data combo
    :return:
    '''

    datalist =[]
    try:
        for d in data:
            for datak, datav in d.items():
                logicId = datav['logicId']
                for l in logic:
                    if logicId in l:
                        logic_dict = copy.deepcopy(l[logicId])
                        for key, value in datav.items():
                            logic_dict[key] = value
                        datalist.append(logic_dict)
    except Exception as e:
        LogError(e)


    return datalist