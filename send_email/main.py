import os;
from dotenv import load_dotenv
load_dotenv()

#email pkg
import email, smtplib, ssl
from email.message import EmailMessage
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#gmail log in
email_sender = os.getenv('email_sender')
email_password = os.getenv('email_password')

# mail
email_receiver = "here"
email_cc = "here"
subject = "Test - Python script"
body = """
    It's a test    
"""
msg = MIMEMultipart()
msg['From'] = email_sender
msg['To'] = email_receiver
msg['Cc'] = email_cc
msg['Subject'] = subject

# Add body to email
msg.attach(MIMEText(body, "plain"))

filename = 'path_file'  # In same directory as script

# Open PDF file in binary mode
with open(filename, "r") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
msg.attach(part)
text = msg.as_string()

# Add SSL (layer of security)
context = ssl.create_default_context()

try :
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)
    print("Email sent successfully !")
except smtplib.SMTPException :
    print("Failed to send email")

