---
title: "Customize Form"
description: "Create custom Helpdesk ticket fields on the storage page (ns_helpdesk 14+)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ns_helpdesk"
  - "Helpdesk"
sidebarTitle: "Customize Form"
---


From **ns_helpdesk 14.0.0**, the **Customize Form** backend module is removed.

Add extra ticket fields as records on the Helpdesk storage page (the **Global Storage PID**
from [Global Settings](/ExtNsHelpDesk/GlobalSettings/Index#ns-helpdesk-constant-editor)).

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmti8wrfr1f50qmcthi8ia2qo?embed_v=2&utm_source=embed" loading="lazy" title="Create custom Helpdesk ticket fields" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

**Step 1.** Open the **List** module (Records) and select the ticket storage page.

**Step 2.** Create a new **Fields Group** record and enter a group title.

**Step 3.** Click **Create new Form Custom Fields**.

**Step 4.** Enter the field title and a unique variable name, then choose the field type.
Available types include Input, Textarea, Select, Checkbox, and Radio.

**Step 5.** For select, checkbox, or radio fields, set the **Options** as required.

**Step 6.** Save.

Default form field labels, placeholders, and include/required flags stay in the
Constant Editor. See [Form Settings](/ExtNsHelpDesk/FormSettings/Index).
