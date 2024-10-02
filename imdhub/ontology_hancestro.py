"""Convert hancestro full json to csv
FILE: ontology_hancestro.py
AUTHOR: David Ruvolo
CREATED: 2024-10-01
MODIFIED: 2024-10-02
PURPOSE: download and prepare data for the IMDHUb Ancestry ontology table
STATUS: stable
PACKAGES: **see below**
COMMENTS: NA
"""

import requests
from tqdm import tqdm
from os.path import basename
from datatable import dt, f

session = requests.Session()
github_url = 'https://raw.githubusercontent.com/EBISPOT/hancestro/refs/heads/main/hancestro-full.json'
gh_response = session.get(github_url)
hancestro_json = gh_response.json()

# ///////////////////////////////////////

# ~ 1 ~
# Prepare ontology

# unpack all nodes and transform into molgenis-ontology format
hancestro_ont = []

for node in tqdm(hancestro_json['graphs'][0]['nodes']):
    mg_ontology_row = {
        'name': node.get('lbl'),
        'type': node.get('type'),
        'description': node.get('meta', {}).get('definition', {}).get('val'),
        'ontologyTermURI': node.get('id')
    }
    hancestro_ont.append(mg_ontology_row)

# convert to datatable object
hancestro_dt = dt.Frame(hancestro_ont)

# Filter dataset select rows that meet the following conditions
#    1) Name is not None
#    2) Type is "CLASS"
#    3) The URI points to 'purl.obolibrary.org
#    4) The word "obsolete" is not present in the name
#
hancestro_dt = hancestro_dt[
    (f.name != None) &
    (f.type == 'CLASS') &
    (dt.re.match(f.name, '.*obsolete.*') == False) &
    (dt.re.match(f.ontologyTermURI, r'.*purl\.obolibrary\.org.*')) &
    dt.re.match(f.ontologyTermURI, '.*(AfPO|HANCESTRO).*'),
    :
]

# add code and codesystem columns
hancestro_dt['code'] = dt.Frame([
    basename(value).replace('_', ':') if value else value
    for value in hancestro_dt['ontologyTermURI'].to_list()[0]
])

hancestro_dt['codesystem'] = dt.Frame([
    value.split(':')[0]if value else value
    for value in hancestro_dt['code'].to_list()[0]
])

# write to file or import
hancestro_dt.to_csv('./data/Ancestry.csv')
