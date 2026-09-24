---
title: "Introduction"
description: "Introduction to TonicTypes Professional (EXT:tonictypes_pro) and required Core — custom TCA record types without a dedicated extension."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "TonicTypes"
  - "tonictypes"
  - "tonictypes_pro"
sidebarTitle: "Introduction"
---

## What This Extension Does

This documentation focuses on **TonicTypes Professional** (`tonictypes_pro` / `k3n/tonictypes_pro`). Professional requires free **TonicTypes Core** (`tonictypes` / `k3n/tonictypes`).

Together they let you build your own record types directly in the TYPO3 backend. You configure fields and datatypes with TCA. There is no need to write a new extension for every content type.

TonicTypes reads your configuration and generates the database table, TCA, and Extbase domain model and repository classes. The TYPO3 Schema Migrator creates the required database structure. After that, you create, edit, and list records the same way you already do in TYPO3.

<Note>
**TonicTypes** is the current product name (successor to **TypoTonic** / extension keys `tonic` and `dataviewer`). This documentation uses **TonicTypes** for the free Core package (`k3n/tonictypes`) and **TonicTypes Professional** for the paid add-on (`k3n/tonictypes_pro`).
</Note>

## Free TonicTypes Extension

Download or install the free Core extension from the [TYPO3 Extension Repository (tonictypes)](https://extensions.typo3.org/extension/tonictypes).

## What You Can Build

Typical record types you can build instead of writing a dedicated extension:

- News, jobs, addresses, events
- Media library or product records
- Awards, companies
- Form answer records for frontend form submissions

Because every record type lives inside one extension, you maintain TonicTypes itself rather than a separate extension per content type.

## Highlights (Core)

- Create custom record types and fields without writing PHP
- Frontend plugins: **List**, **Detail**, **Dynamic**, and **Plain**
- Extbase Domain Model / Repository injection into other extensions
- Template variables (GET/POST, database, session, and more) for Fluid
- Datatype export/import via **System > Export / Import** (from Core 2.1.0)
- Predefined datatype import dashboard widget
- Optional **default_hidden** so new records of a datatype start disabled
- Built on TYPO3 core (TCA, FormEngine, Extbase)

## How It Works

1. Create the fields your record type needs.
1. Create a Datatype and assign the fields.
1. Update the table and generate/update PHP classes on the Datatype.
1. Create records.
1. Create Fluid templates (list and detail).
1. Add a **List** / **Detail** / **Dynamic** / **Plain** plugin to a page.
1. Optionally use [TonicTypes Professional](/en/latest/TonicTypes/Professional/Index) for advanced fields, MCP, toolbar, and related Pro features.

## Core vs Professional

| | TonicTypes (Core) | TonicTypes Professional |
| --- | --- | --- |
| Package | `k3n/tonictypes` | `k3n/tonictypes_pro` |
| Extension key | `tonictypes` | `tonictypes_pro` |
| Requires | PHP 8.2–8.5, TYPO3 12.4–14.9 | Core 2.x plus `ns_license` and `ns_t3af` |
| Role | Datatypes, fields, plugins, export/import | Advanced field types, MCP tools, toolbar, DocHeader buttons, link handler, Form hooks |

Professional requires Core. See [TonicTypes Professional](/en/latest/TonicTypes/Professional/Index).

## Helpful Links

- Free extension (TER): [https://extensions.typo3.org/extension/tonictypes](https://extensions.typo3.org/extension/tonictypes)
- T3Planet product page: [https://t3planet.de/tonictypes](https://t3planet.de/tonictypes)
- T3Planet support: [https://t3planet.de/support](https://t3planet.de/support)
- License activation: [License](/en/latest/License/Index)
