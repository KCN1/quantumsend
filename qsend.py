import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from argparse import ArgumentParser
from pathlib import Path

# mail server settings
server_address = "smtp.mail.ru"
server_port = 25
login, password = "login", "password" # TODO: set login & SMTP/IMAP password

# message content
msg = MIMEMultipart()
msg['From'], msg['To'], msg['Subject'] = "from@mail.ru", "to@mail.ru", "quantumsend test" # TODO: set "FROM", "TO" and "SUBJECT"
msg.attach(MIMEText("some text", 'plain')) # TODO: replace "some text" with your message

# file path parser
parser = ArgumentParser()
parser.add_argument("file_path", type=Path)
p = parser.parse_args()

# adds attachment
if p.file_path.is_file():
    with open(p.file_path, "rb") as fp:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(fp.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={p.file_path.name}')
        msg.attach(part)

# sends message
with smtplib.SMTP(server_address, server_port) as server:
    server.starttls()
    server.login(login, password)
    server.send_message(msg)

