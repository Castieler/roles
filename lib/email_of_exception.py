import smtplib
from email.mime.text import MIMEText

# 第三方 SMTP 服务
mail_host = "smtp.mxhichina.com"  # SMTP服务器
mail_user = "xiamingyu@xywy.com"  # 用户名
mail_pass = "Hello1234"  # 授权密码，非登录密码

sender = 'xiamingyu@xywy.com'  # 发件人邮箱(最好写全, 不然会失败)
receivers = ['1083298593@qq.com','1277338682@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
cc_reciver = ''.join(['1277338682@qq.com','xiamingyu@xywy.com'])
content = '我用Python'
title = 'djongo项目异常'  # 邮件主题


def sendEmail(title='djongo项目异常', content=None):
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title
    message['Cc'] = cc_reciver
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)



if __name__ == '__main__':
    sendEmail(title,content)
