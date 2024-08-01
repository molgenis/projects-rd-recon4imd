## Split xlsx into multiple csvs

# split references schema
xlsx2csv --sheet 0 files/imdhub-refs.xlsx model/imdhub-refs/

# split identifier schema
xlsx2csv --sheet 0 files/imdhub-ids.xlsx model/imdhub-ids/

# split clinical site registration model
xlsx2csv --sheet 0 files/imdhub-site.xlsx model/imdhub-site/


# split demo data
xlsx2csv --sheet 0 \
  data/demo/clinical-site-data.xlsx \
  data/demo/