---
title: "Configuration"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ns_ExtCompatibility"
  - "Configuration"
sidebarTitle: "Configuration"
---

# Configuration

## 1. Compulsory: Update Extension Repository

> To make works perfect this extension, It's very important to-do perform this task. By the way, you can also setup scheduler to make it automatically update ;) You can easily update extension repository with following simple steps:
>
>
> 1. Go to “Extension Manager”.
> 2. Select "Get Extensions" from Dropdown
> 3. Click on 'Update Now' button
>
![Compatibility Check Configuration 3](./images/update_ter.webp)

## 2. Optional: Set default target TYPO3 version

![Compatibility Check Configuration 1](./images/configure_target_version.webp)

## 3. Optional: Configure Scheduler

>
> 1. Go to SYSTEM > **Scheduler** > Create new scheduler with **Update extension list (extensionmanager)**.
>
![Compatibility Check Scheduler 1](./images/1-ns_ext_compatibility_scheduler_1.webp)
>
>
> 1. Go to SYSTEM > **Scheduler** > Create new scheduler with **TYPO3 Extensions Compatibility Report via Email Notification**, It will automatically send you an email whenever new TYPO3 version or extensions will available, Please configure all the fields.
>
![Compatibility Check Scheduler 1](./images/1-ns_ext_compatibility_scheduler_2.webp)
>
![Compatibility Check Scheduler 1](./images/1-ns_ext_compatibility_scheduler_3.webp)

That's it, Now you can enjoy all the benifits of this extension :)
