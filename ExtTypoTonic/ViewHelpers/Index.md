---
title: "ViewHelpers"
description: "ViewHelpers — TypoTonic (EXT:tonic) documentation."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "TypoTonic"
  - "tonic"
  - "TONICTYPES"
sidebarTitle: "ViewHelpers"
---

All TypoTonic ViewHelpers are available through the `t:` namespace. TypoTonic registers this namespace automatically once the extension is active.

To get autocompletion for the namespace in your IDE, add it to your template's `<html>` tag:

```html
<html
    lang="en"
    data-namespace-typo3-fluid="true"
    xmlns:f="http://typo3.org/ns/TYPO3/Fluid/ViewHelpers"
    xmlns:t="http://typo3.org/ns/Aix/Tonic/ViewHelpers">

    ...Your Code here...

</html>
```

## Template.RenderViewHelper

Renders a template file, either a file you predefined in TypoScript, or a manual file path.

- **template** (string) — A file path, or a template identifier configured in `plugin.tx_tonic.templates`.
- **arguments** (array) — Arguments passed into the rendered template.
- **variables** (array) — IDs of additional Template Variables to inject.
- **cache** (boolean) — Enables or disables caching of the output.
- **lifetime** (int) — Cache lifetime in seconds.
- **cacheIdentifier** (string) — A custom cache identifier.

```html
{t:template.render(template:'movieMini',arguments:'{record:record}')}

<t:template.render template="movieMini" arguments="{record:record}" variables="{0:12,1:35}" />
<t:template.render template="fileadmin/templates/tonic/movies/mini.html" arguments="{record:record}" />
```

## Datatype.GetViewHelper

Fetches a Datatype by its UID.

- **uid** (int) — The UID of the Datatype.
- **onlyEnabled** (boolean) — Fetches the Datatype only if it is enabled.

Returns: `Aix\\Tonic\\Domain\\Model\\Datatype`

```html
{t:datatype.get(id:'1',onlyEnabled:'0')}

<t:datatype.get uid="1" onlyEnabled="0" />
```

## Record.GetViewHelper

Fetches a record by its UID.

- **uid** (int) — The UID of the record.
- **datatype** (`Aix\\Tonic\\Domain\\Model\\Datatype`) — Limits the search to this Datatype.
- **onlyEnabled** (boolean) — Fetches the record only if it is enabled.

Returns: `Aix\\Tonic\\Domain\\Model\\AbstractRecordModel`

```html
{t:record.get(id:'1',datatype:datatype,onlyEnabled:'0')}

<t:record.get uid="1" datatype="{datatype}" onlyEnabled="0" />
```

## Link.RecordViewHelper

Creates a link tag to a record's detail page. The detail page ID normally comes from the plugin, through `{detailPid}`.

For additional link parameters, see the TYPO3 `f:link.page` ViewHelper.

```html
<t:link.record record="{record}" pageUid="{detailPid}">Link</t:link.record>
```

## Uri.RecordViewHelper

Creates a URL to a record's detail page. The detail page ID normally comes from the plugin, through `{detailPid}`.

For additional link parameters, see the TYPO3 `f:uri.page` ViewHelper.

```html
{t:uri.record(record:record,pageUid:detailPid)}

<t:uri.record record="{record}" pageUid="{detailPid}" />
```

## Filter.RecordsViewHelper

Adds extra filter conditions to a list of records already injected into your template. Use this to build custom, dynamic filters in Fluid.

### Basic filter structure

- **condition** (string) — `AND` or `OR`.
- **filters** (array) — A list of filter rules.

### Each filter rule

- **field** (string) — The field name to filter on.
- **operator** (string) — See the operator table below.
- **value** (mixed) — The value to compare against.

### Operators

- `equal` → `=`
- `not_equal` → `!=`
- `in` → `IN`
- `not_in` → `NOT IN`
- `less` → `<`
- `less_or_equal` → `<=`
- `greater` → `>`
- `greater_or_equal` → `>=`
- `between` → `BETWEEN`
- `begins_with` → `LIKE 'xyz%'`
- `not_begins_with` → `NOT LIKE 'xyz%'`
- `contains` → `LIKE '%xyz%'`
- `not_contains` → `NOT LIKE '%xyz%'`
- `ends_with` → `LIKE '%xyz'`
- `not_ends_with` → `NOT LIKE '%xyz'`
- `is_empty` → `= ''`
- `is_not_empty` → `!= ''`
- `is_null` → `NULL`
- `is_not_null` → `NOT NULL`

```html
{t:filter.records(records:records,filters:{condition:'AND',rules:{0:{field:'title',operator:'contains',value:'sales'}}})}

<t:filter.records records="{records}" filters="{condition:'AND',rules:{0:{field:'title',operator:'contains',value:'sales'}}}" />
```

## Group.RecordsByPropertyViewHelper

Groups a list of records by a property value. Returns a multidimensional array, grouped by the values found for the property you name.

```html
{t:group.recordsByProperty(records:records,property:'propertyName')}

<t:group.records records="{records}" property="propertyName" />
```
