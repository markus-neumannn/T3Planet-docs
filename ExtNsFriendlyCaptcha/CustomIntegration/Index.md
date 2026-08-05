---
title: "Custom Integration"
description: "To integrate nsFriendlyCaptcha in your own extensions, 2 steps are required:"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ExtNsFriendlyCaptcha"
  - "Custom Integration"
sidebarTitle: "Custom Integration"
---

To integrate ns_Friendly_Captcha in your own extensions, 2 steps are required:

**Step 1.** Add this code to your custom form.

```python
<div class="frc-captcha" data-sitekey="{your-site-key}" data-callback="myCallback"  data-start="none" data-lang="en"></div>
```

**Step 2.** Configure this code in your relevant controller action.

```python
$validCaptcha = false;
$captchaService = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(\NITSAN\NsFriendlycaptcha\Services\CaptchaService::class);
$captchaServiceValidation = $captchaService->validateReCaptcha();
if (isset($captchaServiceValidation['verified'])) {
 if ($captchaServiceValidation['verified'] === true) {
  $validCaptcha = true;
  }
 }
```
