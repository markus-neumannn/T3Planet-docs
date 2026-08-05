---
title: "Real-Time Collaboration Requirements"
description: "Real-Time Collaboration Requirements — T3Planet documentation."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ExtRTECKEditorPack"
  - "Real-Time Collaboration Requirements"
  - "RealTimeCollaborationRequirements"
sidebarTitle: "Real-Time Collaboration R..."
---

Disable the Source Editing plugin.
Raw HTML editing is not compatible with real-time collaboration features like Comments, Track Changes, and Revision History.

Save the RTE content at least one time before editing.
Without this first save, collaboration data might not be stored correctly.

## Best Practice

- Create the new content element or record.
- Click **Save** (even when content is empty).
- Wait until the page reloads.
- Start editing in the RTE.
