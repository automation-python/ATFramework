#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import copy
import collections
from ATFramework.common.Loging import *

class StrKeyDict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key,str):
            raise  KeyError(key)
        return self[str(key)]

    def __contains__(self, item):
        return str(item) in self.data


    def __setitem__(self, key, value):
        if isinstance(value,dict):
            _item = StrKeyDict()
            for _key ,_value in value.items():
                _item[_key] = _value
            self.data[str(key)] = _item
        else:
            self.data[str(key)] = value

    def __getattr__(self, item):
        if item in self:
            return self[str(item)]
        else:
            return None

def analyticalData(paths):
    '''
    解析文件
    :param paths:
    :return:
    '''

    alllist = []
    for path in paths:
        with open(path, "r", encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            dict_ = StrKeyDict()
            for key ,value in data.items():
                dict_[key] = value
            alllist.append((dict_,path))

    return separatedData(alllist)


def separatedData(alllist):
    '''
    分离数据
    :param alllist:
    :return:
    '''
    datalist = []
    logiclist = []
    dataId_tag = []
    logicId_tag = []
    for data ,path in alllist:
        if data.dataId:
            data['dataPath'] = path
            datalist.append(data)
            dataId_tag.append(data.dataId)
        elif data.logicId:
            data['logicPath'] = path
            logiclist.append(data)
            logicId_tag.append(data.dataId)
        else:
            LogError("{}:The dataId or logicId cannot be empty!".format(path))

    logicIdisExists(datalist,logiclist)
    getDuplicatedataId(dataId_tag,datalist)
    getDuplicatelogicId(logicId_tag,logiclist)
    return linkedData(datalist,logiclist)

def logicIdisExists(datalist,logiclist):
    '''
    判断logicId是否存在
    :param datalist:
    :param logiclist:
    :return:
    '''
    l_list = []
    for logic in logiclist:
        l_list.append(logic.logicId)
    for data in datalist:
        if data.logicId not in l_list:
            LogError("{}:logicId({}) does not exist!".format(data.dataPath,data.logicId))


def getDuplicatelogicId(logicId_tag,logiclist):
    '''
    获取重复的logicId
    :param logicId_tag:
    :param logiclist:
    :return:
    '''
    for logicId in [val for val in list(set(logicId_tag)) if logicId_tag.count(val) ==2]:
        string = '\n'
        for logic in logiclist:
            if logicId == logic.logicId:
                string = string + "{}:logicId({}) cannot be repeated!".format(logicId,logic.logicPath)
        LogError(string)

def getDuplicatedataId(dataId_tag, datalist):
    '''
    获取重复的dataId
    :param dataId_tag:
    :param datalist:
    :return:
    '''
    for dataId in [val for val in list(set(dataId_tag)) if dataId_tag.count(val) ==2]:
        string = '\n'
        for data in datalist:
            if dataId == data.dataId:
                string = string + "{}:dataId({}) cannot be repeated!".format(dataId,data.dataPath)
        LogError(string)

def linkedData(datalist,logiclist):
    '''
    关联数据
    :param datalist:
    :param logiclist:
    :return:
    '''
    linkedData_list = StrKeyDict()
    logic_linkedData_list = []
    for data in datalist:
        for logic in logiclist:
            if data.logicId == logic.logicId:
                dict = StrKeyDict()
                for key,value in data.items():
                    dict[key] = value
                for _key,_value in logic.items():
                    dict[_key] = _value
                logic_linkedData_list.append(dict)

    for logic in logic_linkedData_list:
        steps = []
        for step in logic.steps:
            args = step.split("?")[1].split("&")
            for a in args:
                if "ages" not in a:
                    alist = a.split("=")
                    if len(alist) == 2:
                        if alist[-1] in logic.dataItems.keys():
                            a_value = logic.dataItems[alist[-1]]
                            if isinstance(a_value,str):
                                step = step.replace("={}".format(alist[-1]), "='{}'".format(a_value))
                            else:
                                step = step.replace("={}".format(alist[-1]), "={}".format(a_value))
                        else:
                            LogError('{}: {} cannot be empty!'.format(logic.logicPath, a), False)
                    else:
                        LogError('{}: {} invalid syntax!'.format(logic.logicPath, step))
            step = step.replace("?", "(").replace("&", ",") + ")"
            steps.append(step)
        logic["steps"] = steps
        linkedData_list[logic.dataId] = logic
    return linkedData_list

