---
title: "Editor Guide"
description: "Editor guide for T3 Karma"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3 Karma"
  - "Editor Guide"
  - "EditorGuide"
sidebarTitle: "Editor Guide"
---

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmmg0jype50zrnr99x6ac5i2o" loading="lazy" title="Editor Guide" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

After setting up your website, follow the steps below to make it fully functional and versatile.

## Step 1: Create a Standard Page

Create a **Standard Page** in your TYPO3 setup.

## Step 2: Set as Root Page

Go to **Page Properties → Behavior** tab and set the page as a **Root Page**.

## Step 3: Create a TypoScript Template

Go to the **TypoScript** module and create a **template** for your page.

## Step 4: Include Required Extensions

Go to **Template module → Info/Modify** and include the necessary extensions.

Make sure the order of the included extensions is correct:

1. EXT (Fluid Content Elements)
2. EXT (Parent Theme)
3. EXT (Child Theme)

## Step 5: Configure Home Page ID and Main Menu ID

Go to **Theme Options → General** tab and define the **Root Page ID** in the **Home Page ID** and **Main Menu ID** fields. You can optionally configure other settings as needed.

## Step 6: Configure Site Settings

Go to **Site Configuration** and set up your **website title, site identifier, and entry point**.

## Step 7: Configure Languages

To enable **multi-language support**, go to **Site Configuration → Languages** and create a new language, then enter the required details.

## Step 8: Configure Page Layout

Go to **Page Module → Root Page → Page Properties → Appearance** tab and select the appropriate **Backend Layout** and **Frontend Layout** according to your page design.

## Step 9: Apply Website Styling

Go to **Theme Options → Style** tab and configure the **styling options** for your website.

Here you can configure settings such as **Header/Footer options, Color Scheme, Navigation styles, Hover effects, Menu styles, Font styles, Loader styles**, and more.

In the **General** tab, you can enable or disable features such as **Breadcrumbs, Search Bar, Multilanguage Menu, Maintenance Mode, Speed/Performance settings**, and other general configurations.

### How to Enable the Mega Menu on Your Website

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmmiu10pc1hguzdh1b0z964u0" loading="lazy" title="Mega Menu" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

To enable the **Mega Menu**, follow the steps below:

1. Go to the **Page Properties** of the desired page.
2. Open the **General** tab.
3. Enable the **Mega Menu** option.

Once enabled, the selected page will display the **Mega Menu** on your website.

### Subtitles

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmmiua0yh1idtzdh15219n642" loading="lazy" title="Subtitle" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

To add a subtitle, enter the **subtitle** in the **General** tab of the **Page Properties**.

<Note>

The subtitle will only be visible on the frontend if the **Navigation Layout** is set to **“Subtitle”** in the **Theme Options**.

</Note>

**Step 10.** Inserting the Container Element & Content Block Element on your webpage. You can use the Custom & TYPO3 Default element within the container to provide more flexibility in content area.!

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmmiul6yf1j0tzdh1o5ixwvhd" loading="lazy" title="Container Element & Content Block Element" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

<Tip>

How to easy start; It’s all about we highly recommend to go with our demo-pages https://demo.t3planet.de/t3-karma/demos/

</Tip>

### Page-Level Constant Editor

The Page-Level Constant Editor gives you more control over TYPO3 settings directly at the page level.

With this feature, you do not need complex TypoScript changes. You can easily adjust values for a specific page without affecting the entire website.

You don’t need any special setup. Just follow the steps shown in the demo:

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmmetrfmf3ka2nr99usu9m6b9?utm_source=link" loading="lazy" title="Page-Level Constant Editor" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

Steps:

1. Open the **TypoScript** module.
2. Select the page where you want to apply changes.
3. Click **Create an additional TypoScript record**.
4. Open **Theme Options**.
5. Use the **General** tab (and other tabs) to adjust page-level settings, such as the website logo.

Now you can update the available options based on your requirements.

This makes configuration faster, easier, and more flexible.

### Visual Editor in Content Blocks

The Visual Editor helps you edit content directly with a frontend-like preview inside the TYPO3 backend.

It bridges the gap between backend and frontend, so you can see changes while editing.

You don’t need any extra configuration. Just follow the demo:

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmnip567h0z31aburhqag0y29/edit?step=1" loading="lazy" title="Editor Guide" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

Steps:

1. Go to the TYPO3 Backend
2. Open the "Editor" module from the left-side menu

You will see a frontend preview inside the backend.

From here, you can edit content directly and instantly view the changes.

This improves editing speed and makes content management more intuitive.

### Use Existing T3Karma Demo

If you installed T3Karma with demo pages, you can use one of those demos as your main website instead of creating a new root page from scratch.

Follow this walkthrough:

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmqj7pkqm0pqbqmx1daefyh68?utm_source=link" loading="lazy" title="Use Existing T3Karma Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

1. In the page tree, move the demo page you want to use (for example **Business Consulting**) to the required position.
2. Confirm the relocation with **Move this item**.
3. Select the demo page and open **Edit page properties**.
4. Enable **Use as Root Page** and click **Save**.
5. Open **Sites** and edit the site configuration for that demo.
6. Select **Fluid Styled Content CSS**, then close the site configuration.
7. Open the site settings and set the **Main Menu Id**.
8. Click **Save**.
9. Use **View webpage** to preview the demo as your main website.
