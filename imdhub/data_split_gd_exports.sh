## Split xlsx into multiple csvs

# split references schema
xlsx2csv --sheet 0 files/google_drive/imdhub-reference-tables.xlsx model/imdhub-refs/

# split identifier schema
xlsx2csv --sheet 0 files/google_drive/imdhub-identifier-bank.xlsx model/imdhub-ids/

# split clinical site registration model
xlsx2csv --sheet 0 files/google_drive/clinical-site-registration.xlsx model/imdhub-site/


# split demo data
xlsx2csv --sheet 0 \
  data/demo/clinical-site-data.xlsx \
  data/demo/