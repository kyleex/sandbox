import os
from dotenv import load_dotenv
load_dotenv()

import datetime

# data pkg
import mysql.connector
from mysql.connector import Error
import csv

#email pkg
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# SMTP server settings
smtp_server = os.getenv('smtp_server')
smtp_port = os.getenv('smtp_port')
smtp_username = os.getenv('smtp_username')
smtp_password = os.getenv('smtp_password')

# ----------------- define function -----------------

def connect_to_sql_server () :
  connection = None #closes any existing connections so that the server doesn't become confused with multiple open connections
  try :
    mydb = mysql.connector.connect(
      host = os.getenv('sql_server_host'),
      user = os.getenv('sql_server_user'),
      password = os.getenv('sql_server_password')
    )
    print("✅ Successfully connected to MySQL Server")
    return mydb
  
  except Error as err:
    print(f"\n❌ Failed to connect to MySQL Server, error message: '{err}'")

# get the current date (YYYY-MM-DD)
def current_date() :
  now = datetime.datetime.now()
  return now.strftime("%Y-%m-%d")

# ----------------- Main -----------------

csv_file_name = "FileName" + "_" + current_date() + ".csv"

# Créer le fichier csv, collect les données pour les écrires dans le fichier csv
with open(csv_file_name, "w", newline="") as csvfile :

    # créer le fichier csv
    print(f"\n❕ Creating the CSV file '{csv_file_name}'...")
    
    csv_writer = csv.writer(csvfile)
    nb_rows_written_in_csv_file = 0

    # vérifie si le fichier csv a été créé
    if os.path.exists(csv_file_name) :
        print(f"✅ Le fichier CSV '{csv_file_name}' a été créé avec succès.\n")
    else :
        print(f"❌ Erreur lors de la création du fichier CSV '{csv_file_name}'\n")

    # connect & récupère les données de la table
    print(f"❕ Collecting data to insert into the CSV file...")

    mydb = connect_to_sql_server()
    mycursor = mydb.cursor()

    query = "SELECT * FROM sandbox.customer"
    mycursor.execute(query)
    result = mycursor.fetchall()

    #récupère le nombre de lignes de la table
    NB_ROWS = len(result)

    # récupère les données & les écrit dans le fichier csv
    columns = [col[0] for col in mycursor.description]
    csv_writer.writerow(columns)

    for row in result:
        csv_writer.writerow(row)
        nb_rows_written_in_csv_file += 1

    # vérifie si les données récupérées ont été écrites dans le fichier csv
    if nb_rows_written_in_csv_file == NB_ROWS :
        print(f"✅ Les données de la table ont été récupérées avec succès.")
    else :
        print(f"❌ Erreur lors de la récupération des données de la table")
        

    # ferme la connection
    mycursor.close()
    mydb.close()


# Send email with csv file attached
# Email details
email_to = "enter email address here"
email_cc = "enter email address here"
email_cci = "enter email address here"
subject = "CSV File Attachment"
body = "Please find the attached CSV file."

# File details
file_path = str(csv_file_name)

def send_email():
    # Create a MIMEMultipart message
    print(f"\n❕ Sending email with CSV file attached...")

    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = email_to
    msg["Cc"] = email_cc
    msg["Bcc"] = email_cci
    msg["Subject"] = subject

    # Attach the body text to the email
    msg.attach(MIMEText(body, "plain"))

    # Attach the CSV file created above to the email
    with open(file_path, "r") as csvfile:
        part = MIMEApplication(csvfile.read())
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
        msg.attach(part)
        
    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email_to, msg.as_string())
        server.quit()
        print("✅ Email sent successfully !")
    except Exception as e:
        print("❌ Failed to send email", e)

send_email()