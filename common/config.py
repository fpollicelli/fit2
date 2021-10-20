#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: log_config.py
# Project: FIT
# Created Date: Tuesday, August 31st 2021, 10:22:49 pm
# Author: Fabio Zito
# -----
# Last Modified: Sun Sep 26 2021
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

import datetime
import logging
import os


# Produce RFC 3339 timestamps
logging.Formatter.formatTime = (lambda self, record, datefmt: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat())

class LogConfig:
    def __init__(self):

        self.config = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'detailed': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
                },
                'hashreport': {
                    'class': 'logging.Formatter',
                    'format': '%(message)s'
                },
                'acquisition': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s - %(message)s'
                }

            },
            'handlers': {
                "null": {
                    "class": "logging.NullHandler"
                },
                'facquisition': {
                    'class': 'logging.FileHandler',
                    'filename': 'acquisition.log',
                    'mode': 'w',
                    'formatter': 'acquisition',
                },
                'fhashreport': {
                    'class': 'logging.FileHandler',
                    'filename': 'acquisition.hash',
                    'mode': 'w',
                    'formatter': 'hashreport',
                }
            },
            'loggers': {
                'view.web': {
                    'handlers': ['facquisition'],
                    'level' : 'INFO'
                },
                'hashreport': {
                    'handlers': ['fhashreport'],
                    'level' : 'INFO'
                },
            },
            'root': {
                'handlers': ['null'],
                "propagate": False
            }
        }

    def change_filehandlers_path(self, path, exclude=None):
        for key in self.config['handlers']:
            handler = self.config['handlers'][key]
            if 'filename' in handler.keys():
                handler['filename'] = os.path.join(path, handler['filename'])

    def disable_loggers(self, loggers):
        for logger in loggers:
            for handler in logger.handlers.copy():
                logger.removeHandler(handler)    
            logger.addHandler(logging.NullHandler())
            logger.propagate = False