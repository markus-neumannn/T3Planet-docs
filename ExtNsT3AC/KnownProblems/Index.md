---
title: "Known Problems"
description: "Known problems and workarounds for AI Chatbot (T3AC), including streaming gzip issues on older versions."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AC"
  - "Known Problems"
sidebarTitle: "Known Problems"
---

## Streaming chatbot response does not work (T3AC 14.2.2 or older)

**Affected versions:** T3AC **14.2.2 or older** (and the matching T3CS base package), on **TYPO3 v12 / v13**.

On these versions, the chatbot answer may stay empty, appear only after a long delay, or fail in the browser with a content-decoding error. In the Network panel, the streaming request often shows:

```text
Content-Encoding: gzip
```

instead of an uncompressed event stream.

### Cause

TYPO3 frontend compression is still enabled in `settings.php`:

```php
$GLOBALS['TYPO3_CONF_VARS']['FE']['compressionLevel'] = 5;
```

When this value is `1`–`9`, TYPO3 gzip-compresses the full frontend response and adds `Content-Encoding: gzip`. Chatbot streaming needs incremental Server-Sent Events. Gzip waits for the complete body before sending it, so the live response cannot be delivered.

This is TYPO3 core frontend compression, not a chatbot configuration error.

### Workaround (14.2.2 or older)

1. Open `config/system/settings.php`.
2. Find:

```php
$GLOBALS['TYPO3_CONF_VARS']['FE']['compressionLevel'] = 5;
```

3. **Remove** that line, or set:

```php
$GLOBALS['TYPO3_CONF_VARS']['FE']['compressionLevel'] = 0;
```

4. Flush all TYPO3 caches.
5. Send a chatbot message again. The streaming response should work, and `Content-Encoding: gzip` should no longer be applied to that request.

<Note>
Setting `compressionLevel` to `0` disables TYPO3 application-level gzip for **all** frontend pages. HTML compression can still be handled by the web server (Apache `mod_deflate`, nginx `gzip`).
</Note>

<Tip>
**Newer T3AC releases** disable gzip only for chatbot/search streaming requests. After you update past 14.2.2, you can keep `compressionLevel = 5` for normal pages.
</Tip>

## Report a Problem

Facing trouble while using the T3AC extension?

We're here to help! Please report your issues through our support portal:
[https://t3planet.de/support](https://t3planet.de/support)
