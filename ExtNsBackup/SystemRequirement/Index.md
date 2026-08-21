---
title: "System Requirement"
description: "For backup and scheduler, we have installed and configured one of the most popular PHPBU solution."
keywords: ["TYPO3", "T3Planet", "ns_Backup", "System Requirement", "SystemRequirement"]
sidebarTitle: "System Requirement"
---

# System Requirement

![ns-backup-typo3-system-requirement](./images/ns-backup-typo3-system-requirement.webp)

Please make sure to have your web-server is compatible with following installation and configuration.

| Requirement | Details |
| --- | --- |
| TYPO3 version | v8, v9, v10 |
| PHP Version | PHP 7.0 or later |
| PHP Extensions | ext/curl, ext/dom, ext/json |
| POSIX Shell | tar, bzip2 or gzip |

<Tip>

For backup and scheduler, we have installed and configured one of the most popular PHPBU solution. We recommend to see https://phpbu.de/manual/current/en/installation.html#installation.requirements

</Tip>

<Info>

This extension may not works well on shared server, due to PHPBU's SSH command execute ".phar file" with PHP's exec() and shell_exe().

</Info>
