---
title: "Performance Configuration Based on Database Size"
description: "The extension’s performance depends on the amount of vector data stored in the database. As the number of vectors increases, PHP memory and execution limits must be adjusted to…"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AS"
  - "Performance Configuration Based on Database Size"
sidebarTitle: "Performance Configuration Based on Database Size"
---

## Overview

The extension’s performance depends on the amount of vector data stored in the
database. As the number of vectors increases, PHP memory and execution limits
must be adjusted to prevent timeouts and memory issues.

## Low Level (≤ 25,000 vectors)

```ini
memory_limit = 512M
max_execution_time = 120
max_input_time = 120
default_socket_timeout = 120
```

**Recommended for:** Small datasets and initial setups.

## Medium Level (25,000 – 150,000 vectors)

```ini
memory_limit = 1024M
max_execution_time = 300
max_input_time = 300
default_socket_timeout = 300
```

**Recommended for:** Moderate vector volumes.

## High Level (150,000 – 250,000+ vectors)

```ini
memory_limit = 2048M
max_execution_time = 900
max_input_time = 900
default_socket_timeout = 900
```

**Required for:** Large datasets to avoid execution timeouts and memory errors.
