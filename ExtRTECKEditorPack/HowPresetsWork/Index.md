---
title: "How Presets Work?"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ExtRTECKEditorPack"
  - "How Presets Work?"
  - "HowPresetsWork"
sidebarTitle: "How Presets Work?"
---

## Default Behavior

CKEditor Pack automatically creates a separate preset from the default configuration.
This gives you a ready-to-use setup and keeps the original preset unchanged.

## After Modification

All custom changes are stored in your own preset.
The original default configuration stays unchanged.

## After Deletion

If a preset is deleted, the system uses the project default preset automatically.
The editor keeps working without interruption.

## Table of Contents Behavior

The editor follows the allowed tags from the RTE configuration.
If a tag is not allowed, pasted content with that tag is adjusted.

Example:
If `<h1>` is not allowed, pasted `<h1>` content is converted to an allowed format.

## Markdown

When Markdown is enabled, CKEditor Pack can output Markdown instead of HTML.

- Users can write with Markdown shortcuts.
- The Source button shows raw Markdown.
- Markdown supports headings, lists, links, and code blocks.
- Some advanced HTML formatting is limited in Markdown.
- Markdown and Real-time Collaboration do not work together.

Doc: https://ckeditor.com/docs/ckeditor5/latest/features/markdown.html

## Divider and Break (Separator)

You can remove a divider/break element by double-clicking it.

## Load from YAML

Load from YAML reads the default RTE configuration from TYPO3 core YAML.
It helps integrators quickly restore original settings.

<div className="t3-embed">
   <iframe src="https://app.supademo.com/demo/cmirfho5i150pl821fkxxm2ji?step=2" loading="lazy" title="Load From YAML Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
 </div>

## Reset

Reset restores modified settings to default values.
This gives a clean baseline and helps avoid configuration issues.

<div className="t3-embed">
   <iframe src="https://app.supademo.com/demo/cmiresoe813yql821w5tt6n1r?step=3" loading="lazy" title="Load From YAML Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
 </div>

## Sync

Sync aligns values between TYPO3 default RTE YAML and extension custom YAML.
This reduces conflicts and keeps behavior consistent.

<div className="t3-embed">
   <iframe src="https://app.supademo.com/demo/cmirg3t7q15sll821k3ahlmmx?step=2" loading="lazy" title="Load From YAML Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
 </div>

## Import / Export Presets

Import/Export Presets helps you share and reuse CKEditor presets across TYPO3 environments.
This keeps local, staging, and live systems consistent.

## Import Presets

Import Presets adds presets from a YAML file into TYPO3.
Upload the YAML file, and the preset is created automatically with toolbar and settings.

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmjcvzsq24n7lf6zp2wlvrmgm?embed_v=2&utm_source=embed" loading="lazy" title="Premium Pack Configuration Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

## Export Presets

Export Presets downloads an existing or custom preset as a YAML file.
You can import this file into another TYPO3 system to use the same setup.

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmjcvdeyg4mjzf6zpd00w121z?embed_v=2&utm_source=embed" loading="lazy" title="Premium Pack Configuration Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

<Note>

When exporting presets, these features are **not included**:

- Document Outline
- Paste Office Enhanced
- Editoria11y
- Markdown

</Note>
