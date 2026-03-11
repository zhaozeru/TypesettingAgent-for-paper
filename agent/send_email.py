from state.schema import MaingraphState
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from langchain_core.messages import SystemMessage
import mimetypes


def send_email_node(state: MaingraphState):
    system_messages = [
        SystemMessage(content="<-- 进入 11 send_email 发送邮件节点！-->")
    ]
    receiver_email = state.get("email", "")
    if receiver_email:
        receiver_email = receiver_email.strip()
    system_messages.append(SystemMessage(content=f"📨 发送邮件至：{receiver_email}"))

    attachment_path = state.get("final_paper")
    if not attachment_path or not os.path.exists(attachment_path):
        system_messages.append(SystemMessage(content=f"❌ 附件文件不存在：{attachment_path}"))
        return {"messages": system_messages}

    filename = os.path.basename(attachment_path)
    system_messages.append(SystemMessage(content=f"📎 准备发送附件：{filename}"))

    # 3. 邮件配置
    mail_host = 'smtp.163.com'
    mail_user = '13652001060@163.com'
    mail_pass = 'YLT6XjWK8C2g66AU'
    sender = mail_user

    # 4. 构建邮件
    message = MIMEMultipart()
    message['Subject'] = '【论文排版完成】请查收您的文档'
    message['From'] = sender
    message['To'] = receiver_email

    text_content = '您好，您提交的论文已完成格式排版，请查收附件。'
    message.attach(MIMEText(text_content, 'plain', 'utf-8'))

    # 添加附件
    try:
        # 获取文件的MIME类型
        file_ext = os.path.splitext(filename)[1].lower()
        mime_type, _ = mimetypes.guess_type(attachment_path)

        if not mime_type:
            # 根据文件扩展名设置MIME类型
            if file_ext == '.docx':
                mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif file_ext == '.doc':
                mime_type = 'application/msword'
            elif file_ext == '.pdf':
                mime_type = 'application/pdf'
            else:
                mime_type = 'application/octet-stream'  # 默认类型

        # 读取文件并创建附件
        with open(attachment_path, "rb") as f:
            file_data = f.read()

        # 创建MIME附件
        attachment = MIMEBase(*mime_type.split('/', 1))
        attachment.set_payload(file_data)
        encoders.encode_base64(attachment)

        # 正确处理文件名（特别是中文文件名）
        from email.header import Header
        encoded_filename = Header(filename, 'utf-8').encode()

        # 设置附件头信息
        attachment.add_header(
            'Content-Disposition',
            'attachment',
            filename=encoded_filename
        )

        # 添加MIME类型信息
        attachment.add_header('Content-Type', mime_type)
        if mime_type.startswith('application/'):
            attachment.add_header('Content-Transfer-Encoding', 'base64')

        message.attach(attachment)
        system_messages.append(SystemMessage(content="✅ 附件已正确添加"))

    except Exception as e:
        system_messages.append(SystemMessage(content=f"❌ 添加附件失败：{str(e)}"))
        return {"messages": system_messages}

    # 5. 发送邮件
    try:
        with smtplib.SMTP_SSL(mail_host, 465) as smtp:
            smtp.login(mail_user, mail_pass)
            smtp.sendmail(sender, [receiver_email], message.as_string())
        system_messages.append(SystemMessage(content="✅ 邮件发送成功！"))
    except Exception as e:
        system_messages.append(SystemMessage(content=f"❌ 邮件发送失败：{str(e)}"))

    return {"messages": system_messages}