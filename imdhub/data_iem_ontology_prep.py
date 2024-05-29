"""Prepare ontology for IEM codes
FILE: data_ied_ontology_prep.py
AUTHOR: David Ruvolo
CREATED: 2024-05-17
MODIFIED: 2024-05-17
PURPOSE: 
STATUS: 
PACKAGES: 
COMMENTS: 
"""

import re
from datatable import dt, f, fread

iem_raw = fread("./data/ICIMD_VMH_OMIM.csv")

# ///////////////////////////////////////////////////////////////////////////////


# ~ 1 ~
# Clean input dataset

# select columns and exclude rows that are provisional (i.e., not yet confirmed)

iem_dt = iem_raw[:, (
    f.diseaseName,
    f.diseaseClass1,
    f.diseaseClass2,
    f.diseaseClass3,
    f.IEMcode
)][
    (dt.re.match(f.IEMcode, '.*Prov_.*') == False)
    & (f.IEMcode != "-")
    & (f.IEMcode != ""),
    :
]


# clean disease classifications
for column in ['diseaseClass1', 'diseaseClass2', 'diseaseClass3']:
    iem_dt[column] = dt.Frame([
        re.sub(r'^([0-9.\s+]{1,})', '', value)
        for value in iem_dt[column].to_list()[0]
    ])


# determine lowest possible disease classification in all disease class columns
iem_dt['diseaseClassFinal'] = dt.Frame([
    row[2] if bool(row[2]) else (
        row[1] if bool(row[1]) else row[0]
    )
    for row in iem_dt[:, (
        f.diseaseClass1, f.diseaseClass2, f.diseaseClass3
    )].to_tuples()
])

# ///////////////////////////////////////////////////////////////////////////////

# ~ 2 ~
# Prepare ontology dataset

diseases = []

# reduce diseaseClass1 and add them to the dataset
disease_class_1 = dt.unique(
    iem_dt[f.diseaseClass1 != '', f.diseaseClass1]).to_list()[0]

for disease_class in disease_class_1:
    diseases.append({
        'name': disease_class
    })


# reduce diseaseClass2 and add them to the dataset
disease_class_2 = iem_dt[
    f.diseaseClass2 != "", (f.diseaseClass2, f.diseaseClass1)
][:, dt.first(f['diseaseClass1']), dt.by(f.diseaseClass2, f.diseaseClass1)]


for row in disease_class_2.to_pandas().to_dict('records'):
    diseases.append({
        'name': row['diseaseClass2'],
        'parent': row['diseaseClass1']
    })

# reduce diseaseClass3 and add them to the dataset
disease_class_3 = iem_dt[
    f.diseaseClass3 != '', (f.diseaseClass3, f.diseaseClass2)
][:, dt.first(f['diseaseClass3']), dt.by(f.diseaseClass3, f.diseaseClass2)]

for row in disease_class_3.to_pandas().to_dict('records'):
    diseases.append({
        'name': row['diseaseClass3'],
        'parent': row['diseaseClass2']
    })


# isolate IMD diseases, codes, and parent
iem_diseases = iem_dt[:, (f.diseaseName, f.IEMcode, f.diseaseClassFinal)]
for row in iem_diseases.to_pandas().to_dict('records'):
    diseases.append({
        'name': row['diseaseName'],
        'code': row['IEMcode'],
        'parent': row['diseaseClassFinal']
    })

# ///////////////////////////////////////////////////////////////////////////////

# ~ 2 ~
# Prep final dataset

diseases_dt = dt.Frame(diseases)

# add extra columns
diseases_dt['codesystem'] = 'IEM'


diseases_dt.to_csv("./model/lookups/Diseases.csv")
