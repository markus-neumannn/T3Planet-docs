---
title: "Plugin Configurations"
description: "Configure Helpdesk list, ticket submission, and registration plugins."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ns_helpdesk"
  - "Helpdesk"
sidebarTitle: "Plugin Configurations"
---


Add Helpdesk plugins as content elements on the relevant pages. Three plugins are available:

- **Helpdesk - List View**
- **Helpdesk - Ticket Submission**
- **Helpdesk - Front-End User Registration**

## Helpdesk list view

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmti8pazd1edjqmctkkvb7bym?embed_v=2&utm_source=embed" loading="lazy" title="Helpdesk list view plugin" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

Use this plugin to display tickets on the frontend.

**Step 1.** On the ticket listing page, create a new content element.

**Step 2.** Select **Helpdesk - List View**.

**Step 3.** Open the **Plugin** tab and set:

- List page
- Ticket create page
- Listing layout (for example **List Sidebar**)

**Step 4.** Save.

## Helpdesk ticket submission

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmti8qmiq1eh4qmctryn4m43z?embed_v=2&utm_source=embed" loading="lazy" title="Helpdesk ticket submission plugin" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

Use this plugin to show the ticket creation form.

**Step 1.** On the ticket submission page, create a new content element.

**Step 2.** Select **Helpdesk - Ticket Submission**.

**Step 3.** Open the **Plugin** tab. Configure form options and, under **Visitors/Admin Mail Settings**, the admin email subject, email body, and success message.

**Step 4.** Save.

Standard field labels and placeholders are set in the Constant Editor.
See [Form Settings](/ExtNsHelpDesk/FormSettings/Index). Custom fields are added on the storage page.
See [Customize Form](/ExtNsHelpDesk/CustomizeForm/Index).

## Helpdesk front-end user registration

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmti8say21ep8qmctob2pqhov?embed_v=2&utm_source=embed" loading="lazy" title="Helpdesk front-end user registration plugin" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

Use this plugin when visitors must register before creating tickets.

**Step 1.** On the registration page, create a new content element.

**Step 2.** Select **Helpdesk - Front-End User Registration**.

**Step 3.** Configure the plugin options, then save.

Set **Login Page ID** and **Registration Page ID** in [Global Settings](/ExtNsHelpDesk/GlobalSettings/Index).
