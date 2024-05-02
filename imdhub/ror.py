"""Ror Client"""

import requests
from datatable import dt, fread, f
from tqdm import tqdm


class RorClient:
    """Retrieve metadata from ROR Api v2"""

    def __init__(self):
        self.api = 'https://api.dev.ror.org/v2/organizations'
        self.session = requests.Session()

    def _get(self, url: str = None, **kwargs):
        """wrapper for session.get"""
        response = self.session.get(url, **kwargs)
        response.raise_for_status()
        if 'errors' in response:
            raise requests.exceptions.HTTPError(
                'Error in request', str(response['errors']))
        return response.json()

    def get_org(self, ror_id: str = None):
        """
        Retrieve metadata for an organisation by ROR ID.

        :param ror_id: ROR identifier for an organisation
        :type ror_id: string

        :returns: object containing metadata about an organisation 
        """
        url: str = f"{self.api}/{ror_id}"
        return self._get(url)


if __name__ == '__main__':

    # init client
    client = RorClient()

    # import source organisations and prep for querying
    source = fread('./data/organisations_source.csv')
    source['code'] = dt.Frame([
        value.split('/')[-1] for value in source['uri'].to_list()[0]
    ])

    ror_codes = source['code'].to_list()[0]
    for code in tqdm(ror_codes):
        data = client.get_org(ror_id=code)

        # retun displayed name and acronym
        source[f.code == code, 'name'] = ';'.join([
            row['value']
            for row in data['names']
            if 'ror_display' in row['types']
        ])

        source[f.code == code, 'acronym'] = ''.join([
            row['value']
            for row in data['names']
            if 'acronym' in row['types']
        ])

        # extract geonames metadata
        location = data['locations'][0]['geonames_details']
        source[
            f.code == code, ['country', 'city', 'latitude', 'longitude']
        ] = (
            location.get('country_name'),
            location.get('name'),
            location.get('lat'),
            location.get('lng'),
        )

        # extract organisation type
        source[f.code == code, 'type'] = ','.join(data['types'])

    # clean up data
    source.names = {'uri': 'ontologyTermURI'}
    source['code'] = dt.Frame([
        f"ROR:{value}" for value in source['code'].to_list()[0]
    ])

    source['codesystem'] = 'ROR'

    source[:, (
        f.name,
        f.label,
        f.acronym,
        f.type,
        f.codesystem,
        f.code,
        f.ontologyTermURI,
        f.country,
        f.city,
        f.latitude,
        f.longitude,
    )] \
        .to_csv('model/lookups/organisations.csv')
