"""Build ontology from URL"""

import requests
from datatable import dt
from os import path

# enter one or more URLs to build an ontology dataset
entry_point = 'https://www.ebi.ac.uk/ols4/api/ontologies/ncit/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FNCIT_C25464'

output_file = 'data/countries.csv'

if __name__ == "__main__":
    print('Retrieving ontology....')
    session = requests.Session()
    ontology = []

    # get parent term
    parent_response = session.get(entry_point)
    parent = parent_response.json()

    graph_response = session.get(parent['_links']['graph']['href'])
    graph = graph_response.json()['nodes']

    for node in graph:
        if node['label'] not in ['Country', 'Geographic Area']:
            ontology.append({
                'name': node['label'],
                'codesystem': path.basename(node['iri']).split('_')[0],
                'code': path.basename(node['iri']).replace('_', ':'),
                'ontologyTermURI': node['iri']
            })

    # write
    print('saving data....')
    ontology_dt = dt.Frame(ontology)
    ontology_dt.to_csv(output_file)
