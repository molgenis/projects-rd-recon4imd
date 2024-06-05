# IMD-hub data models

In this folder, there are several sets of data models. These are listed below.

1. [imdhub-site](./imdhub-site/): This is a data model template that will be used to create a space for each clinical site. Users associated with the site can log in and view data submissions or submit new data.
2. [imdhub-refs](./imdhub-refs/): This is the data model for all datasets that are reused throughout the IMD-hub. This includes ontologies, reference lists, and any other code lists. All other data models and user interfaces that use these datasets are linked to this data model.
3. [imdhub-ids](./imdhub-ids/): This data model is for storing pregenerated project identifiers (e.g., participant IDs, visit IDs, biospecimen IDs, etc.). This provides us a way to auto assign a new identifier upon registration.

The files stored here are the latest stable version of the data models and datasets used in the IMD-hub. The development version is located on the shared google drive. New releases are downloaded to these folders.

In addition, the files in the [expressions](./expressions/) folder provide documentation on how validation rules are used in the data entry forms.

If you have any suggestions or comments, please open a new github issue.
