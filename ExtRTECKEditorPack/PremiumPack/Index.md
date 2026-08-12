---
title: "Premium Pack"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ExtRTECKEditorPack"
  - "Premium Pack"
sidebarTitle: "Premium Pack"
---

## Start Free Trial

Do you want to try all the premium features of the CKEditor Pack TYPO3 extension?

- **Cloud-hosted**
- 14-day free trial of self-hosted editor
- 1,000 editor loads per month
- Commercial license
- Community support

[Start 14-day Free Trial](https://portal.ckeditor.com/signup?utm_source=t3planet) | [Explore Pricing](https://ckeditor.com/pricing/?utm_source=t3planet)

## Configuration for Premium Pack

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmhzwd9lp05meqnb9utf0xde3" loading="lazy" title="Premium Pack Configuration Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

Configure your settings in simple steps to start using the premium features.

## CKEditor Pack Premium Version Setup Guide

## Step 1: Access Extension Configuration

To access and update extension settings:

- Go to the CKEditor Pack backend.
- Navigate to CKEditor Pack > Premium Settings.
- Click on Feature Configuration.

![Premium Settings Interface](./images/premium_settings.webp)

CKEditor Pack Premium Settings interface showing License key, Authorization Type, Organization ID, and API Key fields

## Step 2: License Key Setup Overview

Certain premium CKEditor 5 features require a valid license key. This includes:

- Real-Time Collaboration
- Revision History
- Track changes
- Comments
- Productivity Pack
- Features Pack
- Collaboration Pack

<Note>
For CKEditor v44.0.0 and above, these features will only work with valid license key.
</Note>

### Create a CKEditor Account

To begin, you must have a CKEditor customer account.

1. Go to the CKEditor Customer Portal.
2. Click Create an account.
3. Complete the registration using your business email.
4. Once registered, you can access all your licenses and product configurations.

### Log In to the Customer Portal

1. Visit the Customer Portal login page.
2. Enter your credentials and sign in.
3. Once logged in, you will see your dashboard with available products and licenses.

### Access the Licensing Section

1. Navigate to the “Subscriptions” or “License Keys” tab.
2. Select the CKEditor 5 product your team is using.
3. You will now see all available license keys associated with your subscription.

### Generate Your License Key

CKEditor automatically creates a default license key when you subscribe.

You can generate additional keys if you’re working on multiple environments (e.g., staging, development, production).

To generate or retrieve a key:

1. Click “Create License Key” (if required).
2. Provide an environment name (e.g., production, dev, staging).
3. Do not use spaces in the name.
4. Save the key.
5. Copy this license key for the next step.

## Add Required License Keys

The license key is required for Real-time Collaboration, Revision History, Track changes, Comments, Productivity Pack and Features Pack.

## Step 3: Select the Authorization Type

Select the Authorization Type from the dropdown. (Access Key, Development Token)

## Step 4: Token URL

The development token URL should be used carefully as it does not provide sufficient permission validation.

## Step 5: Organization ID

The Organization ID can be found in the CKEditor Pack Backend and can be used for the Real-time collaboration and API requests.

## Step 6: API Key

The API Key can be found in the CKEditor Pack Backend.

## Step 7: Access Advanced Settings

You can access the Advanced settings by clicking on the dropdown.

## Step 8: Add the Web Socket URL

Leave this field empty - the system will automatically generate this URL using Organization ID field

## Step 9: API base URL

Leave this field empty - the system will automatically generate this URL using Organization ID and Environment ID fields

## Step 10: Save Changes

---

## Additional content from live docs

## Premium Configuration

Configure your settings to start premium features.

## WebSocket URL

Leave this field empty.
The system creates this URL automatically from the Organization ID.
