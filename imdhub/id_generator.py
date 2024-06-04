"""Generate Identifiers for use in the IMDHub"""

from os import environ
import random
import string
from datetime import datetime
from datatable import dt, f
import pandas as pd
from molgenis_emx2_pyclient import Client
from dotenv import load_dotenv
load_dotenv()

HOST = environ['IMDHUB_HOST']
TOKEN = environ['IMDHUB_TOKEN']


def generate_random_id(length: int = 6):
    """Generate string of letters and numbers to a desired length

    :param length: a number indicating the length of the identifier
    :type length: int
    """
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))


# retrieve organisations
with Client(url=HOST, token=TOKEN) as client:
    organisations = client.get(schema='IMDhub Refs', table="Organisations")

# ///////////////////////////////////////////////////////////////////////////////

# ~ 1 ~
# Generate identifiers

NUM_ITEMS = 20
generated_pids = {}
generated_sids = {}

# create PIDs
for org in organisations:
    print('Generating ids for', org['name'])
    for num in range(NUM_ITEMS):
        is_valid_pid = False
        while is_valid_pid is False:
            new_pid = f"P.{generate_random_id()}"
            if new_pid not in generated_pids:
                generated_pids[new_pid] = {
                    'identifier': new_pid,
                    'clinical_site': org['name'],
                    'date_created': datetime.now().strftime("%F"),
                    'status': 'Available'
                }
                is_valid_pid = True


# Generate SIDs
for org in organisations:
    print('Generating ids for', org['name'])
    for num in range(NUM_ITEMS):

        # generate SID
        is_valid_sid = False
        while is_valid_sid is False:
            new_sid = f"S.{generate_random_id()}"
            if new_sid not in generated_sids:
                generated_sids[new_sid] = {
                    'identifier': new_sid,
                    'clinical_site': org['name'],
                    'date_created': datetime.now().strftime("%F"),
                    'status': 'Available'
                }
                is_valid_sid = True


pids_data = [generated_pids[pid] for pid in generated_pids.keys()]
sids_data = [generated_sids[sid] for sid in generated_sids.keys()]


# ///////////////////////////////////////////////////////////////////////////////

# ~ 2 ~
# save to file and import into central database

pids_dt = dt.Frame(pids_data)
sids_dt = dt.Frame(sids_data)

today = datetime.now().strftime('%F')

# ~ 2a ~
# assign the first 9 participant identifiers
umcg_pids = pids_dt[
    f.clinical_site == "University of Groningen", 'identifier'].to_list()[0][:9]

for id in umcg_pids:
    pids_dt[
        f.identifier == id,
        ('status', 'date_assigned', 'date_updated', 'updated_by')
    ] = ('Assigned', today, today, 'David')


# ~ 2b ~
# Assign the first 9 biospecimen identifiers
umcg_sids = sids_dt[
    f.clinical_site == "University of Groningen", 'identifier'].to_list()[0][:9]

for id in umcg_sids:
    sids_dt[
        f.identifier == id,
        ('status', 'date_assigned', 'date_updated', 'updated_by')
    ] = ('Assigned', today, today, 'David')


with pd.ExcelWriter('./data/IMDhub Identifiers.xlsx') as wb:
    pids_df = pids_dt.to_pandas()
    sids_df = sids_dt.to_pandas()
    pids_df.to_excel(wb, sheet_name='Participant identifiers', index=False)
    sids_df.to_excel(wb, sheet_name='Biospecimen identifiers', index=False)
