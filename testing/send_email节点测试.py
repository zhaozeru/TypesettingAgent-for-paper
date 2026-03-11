import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict


def interrupt(prompt: Dict[str, str]) -> str:
    message = ""
    if isinstance(prompt, dict):
        message = prompt.get("human_input")
        if not message:
            message = next(iter(prompt.values()), "请输入信息：")
    else:
        message = "请输入信息："

    user_input = input(f"\n🟡 [输入地址] {message}")
    return user_input.strip()


raw_input = interrupt({"human_input": "请输入接收文件的邮箱地址~："})
if "@" not in raw_input:
    print("❌ 邮箱格式无效！")

receiver_email = raw_input
print(f"📨 即将发送邮件至：{receiver_email}")

mail_host = 'smtp.163.com'
mail_user = '13652001060@163.com'
mail_pass = 'YLT6XjWK8C2g66AU'

sender = mail_user
receivers = [receiver_email]

message = MIMEMultipart()
message['Subject'] = '测试邮件！'
message['From'] = sender
message['To'] = receiver_email

text_content = '这是测试邮件正文。无需注意查看附件。'
content = MIMEText(text_content, 'plain', 'utf-8')
message.attach(content)

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.set_debuglevel(0)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.quit()
    print("✅ 邮件发送成功！")

except Exception as e:
    print('❌ 邮件发送错误:', e)
