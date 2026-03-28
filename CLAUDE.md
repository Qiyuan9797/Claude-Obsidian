# Claude - Obsidian

Tools for extracting web content into Obsidian training notes.

## Layout

```
scripts/             Python helper scripts
  get_transcript.py  Fetches YouTube transcripts via youtube-transcript-api
.claude/skills/
  extract/           /extract skill — YouTube & article → Obsidian note
```

## Output Directory

All generated notes go to: `C:/QY/Obsidian/TrainingMats/`

Notes follow the standard training note template with frontmatter
(Source, Date Added, Topic, Tags), Overview, Learning Objectives,
and structured Content sections.

## Dependencies

- Python 3.10+
- youtube-transcript-api
- yt-dlp (fallback for transcripts)
- beautifulsoup4
