---
title: "CKEditor AI"
description: "The AI Chat feature provides a conversational AI assistant that supports content creation, editing, and ideation within CKEditor. It enables dynamic, multiturn interactions…"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ExtRTECKEditorPack"
  - "CKEditor AI"
sidebarTitle: "CKEditor AI"
---

## configuration


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmiel3r9wb1glb7b4qrj978xw?step=2" loading="lazy" title="Premium Pack Configuration Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
Adjust the AI configuration as needed

### AI Chat


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmiel9hefb1seb7b4cxqxc0o4?step=2" loading="lazy" title="Premium Pack Configuration Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
The AI Chat feature provides a conversational AI assistant that supports content creation, editing, and ideation within CKEditor. It enables dynamic, multi-turn interactions through a chat interface, offering a collaborative and context-aware writing experience beyond single-prompt text generation.

### 1. Working with the Document

CKEditor AI Chat operates directly within the context of the active document. You can reference specific paragraphs, request full-document proofreading, or ask questions based on the content currently displayed.

Features such as **Web search** and **Reasoning** can be enabled to extend the AI’s capabilities with real-time information retrieval and advanced logical processing.

### 2. Making Changes to Content

AI Chat supports document editing workflows. You can request actions such as summarization, rewriting, or structural improvements. Instead of generating plain text, the AI presents proposed edits that can be reviewed, accepted, rejected, or turned into Track Changes suggestions.

This workflow eliminates the need for copy-pasting and enables a seamless, interactive approach to editing.

### 3. Brainstorming and Content Creation

The AI Chat can assist in ideation and drafting. Users can start from a blank document, generate ideas, build outlines, and refine the final content—all through conversation.
The AI can also rewrite, proofread, or polish the text when needed.

### 4. Integration

To enable the Chat feature, load the `AIChat` plugin in your CKEditor configuration.
When enabled, a **Chat** button appears in the AI interface, along with access to Chat history.

### 5. Available Models

Users can choose from a list of available AI models for their conversation. A model selection dropdown is located at the bottom of the chat panel.

- Once selected, the model remains active for the entire conversation.
- To switch to a different model, users can start a new chat using the **+ New chat** button in the top-right corner.

### 6. Web Search

Web search enables the AI to access and retrieve real-time online information. This allows the model to:

- Provide the most current facts,
- Verify information,
- Generate accurate responses.

The feature can be activated via the **Enable web search** toggle for compatible models.

### 7. Reasoning

Reasoning enhances the AI’s ability to:

- Solve problems,
- Analyze context,
- Generate structured and logically sound outputs.

It can be enabled using the **Enable reasoning** toggle for supported models.

### 8. Adding Context to Conversations

Users can include external resources—such as URLs, files, or documents—through the **Add context** button.
The AI can analyze the provided materials and produce summaries, explanations, or answers based on that content.

This feature also supports integration with centralized resource libraries for large-scale workflows.

### 9. Working with AI-Generated Changes

When requesting edits, the AI returns a list of proposed changes.
Hovering over any suggestion highlights the corresponding section in the document, helping users review context before applying changes.

### 10. Showing Details

A **Show details** toggle allows users to switch between:

- **Detailed view** – shows markup for additions, deletions, and formatting changes.
- **Simplified view** – shows a clean preview of the updated text.

### 11. Previewing Changes

The **Show in the text** option opens a preview window for individual edits. This view includes:

- Navigation controls,
- Options to apply changes,
- Options to convert edits into Track Changes suggestions.

The preview automatically syncs with the relevant document section.

### 12. Applying Changes

- **Apply** inserts the selected suggestion.
- **Apply all** applies the entire set of AI-generated changes at once.

### 13. Inserting Track Changes Suggestions

If Track Changes is enabled, AI edits can be inserted as suggestions:

- Use **Insert suggestion** for individual edits.
- Use **Suggest from the Apply all menu** to convert all changes into Track Changes entries.

### 14. Rejecting Suggestions

Unwanted AI proposals can be dismissed using the **Delete (Reject)** option.

### 15. Chat History

All conversations are stored in the Chat history panel. Users can:

- Reopen past sessions,
- Rename conversations,
- Delete older entries.

Conversations are organized by date and can be filtered using the search bar for easier navigation.

### AI Review

The AI Review feature delivers AI-powered quality assurance by analyzing content for grammar, style, tone, clarity, and other key writing parameters. It provides a streamlined interface that allows users to review, accept, or reject AI-generated suggestions directly within the editor, helping maintain high content standards with minimal manual effort.

To enable the Review feature, load the `AIReviewMode` plugin in your CKEditor configuration. Once activated, the Review Mode button appears in the AI panel, giving users access to review commands and automated content analysis.

For more details, refer to the documentation on installing and enabling AI features.

### AI Quick Actions

AI Quick Actions streamline routine content transformations by providing one-click, AI-powered suggestions directly inside the editor. Users can instantly enhance, refine, or analyze selected text through predefined actions—or send the text to the Chat for deeper AI insights.

This feature is designed to boost speed, consistency, and usability, especially for repetitive or simple editing tasks. Quick Actions appear in an intuitive window interface and can also act as conversation starters with the Chat.

### Integration

To enable the Quick Actions feature, load the `AIQuickActions` plugin in your editor configuration.
Refer to the installation guide for detailed instructions on enabling AI features.

Next, add the **Quick actions** menu (`aiQuickActions`) to your:

- Main toolbar, and/or
- Balloon toolbar

For toolbar setup instructions, see the toolbar configuration guide.

You can also add individual Quick Action shortcuts directly to the toolbar, such as:

- `ask-ai`
- `improve-writing`

You may also include entire Quick Action categories (e.g., *Adjust length*, *Change tone*).
This provides faster access to frequently used actions.

### Types of Actions

Quick Actions come in two functional types.

#### Actions That Open the Chat Interface

These actions send the selected text into the Chat panel.

Examples:

- **Ask AI** – Opens the Chat with the selected text as context.
- **Summarize** – Opens the Chat and automatically generates a summary request for the selected content.

#### Actions That Open the Popup Interface

These actions display an AI-generated suggestion in a popup next to the selected text, allowing users to:

- Accept the result
- Reject the result
- Re-run the action

Examples:

- **Continue writing**
- **Make shorter**

Custom actions can be created, and their behavior can be fully configured by developers.

### Default Quick Actions

The Quick Actions feature includes numerous built-in actions grouped into categories.
All actions are accessible through the **Quick Actions menu** (`aiQuickActions`) and can also be placed individually on the toolbar.

You can freely:

- Add custom actions
- Remove default actions
- Reorder or categorize actions to fit project needs

### Full List of Available Actions

**ask-ai**

**Chat Commands** (`chat-commands`)

- `explain`
- `summarize`
- `highlight-key-points`
- `improve-writing`
- `continue`
- `fix-grammar`

**Adjust Length** (`adjust-length`)

- `make-shorter`
- `make-longer`

**Change Tone** (`change-tone`)

- `make-tone-casual`
- `make-tone-direct`
- `make-tone-friendly`
- `make-tone-confident`
- `make-tone-professional`

**Translate** (`translate`)

- `translate-to-english`
- `translate-to-chinese`
- `translate-to-french`
- `translate-to-german`
- `translate-to-italian`
- `translate-to-portuguese`
- `translate-to-russian`
