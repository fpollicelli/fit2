#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: packetcapture.py
# Project: FIT
# Created Date: Thursday, August 26th 2021, 8:57:06 am
# Author: Fabio Zito
# -----
# Last Modified: Sun Aug 29 2021
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

import pyshark
import tempfile
import os
from datetime import datetime

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox


from view.error import ErrorView

from common.error import ErrorMessage
import common.utility as utility


class PacketCaptureView(QObject):
    finished = pyqtSignal()  # give worker class a finished signal

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.error_msg = ErrorMessage()
        self.run = True
        self.options = None
        self.destroyed.connect(self.stop)

    def set_options(self, options):
        self.output_file = os.path.join(options['acquisition_directory'], options['filename'])
        self.tmp_output_file = os.path.join(tempfile.gettempdir(), 'tmp' + str(datetime.utcnow().timestamp()) + '.pcap')
    
    def start(self):
        capture = pyshark.LiveCapture(output_file=self.tmp_output_file)
        try:
            for packet in capture.sniff_continuously():
                    if not self.run:
                        capture.close()
                        #I don't know why, but if I don't read and rewrite the pcap file generated with Livecapture 
                        #when I open it with WireShark a critical pop-up appears with this error: 
                        # (The capture file appears to have been cut short in the middle of a packet).
                        #I know this not elengant but works:
                        capture = pyshark.FileCapture(self.tmp_output_file, output_file=self.output_file)
                        capture.load_packets()

            os.remove(self.tmp_output_file)
            self.finished.emit()
        except pyshark.capture.capture.TSharkCrashException as error:
            error_dlg = ErrorView(QMessageBox.Critical,
                            self.error_msg.TITLES['capture_packet'],
                            self.error_msg.MESSAGES['capture_packet'],
                            str(error)
                            )
            error_dlg.buttonClicked.connect(quit)
            error_dlg.exec_()

    def stop(self):
        self.run = False