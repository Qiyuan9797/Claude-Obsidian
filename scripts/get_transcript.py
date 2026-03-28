"""Fetch YouTube transcript and video title, output as JSON."""
import sys
import re
import json
import urllib.request
import urllib.error
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def get_video_title(video_id: str) -> str:
    """Fetch video title from YouTube oembed API."""
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        req = urllib.request.Request(oembed_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("title", "Untitled Video")
    except Exception:
        return "Untitled Video"


def get_transcript(video_id: str) -> str:
    """Fetch transcript, preferring manual captions over auto-generated."""
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    formatter = TextFormatter()
    return formatter.format_transcript(transcript)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: get_transcript.py <youtube_url_or_id>"}))
        sys.exit(1)

    url = sys.argv[1]
    try:
        video_id = extract_video_id(url)
        title = get_video_title(video_id)
        text = get_transcript(video_id)
        result = {
            "video_id": video_id,
            "title": title,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "transcript": text,
        }
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
