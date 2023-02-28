import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Acceder a la API de google sheets and google drive:
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]
#Cargar credenciales
credentials = ServiceAccountCredentials.from_json_keyfile_name("Utils/creds.json", scope)
#Obtener un cliente
CLIENT = gspread.authorize(credentials)