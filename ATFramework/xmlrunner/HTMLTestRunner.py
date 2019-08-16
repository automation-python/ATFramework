#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import shutil

class Template_mixin(object):
    """
     Define a HTML template for report customerization and generation.

     Overall structure of an HTML report

     HTML
     +------------------------+
     |<html>                  |
     |  <head>                |
     |                        |
     |   STYLESHEET           |
     |   +----------------+   |
     |   |                |   |
     |   +----------------+   |
     |                        |
     |  </head>               |
     |                        |
     |  <body>                |
     |                        |
     |   HEADING              |
     |   +----------------+   |
     |   |                |   |
     |   +----------------+   |
     |                        |
     |   REPORT               |
     |   +----------------+   |
     |   |                |   |
     |   +----------------+   |
     |                        |
     |   ENDING               |
     |   +----------------+   |
     |   |                |   |
     |   +----------------+   |
     |                        |
     |  </body>               |
     |</html>                 |
     +------------------------+
     """

    STATUS = {
        0: 'pass',
        1: 'fail',
        2: 'error',
        3: 'skip'
    }
    HTML_TMPL = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>测试报告</title>
    <link rel="stylesheet" type="text/css" href="resource/css.css">
    <script type="text/javascript" src="http://libs.baidu.com/jquery/2.1.1/jquery.min.js"></script>
    <script src="resource/js.js"></script>
</head>
<body>
<div class="root">
    {heading}
    {tabdiv}
