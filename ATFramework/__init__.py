#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import os
import sys
import traceback
import unittest
from ATFramework.common.Variable import Var
from ATFramework.common.Ages import ages
from ATFramework.common.Loging import LogInfo,LogError,Step
from ATFramework.runner.Decorator import keywords



if not Var.ROOT:
    for path in inspect.stack():
        if str(path[1]).endswith("runTest.py"):
            Var.ROOT = os.path.dirname(path[1])
            if "framework" in Var.ROOT:
                Var.ROOT = None
            break

if Var.ROOT:
    sys.path.append(Var.ROOT)

    try:
        sys.path.append(os.path.join(Var.ROOT, "AW"))

        for rt,dirs,files in os.walk(os.path.join(Var.ROOT,"AW")):
            for f in files:
                if f == "__init__.py" or f.endswith("pyc") or f.startswith("."):
                    continue
                exec("from AW.{} import *" .format(f[:-3]))


    except Exception as e:
        traceback.print_exc()

from ATFramework.runner.TestScripts import *
from ATFramework.project import *