---
title: "Global Settings"
description: "Configure ns_helpdesk in the TypoScript Constant Editor (ns_helpdesk 14+)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ns_helpdesk"
  - "Helpdesk"
sidebarTitle: "Global Settings"
---


<span id="ns-helpdesk-constant-editor"></span>

From **ns_helpdesk 14.0.0**, Helpdesk is no longer configured in a backend module.
After you [include the Helpdesk TypoScript](/en/latest/ExtNsHelpDesk/Installation/Index#ns-helpdesk-include-typoscript),
use the **Constant Editor**.

**Step 1.** Open the **TypoScript** module and select the root page.

**Step 2.** Switch to **Constant Editor**.

**Step 3.** Choose the Helpdesk global settings category from the category dropdown.

**Step 4.** Set the values required for your site, then save.

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmti8g5y71dmuqmctgof78avq?embed_v=2&utm_source=embed" loading="lazy" title="Configure ns_helpdesk in the Constant Editor" allow="clipboard-write; fullscreen" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

Typical global constants include:

- **Admin Email** and **Admin Name**
- **Notify Admin via email**
- **jQuery library** (enable only if your site does not already load jQuery)
- **Global Storage PID** for Helpdesk records
- **Login Page ID** and **Registration Page ID**
- **Google reCaptcha** site key
- **Default ticket status ID**
- **Default Assignee ID** (backend user used for automatic assignment)

<Note>
Category-wise assignment requires a default assignee and ticket categories.
Set **Default Assignee ID** in the Constant Editor, and keep categories on
the storage page. See [Ticket Categories](/en/latest/ExtNsHelpDesk/CategoryStatus/Index).
</Note>

Ticket form labels, placeholders, and popup options are configured in the same
Constant Editor. See [Form Settings](/en/latest/ExtNsHelpDesk/FormSettings/Index).
