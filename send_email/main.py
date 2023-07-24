import os;
from dotenv import load_dotenv
load_dotenv()

#email pkg
import smtplib, ssl
from email.message import EmailMessage

#gmail log in
email_sender = os.getenv('email_sender')
email_password = os.getenv('email_password')

# mail
email_receiver = ["antwill34@icloud.com"]
email_cc = ["antwill344@gmail.com"]
subject = "Test - Python script"
body = """
    It's a test    
"""
msg = EmailMessage()
msg['From'] = email_sender
msg['To'] = email_receiver
msg['Cc'] = email_cc
msg['Subject'] = subject
msg.set_content(body)

# Add SSL (layer of security)
context = ssl.create_default_context()

try :
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)
    print("Email sent successfully !")
except smtplib.SMTPException :
    print("Failed to send email")

