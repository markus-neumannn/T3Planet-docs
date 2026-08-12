---
title: "Accessibility Widgets"
description: "Documentation for Accessibility Widgets (ExtNsT3AA)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ExtNsT3AA"
sidebarTitle: "Accessibility Widgets"
---

## What it is

**Accessibility Widgets** configures the frontend accessibility widget in
T3AA (`EXT:ns_t3aa`).

The widget is a floating button on the website. Visitors open it and turn
accessibility tools on or off for their own browser session (font size,
contrast, reading aids, and similar options).

In the TYPO3 backend you decide:

- Whether the widget is shown
- How the button and panel look (icon, size, color, position, layout)
- Which tools and accessibility profiles are available

Settings are saved per site in `config.yaml`. They do not change page content
in the database.

## How to use it

**Activate the feature**

1. Open **AI Foundation** → **AI Features**.
2. Open **General Settings**.
3. Enable **Enable Assistant Widget** and save.

**Configure the widget**

1. Open the T3AA dashboard and click **Accessibility Widgets**.
2. Set widget options (icon, position, style, layout, profiles, settings).
3. Enable or disable the accessibility tools you want visitors to see.
4. Click **Save Settings**.
5. Flush caches and check the frontend.

On the website, visitors click the floating button, open the panel, and use the
enabled tools or profiles. Changes apply only in their browser.

<Note>
The widget needs **Enable Assistant Widget** (under **AI Foundation** →
**AI Features** → **General Settings**) and a valid license/domain for the
site. If it does not appear, check those first, then flush caches.
</Note>

## Widget configuration

Accessibility Widgets has these configuration tabs:

### Widget Icon and Size

Choose the launcher size (**Small**, **Medium**, **Large**) and one of six icon
styles (**Widget Style 1–6**).

Default in the extension: **Large** + **Style 1**.

### Widget Position

Set desktop and mobile placement separately.

- **Standard position** — left/right and top/middle/bottom (default: right
bottom on desktop and mobile).
- **Widget Hide on Desktop / Mobile** — hide the launcher on that device type.
- **Exact positioning** — enable exact position, then set X/Y in pixels
(desktop about **5–500** px; mobile about **5–300** px as labeled in the UI).

Exact position fields work only when exact positioning is enabled.

### Widget Style

- Primary color: **Solid** or **Gradient**
- Color pickers for solid/gradient and header text color
- Appearance: Default, Dark, or System

Default solid color in code: `#0101d9`. Default header text: `#ffffff`.

### Widget Layout

- **Simple Layout** — default, clear single panel
- **Flexible Layout** — responsive arrangement
- **Minimal Layout** — fewer controls (Motor Impaired and Blind profiles are
hidden with this layout)
- **3 Column Layout** — tools arranged in three columns

### Profile Selection

Turn accessibility profiles on or off, then choose which profiles appear:

Motor Impaired, Blind, Color Blind, Dyslexia, Low Vision, Cognitive and
Learning, Seizure and Epileptic, ADHD, Elder.

A profile turns on a fixed group of tools at once. Only one profile can be
active at a time.

### Widget Settings

- **Select Widget Language** — default or `en`, `es`, `fr`, `de`,
`it`, `pt`
- **Move/Drag Widget** — visitors can drag the button (not on mobile)
- **Widget Large** — larger text/icons/buttons inside the widget
- **Widget Tooltip** — hover help text on widget options
- **Widget Mode** — light / dark / system for the widget UI

## Accessibility tools

Each tool is a card in Accessibility Widgets. If enabled and saved, it appears
in the frontend widget. If disabled, visitors do not see it.

### Reading and text

- **Screen Reader** — reads page content aloud (speed/pitch can be limited in
config)
- **Readable Font** — switches to clearer fonts
- **Font Size** — increases or decreases text size
- **Letter Space** — changes space between letters
- **Word Space** — changes space between words
- **Line Height** — changes space between lines
- **Text Align** — left / center / right
- **Text Magnify** — magnifies text
- **Highlight Header** — highlights headings
- **Highlight Links** — highlights links
- **Reading Mask** — focuses on one reading band
- **Reading Guide** — follow-along reading line
- **Read Mode** — simpler reading layout

### Vision and color

- **Contrast** — overall contrast
- **Color Contrast** — text vs background contrast
- **Saturation** — color intensity
- **Invert Filter** — inverts colors
- **Grayscale** — removes color
- **Color Deficiency** — color correction modes
- **Dark/Light** — light or dark page mode
- **Blue Filter** — warmer screen tone
- **Blue Filter by Sun Position** — blue filter by sun position
- **Blue Filter by Time** — blue filter by time of day
- **Cursor** — larger or colored cursor
- **Blur** — softens parts of the view
- **Zoom** — zoom in/out
- **Hide Images** — hides images

### Motion, sound, and structure

- **Pause Animations** — stops motion effects
- **Mute** — mutes audio
- **Voice Navigation** — voice commands (browser support required)
- **Page Structure** — shows page structure for orientation

## How profiles behave

When a visitor selects a profile, the widget enables this tool set:

| Profile | Tools turned on |
| --- | --- |
| Motor Impaired | Pause animations, Text magnify |
| Blind | Screen Reader |
| Color Blind | Contrast, high saturation, readable/dyslexia font, pause animations |
| Dyslexia | Dyslexia-oriented font |
| Low Vision | Bigger text, pause animations, readable font, bigger cursor, text magnify, high saturation |
| Cognitive and Learning | Contrast, bigger text, pause animations, reading guide, text magnify |
| Seizure and Epileptic | Pause animations, low saturation |
| ADHD | Pause animations, reading mask, low saturation |
| Elder | Bigger text, bigger cursor |

Selecting another profile replaces the previous one. Visitors can also use
individual tools without a profile.

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmspx6nk71m45qm339sebmr9a?embed_v=2&utm_source=embed" loading="lazy" title="Interactive demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
