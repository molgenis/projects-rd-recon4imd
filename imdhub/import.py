from molgenis_emx2_pyclient.client import Client
from os import environ
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

with Client(environ['IMDHUB_HOST'], token=environ['IMDHUB_TOKEN']) as client:
    client.save_schema(table='Participant identifiers', name='Site 01',
                       file='data/example_site_data.csv')


with Client(environ['IMDHUB_HOST'], token=environ['IMDHUB_TOKEN']) as client:
    client.save_schema(
        table='Clinical recruitment strategy',
        name='NL4',
        file='data/demo/Clinical recruitment strategy.csv'
    )
