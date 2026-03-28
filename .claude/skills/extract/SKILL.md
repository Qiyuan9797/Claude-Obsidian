---
name: extract
description: >
  Use this skill when the user wants to extract content from a YouTube video
  or web article and save it as an Obsidian training note and/or Notion page.
  Supports Chinese translation for RedBook. Trigger phrases:
  "extract", "/extract", "save this video", "save this article", "add to obsidian".
argument-hint: <url> [cn] [redbook]
---

# Extract to Obsidian + Notion — Skill

You extract content from YouTube videos or web articles and save them as:
- **English** training notes → **Obsidian** only
- **Chinese** translated notes → **Obsidian** + **Notion** (RedBook content hub)

## Arguments

```
/extract <url>              → English note → Obsidian
/extract <url> cn           → English (Obsidian) + Chinese (Obsidian + Notion)
/extract <url> cn redbook   → English (Obsidian) + Chinese RedBook-optimized (Obsidian + Notion)
```

## Procedure

### 1. Parse the URL and Options

The user provides a URL as the first argument. Additional options:
- `cn` — also create a Chinese translated version
- `redbook` — optimize the Chinese version for RedBook style

Determine the source type:
- **YouTube** if the URL contains `youtube.com`, `youtu.be`, or is a bare 11-char video ID
- **Web article** for everything else

### 2a. YouTube — Extract Transcript

Run the helper script:

```bash
python "c:/QY/AIToolbox/Claude - Obsidian/scripts/get_transcript.py" "<URL>"
```

This returns JSON with fields: `video_id`, `title`, `url`, `transcript`.

If the script fails (no transcript available), inform the user and suggest
they provide an alternative source.

### 2b. Web Article — Extract Content

Use the **WebFetch** tool to fetch the page at the given URL. Extract the
main article content from the fetched page. Strip navigation, ads, footers,
and other non-content elements. Keep the meaningful text and any headings.

### 3. Generate the Obsidian Note

Read one existing note for reference to match formatting style:
`C:/QY/Obsidian/TrainingMats/Claude Code - 6 Levels of Progression - Training.md`

Create the note using this template:

```markdown
# {Title} - Training

> **Source:** [{Display Name}]({Full URL})
> **Date Added:** {today's date as YYYY-MM-DD}
> **Topic:** {inferred topic}
> **Tags:** #{tag1} #{tag2} #{tag3}

---

## Overview

{Write 2-3 sentences summarizing what this resource covers, based on
the extracted content.}

---

## Learning Objectives

By the end of this session, you will be able to:

- [ ] {objective 1}
- [ ] {objective 2}
- [ ] {objective 3}

---

## Content

{For YouTube: format the transcript with timestamp headers where topic
shifts occur. Group related paragraphs together. Add section headings
like ### Introduction, ### Key Concepts, etc.}

{For articles: preserve the original heading structure. Clean up
formatting for Obsidian compatibility.}
```

**Guidelines for generating the note:**

- **Title**: Use the video/article title. Remove channel names or site names
  from the end if present. Append ` - Training` as suffix in the H1.
- **Display Name**: For YouTube use `YouTube — {Video Title}`. For articles
  use the site name and article title.
- **Tags**: Generate 3-5 lowercase kebab-case tags relevant to the content.
- **Learning Objectives**: Infer 3-5 actionable objectives from the content.
- **Content section**: This is the most important part. Structure the raw
  transcript/article into readable sections with headings. For transcripts,
  clean up filler words and add paragraph breaks at topic shifts.

### 4. Save the English Note (Obsidian only)

**Obsidian:** Generate a filename from the title: `{Clean Title} - Training.md`
- Replace special characters with hyphens
- Keep it readable and consistent with existing files
- Save to: `C:/QY/Obsidian/TrainingMats/{filename}`

**Do NOT save English notes to Notion.** Notion is reserved for Chinese/RedBook content only.

### 5. Chinese Translation (if `cn` or `redbook` flag)

Translate the entire note into **Simplified Chinese**. Do this yourself inline — no external script needed.

**Translation guidelines:**
- Translate all sections: Overview, Learning Objectives, Content
- Keep technical terms in English with Chinese explanation in parentheses where helpful
- Keep the same markdown structure and headings (translated)
- Tags remain in English (kebab-case)

**If `redbook` flag is set, also adapt for RedBook style:**
- Shorter paragraphs (2-3 sentences max)
- Add relevant emoji at section starts
- Use a more conversational, engaging tone
- Add a catchy Chinese title optimized for RedBook search
- Keep total length manageable (RedBook posts prefer concise content)
- Focus on the most actionable takeaways rather than full transcript

**Save the Chinese version:**

**Obsidian:** Save as `{Clean Title} - CN - Training.md` in the same folder.

**Notion (RedBook hub):** Create a page in the Training Materials database using `mcp__claude_ai_Notion__notion-create-pages`.
- Database data source URL: `collection://6f10ab91-731c-4669-8981-a4e9ca6d16a7`
- Set properties: Title (Chinese), Source URL, Date Added, Topic (Chinese), Type (YouTube/Article), Language (CN), Tags
- Page body: the full Chinese note content
- If RedBook style, add `redbook` to the Tags.

### 6. Confirm

Tell the user:
- The English note has been saved (Obsidian path)
- If CN: the Chinese note has been saved (Obsidian path + Notion link)
- A brief summary of what was extracted

## Notion Database Reference (RedBook content only)

- **Database:** Training Materials
- **Parent page:** Redbook
- **Data source URL:** `collection://6f10ab91-731c-4669-8981-a4e9ca6d16a7`
- **Properties:** Title, Source URL, Date Added, Topic, Type, Language, Tags
- **Usage:** Chinese/RedBook content only — English notes go to Obsidian only

## Error Handling

- If YouTube transcript is unavailable: tell the user, suggest trying
  `yt-dlp --write-auto-sub` as an alternative
- If web page cannot be fetched: inform the user and suggest checking the URL
- If content is too short or empty: warn the user before saving
- If Notion API fails: save to Obsidian anyway, report the Notion error
