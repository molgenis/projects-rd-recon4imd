"""Generate Identifiers for use in the IMDHub"""

from os import environ
import random
import string
from datetime import datetime
import pandas as pd
from molgenis_emx2_pyclient import Client
from dotenv import load_dotenv
load_dotenv()

HOST = environ['IMDHUB_HOST']
TOKEN = environ['IMDHUB_TOKEN']


def generate_random_id(length: int = 12):
    """Generate string of letters and numbers to a desired length

    :param length: a number indicating the length of the identifier
    :type length: int
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


# retrieve organisations
with Client(url=HOST, token=TOKEN) as client:
    organisations = client.get(schema='IMDHub Refs', table="Organisations")


generated_pids = {}
generated_sids = {}

# create PIDs
for org in organisations:
    print('Generating ids for', org['name'])
    for num in range(60):
        is_valid_pid = False
        while is_valid_pid is False:
            new_pid = f"P-{generate_random_id()}"
            if new_pid not in generated_pids:
                generated_pids[new_pid] = {
                    'identifier': new_pid,
                    'clinical_site': org['name'],
                    'date_created': datetime.now().strftime("%Y-%m-%d"),
                    'status': 'Available'
                }
                is_valid_pid = True


for org in organisations:
    print('Generating ids for', org['name'])
    for num in range(60):

        # generate SID
        is_valid_sid = False
        while is_valid_sid is False:
            new_sid = f"S-{generate_random_id()}"
            if new_sid not in generated_sids:
                generated_sids[new_sid] = {
                    'identifier': new_sid,
                    'clinical_site': org['name'],
                    'date_created': datetime.now().strftime("%Y-%m-%d"),
                    'status': 'Available'
                }
                is_valid_sid = True


pids_data = [generated_pids[pid] for pid in generated_pids.keys()]
sids_data = [generated_sids[sid] for sid in generated_sids.keys()]


# ///////////////////////////////////////

# save to file and import into central database
pd.DataFrame(pids_data).to_csv(
    "Patient identifiers.csv", encoding="UTF-8", index=False)

pd.DataFrame(sids_data).to_csv(
    "Biospecimen identifiers.csv", encoding="UTF-8", index=False)

with Client(url=HOST, token=TOKEN) as client:
    client.save_schema(
        name="IMDHub Identifier Lists",
        table="Patient identifiers",
        file="Patient identifiers.csv"
    )

    client.save_schema(
        name="IMDHub Identifier Lists",
        table="Biospecimen identifiers",
        file="Biospecimen identifiers.csv"
    )

# ///////////////////////////////////////


# subset data and import into demo institution
umcg_pids = [
    row for row in pids_data if row['clinical_site'] == 'University of Groningen'
]
umcg_sids = [
    row for row in sids_data if row['clinical_site'] == 'University of Groningen'
]

pd.DataFrame(umcg_pids) \
    .to_csv("Patient identifiers.csv", encoding="UTF-8", index=False)

pd.DataFrame(umcg_sids) \
    .to_csv("Biospecimen identifiers.csv", encoding="UTF-8", index=False)

with Client(url=HOST, token=TOKEN) as client:
    client.save_schema(
        name="Site 04",
        table="Patient identifiers",
        file="Patient identifiers.csv"
    )

    client.save_schema(
        name="Site 04",
        table="Biospecimen identifiers",
        file="Biospecimen identifiers.csv"
    )
