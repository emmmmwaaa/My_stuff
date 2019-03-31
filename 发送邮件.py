from email.mime.image import MIMEImage
from email.header import Header
from email.utils import parseaddr,formataddr
from email.mime.base import MIMEBase
from email import encoders
#先定义署名格式化函数
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

#发送人，接收人
sender='13218022128@163.com'
pwd='Gxc072403666' #请自行登陆邮箱打开SMTP服务，会自动生成第三方授权码，不是登陆密码！
receiver='1540214631@qq.com'

#格式化的署名和接收人信息
message=MIMEMultipart()
message['From']=_format_addr('这是xx<%s>'%sender)
message['To']=_format_addr(receiver)
message['Subject']=('我是标题！！')
message.attach(MIMEText('<html><body>'
                        +'<h1>Hello</h1>'
                        +'<p>礼物<img src="cid:Imgid">'
                        +'</body></html>','html','utf-8'))

#MIMEImage，只要打开相应图片，再用read()方法读入数据，指明src中的代号是多少，如这里是'Imgid’，在HTML格式里就对应输入。
with open('C:/Users/NJU-GXC/test.png', 'rb') as f:
    mime=MIMEImage(f.read())
    mime.add_header('Content-ID','Imgid')
    message.attach(mime)

with open('C:/Users/NJU-GXC/test.png', 'rb') as f:

    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'png', filename='test.png')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='test.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    message.attach(mime)
#发送邮件！
try:
    smtpobj=smtplib.SMTP('smtp.163.com', 25)
    smtpobj.set_debuglevel(1)
    smtpobj.login(sender,pwd)
    smtpobj.sendmail(sender,[receiver],message.as_string())
    print('邮件发送成功')
    smtpobj.quit()
except smtplib.SMTPException as e:
    print('邮件发送失败，Case:%s'%e)
	