"""Generate Identifiers for use in the IMDHub"""

from os import environ
from datetime import datetime
from datatable import dt, f
import pandas as pd
from molgenis_emx2_pyclient import Client
from dotenv import load_dotenv
from pandas.io.formats import excel
from imdhub.utils import generate_random_id

excel.ExcelFormatter.header_style = None

load_dotenv()
HOST = environ['IMDHUB_HOST']
TOKEN = environ['IMDHUB_TOKEN']

# retrieve organisations
with Client(url=HOST, token=TOKEN) as client:
    organisations = client.get(schema='IMDHub Refs', table="Organisations")

# ///////////////////////////////////////////////////////////////////////////////

# ~ 1 ~
# Generate identifiers

NUM_ITEMS = 50
generated_pids = {}

today = datetime.now().strftime('%F')

# create PIDs
for org in organisations:
    print('Generating ids for', org['name'])
    for num in range(NUM_ITEMS):
        is_valid_pid = False
        while is_valid_pid is False:
            new_pid = f"P{generate_random_id(length=5)}"
            if new_pid not in generated_pids:
                generated_pids[new_pid] = {
                    'identifier': new_pid,
                    'clinical site': org['name'],
                    'date created': today,
                    'status': 'Available'
                }
                is_valid_pid = True

pids_data = [generated_pids[pid] for pid in generated_pids.keys()]

# ///////////////////////////////////////////////////////////////////////////////

# ~ 2 ~
# save to file and import into central database

pids_dt = dt.Frame(pids_data)
site_id_dt = pids_dt[f['clinical site'] == 'University Hospital Heidelberg', :]

# import all participant identifiers
with Client(url=HOST, token=TOKEN) as client:
    client.save_schema(
        name='IMDHub Site Identifiers',
        table='Participant identifiers',
        data=pids_dt.to_pandas().to_dict('records')
    )
    client.save_schema(
        name='DE4',
        table='Participant identifiers',
        data=site_id_dt.to_pandas().to_dict('records')
    )
