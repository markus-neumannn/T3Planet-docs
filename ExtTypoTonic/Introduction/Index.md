---
title: "Introduction"
description: "Introduction — TypoTonic (EXT:tonic) documentation."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "TypoTonic"
  - "tonic"
  - "TONICTYPES"
sidebarTitle: "Introduction"
---

## What This Extension Does

TypoTonic (extension key `tonic`) lets you build your own record types directly in the TYPO3 backend.
You configure everything with TCA, TYPO3's standard configuration format.
There is no need to write a new extension for every content type you want.

TypoTonic reads your configuration and generates the database table, the TCA, and the domain model and repository classes for you.
The TYPO3 Schema Migrator then creates the required database structure.
Once a record type exists, you can create, edit, and list records the same way you already do in TYPO3.

<Note>
The vendor is rebranding this extension from **TypoTonic** to **TONICTYPES**. Both names refer to the same product. This documentation uses **TypoTonic**, matching the extension key `tonic` and the name used throughout the technical documentation.
</Note>

## What You Can Build

The vendor lists these as typical examples of record types you can build with TypoTonic instead of writing a dedicated extension:

- News records
- Job records
- Address records
- Event records
- Media records, for building a media library
- Product records
- Award records
- Company records
- Form answer records, for saving submissions from frontend forms

Because every record type is built and maintained inside one extension, you only have to update and maintain TypoTonic itself, not a separate extension for each content type.

## Highlights

- Create custom record types and fields without writing PHP
- List and detail frontend plugins are included
- Records can be injected into other extensions through the normal Extbase Domain and Repository structure
- Template variables let you inject dynamic values (GET/POST parameters, database values, session values, and more) into your Fluid templates
- Fluid templating with configurable variable names
- Different output formats, such as XML, JSON, or PDF, are possible through ViewHelpers and custom response headers
- Built entirely on TYPO3 core functionality (TCA, FormEngine, Extbase)

## How It Works

Building a new record type with TypoTonic follows the same seven steps every time:

1. Create the fields your record type needs.
1. Create a Datatype and assign the fields to it.
1. Use the table and class generator on the Datatype to create the database table and the PHP classes.
1. Create or import records. Editors can also do this once the Datatype exists.
1. Create Fluid templates for the frontend, for example a list view and a detail view.
1. Add the Display Records plugin to a page to show the records.
1. Optionally, add other plugins, such as filtering or search, and connect them to the Display Records plugin.

The following sections in this documentation walk through each of these steps in detail.

## TypoTonic Professional

The vendor also sells a separate **TypoTonic Professional** extension with additional tools, such as a backend toolbar item and frontend record editing.
This is an optional product sold directly by the vendor, not by T3Planet.
See **typotonic-professional** for details.

## Helpful Links

<Note>
- Product:
- Get support: [https://t3planet.de/support](https://t3planet.de/support)
- License activation: [https://docs.t3planet.de/en/latest/License/Index.html](/License/Index)
</Note>
