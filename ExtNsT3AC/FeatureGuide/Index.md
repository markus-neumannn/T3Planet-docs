---
title: "Feature Guide"
description: "Feature guide for T3AC (EXT:ns_t3ac) chatbot, training, and analytics."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AC"
  - "Feature Guide"
sidebarTitle: "Feature Guide"
---

## Dashboard

![Extension](https://docs.t3planet.de/en/latest/_images/Dashboard2.png)

- View, activate, deactivate, and manage all created chatbots.
- Create new chatbot instances.

## Configuration


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmjbg1qui2wjxf6zpfv4miwkc?embed_v=2&utm_source=embed" loading="lazy" title="AI FileMeta Overview Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
While creating or editing a chatbot, you can configure:

- Title (e.g., AI Chatbot)
- Short Description
- Bubble Message (example: “Hey there, How can I help you?”)
- Welcome Message (example: “Hi, how can I help you?”)
- Chatbot Language
- Chatbot Instructions

## Customization


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmjbh6aie2zhgf6zpxhn57f6t?embed_v=2&utm_source=embed" loading="lazy" title="AI FileMeta Overview Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
Customize the appearance and behavior of the chatbot:

- Upload Logo
- Upload Avatar
- Avatar Size
- Chatbot Color
- Show/Hide Logo
- Show/Hide Date & Time
- Transparent Trigger Option
- Chatbot Position (e.g., bottom-right)
- Widget Bottom Space (In Pixel Min: 15px, Max: 200px)

## Training


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmjbj5eum33fkf6zpon3rvzgz?embed_v=2&utm_source=embed" loading="lazy" title="AI FileMeta Overview Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
T3AC offers multiple methods to train your chatbot for better and specific responses:

**Meaning of Status Labels:**

- **Untrained** means the Chatbot has not been trained on the data yet.
- **Trained** means the Chatbot has already been trained and has learned from the data.

**Typo3 Sitemap:**

This feature allows the chatbot to automatically fetch URLs from your TYPO3 website’s sitemap, scan the pages, and extract content for AI training — helping you keep the chatbot’s knowledge base up to date and well-trained.

**Website Training:**

- Website Mode: Enter a website URL to fetch and train from all available pages.
- Single URL Mode: Enter a single webpage URL to train specifically.

**PDF Training:**

- Upload a PDF file and allow the chatbot to learn from its content.

**Text Training:**

- Manually add a custom Title and corresponding Text for specific training.

**Q&A Training:**

- Add Question & Answer pairs to create a focused FAQ-based training set.

After feeding the data, simply select and click *Train GPT*.

## Embed

If you’d like to use this chatbot on another domain, follow these simple steps:

![Extension](https://docs.t3planet.de/en/latest/_images/T3AC_Embed.png)

- Go to tab Embed
- Click the Copy button to copy the embed code.
- Paste the code inside the **`<body>`** tag of your website.
- Allow the specific domain in the .htaccess file of the website where the chatbot is created to enable proper access.

## Chat Logs


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmjcpqrew4eb4f6zpv7o7s06c?embed_v=2&utm_source=embed" loading="lazy" title="AI FileMeta Overview Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
- Access all conversations recorded by the chatbot.
- Monitor interactions, review conversations, and improve chatbot training based on real user inputs.

## Multilanguage


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmjcqdwzn4fewf6zpp0xvswuc?embed_v=2&utm_source=embed" loading="lazy" title="Multilanguage Feature Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
Configure your chatbot to support multiple languages directly from the **Configuration** tab by selecting the default language from the dropdown menu. Only the languages that have already been added to your domain will be available for selection.

## Scheduler


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmjcqxd4f4g3gf6zpaxu4str4?embed_v=2&utm_source=embed" loading="lazy" title="Scheduler Feature Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
Use the **Scheduler** under the **Website** section of the **Training** tab to automate training tasks on large website datasets—ideal for frequent content updates or large-scale web crawling.

## Sitemap Crwaling

- To run the scheduler via CLI, use the command (1 is the ID of the scheduler):

```bash
vendor/bin/typo3 nst3ac:crawl:sitemap "https://v13-composer.ddev.site/sitemap.xml" 1
```

- This scheduler allows you to crawl the content of all URLs defined in the sitemap.
- When executed via the CLI, it displays the crawl progress.
- After execution, a summary of successfully processed and failed URLs is shown.

![Crawl Command](https://docs.t3planet.de/en/latest/_images/Command_crawl.png)

## Chatbot visibility

![Sites Feature](https://docs.t3planet.de/en/latest/_images/Show_Hide_page.png)

**Show Chatbot on Specific Pages**

- Enter the Page IDs where the chatbot should be visible (e.g., 10, 22, 35).

**Hide Chatbot on Specific Pages**

- Enter the Page IDs where the chatbot should be hidden, even if it is enabled globally (e.g., 45, 60, 72).

## Basic Authentication Support

If you want to crawl URLs protected by htaccess, simply enable the Basic Authentication checkbox and enter the htaccess username and password.

![Basic Authentication](https://docs.t3planet.de/en/latest/_images/Basic_Authentication.png)

## Configurable Database Chunking for various types of Dataset Processing

**Overview**

- This feature provides configurable database chunking to efficiently process large datasets while maintaining optimal performance and stability. Instead of loading all records in a single query, data is fetched and processed in smaller chunks, reducing memory usage and preventing execution timeouts.
- The chunk size is configurable via the extension settings, allowing administrators to adjust it according to server capacity and dataset size.

**Default Configuration**

- By default, database chunking is enabled with a chunk size of 1000 records.
- If required, this value can be modified in the extension settings to better suit the execution environment.

![Chunk Size](https://docs.t3planet.de/en/latest/_images/Chunk_Size.png)