</div>
</body>
</html>
    '''

    # 测试汇总
    HEADING_TMPL = r'''
        <div class="title">
            <h2 style="color: white;text-align: center;line-height: 65px">{title}</h2>
        </div>
        <div class="head" style="height: 240px">
            <div class="head_title">Summarization</div>
            <div style="height: 210px;border: 1px solid rgb(220,220,220); background-color: white">
                <p class="text">Total：{total}</p>
                <p class="text">Pass：{Pass}</p>
                <p class="text">Failure：{failure}</p>
                <p class="text">Error：{error}</p>
                <p class="text">Skipped：{skipped}</p>
                <p class="text">StartTime：{startTime}</p>
                <p class="text">Duration：{duration}</p>
            </div>
        </div>
        '''

    # 详细数据
    TABDIV_TMPL = r'''
        <div class="tabdiv" style="height: auto">
        <div class="head_title">Details</div>
        <div style="height:auto;border: 1px solid rgb(220,220,220); background-color: white">
            <table class="table" cellspacing="0">
                <tr>
                    <th width="20%%">CaseName</th>
                    <th width="30%%">Description</th>
                    <th width="12%%">StartTime</th>
                    <th width="12%%">Duration</th>
                    <th width="12%%">Status</th>
                    <th width="12%%">Open/Close</th>
                </tr>
                {trlist}
            </table>
        </div>
        </div>
    '''

    # module_name
    MODULE_NAME = r'''
                <tr>
                    <td class="module_td" colspan="2" style=" text-align:left; text-indent: 20px;">{module_name}</td>
                    <td class="module_td" colspan="3"><span class="Pass status">&nbsp;Pass:{Pass}&nbsp;</span> | <span class="failure status">&nbsp;failure:{failure}&nbsp;</span> | <span class="error status">&nbsp;error:{error}&nbsp;</span> | <span class="skipped status">&nbsp;skipped:{skipped}&nbsp;</span></td>
                    <td class="module_name" data-tag='{tag_module_name}'>Open</td>
                </tr>
    '''

    # case
    CASE_TMPL = r'''
                <tr class='{module_name}' style="display: none">
                    <td class="module_td {b_color}" style=" text-align:left; text-indent: 40px;">{casename}</td>
                    <td class="module_td {b_color}">{description_data}</td>
                    <td class="module_td {b_color}">{startTime}</td>
                    <td class="module_td {b_color}">{duration}</td>
                    <td class="module_td {b_color}">{status}</td>
                    <td class="module_td_view {b_color}" data-tag='{dataId}'>Open</td>
                </tr>
    '''

    # case details
    CASE_DETA_NOT_SNAPSHOT = r'''
                <tr class="{dataId}" style="display: none">
                    <td class="module_deta" colspan="2" style="border-right: 0">
                        <div class="errordiv">
                            <h3 style="margin-bottom: 10px">Steps</h3>
                            <pre class="errorp" style="white-space: pre-wrap;overflow-wrap: break-word;margin-top: 0">{steplist}</pre>
                        </div>
                    </td>
                    <td class="module_deta" colspan="4">
                        <div class="errordiv">
                            <h3 style="margin-bottom: 10px">Logs</h3>
                            <pre class="errorp" style="white-space: pre-wrap;overflow-wrap: break-word;margin-top: 0">{errlist}</pre>
                        </div>
                    </td>
                </tr>
    '''

    CASE_DETA_SNAPSHOT = r'''
                <tr class="{dataId}" style="display: none">
                    <td class="module_deta" colspan="2" style="border-right: 0">
                        <div class="errordiv">
                            <h3 style="margin-bottom: 10px">Steps</h3>
                            <div class="SnapshotDiv_root">
                                <div class="SnapshotDiv_left">
                                    <div>
                                        <img class="img" src="2.jpg">
                                        <span class="stepspan">
                                            <p>2019-08-15 20:35:24</p>
                                            <p>Step 1:Login</p>
                                        </span>
                                    </div>
                                </div>
                                <div class="SnapshotDiv_right"></div>
                            </div>
                        </div>
                    </td>
                    <td class="module_deta" colspan="4">
                        <div class="errordiv">
                            <h3 style="margin-bottom: 10px">Logs</h3>
                            <pre class="errorp" style="white-space: pre-wrap;overflow-wrap: break-word;margin-top: 0">{errlist}</pre>
                        </div>
                    </td>
                </tr>
    '''

    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = ''

class HTMLTestRunner(Template_mixin):

    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):
        self.stream = stream
        self.verbosity = verbosity
        self.title = title if title else self.DEFAULT_TITLE
        self.description = description if description else self.DEFAULT_DESCRIPTION

    def generateReport(self,result,starttime,stoptime):
        report_attrs = self._getReportAttributes(result, starttime, stoptime)
        report = self._generate_report(result)
        heading = self._generate_heading(report_attrs)
        tabdiv = self.TABDIV_TMPL.format(
            trlist = report
        )
        output = self.HTML_TMPL.format(
            heading = heading,
            tabdiv = tabdiv
        )
        resource = os.path.join(os.path.split(os.path.abspath(__file__))[0], "resource")
        shutil.copy(os.path.join(resource,"css.css"), os.path.join(result.Report,'resource'))
        shutil.copy(os.path.join(resource,"js.js"), os.path.join(result.Report,'resource'))
        self.stream.write(output.encode('utf-8'))

    def _getReportAttributes(self,result,starttime,stoptime):

        startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starttime))
        duration = str(int(stoptime - starttime)) + 's'
        Total = result.testsRun
        Pass = len(result.successes)
        Failure = len(result.failures)
        Error = len(result.errors)
        skipped = len(result.skipped)
        return (Total,Pass,Failure,Error,skipped,startTime,duration)

    def _generate_report(self, result):

        sortedResult = self.sortResult(result.result)
        table_lsit = []
        for cid, (cls, cls_results) in enumerate(sortedResult):
            module_name = cls
            status_list = ['Pass','failure','error','skipped']
            Pass = 0
            failure = 0
            error = 0
            skipped = 0

            cls_list = []
            for tup_result in cls_results:
                _status = tup_result[0]
                testinfo = tup_result[1]

                caseinfo = self._generate_case(testinfo, status_list[_status])
                cls_list.append(caseinfo)

                if _status != 3: # 跳过
                    casedeta = self._generate_case_deta(testinfo)
                    cls_list.append(casedeta)

                if _status == 0:
                    Pass += 1
                elif _status == 1:
                    failure += 1
                elif _status == 2:
                    error += 1
                elif _status == 3:
                    skipped += 1

            module_name = self.MODULE_NAME.format(
                module_name = module_name,
                Pass = Pass,
                failure = failure,
                error = error,
                skipped = skipped,
                tag_module_name = module_name
            )

            table_lsit.append(module_name)
            for tr in cls_list:
                table_lsit.append(tr)


        tr_ = ''
        for tr in table_lsit:
            tr_ = tr_ + tr
        return tr_


    def sortResult(self,result_list):

        rmap = {}
        classes = []
        for n, t, o in result_list:
            cls = t.module_name
            if str(cls).count(".") == 0:
                cls = cls
            else:
                cls = ".".join(cls.split(".")[:-1])
            if not cls in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def _get_info_by_testcase(self,result):

        tests_by_testcase = {}
        for tests in (result.successes, result.failures, result.errors,
                      result.skipped):
            for test_info in tests:
                if isinstance(test_info, tuple):
                    # This is a skipped, error or a failure test case
                    test_info = test_info[0]
                testcase_name = test_info.test_name
                if testcase_name not in tests_by_testcase:
                    tests_by_testcase[testcase_name] = []
                tests_by_testcase[testcase_name].append(test_info)

        return tests_by_testcase

    def _generate_heading(self,report_attrs):

        if report_attrs:
            heading = self.HEADING_TMPL.format(
                title = self.title,
                total = report_attrs[0],
                Pass = report_attrs[1],
                failure = report_attrs[2],
                error = report_attrs[3],
                skipped = report_attrs[4],
                startTime = report_attrs[5],
                duration = report_attrs[6]
            )
            return heading

    def _generate_case(self,testinfo,status):

        casename = testinfo.casename
        description_data = testinfo.description_data
        startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(testinfo.start_time))
        duration = str(int(testinfo.stop_time - testinfo.start_time)) + 's'
        dataId = testinfo.dataId
        module_name = testinfo.module_name

        caseinfo = self.CASE_TMPL.format(
            module_name=module_name,
            casename=casename,
            description_data=description_data,
            startTime=startTime,
            duration=duration,
            status=status,
            dataId=dataId,
            b_color=status
        )
        return caseinfo

    def _generate_case_deta(self,testinfo):
        dataId = testinfo.dataId
        setps = testinfo.stdout
        err = '\n' + testinfo.test_exception_info if testinfo.test_exception_info else 'Nothing'

        # steplist = []
        # errlist= []


        # for step_P in setps.replace(' ', '&nbsp;').split('\n'):
        #     p = '<p class="errorp">{}</p>'.format(step_P)
        #     steplist.append(p)
        # for err_P in err.replace(' ', '&nbsp;').split('\n'):
        #     p = '<p class="errorp">{}</p>'.format(err_P)
        #     errlist.append(p)

        if err != 'Nothing':
            os.makedirs(testinfo.SnapshotDir)

        if os.path.exists(testinfo.SnapshotDir):
            casedeta = self.CASE_DETA_SNAPSHOT.format(
                dataId=dataId,
                steplist=setps,
                errlist=err
            )
        else:
            casedeta = self.CASE_DETA_NOT_SNAPSHOT.format(
                dataId=dataId,
                steplist=setps,
                errlist=err
            )

        return casedeta
