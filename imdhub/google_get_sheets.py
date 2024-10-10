"""Download google sheets
# FILE: google_get_sheets.py
# AUTHOR: David Ruvolo
# CREATED: 2024-10-02
# MODIFIED: 2024-10-02
# PURPOSE: Retrieve google sheet files
# STATUS: stable
# PACKAGES: **see below**
# COMMENTS: NA
"""

import os.path
import pandas as pd
from os import environ, system
from dotenv import load_dotenv
from pandas.io.formats import excel
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

excel.ExcelFormatter.header_style = None

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def get_imdhub_site(service):
    """Get IMDHUB-SITE File"""
    print('Downloading IMDHUB-SITE data model....')
    try:
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=environ['IMDHUB_SITE_FILE'], range='molgenis!A2:Q')
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        print('Saving data....')
        data = pd.DataFrame(values[1:], columns=values[0])
        filtered = data[data['shouldImport'] == "TRUE"]
        filtered = data[data['rowsToTest'] == "TRUE"]
        filtered.to_excel('imdhub-site.xlsx', sheet_name='molgenis', index=0)

    except HttpError as err:
        print(err)


def get_imdhub_ids(service):
    """Get identifier data model"""
    print('Retrieving IMDHUB Identifier list data model....')
    try:
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=environ['IMDHUB_IDS_FILE'], range='molgenis!A1:M')
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        print('Saving data')
        data = pd.DataFrame(values[1:], columns=values[0])
        filtered = data[data['shouldImport'] == "TRUE"]
        filtered.to_excel('imdhub-ids.xlsx', sheet_name='molgenis', index=0)
    except HttpError as err:
        print(err)


def get_imdhub_staging(service):
    """Get staging table data model"""
    print('Retrieving IMDHUB Staging table data model....')
    try:
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=environ['IMDHUB_STAGING_FILE'], range='molgenis!A2:K')
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        print('Saving data')
        data = pd.DataFrame(values[1:], columns=values[0])
        filtered = data[data['shouldImport'] == "TRUE"]
        filtered.to_excel('imdhub-staging.xlsx',
                          sheet_name='molgenis', index=0)
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)

    # ///////////////////////////////////////

    # get imdhub-ids.xlsx
    get_imdhub_ids(service=service)
    system('xlsx2csv --sheet 0 imdhub-ids.xlsx model/imdhub-ids/')
    system('mv imdhub-ids.xlsx files/')

    # get imdhub-site.xlsx
    get_imdhub_site(service=service)
    system('xlsx2csv --sheet 0 imdhub-site.xlsx model/imdhub-site/')
    system("mv imdhub-site.xlsx files/")

    # get imdhub-staging.xlsx
    get_imdhub_staging(service=service)
    system('xlsx2csv --sheet 0 imdhub-staging.xlsx model/imdhub-staging/')
    system('mv imdhub-staging.xlsx files/')
