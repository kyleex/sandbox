import os;
from dotenv import load_dotenv
load_dotenv()

#email pkg
import smtplib
import ssl
from email.message import EmailMessage

#gmail log in
email_sender = os.getenv('email_sender')
email_password = os.getenv('email_password')

# mail
email_receiver = "antwill34@icloud.com"
subject = "Test - Python script"
body = """
    It's a test    
"""
em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())





