#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
from ATFramework.common.Variable import Var
from logging.handlers import RotatingFileHandler

logger = None

def Loging(log_level):
    global logger

    log_file_path = Var.Report
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)

    log_file_path = os.path.join(log_file_path,"project.log")

    logger = logging.getLogger(logging.NOTSET)
    logger.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(asctime)s %(levelname)s :%(message)s')

    ch = logging.StreamHandler(stream=sys.stdout)
    rh = logging.handlers.RotatingFileHandler(log_file_path, mode='a', maxBytes=50 * 1024 * 1024, backupCount=10)

    logger.addHandler(ch)
    logger.addHandler(rh)

    ch.setFormatter(formatter)
    ch.setLevel(log_level)

    rh.setFormatter(formatter)
    rh.setLevel(log_level)

    logging.info("Logger is initialized")
    return logger

def LogInfo(message):
    try:
        logger.info(message)
    except:
        print(message)

def LogError(message,exit=True):
    try:
        logger.error(message)
        if exit:
            os._exit(0)
    except:
        print(message)

def Step(message):
    Var.CaseStepIndex = Var.CaseStepIndex + 1
    message = "Step %s: "%str(Var.CaseStepIndex) + str(message)
    logger.info(message)
    message_new = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time())) + message
    Var.CaseMessage = Var.CaseMessage + "\n" +  message_new