---
title: "FAQ"
description: "How to set WordPress’ media path to TYPO3’s fileadmin?"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ExtNsRevolutionSlider"
  - "FAQ"
sidebarTitle: "FAQ"
---

## How to set WordPress’ media path to TYPO3’s fileadmin?

Currently, all the slider revolution plugin’s assets (images, video) are stored at WordPress’s default media path. If you want to keep all the media assets to TYPO3 core’s fileadmin folder, you will need to create a symlink path using CLI commands. You will need to run the below commands at Installation and Update the new version.

```python
- mv typo3conf/ext/ns_revolution_slider/vendor/wp/wp-content/uploads public/fileadmin/revslider
- chmod -R 755 public/fileadmin/revslider/uploads
- rm -rf typo3conf/ext/ns_revolution_slider/vendor/wp/wp-content/uploads
- ln -sf public/fileadmin/revslider/uploads typo3conf/ext/ns_revolution_slider/vendor/wp/wp-content/uploads
```
