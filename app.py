#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: app.py
# Project: FIT
# Created Date: Saturday, June 19th 2021, 8:25:20 am
# Author: Fabio Zito
# -----
# Last Modified: Tue Oct 19 2021
# Modified By: Fabio Zito
# -----
# MIT License
# 
# Copyright (c) 2021 ZF zitelog@gmail.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
###### 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys
from view.wizard import WizardView
from view.web import WebView
from view.insta import InstaView
from view.fb import FbView
from view.verifysignature import VerifySignatureView

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wizard = WizardView()
    wizard.init_wizard()
    web = WebView()
    web.hide()
    insta = InstaView()
    insta.hide()
    fb = FbView()
    fb.hide()
    verify_signature = VerifySignatureView()
    verify_signature.hide()


    def start_task(task, case_id):

        if (task == 'web'):
            acquisition_window = web
        elif (task == 'mail'):
            pass
        elif (task == 'insta'):
            acquisition_window = insta
        elif (task == 'fb'):
            acquisition_window = fb
        elif (task == 'verify_signature'):
            acquisition_window = verify_signature

        acquisition_window.init(case_id)
        acquisition_window.show()


    # Wizard sends a signal when finish button is clicked and case is stored on the DB
    wizard.finished.connect(lambda task, case_id: start_task(task, case_id))

    wizard.show()

    sys.exit(app.exec_())