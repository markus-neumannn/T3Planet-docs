---
title: "How to get Google Client ID, Secret Key & Refresh Token?"
description: "How to get Google Client ID, Secret Key & Refresh Token? — T3Planet documentation."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ns_GoogleDocs"
  - "How to get Google Client ID, Secret Key & Refresh Token?"
  - "GoogleDocsConfiguration"
sidebarTitle: "How to get Google Client ..."
---

Before you can start using EXT:ns_googledocs, You need to get Google Client ID, Secret Key and Refresh Token for your Gmail account. These details will help to fetch Google Docs from your Gmail account.

1. To Create Google Client ID and Secret Key go to https://console.developers.google.com
2. Create a New Project or select existing project.

![Select Project](./images/select_project.webp)

3. Switch to Credentials. Click on Create Credentials button and Select OAuth Client ID

![Create OAuth Client](./images/create_client.webp)

4. Select "Web Application" option and set Authorized redirect URIs "https://developers.google.com/oauthplayground"

![Create OAuth Client](./images/create_client_2.webp)

5. This will generate Client ID and Client Secret Key.

![Client ID & Secret Key](./images/client_id_secret_key.webp)

6. Switch to Library and search for "Google Drive API". Select API and enable it.

![Enable API](./images/enable_api.webp)

7. Now go to https://developers.google.com/oauthplayground/
8. Set your Client ID and Secret Key in Settings

![Set ID and Secret Key in Settings](./images/set_id_secret_key.webp)

9. Go to Step 1 section. Search & expand Drive API v3. Select all options and click on Authorize APIs button.

![Authorize APIs](./images/authorize_apis.webp)

10. Now, go to Step 2 and there you can find your Refresh token.

![Refresh Token](./images/refresh_token.webp)

Once you complete these steps, you will have Google Client ID, Secret Key and Refresh Token for your account. You have to set those in Global Settings of EXT:ns_googledocs.
