# encoding: utf8

"""
Created on 2017.07.11

@author: yalei
"""

import glob
import logging
import itchat
from datetime import datetime
from itchat.content import *
from config import *
from camera import capture_now
from mail import send_mail


MS_ROBOT = ''
ADMIN_USER = ''
LAST_CHAT_USER = ''
USER_MAP = dict()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:[%(levelname)s] %(message)s',
                    filename='wechat.log',
                    filemode='a')


def get_user_name(uid):
    global USER_MAP
    if uid not in USER_MAP:
        USER_MAP[uid] = itchat.search_friends(userName=uid).get('NickName')
    return USER_MAP[uid]


def get_last_file(folder):
    import os
    list_of_files = glob.glob(os.path.join(folder, '*.jpg'))
    return max(list_of_files, key=os.path.getctime)


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def robot_text_reply(msg):
    # 使用小冰回复
    global LAST_CHAT_USER, MS_ROBOT
    if msg['FromUserName'] == MS_ROBOT:
        logging.info('[xiaobing-ms]:[%s]' % msg['Text'])
        if LAST_CHAT_USER:
            itchat.send(msg['Text'], LAST_CHAT_USER)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isMpChat=True)
def robot_media_reply(msg):
    global LAST_CHAT_USER
    if msg['FromUserName'] == MS_ROBOT and LAST_CHAT_USER:
        itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']),
                    LAST_CHAT_USER)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isMpChat=False)
def user_media_reply(msg):
    global LAST_CHAT_USER
    LAST_CHAT_USER = msg['FromUserName']
    itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']),
                MS_ROBOT)


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=False)
def user_text_reply(msg):
    global LAST_CHAT_USER
    msg_text = msg['Text']
    user = msg['FromUserName']
    logging.info('[%s]:[%s]' % (get_user_name(user), msg_text))
    # 拍照并传送
    if msg_text == TEXT_CAMERA:
        itchat.send(u'请稍等，正在尝试拍照传送', user)
        filename = os.path.join(IMAGE_DIR, datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.jpg')
        code_status, msg = capture_now(filename)
        if code_status == 0:
            itchat.send_image(filename, user)
        else:
            itchat.send('Error: ' + msg, user)

    # 传送图片
    elif msg_text == TEXT_PIC:
        itchat.send(u'请稍等，正在查找最近拍摄的图片', user)
        filename = get_last_file(IMAGE_DIR)
        if filename:
            itchat.send_image(filename, user)
        else:
            itchat.send(u'当前暂无图片文件', user)

    elif msg_text == START_JOB:
        setup_job()
        itchat.send(u'已开启定时拍照任务', user)
    elif msg_text == STOP_JOB:
        stop_job()
        itchat.send(u'已关闭定时拍照任务', user)

    elif msg_text.startswith(COMMAND) and user == ADMIN_USER:
        cmd = msg_text.lstrip(COMMAND).strip()
        result = run_shell(cmd) if cmd else u'错误的空命令'
        itchat.send(result, user)

    else:
        # 传给小冰等回复
        LAST_CHAT_USER = user
        itchat.send(msg['Text'], MS_ROBOT)


def qr_callback(uuid, status, qrcode):
    send_mail(qrcode)
    print('Check your email to login wechat.')


if __name__ == '__main__':
    itchat.auto_login(hotReload=True, enableCmdQR=False, qrCallback=qr_callback)
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    ADMIN_USER = itchat.search_friends(name=u'yalei')[0]["UserName"]
    MS_ROBOT = itchat.search_mps(name=u'小冰')[0]['UserName']
    print("Login with account: [%s]" % myUserName)
    itchat.run()
