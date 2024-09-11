"""Generate barcodes"""

from datatable import dt, f, as_type
from barcode import Code39
from barcode.writer import ImageWriter, SVGWriter

from imdhub.utils import generate_random_id


# generate example identifiers
participant_id = 'P' + generate_random_id(length=5)
pids_dt = dt.Frame([
    {'specimen': 'Urine', 'specimen_code': 'U'},
    {'specimen': 'Urine', 'specimen_code': 'Ua1'},
    {'specimen': 'Urine', 'specimen_code': 'Ua2'},
    {'specimen': 'Urine', 'specimen_code': 'Ua3'},
    {'specimen': 'Blood Plasma', 'specimen_code': 'P'},
    {'specimen': 'Blood Plasma', 'specimen_code': 'Pa1'},
    {'specimen': 'Blood Plasma', 'specimen_code': 'Pa2'},
    {'specimen': 'Blood Plasma', 'specimen_code': 'Pa3'},
    {'specimen': 'Blood DNA', 'specimen_code': 'BG'},
    {'specimen': 'Blood RNA', 'specimen_code': 'Pax'},
    {'specimen': 'Fibroplasts', 'specimen_code': 'FP'},
    {'specimen': 'Stool', 'specimen_code': 'S'},
    {'specimen': 'Gaucher', 'specimen_code': 'v1-Ua1'},
    {'specimen': 'Gaucher', 'specimen_code': 'v1-Ua2'},
    {'specimen': 'Gaucher', 'specimen_code': 'v1-Ua3'},
    {'specimen': 'Gaucher', 'specimen_code': 'v2-Ua1'},
    {'specimen': 'Gaucher', 'specimen_code': 'v2-Ua2'},
    {'specimen': 'Gaucher', 'specimen_code': 'v2-Ua3'},
])

pids_dt['participant_id'] = participant_id
pids_dt['biospecimen_id'] = dt.Frame([
    f"{row[0]}-{row[1]}" for row in pids_dt[:, (f.participant_id, f.specimen_code)].to_tuples()
])

for _id in pids_dt['biospecimen_id'].to_list()[0]:
    specimen_barcode = Code39(_id, writer=SVGWriter)
    pids_dt['barcode'] = specimen_barcode.get_fullcode()

    # len(test_id)
    # x = Code39(test_id)
    # x.get_fullcode()

    # with open("somefile.jpeg", "wb") as f:
    #     Code39(test_id, writer=ImageWriter()).write(f)
