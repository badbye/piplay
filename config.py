# encoding: utf8

"""
Created on 2017.07.12

@author: yalei
"""

import os
import logging
from crontab import CronTab
from subprocess import Popen, PIPE


# RESOLUTION = [1080, 810]
# FPS = 16
TEXT_CAMERA = u'拍照'
TEXT_PIC = u'照片'
START_JOB = u'开始任务'
STOP_JOB = u'停止任务'
COMMAND = u'执行命令'

# BASE_DIR = os.path.dirname(__file__)
BASE_DIR = '/home/yalei/piplay'
IMAGE_DIR = os.path.join(BASE_DIR, 'pic')
if not os.path.exists(IMAGE_DIR):
    os.mkdir(IMAGE_DIR)


def setup_job():
    my_cron = CronTab(user='yalei')
    for job in my_cron:
        if job.comment == u'camera':
            return
    job = my_cron.new(command='bash /home/yalei/cronpic/app.sh 2>&1', comment='camera')
    job.minute.every(1)
    my_cron.write()


def stop_job():
    my_cron = CronTab(user='yalei')
    for job in my_cron:
        if job.comment == u'camera':
            my_cron.remove(job)
            my_cron.write()
            return


def run_shell(cmd, **kwargs):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    logging.info('shell command: [%s]' % cmd)
    return u'stdout: %s; error: %s' % p.communicate()