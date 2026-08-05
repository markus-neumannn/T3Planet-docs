---
title: "Verifying Indexed Data Content in TYPO3 AI Search"
description: "To ensure that the data from your selected search engines Solr, keSearch, IndexedSearch is properly fetched, stored, and trained in TYPO3, follow these steps:"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AS"
  - "Verifying Indexed Data Content in TYPO3 AI Search"
sidebarTitle: "VerifyIndexedData"
---

To ensure that the data from your selected search engines (Solr, keSearch, IndexedSearch) is properly fetched, stored, and trained in TYPO3, follow these steps:

1. **Verify Column Values** In the table tx_nst3as_domain_model_indexed_data, check the following columns for each search engine type:
  - **`type`**: solr, keSearch, or indexedSearch
  - **`status`**: trained
  - **`path`**: The corresponding data URL
2. **Check Trained Data** Replace **`solr`** with the type of search engine you want to check (e.g., **`solr`**, **`kesearch`**, or **`indexedsearch`**): SELECT *
FROM `tx_nst3as_domain_model_indexed_data`
WHERE `type` = 'solr'
  AND `status` = 'trained';
3. **Check Untrained Data** Replace **`solr`** with your search engine type as needed: SELECT *
FROM `tx_nst3as_domain_model_indexed_data`
WHERE `type` = 'solr'
  AND `status` = 'Untrained'
  AND `path` != '';

<Note>
This is not use when you use the CustomLLM because we didn’t save the any data inside the TYPO3 Database.
</Note>

```sql
SELECT *
FROM `tx_nst3as_domain_model_indexed_data`
WHERE `type` = 'solr'
  AND `status` = 'trained';
```

```sql
SELECT *
FROM `tx_nst3as_domain_model_indexed_data`
WHERE `type` = 'solr'
  AND `status` = 'Untrained'
  AND `path` != '';
```
