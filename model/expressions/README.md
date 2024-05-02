# Data Model Expressions

[Expressions](https://demo-recon4imd.molgeniscloud.org/Site%2004/docs/#/molgenis/use_schema?id=expressions) are a MOLGENIS EMX2 feature that allows to you to control the input of data. You can either set default values, make a field required based on the value of another field, show or hide a field, or create a computed value. Expressions are written in javascript and copied directly into the model.

For the IMDHub, expressions are written in this file to serve as a development space and documentation. (It is much easier to write the expression using javascript extensions and linting.) This file does not contain all expressions defined in the model, but the more complex or commonly used expressions.

## Computed Expressions

### Current date

Some date fields are automically populated with today's date. Rather than having the user select or enter the date, this can be calculated automatically.

```js
new Date().toISOString().split("T")[0]
```

### Patient id

During the patient registration process, it was decided that it would nice if we could automatically suggest the next available patient identifier. The following query retrieves the next unassigned identifier from the table `PatientIdentifer` (which is stored in the same schema).

```js
(function() {
  const result = simplePostClient(
    `query PatientIdentifiers($filter:PatientIdentifiersFilter, $orderby:PatientIdentifiersorderby ) { PatientIdentifiers( filter:$filter, limit:1, orderby:$orderby ) { identifier } }`,
    {
      filter: { status: { name: { equals: "Available" } } },
      orderby: { mg_insertedOn: "ASC" },
    }
  );
  return result?.PatientIdentifiers[0].identifier;
})();
```

An additional script is needed to update the PatientIdentifier table when the record is saved.

## Validation Expressions

### Year of Birth

This expression is used in the column `year_of_birth` (found in the `Patient registration` table). The purpose is to make sure the user has entered the year as four digits. This also checks to see if the user entered a year greater than the current year.

```js
(function(){
 const current_year = new Date().toLocaleDateString("en",{year: "numeric"});
 
 if (year_of_birth < 1900) {
  return 'Year of birth must be after the year 1900';
 }
 
 if (year_of_birth > current_year) {
  return 'Year of birth cannot be greater than the current year';
 }
  
})();
```
