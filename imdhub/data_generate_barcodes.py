"""Generate barcodes and labels
FILE: data_generate_barcodes.py
AUTHOR: David Ruvolo
CREATED: 2024-09-12
MODIFIED: 2024-09-12
PURPOSE: generating barcodes and label sheets
STATUS: in.progress
PACKAGES: **see below**
COMMENTS: Data and structure is based on the requirements outlined in the Recom4IMD Sample Labeling Proposal document
"""

import re
from datatable import dt, f
from imdhub.utils import generate_random_id
from blabel import LabelWriter

# ///////////////////////////////////////////////////////////////////////////////

# ~ 1 ~
# Build specimen mappings and generate identifiers for a random participant identifier


# create specimen codes
biospecimens = {
    'Worksheet': [''],
    'Patient record': [''],
    'Urine cup': ['U'],
    'Urine centrifugation tube': ['U'],
    'Urine supernatant aliquot': ['Ua1', 'Ua2', 'Ua3'],
    'EDTA blood': ['P'],
    'Plasma supernatant aliquot': ['Pa1', 'Pa2', 'Pa3'],
    'EDTA blood (Genomics)': ['BG'],
    'Pax tube (transcriptomics)': ['Pax'],
    'Falcon tube for Pax liqui': ['Pax'],
    'Fibroblasts (protemoics)': ['FP1', 'FP2', 'FP3'],
    'Stool (microbiomics)': ['S'],
    # 'Gaucher': ['v1-Ua1', 'v1-Ua2', 'v1-Ua3', 'v2-Ua1', 'v2-Ua2', 'v2-Ua3']
}


# generate participant and biospecimen identifiers
participant_id = 'P' + generate_random_id(length=5)
identifiers = []

for specimen in biospecimens.keys():
    for code in biospecimens[specimen]:
        bid = f"{participant_id}-{code}" if code != '' else participant_id
        identifiers.append({
            'specimen': specimen,
            'participant_id': participant_id,
            'sample_code': code,
            'sample_id': bid
        })

identifiers_dt = dt.Frame(identifiers)

identifiers_dt['label_color'] = dt.Frame([
    'label-yellow' if re.match(r'(U(a[1-3])?)', code) else (
        'label-purple' if re.match(r'(P(a[1-3])?)', code) and code != 'Pax' else (
            'label-blue' if code == 'Pax' else (
                'label-red' if code == 'BG' else 'white'
            )
        )
    )
    for code in identifiers_dt[:, (f.sample_code)].to_list()[0]
])

# ///////////////////////////////////////////////////////////////////////////////

# ~ 2 ~
# Generate barcodes

labels = identifiers_dt[:, (f.sample_id, f.label_color)
                        ].to_pandas().to_dict('records')

label_writer = LabelWriter(
    item_template_path='./imdhub/blabel/template.html',
    default_stylesheets=('./imdhub/blabel/template.css',)
)


label_writer.write_labels(labels, target='files/labels.pdf')
