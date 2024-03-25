# Recon4Imd Data models

## Biosampling

The purpose of the biosampling model is to reproduce the biosampling SOP as an EMX2 schema; specifically, the capture of specimen collection and shipment. End users will be allowed to register new patients and to submit new samples into IMDhub, as well as to link patients with one or more samples.

### Structure

At the core, the biospecimen model has one `data` table and several `ontology` tables (i.e., reference tables or lookup tables). These are described in the below.

| Name | Type | Description |
|------|------|-------------|
| Biospecimens | DATA | table for entering and storing information on samples collected |
| AssignedGenderAtBirth | ONTOLOGY | gender values to describe patients |
| Centrifugation | ONTOLOGY | centrifuge options by biospecimen type |
| Persons | ONTOLOGY | reference table for storing information on personnel |
| Specimen Types | ONTOLOGY | Recon4imd reference for speciment types |
| Statuses | ONTOLOGY | context values to describe a data point |
| Storage | ONTOLOGY | storage conditions and temperatures by biospecimen type |
| Supernatant aliquots | ONTOLOGY | context values by biospecimen type |
