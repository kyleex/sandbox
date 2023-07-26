
import os
from dotenv import load_dotenv
load_dotenv()

import datetime

import mysql.connector
from mysql.connector import Error
import csv

# -----------------

# define function to connect to the sql server
def connect_to_sql_server () :
  connection = None #closes any existing connections so that the server doesn't become confused with multiple open connections
  try :
    mydb = mysql.connector.connect(
      host = os.getenv('sql_server_host'),
      user = os.getenv('sql_server_user'),
      password = os.getenv('sql_server_password')
    )
    print("MySQL Database connection successfull")
    return mydb
  
  except Error as err:
    print(f"Error: '{err}'")

# get the current date (YYYY-MM-DD)
def current_date() :
  now = datetime.datetime.now()
  return now.strftime("%Y-%m-%d")

# ----------------- 

csv_file_name = input("Enter the name of the csv file you want to create : ") + "_" + current_date() + ".csv"

# Créer le fichier csv, collect les données pour les écrires dans le fichier csv
with open(csv_file_name, "w", newline="") as csvfile :

  # créer le fichier csv
  print(f"\nCreating the CSV file '{csv_file_name}'...")
  csv_writer = csv.writer(csvfile)

  # vérifie si le fichier csv a été créé
  if os.path.exists(csv_file_name) :
    print(f"Le fichier CSV '{csv_file_name}' a été créé avec succès.\n")
  else :
    print(f"Erreur lors de la création du fichier CSV '{csv_file_name}'\n")


  # connect & récupère les données de la table
  mydb = connect_to_sql_server()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM sandbox.customer")

  # noms des colonnes de la table
  columns = [col[0] for col in mycursor.description]
  csv_writer.writerow(columns)

  # data
  for row in mycursor.fetchall():
    print(row)
    csv_writer.writerow(row)

  # ferme la connection
  mycursor.close()
  mydb.close()