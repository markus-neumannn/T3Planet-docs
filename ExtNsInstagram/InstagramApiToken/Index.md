---
title: "Generating an Instagram access token"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ns_Instagram"
  - "Generating an Instagram access token"
  - "InstagramApiToken"
sidebarTitle: "Generating an Instagram a..."
---

# Generating an Instagram access token

Follow these steps to create an Instagram access token for **EXT:ns_instagram** using Meta for Developers (Facebook Developer App and Instagram Login).

## Create a Facebook Developer App

**Step 1.** Navigate to the [Meta for Developers](https://developers.facebook.com/) portal.

**Step 2.** Click **Create App**.

**Step 3.** Enter the following details:

- **App Name:** Typo3 EXT
- **App Contact Email:** info@typ3-ext.com

**Step 4.** Click **Next**.

## Select app type

**Step 1.** Choose **Other** as the use case.

**Step 2.** Click **Next**.

**Step 3.** Select **Business** as the app type.

**Step 4.** Click **Next**.

**Step 5.** Review your app details and click **Create App**.

**Step 6.** Enter your Facebook account password to confirm.

## Add the Instagram product

**Step 1.** After app creation, you are redirected to the app dashboard.

**Step 2.** Locate the **Instagram** product.

**Step 3.** Click **Set Up** to enable Instagram integration.

## Configure app roles

**Step 1.** In the left sidebar, go to **App Roles** → **Roles**.

**Step 2.** Click **Add People**.

**Step 3.** Select the role **Instagram Tester**.

**Step 4.** Enter the Instagram username you want to grant access to.

**Step 5.** Click **Add** to send the invitation.

## Accept the Instagram tester invitation

**Step 1.** Log in to the Instagram account you added as a tester.

**Step 2.** Open [Instagram](https://www.instagram.com/).

**Step 3.** Go to **Settings** → **Apps and Websites**.

**Step 4.** Open the **Tester Invites** section.

**Step 5.** Accept the pending invitation sent from your app.

## Complete Instagram API setup

**Step 1.** Return to your Facebook Developer App dashboard.

**Step 2.** Go to **Instagram** → **API Setup with Instagram Login**.

**Step 3.** Click **Generate Token** and authenticate with your Instagram account.

**Step 4.** Save the token securely and use it in your TYPO3 extension.

