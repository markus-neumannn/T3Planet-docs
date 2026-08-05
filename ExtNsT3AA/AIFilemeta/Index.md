---
title: "AI FileMeta"
description: "AI FileMeta."
keywords:
  - "TYPO3"
  - "T3Planet"
sidebarTitle: "AI FileMeta"
---

The **AI FileMeta** feature in T3AA helps you automatically generate metadata for your images using artificial intelligence. It supports both individual and bulk image processing, including those attached to content elements.

- Automatically generate metadata for single images, including **title**, **description**, and **alt text**.
- Generate metadata for images attached to content elements.
- Process multiple files at once using the **Bulk Metadata** feature.

# AI FileMeta (TextAlt.ai API)



<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmraryza91hd3qmhxpq8887qs?utm_source=link" loading="lazy" title="FileMeta TextAlt.ai Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cm9l8y105022nxu0imradkih5" loading="lazy" title="FileMeta TextAlt.ai Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cm9ldiyrj4jjtljv57t7unmsv" loading="lazy" title="AI FileMeta Overview Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

With **TextAlt.ai API**, you can easily generate SEO-friendly and accessible metadata (title, description, alt text) for any image.

**Steps to generate metadata using TextAlt.ai:**

**Step 1** : Navigate to the **File List** in the TYPO3 backend.

**Step 2** : Select a folder.

**Step 3** : Choose an image from the list.

**Step 4** : Click on **Edit Image Alt Metadata**.

**Step 5** : Click the **Generate AI Alt Metadata** button.

**Step 6** : Select **TextAlt.ai** from the dropdown.

**Step 7** : Click **Generate**.

**Step 8** : Click **Save** to apply the generated metadata.

# FileMeta (Vision API)



<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmraru0z91h11qmhxwzq9omc7?utm_source=link" loading="lazy" title="FileMeta Vision API Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cm9l8fads4fnmljv5ala8pvfg" loading="lazy" title="FileMeta Vision API Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
With **Vision API**, you can extract and generate metadata from images using advanced visual recognition.

**Steps to generate metadata using Vision API:**

**Step 1** : Open the **File List** in the TYPO3 backend.

**Step 2** : Choose a folder and select an image.

**Step 3** : Click **Edit Image Alt Metadata**.

**Step 4** : Click **Generate AI Alt Metadata**.

**Step 5** : Select **Vision API**.

**Step 6** : Click **Generate**, then click **Save** to apply.

# Multilingual Metadata Creation

The **Multilingual Metadata** feature allows you to generate image metadata (like title, alt text, and description) in multiple languages using AI.

You have two options for generating multilingual image metadata:

# Manual Metadata Generation per Image


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmd7fds316tuhc4kjv76erv7o?embed_v=2" loading="lazy" title="Multilingual Metadata Manual Option Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
# Bulk Metadata Generation with Multilingual Support using a Scheduler



<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmras49y91hl2qmhxltv9w9d6?utm_source=link" loading="lazy" title="AI Bulk Metadata Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmfw69mbh2urm10k87q2yb338?utm_source=link" loading="lazy" title="AI Bulk Metadata Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
Manually writing alt texts for images can be repetitive. With AI Bulk Metadata, you can generate or update image metadata for entire folders at once — even across multiple languages.

Steps to Generate Bulk Metadata

**Step 1:** Go to the File List module.

**Step 2:** Select the folder that contains the images you want to update.

**Step 3:** Click the Mass AI File Meta button in the toolbar.

**Step 4:** Choose how you want AI to handle your images:

Queue only missing metadata → Adds AI-generated metadata only where none exists.

Queue and override all metadata → Regenerates metadata for every image, even if some already have alt text.

**Step 5 (Multilingual Option):**

Use the language selector to pick the language in which you want metadata generated.

If you check the box **“Generate file if translation is missing”**, the system will automatically create the translation file for that language if it doesn’t already exist.

**Step 6**: Run the Scheduler from the System Module to process the queued metadata jobs.

**Step 7:** Revisit the File List to check the newly added or updated alt texts in your chosen language(s).
