#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : report1.py
# @Author: 橘子
# @Date  : 2021/1/11
# @Desc  : execise


 # URL: http://tungwaiyip.info/software/HTMLTestRunner.html

__author__ = "Wai Yip Tung,  Findyou，Adil"
__version__ = "0.8.2.3"


 """
 Change History
 Version 0.8.2.1 -Findyou
* 改为支持python3

 Version 0.8.2.1 -Findyou
 * 支持中文，汉化
 * 调整样式，美化（需要连入网络，使用的百度的Bootstrap.js）
 * 增加 通过分类显示、测试人员、通过率的展示
 * 优化“详细”与“收起”状态的变换
 * 增加返回顶部的锚点

 Version 0.8.2
* Show output inline instead of popup window (Viorel Lupu).

 Version in 0.8.1
 * Validated XHTML (Wolfgang Borgert).
 * Added description of test classes and test cases.

 Version in 0.8.0
* Define Template_mixin class for customization.
* Workaround a IE 6 bug that it does not treat <script> block as CDATA.

Version in 0.7.1
 * Back port to Python 2.3 (Frank Horowitz).
 * Fix missing scroll bars in detail log (Podi).
 """

# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?

import datetime
import io
import sys
import time
import unittest
from xml.sax import saxutils
import sys

# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing. Output
 # sent to sys.stdout and sys.stderr are automatically captured. However
 # in some cases sys.stdout is already cached before HTMLTestRunner is
 # invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
 #   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>

class OutputRedirector(object):
     """ Wrapper to redirect stdout or stderr """
     def __init__(self, fp):
         self.fp = fp

     def write(self, s):
         self.fp.write(s)

     def writelines(self, lines):
         self.fp.writelines(lines)
     def flush(self):
         self.fp.flush()

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

# ----------------------------------------------------------------------
# Template

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
     0: '通过',
     1: '失败',
     2: '错误',
     }
     # 默认测试标题
     DEFAULT_TITLE = 'UI测试报告'
     DEFAULT_DESCRIPTION = ''
     # 默认测试人员
     DEFAULT_TESTER = 'WangYIngHao'

     # ------------------------------------------------------------------------
     # HTML Template

     HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
