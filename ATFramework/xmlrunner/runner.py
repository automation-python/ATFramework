# -*- coding: utf-8 -*-
import sys
import time
import traceback

from .unittest import TextTestRunner
from .result import _XMLTestResult
from ATFramework.runner import HTMLTestRunner
import os
from ATFramework import Var



# see issue #74, the encoding name needs to be one of
# http://www.iana.org/assignments/character-sets/character-sets.xhtml
UTF8 = 'UTF-8'


class XMLTestRunner(TextTestRunner):
    """
    A test runner class that outputs the results in JUnit like XML files.
    """
    def __init__(self, output='.', outsuffix=None, stream=sys.stderr,
                 descriptions=True, verbosity=1, elapsed_times=True,
                 failfast=False, buffer=False, encoding=UTF8,
                 resultclass=None):
        TextTestRunner.__init__(self, stream, descriptions, verbosity,
                                failfast=failfast, buffer=buffer)
        self.verbosity = verbosity
        self.output = output
        self.encoding = encoding
        # None means default timestamped suffix
        # '' (empty) means no suffix
        if outsuffix is None:
            outsuffix = time.strftime("%Y%m%d%H%M%S")
        self.outsuffix = outsuffix
        self.elapsed_times = elapsed_times
        if resultclass is None:
            self.resultclass = _XMLTestResult
        else:
            self.resultclass = resultclass

    def _make_result(self):
        """
        Creates a TestResult object which will be used to store
        information about the executed tests.
        """
        # override in subclasses if necessary.
        return self.resultclass(
            self.stream, self.descriptions, self.verbosity, self.elapsed_times
        )

    def run(self, test):
        """
        Runs the given test case or test suite.
        """
        try:
            # Prepare the test execution
            result = self._make_result()
            result.failfast = self.failfast
            if hasattr(test, 'properties'):
                # junit testsuite properties
                result.properties = test.properties

            # Print a nice header
            self.stream.writeln()
            #self.stream.writeln('Running tests...')
            #self.stream.writeln(result.separator2)

            # Execute tests

            start_time = time.time()
            test(result)
            stop_time = time.time()
            duration = start_time - stop_time



            # 生成test report of xml format
            result.generate_reports(self, start_time, stop_time)
            html_file = os.path.join(Var.Report, "report.html")
            fp = open(html_file, "wb")
            html_runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                                   title=u"测试",
                                                   description=u"测试")
            html_runner.generateReport(result, start_time, stop_time)
            fp.close()

        except Exception as e:
            traceback.print_exc()
            result = None

        return result
