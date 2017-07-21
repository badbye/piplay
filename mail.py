# encoding: utf8

"""
Created on 2017.07.12

@author: yalei
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


mailto_list = ["xxxx@163.com"]  # 目标邮箱
mail_host = "smtp.163.com"
mail_user = "xxxxx@163.com"
mail_pass = "xxxx"


def send_mail(binary_img_data, title='wechat QR code', img_id='qrcode'):
    me = "yalei" + "<" + mail_user + ">"
    msg = MIMEMultipart()
    msg['Subject'] = title
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)
    try:
        # set data
        msg_text = MIMEText('<b>Scan to login.</b><br><img src="cid:%s"><br>' % img_id, 'html')
        msg.attach(msg_text)
        img_data = MIMEImage(binary_img_data)
        img_data.add_header('Content-ID', '<%s>' % img_id)
        msg.attach(img_data)
        # send mail
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, msg['To'], msg.as_string())
        server.close()
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    print('success:')
