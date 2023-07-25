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

def send_email(email_login, password_login, email_to, email_cc, email_cci, email_subject, email_body, email_attach_file) :
    msg = MIMEMultipart()
    msg['From'] = email_login
    msg['To'] = email_to
    msg['Cc'] = email_cc
    msg['Cci'] = email_cci
    msg['Subject'] = email_subject
    
    # # Add body to email
    msg.attach(MIMEText(email_body, "plain"))

    # Open PDF file in binary mode
    with open(email_attach_file, "r") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {email_attach_file}",
    )

    # Add attachment to message and convert message to string
    msg.attach(part)
    text = msg.as_string()

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    try :
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_login, password_login)
            smtp.send_message(msg)
        print("✅ Email sent successfully !")
    except smtplib.SMTPException :
        print("❌ Failed to send email")

print("\ne̳m̳a̳i̳l̳ s̳e̳n̳d̳e̳r̳\n")


# Ask for login informations
print("Login :")
email_login = input("Enter your email address : ")
password_login = input("Enter your app password : ")
print("Thank you, your information has temporary been save until the end of the process !\n")

# ask for email campaign details
print("Details : ")
email_to = input("Send to : ")
email_cc = input("Cc : ")
email_cci = input("Cci : ")
email_subject = input("Subject : ")
email_body = input("Write your message : ")
email_attach_file = input("Paste the path file you want to attach : ")

#proceed to send the email
send_email(email_login, password_login, email_to, email_cc, email_cci, email_subject, email_body, email_attach_file)    

