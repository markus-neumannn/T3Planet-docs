---
title: "ViewHelpers"
description: "TonicTypes Fluid ViewHelpers (dv namespace) — template, datatype, record, link, filter, group."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "TonicTypes"
  - "tonictypes"
  - "tonictypes_pro"
sidebarTitle: "ViewHelpers"
---

All Core ViewHelpers are available through the **`dv:`** namespace (`K3n\Tonictypes\ViewHelpers`). The namespace is registered automatically when EXT:tonictypes is active.

IDE hint:

```html
<html
    lang="en"
    data-namespace-typo3-fluid="true"
    xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
    xmlns:dv="http://typo3.org/ns/K3n/Tonictypes/ViewHelpers">
</html>
```

ViewHelpers ship with **Core**. Professional does not add a separate ViewHelper package; it extends field types, MCP, toolbar, and related backend/frontend tooling.

## Template.RenderViewHelper

Renders a predefined TypoScript template identifier or a file path.

- **template** (string) — Identifier under `plugin.tx_tonictypes.templates`, or a file path.
- **arguments** (array) — Arguments passed into the template.
- **variables** (array) — UIDs of additional Template Variables.
- **cache** (boolean) — Cache output.
- **lifetime** (int) — Cache lifetime in seconds.
- **cacheIdentifier** (string) — Custom cache id.

```html
{dv:template.render(template:'movieMini',arguments:'{record:record}')}

<dv:template.render template="movieMini" arguments="{record:record}" variables="{0:12,1:35}" />
<dv:template.render template="fileadmin/templates/tonictypes/movies/mini.html" arguments="{record:record}" />
```

## Datatype.GetViewHelper

Fetches a Datatype by UID.

- **uid** (int)
- **onlyEnabled** (boolean)

Returns: `K3n\Tonictypes\Domain\Model\Datatype`

```html
<dv:datatype.get uid="1" onlyEnabled="0" />
```

## Record.GetViewHelper

Fetches a record by UID.

- **uid** (int)
- **datatype** (`K3n\Tonictypes\Domain\Model\Datatype`)
- **onlyEnabled** (boolean)

Returns: record model for that Datatype

```html
<dv:record.get uid="1" datatype="{datatype}" onlyEnabled="0" />
```

## Link.RecordViewHelper

Link to a record detail page (typically `{detailPid}` from the plugin).

```html
<dv:link.record record="{record}" pageUid="{detailPid}">Link</dv:link.record>
```

## Uri.RecordViewHelper

URL only (same arguments as the link ViewHelper).

```html
<dv:uri.record record="{record}" pageUid="{detailPid}" />
```

## Filter.RecordsViewHelper

Adds filter conditions to an already injected record list.

- **condition** — `AND` or `OR`
- **filters** / **rules** — field, operator, value

Operators include: `equal`, `not_equal`, `in`, `not_in`, `less`, `less_or_equal`, `greater`, `greater_or_equal`, `between`, `begins_with`, `contains`, `ends_with`, `is_empty`, `is_null`, and their negations.

```html
<dv:filter.records records="{records}" filters="{condition:'AND',rules:{0:{field:'title',operator:'contains',value:'sales'}}}" />
```

## Group.RecordsByPropertyViewHelper

Groups records by a property. Returns a multidimensional array.

```html
{dv:group.recordsByProperty(records:records,property:'propertyName')}
```

## Other Core ViewHelpers

Also available under `dv:` (same package): Backend link helpers (`dv:backend.*`), Format helpers (`dv:format.*`), String/Array helpers, and `dv:typo3.isVersion`.