200 <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
201 <html xmlns="http://www.w3.org/1999/xhtml">
202 <head>
203     <title>%(title)s</title>
204     <meta name="generator" content="%(generator)s"/>
205     <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
206     <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
207     <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
208     <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
209     %(stylesheet)s
210 </head>
211 <body >
212 <script language="javascript" type="text/javascript">
213 output_list = Array();
214
215 /*level 调整增加只显示通过用例的分类 --Adil
216 0:Summary //all hiddenRow
217 1:Failed  //pt hiddenRow, ft none
218 2:Pass    //pt none, ft hiddenRow
219 3:Error   // pt hiddenRow, ft none
220 4:All     //pt none, ft none
221 下面设置 按钮展开逻辑  --Yang Yao Jun
222 */
223 function showCase(level) {
224     trs = document.getElementsByTagName("tr");
225     for (var i = 0; i < trs.length; i++) {
226         tr = trs[i];
227         id = tr.id;
228         if (id.substr(0,2) == 'ft') {
229             if (level == 2 || level == 0 ) {
230                 tr.className = 'hiddenRow';
231             }
232             else {
233                 tr.className = '';
234             }
235         }
236         if (id.substr(0,2) == 'pt') {
237             if (level < 2 || level ==3 ) {
238                 tr.className = 'hiddenRow';
239             }
240             else {
241                 tr.className = '';
242             }
243         }
244     }
245
246     //加入【详细】切换文字变化 --Findyou
247     detail_class=document.getElementsByClassName('detail');
248     //console.log(detail_class.length)
249     if (level == 3) {
250         for (var i = 0; i < detail_class.length; i++){
251             detail_class[i].innerHTML="收起"
252         }
253     }
254     else{
255             for (var i = 0; i < detail_class.length; i++){
256             detail_class[i].innerHTML="详细"
257         }
258     }
259 }
260
261 function showClassDetail(cid, count) {
262     var id_list = Array(count);
263     var toHide = 1;
264     for (var i = 0; i < count; i++) {
265         //ID修改 点 为 下划线 -Findyou
266         tid0 = 't' + cid.substr(1) + '_' + (i+1);
267         tid = 'f' + tid0;
268         tr = document.getElementById(tid);
269         if (!tr) {
270             tid = 'p' + tid0;
271             tr = document.getElementById(tid);
272         }
273         id_list[i] = tid;
274         if (tr.className) {
275             toHide = 0;
276         }
277     }
278     for (var i = 0; i < count; i++) {
279         tid = id_list[i];
280         //修改点击无法收起的BUG，加入【详细】切换文字变化 --Findyou
281         if (toHide) {
282             document.getElementById(tid).className = 'hiddenRow';
283             document.getElementById(cid).innerText = "详细"
284         }
285         else {
286             document.getElementById(tid).className = '';
287             document.getElementById(cid).innerText = "收起"
288         }
289     }
290 }
291
292 function html_escape(s) {
293     s = s.replace(/&/g,'&');
294     s = s.replace(/</g,'<');
295     s = s.replace(/>/g,'>');
296     return s;
297 }
298 </script>
299 %(heading)s
300 %(report)s
301 %(ending)s
302
303 </body>
304 </html>
305 """
306     # variables: (title, generator, stylesheet, heading, report, ending)
307
308
309     # ------------------------------------------------------------------------
310     # Stylesheet
311     #
312     # alternatively use a <link> for external style sheet, e.g.
313     #   <link rel="stylesheet" href="$url" type="text/css">
314
315     STYLESHEET_TMPL = """
316 <style type="text/css" media="screen">
317 body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 80%; }
318 table       { font-size: 100%; }
319
320 /* -- heading ---------------------------------------------------------------------- */
321 .heading {
322     margin-top: 0ex;
323     margin-bottom: 1ex;
324 }
325
326 .heading .description {
327     margin-top: 4ex;
328     margin-bottom: 6ex;
329 }
330
331 /* -- report ------------------------------------------------------------------------ */
332 #total_row  { font-weight: bold; }
333 .passCase   { color: #5cb85c; }
334 .failCase   { color: #d9534f; font-weight: bold; }
335 .errorCase  { color: #f0ad4e; font-weight: bold; }
336 .hiddenRow  { display: none; }
337 .testcase   { margin-left: 2em; }
338 </style>
339 """
340
341     # ------------------------------------------------------------------------
342     # Heading
343     #
344
345     HEADING_TMPL = """<div class='heading'>
346 <h1 style="font-family: Microsoft YaHei">%(title)s</h1>
347 %(parameters)s
348 <p class='description'>%(description)s</p>
349 </div>
350
351 """ # variables: (title, parameters, description)
352
353     HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s : </strong> %(value)s</p>
354 """ # variables: (name, value)
355
356
357
358     # ------------------------------------------------------------------------
359     # Report
360     #
361     # 汉化,加美化效果 --Yang Yao Jun
362     #
363     # 这里涉及到了 Bootstrap 前端技术，Bootstrap 按钮 资料介绍详见：http://www.runoob.com/bootstrap/bootstrap-buttons.html
364     #
365     REPORT_TMPL = """
366     <p id='show_detail_line'>
367     <a class="btn btn-primary" href='javascript:showCase(0)'>通过率 [%(passrate)s ]</a>
368     <a class="btn btn-success" href='javascript:showCase(2)'>通过[ %(Pass)s ]</a>
369     <a class="btn btn-warning" href='javascript:showCase(3)'>错误[ %(error)s ]</a>
370     <a class="btn btn-danger" href='javascript:showCase(1)'>失败[ %(fail)s ]</a>
371     <a class="btn btn-info" href='javascript:showCase(4)'>所有[ %(count)s ]</a>
372     </p>
373 <table id='result_table' class="table table-condensed table-bordered table-hover">
374 <colgroup>
375 <col align='left' />
376 <col align='right' />
377 <col align='right' />
378 <col align='right' />
379 <col align='right' />
380 <col align='right' />
381 </colgroup>
382 <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
383     <td>用例集/测试用例</td>
384     <td>总计</td>
385     <td>通过</td>
386     <td>错误</td>
387     <td>失败</td>
388     <td>详细</td>
389 </tr>
390 %(test_list)s
391 <tr id='total_row' class="text-center active">
392     <td>总计</td>
393     <td>%(count)s</td>
394     <td>%(Pass)s</td>
395     <td>%(error)s</td>
396     <td>%(fail)s</td>
397     <td>通过率：%(passrate)s</td>
398 </tr>
399 </table>
400 """ # variables: (test_list, count, Pass, fail, error ,passrate)
401
402     REPORT_CLASS_TMPL = r"""
403 <tr class='%(style)s warning'>
404     <td>%(desc)s</td>
405     <td class="text-center">%(count)s</td>
406     <td class="text-center">%(Pass)s</td>
407     <td class="text-center">%(error)s</td>
408     <td class="text-center">%(fail)s</td>
409     <td class="text-center"><a href="javascript:showClassDetail('%(cid)s',%(count)s)" class="detail" id='%(cid)s'>详细</a></td>
410 </tr>
411 """ # variables: (style, desc, count, Pass, fail, error, cid)
412
413     #失败 的样式，去掉原来JS效果，美化展示效果  -Findyou
414     REPORT_TEST_WITH_OUTPUT_TMPL = r"""
415 <tr id='%(tid)s' class='%(Class)s'>
416     <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
417     <td colspan='5' align='center'>
418     <!--默认收起错误信息 -Findyou
419     <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
420     <div id='div_%(tid)s' class="collapse">  -->
421
422     <!-- 默认展开错误信息 -Findyou -->
423     <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
424     <div id='div_%(tid)s' class="collapse in" style='text-align: left; color:red;cursor:pointer'>
425     <pre>
426     %(script)s
427     </pre>
428     </div>
429     </td>
430 </tr>
431 """ # variables: (tid, Class, style, desc, status)
432
433     # 通过 的样式，加标签效果  -Findyou
434     REPORT_TEST_NO_OUTPUT_TMPL = r"""
435 <tr id='%(tid)s' class='%(Class)s'>
436     <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
437     <td colspan='5' align='center'><span class="label label-success success">%(status)s</span></td>
438 </tr>
439 """ # variables: (tid, Class, style, desc, status)
440
441     REPORT_TEST_OUTPUT_TMPL = r"""
442 %(id)s: %(output)s
443 """ # variables: (id, output)
444
445     # ------------------------------------------------------------------------
446     # ENDING
447     #
448     # 增加返回顶部按钮  --Findyou
449     ENDING_TMPL = """<div id='ending'> </div>
450     <div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
451     <a href="#"><span class="glyphicon glyphicon-eject" style = "font-size:30px;" aria-hidden="true">
452     </span></a></div>
453     """
454
455 # -------------------- The end of the Template class -------------------
456
457
458 TestResult = unittest.TestResult
459
460 class _TestResult(TestResult):
461     # note: _TestResult is a pure representation of results.
462     # It lacks the output and reporting ability compares to unittest._TextTestResult.
463
464     def __init__(self, verbosity=1):
465         TestResult.__init__(self)
466         self.stdout0 = None
467         self.stderr0 = None
468         self.success_count = 0
469         self.failure_count = 0
470         self.error_count = 0
471         self.verbosity = verbosity
472
473         # result is a list of result in 4 tuple
474         # (
475         #   result code (0: success; 1: fail; 2: error),
476         #   TestCase object,
477         #   Test output (byte string),
478         #   stack trace,
479         # )
480         self.result = []
481         #增加一个测试通过率 --Findyou
482         self.passrate=float(0)
483
484
485     def startTest(self, test):
486         TestResult.startTest(self, test)
487         # just one buffer for both stdout and stderr
488         self.outputBuffer = io.StringIO()
489         stdout_redirector.fp = self.outputBuffer
490         stderr_redirector.fp = self.outputBuffer
491         self.stdout0 = sys.stdout
492         self.stderr0 = sys.stderr
493         sys.stdout = stdout_redirector
494         sys.stderr = stderr_redirector
495
496
497     def complete_output(self):
498         """
499         Disconnect output redirection and return buffer.
500         Safe to call multiple times.
501         """
502         if self.stdout0:
503             sys.stdout = self.stdout0
504             sys.stderr = self.stderr0
505             self.stdout0 = None
506             self.stderr0 = None
507         return self.outputBuffer.getvalue()
508
509
510     def stopTest(self, test):
511         # Usually one of addSuccess, addError or addFailure would have been called.
512         # But there are some path in unittest that would bypass this.
513         # We must disconnect stdout in stopTest(), which is guaranteed to be called.
514         self.complete_output()
515
516
517     def addSuccess(self, test):
518         self.success_count += 1
519         TestResult.addSuccess(self, test)
520         output = self.complete_output()
521         self.result.append((0, test, output, ''))
522         if self.verbosity > 1:
523             sys.stderr.write('ok ')
524             sys.stderr.write(str(test))
525             sys.stderr.write('\n')
526         else:
527             sys.stderr.write('.')
528
529     def addError(self, test, err):
530         self.error_count += 1
531         TestResult.addError(self, test, err)
532         _, _exc_str = self.errors[-1]
533         output = self.complete_output()
534         self.result.append((2, test, output, _exc_str))
535         if self.verbosity > 1:
536             sys.stderr.write('E  ')
537             sys.stderr.write(str(test))
538             sys.stderr.write('\n')
539         else:
540             sys.stderr.write('E')
541
542     def addFailure(self, test, err):
543         self.failure_count += 1
544         TestResult.addFailure(self, test, err)
545         _, _exc_str = self.failures[-1]
546         output = self.complete_output()
547         self.result.append((1, test, output, _exc_str))
548         if self.verbosity > 1:
549             sys.stderr.write('F  ')
550             sys.stderr.write(str(test))
551             sys.stderr.write('\n')
552         else:
553             sys.stderr.write('F')
554
555
556 class HTMLTestRunner(Template_mixin):
557     """
558     """
559     def __init__(self, stream=sys.stdout, verbosity=1,title=None,description=None,tester=None):
560         self.stream = stream
561         self.verbosity = verbosity
562         if title is None:
563             self.title = self.DEFAULT_TITLE
564         else:
565             self.title = title
566         if description is None:
567             self.description = self.DEFAULT_DESCRIPTION
568         else:
569             self.description = description
570         if tester is None:
571             self.tester = self.DEFAULT_TESTER
572         else:
573             self.tester = tester
574
575         self.startTime = datetime.datetime.now()
576
577
578     def run(self, test):
579         "Run the given test case or test suite."
580         result = _TestResult(self.verbosity)
581         test(result)
582         self.stopTime = datetime.datetime.now()
583         self.generateReport(test, result)
584         print('\nTime Elapsed: %s' % (self.stopTime-self.startTime), file=sys.stderr)
585         return result
586
587
588     def sortResult(self, result_list):
589         # unittest does not seems to run in any particular order.
590         # Here at least we want to group them together by class.
591         rmap = {}
592         classes = []
593         for n,t,o,e in result_list:
594             cls = t.__class__
595             if cls not in rmap:
596                 rmap[cls] = []
597                 classes.append(cls)
598             rmap[cls].append((n,t,o,e))
599         r = [(cls, rmap[cls]) for cls in classes]
600         return r
601
602     #替换测试结果status为通过率 --Findyou
603     def getReportAttributes(self, result):
604         """
605         Return report attributes as a list of (name, value).
606         Override this to add custom attributes.
607         """
608         startTime = str(self.startTime)[:19]
609         duration = str(self.stopTime - self.startTime)
610         status = []
611         status.append('共 %s' % (result.success_count + result.failure_count + result.error_count))
612         if result.success_count: status.append('通过 %s'    % result.success_count)
613         if result.failure_count: status.append('失败 %s' % result.failure_count)
614         if result.error_count:   status.append('错误 %s'   % result.error_count  )
615         if status:
616             status = '，'.join(status)
617             self.passrate = str("%.2f%%" % (float(result.success_count) / float(result.success_count + result.failure_count + result.error_count) * 100))
618         else:
619             status = 'none'
620         return [
621             ('测试人员', self.tester),
622             ('开始时间',startTime),
623             ('合计耗时',duration),
624             ('测试结果',status + "，通过率= "+self.passrate),
625         ]
626
627
628     def generateReport(self, test, result):
629         report_attrs = self.getReportAttributes(result)
630         generator = 'HTMLTestRunner %s' % __version__
631         stylesheet = self._generate_stylesheet()
632         heading = self._generate_heading(report_attrs)
633         report = self._generate_report(result)
634         ending = self._generate_ending()
635         output = self.HTML_TMPL % dict(
636             title = saxutils.escape(self.title),
637             generator = generator,
638             stylesheet = stylesheet,
639             heading = heading,
640             report = report,
641             ending = ending,
642         )
643         self.stream.write(output.encode('utf8'))
644
645
646     def _generate_stylesheet(self):
647         return self.STYLESHEET_TMPL
648
649     #增加Tester显示 -Findyou
650     def _generate_heading(self, report_attrs):
651         a_lines = []
652         for name, value in report_attrs:
653             line = self.HEADING_ATTRIBUTE_TMPL % dict(
654                     name = saxutils.escape(name),
655                     value = saxutils.escape(value),
656                 )
657             a_lines.append(line)
658         heading = self.HEADING_TMPL % dict(
659             title = saxutils.escape(self.title),
660             parameters = ''.join(a_lines),
661             description = saxutils.escape(self.description),
662             tester= saxutils.escape(self.tester),
663         )
664         return heading
665
666     #生成报告  --Findyou添加注释
667     def _generate_report(self, result):
668         rows = []
669         sortedResult = self.sortResult(result.result)
670         for cid, (cls, cls_results) in enumerate(sortedResult):
671             # subtotal for a class
672             np = nf = ne = 0
673             for n,t,o,e in cls_results:
674                 if n == 0: np += 1
675                 elif n == 1: nf += 1
676                 else: ne += 1
677
678             # format class description
679             if cls.__module__ == "__main__":
680                 name = cls.__name__
681             else:
682                 name = "%s.%s" % (cls.__module__, cls.__name__)
683             doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
684             desc = doc and '%s: %s' % (name, doc) or name
685
686             row = self.REPORT_CLASS_TMPL % dict(
687                 style = ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
688                 desc = desc,
689                 count = np+nf+ne,
690                 Pass = np,
691                 fail = nf,
692                 error = ne,
693                 cid = 'c%s' % (cid+1),
694             )
695             rows.append(row)
696
697             for tid, (n,t,o,e) in enumerate(cls_results):
698                 self._generate_report_test(rows, cid, tid, n, t, o, e)
699
700         report = self.REPORT_TMPL % dict(
701             test_list = ''.join(rows),
702             count = str(result.success_count+result.failure_count+result.error_count),
703             Pass = str(result.success_count),
704             fail = str(result.failure_count),
705             error = str(result.error_count),
706             passrate =self.passrate,
707         )
708         return report
709
710
711     def _generate_report_test(self, rows, cid, tid, n, t, o, e):
712         # e.g. 'pt1.1', 'ft1.1', etc
713         has_output = bool(o or e)
714         # ID修改点为下划线,支持Bootstrap折叠展开特效 - Findyou
715         tid = (n == 0 and 'p' or 'f') + 't%s_%s' % (cid+1,tid+1)
716         name = t.id().split('.')[-1]
717         doc = t.shortDescription() or ""
718         desc = doc and ('%s: %s' % (name, doc)) or name
719         tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL
720
721         # utf-8 支持中文 - Findyou
722          # o and e should be byte string because they are collected from stdout and stderr?
723         if isinstance(o, str):
724             # TODO: some problem with 'string_escape': it escape \n and mess up formating
725             # uo = unicode(o.encode('string_escape'))
726             # uo = o.decode('latin-1')
727             uo = o
728         else:
729             uo = o
730         if isinstance(e, str):
731             # TODO: some problem with 'string_escape': it escape \n and mess up formating
732             # ue = unicode(e.encode('string_escape'))
733             # ue = e.decode('latin-1')
734             ue = e
735         else:
736             ue = e
737
738         script = self.REPORT_TEST_OUTPUT_TMPL % dict(
739             id = tid,
740             output = saxutils.escape(uo+ue),
741         )
742
743         row = tmpl % dict(
744             tid = tid,
745             Class = (n == 0 and 'hiddenRow' or 'none'),
746             style = n == 2 and 'errorCase' or (n == 1 and 'failCase' or 'passCase'),
747             desc = desc,
748             script = script,
749             status = self.STATUS[n],
750         )
751         rows.append(row)
752         if not has_output:
753             return
754
755     def _generate_ending(self):
756         return self.ENDING_TMPL
757
758
759 ##############################################################################
760 # Facilities for running tests from the command line
761 ##############################################################################
762
763 # Note: Reuse unittest.TestProgram to launch test. In the future we may
764 # build our own launcher to support more specific command line
765 # parameters like test title, CSS, etc.
766 class TestProgram(unittest.TestProgram):
767     """
768     A variation of the unittest.TestProgram. Please refer to the base
769     class for command line parameters.
770     """
771     def runTests(self):
772         # Pick HTMLTestRunner as the default test runner.
773         # base class's testRunner parameter is not useful because it means
774         # we have to instantiate HTMLTestRunner before we know self.verbosity.
775         if self.testRunner is None:
776             self.testRunner = HTMLTestRunner(verbosity=self.verbosity)
777         unittest.TestProgram.runTests(self)
778
779 main = TestProgram
780
781 ##############################################################################
782 # Executing this module from the command line
783 ##############################################################################
784
785 if __name__ == "__main__":
786     main(module=None)