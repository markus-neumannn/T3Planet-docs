---
title: "Composer Update Guide"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "License"
  - "Composer Update Guide"
sidebarTitle: "Composer Update Guide"
---

## Minor/Major Version Update

Whenever you run composer update, You’ll automatically get the latest version of your purcahsed TYPO3 extension.

<Note>
If you are still using old-way of composer installation e.g., install extension with :@dev then consider to update with our modern and automated composer-way - just like packagist.org ;) then we highly recommend to follow our “Migration To New Composer” at [https://docs.t3planet.de/en/latest/License/Migration/Composer/Index.html](/License/Migration/Composer/Index)
</Note>

<Warning>
Before you start the migration, we recommend taking a backup (code & database) of your TYPO3 instance. During the migration, If any problem occurs, then you can roll back your TYPO3 instance. So, please take a backup now :)
</Warning>

```python
composer update nitsan/EXTENSION-NAME
```

```python
composer dump-autoload
```

```python
vendor/bin/typo3 cache:flush
```

<Warning>
For EXT:ns_revolution_slider, Please don’t forget to follow below step “Make Symlink of Your Assets”.
</Warning>

**For TYPO3 v11 and below**

```python
- rm -rf typo3conf/ext/ns_revolution_slider/vendor/wp/wp-content/uploads
- ln -sf public/fileadmin/revslider/uploads typo3conf/ext/ns_revolution_slider/vendor/wp/wp-content/uploads
```

**For TYPO3 v12 and above**

```python
- rm -rf vendor/nitsan/ns-revolution-slider/Resources/Public/vendor/wp/wp-content/uploads
- ln -sf ../../../../../../../../public/fileadmin/revslider/uploads vendor/nitsan/ns-revolution-slider/Resources/Public/vendor/wp/wp-content/uploads
```
