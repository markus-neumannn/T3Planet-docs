---
title: "T3AS Search Plugin"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AS"
  - "T3AS Search Plugin"
sidebarTitle: "T3AS Search Plugin"
---

## Overview


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmf40ewn21x4v39ozrnrdxqmm" loading="lazy" title="AI FileMeta Overview Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
The **T3AS Search** plugin places an AI search box on your TYPO3 frontend. Visitors type a question in plain language and get an answer based on content you have trained in T3AS.

You can set colours, layout, suggested questions, chatbot follow-ups, voiceover, and feedback for each page. Site-wide defaults are in **T3AS → Search** (see [5. Search tab](/ExtNsT3AS/Configuration/Index#t3as-search-global-settings)).

## Interactive Demo


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmrak5f4u0vicqmhxqgs1cufg?utm_source=link" loading="lazy" title="T3AS Search Plugin Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
## Add the Plugin to a Page

**Step 1:** Open the page in the **Page** module.

**Step 2:** Click **Create new content** and choose a container — for example **Accordion** for Q&A-style layouts.

**Step 3:** Inside the container, add the **T3AS Search** plugin.

**Step 4:** Configure the **Plugin**, **Search Box**, and **Search Results** tabs.

**Step 5:** Click **Save and close** or **Save and refresh**, then check the frontend.

## Plugin Tab

Controls the look of the search box on this page.

- **Title** — Heading above the search box (e.g. `Search`)
- **Select Style** — **Default Style** uses your site theme; **Customized Style (plugin)** lets you pick colours
- **Box Layout** — Container layout (e.g. `Box`)
- **Search Icon** — Icon shown in the search field
- **Select Loader** — Loading animation: **Skeleton Loader** or **Typing Loader**
- **Primary Color** / **Secondary Color** / **Text Color** — Only available with **Customized Style**
- **Border Radius** — Corner style (e.g. **Semi Rounded**)
- **Reference Links** — Show source links below the AI answer

## Search Box Tab

Controls the search input and suggested questions.

- **Search Form Type** — How the input is laid out (e.g. `With Button`)
- **Button Type** — **Search Icon** or **With Label**
- **Search Input Placeholder** — Hint text inside the field
- **Recent Search** — Show the visitor’s previous searches
- **Recent Search Title** — Label above recent searches
- **Predefined Questions** — Show clickable question suggestions
- **Question Position** — Where suggestions appear relative to the search box
- **Number of Questions Limit** — How many suggestions to show
- **Questions Storage Folder(s)** — TYPO3 folder that holds question records

## Search Results Tab

Controls how AI answers are displayed on this page.

- **Enable Chatbot Mode** — Visitors can ask follow-up questions after the first answer
- **Enable Search Feedback** — Thumbs up/down on answers; saved in **Usage Analytics**
- **Enable Voiceover** — Play button to hear the answer read aloud
- **Result Style** — **Summarize** (short) or **Long Answer** (detailed)
- **Reference Links** — Source links for this plugin instance

<Note>
Plugin settings apply to this content element only. For site-wide defaults, use **T3AS → Search**.
</Note>

## Tips

- Use **Default Style** unless this page needs its own brand colours
- Enable **Chatbot Mode** on help, docs, or FAQ pages
- Show 3–5 predefined questions to keep the interface clean
- After saving, refresh the frontend and test a real search query
