---
title: "Installation"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ns_AllChat"
  - "Installation"
sidebarTitle: "Installation"
---

# Installation

Just install this extension the usual way like any other TYPO3 extension.

1. Get the extension

   In the TYPO3 backend you can use the extension manager (EM).

   1. Switch to the module “Extension Manager”.
   2. Get the extension
   3. **Get it from the Extension Manager:**
      Press the “Retrieve/Update” button and search for the extension key
      *ns_all_chat* and import the extension from the repository.
   4. **Get it from typo3.org:** You can always get the current version from
      https://extensions.typo3.org/extension/ns_all_chat/ by downloading either
      the t3x or zip version. Upload the file afterwards in the Extension Manager.

![installation with the extension manager in the backend](./images/TYPO3_Allchats_Extension_NITSAN_Backend_Install_Extensions.jpeg)

2. Activate the TypoScript

   The extension ships some static TypoScript code which needs to be included.

   1. Switch to the root page of your site.
   2. Switch to the **Template module** and select *Info/Modify*.
   3. Click the link **Edit the whole template record** and switch to the tab
      *Includes*.
   4. Select **[NITSAN] ns_all_chat** at the field *Include static
      (from extensions):*
   5. Include **[NITSAN] ns_all_chat** at the last place.

![installation](./images/TYPO3_Allchats_Extension_NITSAN_Backend_Include_Static_Template.webp)

## How to Install TYPO3 Extension ns_all_chat

**Extension Installation Via without Composer mode**
https://www.youtube.com/watch?v=SN5HoFQcDM4

**Extension Via Composer**
https://www.youtube.com/watch?v=_7ILu4lwU-k
