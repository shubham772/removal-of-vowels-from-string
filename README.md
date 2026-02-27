# Deployment & Setup Guide

## Prerequisites
- Salesforce org with Experience Cloud enabled
- System Administrator profile
- SFDX CLI installed (for source-based deployment)

## Step 1: Deploy Metadata

### Using SFDX CLI:
```bash
# Authenticate to org
sf org login web -a GrantApp

# Deploy all metadata
sf project deploy start --source-dir force-app/main/default -o GrantApp
```

### Manual Deployment Order:
1. **Custom Labels** — `labels/CustomLabels.labels-meta.xml`
2. **Custom Metadata Type** — `objects/Support_Option__mdt/` (type + fields)
3. **Custom Metadata Records** — `customMetadata/Support_Option.*.md-meta.xml`
4. **Contact Custom Fields** — `objects/Contact/fields/`
5. **Grant_Disbursed__c Object + Fields** — `objects/Grant_Disbursed__c/`
6. **Apex Classes** — Deploy in order:
   - `GrantApplicationService`
   - `GrantApplicationController`
   - `ContactTriggerHandler`
   - `TestDataFactory`
7. **Apex Trigger** — `ContactTrigger`
8. **Test Classes** — All `*Test` classes
9. **LWC** — `lwc/grantApplicationForm/`

## Step 2: Configure Experience Cloud Site

1. **Setup → Digital Experiences → All Sites → New**
   - Template: Customer Service or Build Your Own
   - Name: "Agency X Grant Portal"

2. **Add the LWC to a page:**
   - Open Experience Builder
   - Navigate to a page (e.g., Home)
   - Drag "Grant Application Form" component onto the page

3. **Configure Guest User Access:**
   - Setup → Digital Experiences → [Your Site] → Administration → Pages
   - Set the page with the form as the default landing page
   - Go to Administration → General → Enable "Allow guest users"

4. **Guest User Profile Permissions:**
   Navigate to the Guest User profile and grant:
   - **Object Permissions:**
     - Contact: Read, Create, Edit
     - Grant_Disbursed__c: Read, Create, Edit, Delete
   - **Field-Level Security:** Ensure all custom fields are visible
   - **Apex Class Access:**
     - `GrantApplicationController`
     - `GrantApplicationService`

5. **Publish the site**

## Step 3: Validate Deployment

### Run All Tests:
```bash
sf apex run test --test-level RunLocalTests --code-coverage -o GrantApp
```

### Verify Coverage:
All classes should show >90% coverage:
- `GrantApplicationService` — ~95%+
- `GrantApplicationController` — ~95%+
- `ContactTriggerHandler` — ~95%+

## Step 4: Bulk Upload (User Story 4)

### Using Data Loader:
1. Open Salesforce Data Loader
2. Select "Insert" operation
3. Choose "Contact" object
4. Map CSV columns to Salesforce fields:
   | CSV Column | Salesforce Field |
   |------------|-----------------|
   | FirstName | FirstName |
   | LastName | LastName |
   | Phone | Phone |
   | MailingPostalCode | MailingPostalCode |
   | MailingCountry | MailingCountry |
   | Monthly_Income__c | Monthly_Income__c |
   | Support_Option__c | Support_Option__c |
5. Use `scripts/sample_bulk_upload.csv` as the data file
6. Execute the upload

### For Updates (matching phone):
1. Use "Upsert" with Phone as the External ID field
2. Or use "Update" after querying existing Contact IDs

### Validation During Upload:
- The `ContactTrigger` enforces all validation rules
- Invalid records are rejected with descriptive error messages
- Valid records proceed with automatic disbursement record creation

## Admin Configuration

### Modifying Error Messages:
Setup → Custom Labels → Filter by Category: "Grant_Application"
- Edit any label's Value field to change the displayed message
- No code changes required

### Adding New Support Options:
Setup → Custom Metadata Types → Support Option → Manage Records → New
- Label: e.g., "Option Four"
- DeveloperName: e.g., "Option_Four"
- Monthly Amount: e.g., 150
- Duration (Months): e.g., 18
- The new option will automatically appear in the LWC form

### Modifying Income Threshold:
Currently hardcoded at SGD 2,000 in `GrantApplicationService.INCOME_THRESHOLD`.
To make configurable, move to Custom Metadata or Custom Settings.
