# Data Model Expressions

[Expressions](https://demo-recon4imd.molgeniscloud.org/Site%2004/docs/#/molgenis/use_schema?id=expressions) are a MOLGENIS EMX2 feature that allows to you to control the input of data. You can either set default values, make a field required based on the value of another field, show or hide a field, or create a computed value. Expressions are written in javascript and copied directly into the model.

For the IMDHub, expressions are written in this file to serve as a development space and documentation. (It is much easier to write the expression using javascript extensions and linting.) This file does not contain all expressions defined in the model, but the more complex or commonly used expressions.

Expressions can be written using standard conditions.

```js
myVariable === "some value"
```

This returns a nasty error so it may be better to use an if statement.

```js
if (myVariable === "some value") "This field is required"
```

Or using a [conditional (ternary) operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_operator).

```js
myVariable === "some value" ? "This field is required" : false
```

For more complex requirement statements, you may consider using an anonmyous function.

```js
(function() {
  if (myVariable === "some value") {
    return "This field is required";
  }
})();
```

In the following sections, we've provided documentation on how expressions are written by table and column.

## Participant registrations table

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

### Prefill clinical site

We would like to be able to auto fill the clinical site column so that users do not have to. The following computed statement will retrieve the value based on the current schema.

```js
(function () {
  if (clinicalSite === null) {
    const schemaMetaResponse = simplePostClient(`query { _schema { name }}`, {});
    const siteId = schemaMetaResponse._schema?.name;
    const siteMetaResponse = simplePostClient(
      `query Organisations ($filter:OrganisationsFilter){ Organisations(filter:$filter) { name }}`,
      {"filter": {"alternativeIdentifier": { "equals": siteId }}},
      "IMDHub Refs"
    );
    const siteName = siteMetaResponse.Organisations[0].name;
    return {
      name: siteName
    }
  }
  return clinicalSite;
})();
```

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

### Has agreed to genetic analysis

This question is shown if the cohort assignment is not one of the negative control groups.

```js
// visibility
cohortAssignment !== null ? !cohortAssignment.name.includes("Negative") : false

// required
cohortAssignment !== null ? (!cohortAssignment.name.includes("Negative") && hasAgreedToGeneticAnalysis === null ? "Indicate if the participant has agreed to genetic analysis" : false ) : false
```

### Has agreed to transfer of data

```js
// required
cohortAssignment !== null ? (!cohortAssignment.name.includes("Negative") && hasAgreedToTransferOfGeneticData === null ? "Indicate if the participant has agreed to the transfer of genetic data" : false ) : false
```

### Has agreed to recontact of medical findings

```js
// required
cohortAssignment !== null ? (!cohortAssignment.name.includes("Negative") && hasAgreedToRecontactOfMedicalFindings === null ? "Indicate if the participant has agreed to recontact in the event of medical findings" : false ) : false
```

### Has agreed to recontact of incidental findings

```js
cohortAssignment !== null ? (!cohortAssignment.name.includes("Negative") && hasAgreedToRecontactOfIncidentalFindings === null ? "Indicate if the participant has agreed to recontact in the event of incidental findings" : false ) : false
```

## Participant visits table

### visit id

To automate and standardize the generation of the visit identifier, the following formula is used.

```js
(function() {
  if (participant !== null && visitType !== null) {
    const visitNum = visitType.name.includes("Enrolment") ? "v1" : "v2";
    return participant.participantId?.identifier + '-' + visitNum;
  }
})();
```

## Biospecimen log

### Weight

```js
// visibility
specimenType !== null ? (["PAXgene-RNA", "EDTA-Blood/DNA"].includes(specimenType.name)) : false

// validation
(function () {
  if (specimenType !== null && weight !== null) {
    if (["PAXgene-RNA", "EDTA-Blood/DNA"].includes(specimenType.name)) {
      if (weight < 0) {
        return "Weight cannot be less than 0kg";
      }
      
      if (weight > 10) {
        return "Weight cannot be more than 10kg";
      }
    }
  }
})();
```

### Total volume of blood draw

```js
// visibility
specimenType !== null && weight !== null ? (["PAXgene-RNA", "EDTA-Blood/DNA"].includes(specimenType.name) && weight < 10) : false

// required
specimenType !== null && weight !== null ? (["PAXgene-RNA", "EDTA-Blood/DNA"].includes(specimenType.name) && weight < 10 ? "Enter the total volume of the blood draw" : false) : false

// validation
(function () {
  if (specimenType !== null && totalVolumeOfDraw !== null) {
    if (["PAXgene-RNA", "EDTA-Blood/DNA"].includes(specimenType.name)) {
      if (totalVolumeOfDraw < 0) {
        return "Total volume of blood draw cannot be less than 0ml";
      }
    }
  }
})();
```

### Aliquots

The Aliquot selection is applies to two sample types. This field should be shown and required based on other inputs. These expressions are listed below.

```js
// visibility
wasCollected && specimenType !== null ? (["EDTA-Tube/Plasma", "Urine"].indexOf(specimenType.name) > -1 ? true : false) : false

// required
(function () {
  if (wasCollected && specimenType !== null) {
    if (["EDTA-Tube/Plasma", "Urine"].indexOf(specimenType.name) > -1 && aliquots === null) {
      return "Select the number of aliquots"
    }
  }
})();
```

### Shipment Registration

```js
// visibility
shipmentRegistration !== null
```

### shipmentReceived

```js
// visibility
shipmentRegistration !== null

// required
(function () {
  if (shipmentRegistration !== null) {
    if (specimenReceived === null) {
      return "Indicate if the specimen was received at the destination point"
    }
  }
})();

// visibility
specimenReceived !== null ? specimenReceived : false
```

### Reason not received

```js
// visibility
specimenReceived !== null ? specimenReceived === false : false

// required
(function() {
  if (specimenReceived !== null) {
    if (!specimenReceived && reasonNotReceived === null) {
      return "Please provide a reason the specimen was not received"
    } 
  }
})();
```

### Other reason sample not received

```js
// visibility
specimenReceived !== null && reasonNotReceived !== null ? reasonNotReceived === "Other" : false

// required
(function() {
  if (specimenReceived !== null) {
    if (!specimenReceived && reasonNotReceived !== null) {
       if (reasonNotReceived.name === "Other") {
        return "Please provide a reason if there was another issue with the shipment";
      }
    } 
  }
})();

// visible
(function() {
  if (shipmentRegistration !== null && specimentReceived !== null) {
    if (!specimenReceived && reasonNotReceived !== null) {
      if (reasonNotReceived.name === "Other") {
        return true;
      }
    }
  }
  return false;
})();
```

## Participant genetic data table

### has existing genetic data

```js
(function () {
  if (participant !== null) {
    if (participant.hasAgreedToTransferOfGeneticData && hasExistingSequenceData === null) {
      return "Indicate if there is WGS or WES data"
    }
  }
})();
```

### sequencing third party expressions

```js
// visibility
hasExistingSequenceData && sequencingStorageOption !== null ? sequencingStorageOption.name === "Third party" : false


// required
(function() {
  if (hasExistingSequenceData && sequencingStorageOption !== null) {
    if (sequencingStorageOption.name === "Third party" && sequencingStorageThirdParth === null) {
      return "Please provide the name of the third party";
    }
  }
})();
```

### sequencing kits

```js
// required
(function() {
  if (hasExistingSequenceData && sequencer !== null) {
    if (sequencer !== "Not provided" && sequencingKits === null) {
      return "Enter the sequencing kit"
    }
  }
})();
```

### has existing files

```js
// required
(function() {
  if (hasExistingSequenceData && sequencer !== null) {
    if (sequencer !== "Not provided" && hasExistingFiles === null) {
      return "Indicate if there are existing files";
    }
  }
})();
```

## Off Study

### Participant withdraw of data

```js
// required
(function () {
  if (offStudyReason !== null) {
    if (offStudyReason === "Withdrawal of participant consent" && paticipantWithdrawData === null) {
      return "Indicate what will happen with the participant's data";
    }
  }
})();

// visibility
offStudyReason !== null ? offStudyReason.name === "Withdrawal of participant consent" : false
```

### date of death

```js
// required
(function () { 
  if (offStudyReason !== null) {
    if (offStudyReason.name === "Death" && dateOfDeath === null) {
      return "Enter the date of death";
    }
  }
})();

// visibility
offStudyReason !== null ? offStudyReason.name === "Death" : false
```

### Participant withdraw of samples

```js
// required
(function () {
  if (offStudyReason !== null) {
    if (offStudyReason === "Withdrawal of participant consent" && paticipantWithdrawSamples === null) {
      return "Indicate what will happen with the participant's samples";
    }
  }
})();

// visibility
offStudyReason !== null ? offStudyReason.name === "Withdrawal of participant consent" : false
```

## Computed Expressions

### Current date

Some date fields are automically populated with today's date. Rather than having the user select or enter the date, this can be calculated automatically.

```js
new Date().toISOString().split("T")[0]
```

When integrated into an auto date column, check to see if the value is null. This will make sure that the date is generated on the first save and never overwritten.

```js
!date ?new Date().toISOString().split("T")[0] : return date;
```

\*Note: change `date` to the name of the column you wish to use
