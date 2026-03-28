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

### 6. RedBook Post Assets (if `redbook` flag)

When the `redbook` flag is set, generate posting-ready assets **after** saving the Obsidian + Notion notes.
Run substeps 6a and 6b concurrently where possible.

**Output folder:** Create a dated folder for all RedBook assets:
`C:/QY/Obsidian/TrainingMats/RedBook/{YYYY-MM-DD} - {Short Title}/`

All RedBook assets (post description, slides, infographic) go into this folder.

#### 6a. Generate RedBook Post Description

Using the Chinese note content, write a RedBook post description optimized for engagement:

**Structure:**
- **Hook** (first 50 chars): specific, curiosity-driven opening that makes users stop scrolling
- **Body** (500-700 chars total): 2-3 sentence paragraphs, use emoji as functional bullet points (✅ 💡 🔍 ✨ ▶️)
- **CTA**: encourage saves and follows — e.g. "觉得有用记得收藏❤️关注我获取更多干货！"
- **Hashtags**: 3-5 targeted Chinese hashtags at the end (use native Chinese terms, not translated English tags)

**Guidelines:**
- Use platform-native phrases: 实用、亲测有效、干货、避坑
- Keep paragraphs to 2-3 sentences max for scannability
- Lead with the value proposition, not a generic intro
- Total length: under 1000 Chinese characters

**Save to:** `C:/QY/Obsidian/TrainingMats/RedBook/{YYYY-MM-DD} - {Short Title}/post-description.md` with this format:

```markdown
# {Chinese Title} - RedBook Post

> **Source Note:** [[{Clean Title} - CN - Training]]
> **Date:** {YYYY-MM-DD}

---

## 小红书文案 (Post Description)

{The full post description text, ready to copy-paste into RedBook}

---

## 标签 (Hashtags)

{Hashtags listed individually for easy copying}
```

#### 6b. Generate NotebookLM Visual Assets

Use NotebookLM to generate visual content from the Chinese note. Run these steps:

1. **Create a notebook:** Call `mcp__notebooklm-mcp__notebook_create` with a title like `"RedBook - {Chinese Title}"`
2. **Add the CN note as source:** Call `mcp__notebooklm-mcp__source_add` with:
   - `source_type`: `"file"`
   - `file_path`: the CN Obsidian note path (`C:/QY/Obsidian/TrainingMats/{Clean Title} - CN - Training.md`)
   - `wait`: `true`
3. **Generate slide deck + infographic in parallel:** Call `mcp__notebooklm-mcp__studio_create` twice:
   - **Slide deck:**
     - `artifact_type`: `"slide_deck"`
     - `slide_format`: `"detailed_deck"`
     - `language`: `"zh"`
     - `focus_prompt`: describe the RedBook knowledge card style — one key concept per slide, actionable takeaways, engaging tone
     - `confirm`: `true`
   - **Infographic (portrait):**
     - `artifact_type`: `"infographic"`
     - `orientation`: `"portrait"`
     - `detail_level`: `"standard"`
     - `language`: `"zh"`
     - `focus_prompt`: summarize the key framework and data points, visual knowledge card style for RedBook
     - `confirm`: `true`
4. **Poll for completion:** Call `mcp__notebooklm-mcp__studio_status` until both artifacts are completed
5. **Download artifacts:**
   - Slide deck → `{output folder}/slides.pdf` (temporary)
   - Infographic → `{output folder}/infographic.png`
6. **Convert slides to RedBook-ready PNGs** (RedBook only accepts images, not PDF):
   ```python
   import fitz
   from PIL import Image, ImageDraw

   CANVAS_W, CANVAS_H = 1242, 1660  # RedBook 3:4
   BG_COLOR = (255, 251, 240)       # warm cream
   ACCENT_COLOR = (230, 200, 77)    # gold

   doc = fitz.open("{output folder}/slides.pdf")
   for i, page in enumerate(doc):
       pix = page.get_pixmap(dpi=200)
       slide = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
       canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), BG_COLOR)
       draw = ImageDraw.Draw(canvas)
       draw.rectangle([0, 0, CANVAS_W, 8], fill=ACCENT_COLOR)
       draw.rectangle([0, CANVAS_H-8, CANVAS_W, CANVAS_H], fill=ACCENT_COLOR)
       padding = 40
       ratio = (CANVAS_W - padding*2) / slide.width
       resized = slide.resize((int(slide.width*ratio), int(slide.height*ratio)), Image.LANCZOS)
       canvas.paste(resized, ((CANVAS_W-resized.width)//2, (CANVAS_H-resized.height)//2))
       canvas.save(f"{output folder}/slide-{i+1:02d}.png", quality=95)
   ```
   Then delete the PDF: `rm "{output folder}/slides.pdf"`
7. **Open output folder** for review: `start "" "{output folder}"`

**Image size notes for RedBook:**
- RedBook prefers **3:4** (1242x1660px) or **square** (1080x1080) images
- **9:16** (portrait, like Stories) is also supported and fills the feed well
- NotebookLM infographic (portrait) outputs ~1536x2752 (≈9:16) — usable directly on RedBook
- NotebookLM slides output 16:9 landscape — less ideal for RedBook's vertical feed, but still supported
- The **infographic is the primary RedBook visual asset**; slides serve as supplementary or can be cropped

### 7. Confirm

Tell the user:
- The English note has been saved (Obsidian path)
- If CN: the Chinese note has been saved (Obsidian path + Notion link)
- A brief summary of what was extracted
- If RedBook: additionally report:
  - Output folder path
  - RedBook post description saved — ready to copy-paste
  - Infographic PNG (portrait, primary RedBook visual — 9:16 ratio, usable directly)
  - Slide deck PDF (12 slides, 16:9 landscape — supplementary, may need cropping for RedBook)
  - NotebookLM notebook link (for further edits/regeneration)

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
